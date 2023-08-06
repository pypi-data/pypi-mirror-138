import datetime as dt
import functools
import uuid as guid
import pytz
import typing

import geopandas as gpd
import numpy as np
import pandas as pd
import pyproj
import osgeo
import shapely.geometry as shp
import shapely.ops as ops
import shapely.wkt as wkt
from pyproj import Geod
from pyproj.enums import WktVersion
from osgeo import ogr
from osgeo import osr
from pyarrow import feather, parquet
import pygeos
import collections
from dataclasses import dataclass, field


class __WGS84Meta(type):
    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)
        new_class.WGS84 = pyproj.crs.CRS.from_epsg(4326)
        return new_class


class CRS(metaclass=__WGS84Meta):

    @classmethod
    def crs_from_epsg(cls, epsg=4326):
        return pyproj.crs.CRS.from_epsg(epsg)

    @classmethod
    def crs_from_wkt(cls, wkt_string):
        return pyproj.crs.CRS.from_wkt(wkt_string)

    @classmethod
    def crs_from_wkt_str(cls, txt='ESPG:4326'):
        return pyproj.crs.CRS.from_string(txt)

    @classmethod
    def epsg_from_crs(cls, crs):
        return crs.to_espg()

    @classmethod
    def wkt_from_crs(cls, crs):
        return crs.to_wkt()

    @classmethod
    def from_user_input(cls, crs):
        return pyproj.CRS.from_user_input(crs)

    @classmethod
    def crs_from_srs(cls, srs):
        """convert osgeo.osr.SpatialReference to pyproj.crs.CRS"""
        if osgeo.version_info.major < 3:
            return pyproj.crs.CRS.from_wkt(srs.ExportToWkt())
        else:
            return pyproj.crs.CRS.from_wkt(srs.ExportToWkt(["FORMAT=WKT2_2018"]))

    @classmethod
    def srs_from_crs(cls, crs):
        """Convert from pyproj.crs.CRS to osgeo.osr.SpatialReference

        WKT2 is the best format for storing your CRS according to the PROJ FAQ and
        only supported in GDAL 3+
        """
        crs = cls.from_user_input(crs)

        srs = osr.SpatialReference()
        if osgeo.version_info.major < 3:
            srs.ImportFromWkt(crs.to_wkt(WktVersion.WKT1_GDAL))
        else:
            srs.ImportFromWkt(crs.to_wkt())
        return srs


def pyproj_transformer(crs, crs2):
    _crs = pyproj.CRS.from_user_input(crs)
    to_crs = pyproj.CRS.from_user_input(crs2)
    return pyproj.Transformer.from_crs(_crs, to_crs, always_xy=True)


@dataclass
class RelocsCoordinateFilter:
    """Filter parameters for filtering get_fixes based on X/Y coordinate ranges or specific coordinate values"""
    min_x: float = -180.
    max_x: float = 180.
    min_y: float = -90.
    max_y: float = 90.
    filter_point_coords: typing.Union[typing.List[typing.List[float]], gpd.GeoSeries] = field(
        default_factory=[[0., 0.]])

    def __post_init__(self):
        if isinstance(self.filter_point_coords, list):
            self.filter_point_coords = gpd.GeoSeries(shp.Point(coord) for coord in self.filter_point_coords)


@dataclass
class RelocsDateRangeFilter:
    """Filter parameters for filtering based on a datetime range"""
    start: dt.datetime
    end: dt.datetime


@dataclass
class RelocsSpeedFilter:
    """Filter parameters for filtering based on the speed needed to move from one fix to the next"""
    max_speed_kmhr: float = float("inf")
    temporal_order: str = 'ASC'


@dataclass
class RelocsDistFilter:
    """Filter parameters for filtering based on the distance needed to move from one fix to the next"""

    max_dist_km: float = float("inf")
    temporal_order: str = "ASC"


@dataclass
class TrajSegFilter:
    """Class filtering a set of trajectory segment segments"""

    min_length_meters: float = 0.0
    max_length_meters: float = float("inf")
    min_time_secs: float = 0.0
    max_time_secs: float = float("inf")
    min_speed_kmhr: float = 0.0
    max_speed_kmhr: float = float("inf")


class BaseMixin:
    """
    A class that contains methods for use by other classes without having to be
    the parent class of those other classes.
    '"""

    @classmethod
    def get_value(cls, item: typing.Dict, keyname: str):
        """Get the value from the dictionary"""
        return item.get(keyname)

    @classmethod
    def pack_columns(cls, dataframe: typing.Union[gpd.GeoDataFrame, pd.DataFrame], columns: typing.List):
        """This method would add all extra columns to single column"""
        metadata_cols = set(dataframe.columns).difference(set(columns))

        # To prevent additional column from being dropped, name the column metadata (rename it back).
        dataframe['metadata'] = dataframe[metadata_cols].to_dict(orient='records')
        dataframe.drop(metadata_cols, inplace=True, axis=1)
        dataframe.rename(columns={'metadata': 'additional'}, inplace=True)
        return dataframe

    @classmethod
    def unpack_columns(cls,
                       dataframe: typing.Union[gpd.GeoDataFrame, pd.DataFrame],
                       dict_column: str,
                       keyname: typing.Union[str, typing.List[str]] = None,
                       colname: typing.Union[str, typing.List[str]] = None):
        """function to selectively unpack (additional) column and create independent column"""
        if not type(keyname) == type(colname) or any([keyname is None, colname is None]):
            TypeError(f'keyname and colname should be of the same datatype')

        colname = colname or keyname
        columns = dataframe.columns
        assign_colname = functools.partial(lambda k: k if not all([k in columns]) else '_'.join([k, dict_column]))

        if isinstance(keyname, str):
            dataframe[assign_colname(colname)] = dataframe[dict_column].map(functools.partial(BaseMixin.get_value,
                                                                                              keyname=keyname))
        elif isinstance(keyname, list):
            for key, name in zip(keyname, colname):
                dataframe[assign_colname(name)] = dataframe[dict_column].map(functools.partial(BaseMixin.get_value,
                                                                                               keyname=key))
        elif keyname is None:
            metadata_df = pd.DataFrame(dataframe[dict_column].to_dict()).T
            dataframe = dataframe.merge(metadata_df, how='left', left_index=True, right_index=True)
        return dataframe

    @classmethod
    def add_col_metadata(cls, dataframe, colnames):
        """Add col to additional column"""
        if colnames:
            df = pd.json_normalize(dataframe.additional)

            for colname in colnames:
                df[colname] = dataframe[colname].to_list()
            dataframe = dataframe.assign(additional=df.to_dict(orient='records'))
        return dataframe


@dataclass
class GeoPoint:
    """A geographic point is the most basic geometry"""

    def __new__(cls, _pnt=None, *args, **kwargs):
        instance = object.__new__(cls)
        instance._shapely_geo = _pnt
        return instance

    x: float = 0.
    y: float = 0.
    z: float = 0.
    crs: pyproj.CRS = CRS.WGS84

    def __post_init__(self):
        self.shapely_geometry = self._shapely_geo or shp.Point(self.x, self.y, self.z)
        self.wkt_geometry = self.shapely_geometry.wkt
        self.ogr_geometry = ogr.CreateGeometryFromWkt(self.wkt_geometry)

    def to_crs(self, crs):
        """https://shapely.readthedocs.io/en/stable/manual.html#shapely.ops.transform"""
        if isinstance(crs, pyproj.transformer.Transformer):
            return ops.transform(crs.transform, self.shapely_geometry)
        tranformer = pyproj_transformer(self.crs, crs)
        return ops.transform(tranformer.transform, self.shapely_geometry)


@dataclass
class Fix:
    """A Fix is a temporal geopoint"""
    geopoint: GeoPoint = None
    fixtime: dt.datetime = None
    fix_id: typing.Any = str(guid.uuid4().hex)
    filter_status: bool = False  # Holds a boolean value to indicate whether this point is junk or not
    additional_data: typing.Dict = field(default_factory=dict())

    def __post_init__(self):
        self.shapely_geometry = self.geopoint.shapely_geometry
        self.wkt_geometry = self.shapely_geometry.wkt
        self.ogr_geometry = ogr.CreateGeometryFromWkt(self.wkt_geometry) if self.shapely_geometry else None

    @property
    def status(self):
        return self.filter_status

    @status.setter
    def status(self, value):
        assert type(value) is bool
        self.filter_status = value

    @staticmethod
    def from_dict(in_dict=None,
                  id_key='observation_id',
                  fixtime_key='fixtime',
                  lat_key='lat',
                  lon_key='lon',
                  height_key='height',
                  junk_key=None):
        """ A function to create a Fix object from a dictionary object"""
        raise NotImplementedError()


def straighttrack_properties(df: gpd.GeoDataFrame):
    """Make sure dataframe gets explicitly converted to WGS84 projection."""

    class Properties:
        @property
        def start_fixes(self):
            # unpack xy-coordinates of start fixes
            return df['geometry'].x, df['geometry'].y

        @property
        def end_fixes(self):
            # unpack xy-coordinates of end fixes
            return df['_geometry'].x, df['_geometry'].y

        @property
        def inverse_transformation(self):
            # use pyproj geodesic inverse function to compute vectorized distance & heading calculations
            return Geod(ellps="WGS84").inv(*self.start_fixes, *self.end_fixes)

        @property
        def heading(self):
            # Forward azimuth(s)
            forward_azimuth, _, _ = self.inverse_transformation
            forward_azimuth[forward_azimuth < 0] += 360
            return forward_azimuth

        @property
        def dist_meters(self):
            _, _, distance = self.inverse_transformation
            return distance

        @property
        def timespan_seconds(self):
            return (df['_fixtime'] - df['fixtime']).dt.total_seconds()

        @property
        def speed_kmhr(self):
            return (self.dist_meters / self.timespan_seconds) * 3.6

        @property
        def x_displacement(self):
            return self.end_fixes[0] - self.start_fixes[0]

        @property
        def y_displacement(self):
            return self.end_fixes[1] - self.start_fixes[1]

    instance = Properties()
    return instance


class Relocations:
    """Relocations is a model for a set of fixes from a given subject.
    Because fixes are temporal, they can be ordered asc or desc. The additional_data dict can contain info
    specific to the subject and relocations: name, type, region, sex etc. These values are applicable to all
    fixes in the relocations array. If they vary, then they should be put into each fix's additional_data dict.
    """

    # TODO: Net Square Displacement
    # TODO: Correlated Random Walk from start fix
    # TODO: Biased Random Walk from start fix
    # TODO: Centroid as the harmonic mean of coordinates (see Avagar et al. 2012)

    def __init__(self, fixes=None, additional_data=None, crs=CRS.WGS84):
        self._fixes = fixes
        self._crs = crs
        self._gdf = self._create_dataframe(fixes)
        self._additional_data = additional_data or dict()

    def _create_dataframe(self, fixes):
        """Create Relocations dataframe. Get all the tranformer instances needed for different reprojection.
        """
        if isinstance(fixes, gpd.GeoDataFrame):
            return fixes.loc[:, ['subject_id', 'fixtime', 'geometry', 'filter_status', 'additional']]
        elif fixes is not None:
            self._crs_strings = set(np.vectorize(lambda x: str(x.geopoint.crs))(self._fixes))
            self.transformers = {crs_str: pyproj_transformer(crs_str, self._crs) for crs_str in self._crs_strings}
            vfunc = np.vectorize(self._fix)
            return gpd.GeoDataFrame(vfunc(fixes).tolist(), crs=self._crs)
        else:
            return gpd.GeoDataFrame()

    def _fix(self, f):
        tranformer = self.transformers.get(str(f.geopoint.crs))
        return pd.Series({'uuid': f.fix_id,
                          'fixtime': f.fixtime,
                          'geometry': f.geopoint.to_crs(tranformer),
                          'filter_status': f.filter_status,
                          'additional': f.additional_data
                          })

    def df(self, temporal_order='ASC', filtered=False):
        ascending = True if temporal_order == 'ASC' else False
        return self._gdf[self._gdf.filter_status == filtered].sort_values(by='fixtime', ascending=ascending)

    _dataframe = property(df)

    @property
    def timespan_seconds(self):
        """Returns the total time between start and end times in seconds"""
        if not self._dataframe.empty:
            earliest_fixtime = self.earliest_fix.fixtime
            latest_fixtime = self.latest_fix.fixtime

            if (earliest_fixtime is not None) and (latest_fixtime is not None):
                ts = latest_fixtime - earliest_fixtime
                return ts.total_seconds()
        else:
            return 0

    @property
    def subject_id(self):
        if not self._gdf.empty:
            return self._gdf.subject_id.unique()
        return

    @property
    def additional_data(self):
        return self._additional_data

    @property
    def fix_count(self):
        """ get_fixes array length"""
        return self._dataframe.shape[0]

    @property
    def earliest_fix(self):
        """ Return the earliest fix from the get_fixes array"""
        _df = self._dataframe
        if not _df.empty:
            return _df.iloc[0]
        else:
            return None

    @property
    def latest_fix(self):
        """ Return the latest fix from the get_fixes array"""
        _df = self._dataframe
        if not _df.empty:
            return _df.iloc[-1]
        else:
            return None

    @property
    def shapely_geometry(self):
        """Return the shapely multipoint geometry of the relocation get_fixes"""
        _pnts = shp.MultiPoint(self._dataframe.geometry)
        return _pnts

    @property
    def wkt_geometry(self):
        return self.shapely_geometry.wkt

    @property
    def ogr_geometry(self):
        """Return the ogr multipoint geometry of the relocation get_fixes"""
        return ogr.CreateGeometryFromWkt(self.wkt_geometry)

    def clip(self, region=None):

        if not type(region) is Region:
            return None

        if self._gdf.empty:
            return None

        if self._gdf.crs == region.crs:
            self._gdf = gpd.clip(self._gdf, Region.shapely_geometry)

        return self

    def to_crs(self, crs):  # rename to_crs
        """function to change coordinate reference system."""
        return self._dataframe.to_crs(crs)

    @property
    def centroid(self):
        """returns GeoSeries of centroids"""
        return self._dataframe.centroid

    def unpack_additional(self,
                          keyname: typing.Union[str, typing.List[str]] = None,
                          colname: typing.Union[str, typing.List[str]] = None):
        """function to extract values from metadata (additional) column and create independent column"""
        self._gdf = BaseMixin.unpack_columns(dataframe=self._gdf,
                                             dict_column='additional',
                                             keyname=keyname,
                                             colname=colname)

    @staticmethod
    def _to_geopandas(df,
                      subject_field,
                      x_field,
                      y_field,
                      wkt_field,
                      wkb_field,
                      fixtime_field,
                      status_field,
                      timezone,
                      crs):
        df[fixtime_field] = pd.to_datetime(df[fixtime_field], utc=timezone)

        if not status_field:
            df[status_field] = False

        if isinstance(df, gpd.GeoDataFrame):
            # make a copy of geodataframe to avoid pointing two variables to the same object in memory.
            gdf = df.copy()
        else:
            if wkt_field:
                geometry = df[wkt_field].apply(lambda x: wkt.loads(x))
            elif wkb_field:
                geometry = gpd.array.from_wkb(df[wkb_field], crs=crs)
            elif x_field and y_field:
                geometry = gpd.points_from_xy(df[x_field], df[y_field])
            else:
                raise ValueError("""No geometry columns fields were passed in the parameters""")
            gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)

        columns = {subject_field: "subject_id",
                   fixtime_field: "fixtime",
                   status_field: "filter_status",
                   'geometry': 'geometry'}

        gdf.rename(columns=columns, inplace=True)
        gdf.index.rename('uuid', inplace=True)
        gdf = BaseMixin.pack_columns(gdf, list(columns.values()))
        return gdf

    @classmethod
    def from_csv(cls,
                 csv_file,
                 subject_field,
                 x_field='lon',
                 y_field='lat',
                 unique_field=None,
                 wkt_field=None,
                 wkb_field=None,
                 fixtime_field='fixtime',
                 filter_status_field=None,
                 timezone=pytz.UTC,
                 crs=CRS.WGS84,
                 header_row=0,
                 compression="infer"
                 ):

        df = pd.read_csv(csv_file, header=header_row, compression=compression)

        if unique_field is not None:
            df.set_index(unique_field, inplace=True)
        else:
            df.index = np.vectorize(lambda x: guid.uuid4())(range(df.shape[0]))

        gdf = cls._to_geopandas(df, subject_field=subject_field,
                                x_field=x_field, y_field=y_field,
                                wkt_field=wkt_field,
                                wkb_field=wkb_field,
                                fixtime_field=fixtime_field,
                                status_field=filter_status_field,
                                timezone=timezone,
                                crs=crs
                                )
        return cls(gdf, crs=crs)

    @classmethod
    def from_geodataframe(cls,
                          gdf,
                          fixtime_field,
                          subject_field='subject_id',
                          unique_field=None,
                          filter_status_field=None,
                          crs=CRS.WGS84,
                          timezone=pytz.UTC
                          ):

        if not isinstance(gdf, gpd.GeoDataFrame):
            raise TypeError('Expecting GeoDataFrame')

        if unique_field is not None:
            gdf.set_index(unique_field, inplace=True)
        else:
            gdf.index = np.vectorize(lambda x: guid.uuid4())(range(gdf.shape[0]))

        gdf = cls._to_geopandas(gdf, subject_field=subject_field,
                                x_field=None,
                                y_field=None,
                                wkt_field=None,
                                wkb_field=None,
                                fixtime_field=fixtime_field,
                                status_field=filter_status_field,
                                crs=crs,
                                timezone=timezone
                                )
        return cls(gdf, crs=crs)

    @classmethod
    def from_feather(cls, path,
                     subject_field,
                     x_field=None,
                     y_field=None,
                     wkt_field=None,
                     wkb_field='geometry',
                     fixtime_field='fixtime',
                     filter_status_field=None,
                     crs=CRS.WGS84,
                     timezone=pytz.UTC,
                     **kwargs):
        """Load a Feather object from the file path, returning a GeoDataFrame."""
        df = feather.read_table(path, **kwargs).to_pandas()

        gdf = cls._to_geopandas(df, subject_field=subject_field,
                                x_field=x_field, y_field=y_field,
                                wkt_field=wkt_field,
                                wkb_field=wkb_field,
                                fixtime_field=fixtime_field,
                                status_field=filter_status_field,
                                timezone=timezone,
                                crs=crs
                                )

        return cls(gdf, crs=crs)

    @classmethod
    def from_parquet(cls, path,
                     subject_field,
                     x_field=None,
                     y_field=None,
                     wkt_field=None,
                     wkb_field='geometry',
                     fixtime_field='fixtime',
                     filter_status_field=None,
                     crs=CRS.WGS84,
                     timezone=pytz.UTC,
                     **kwargs
                     ):
        kwargs["use_pandas_metadata"] = True
        df = parquet.read_table(path, **kwargs).to_pandas()

        gdf = cls._to_geopandas(df, subject_field=subject_field,
                                x_field=x_field, y_field=y_field,
                                wkt_field=wkt_field,
                                wkb_field=wkb_field,
                                fixtime_field=fixtime_field,
                                status_field=filter_status_field,
                                timezone=timezone,
                                crs=crs
                                )
        return cls(gdf, crs=crs)

    @classmethod
    def from_observations(cls, obs_df):
        if not obs_df.empty:
            df = obs_df.assign(filter_status=False)
            df.index.rename('uuid', inplace=True)
            df = BaseMixin.pack_columns(df, ['subject_id', 'fixtime', 'geometry', 'filter_status'])
        else:
            df = None
        return cls(df)

    def sort_fixes(self, temporal_order='ASC'):
        return self._gdf.sort_values(by='fixtime', ascending=True if temporal_order == 'ASC' else False)

    @staticmethod
    def _apply_speedfilter(df, fix_filter):
        gdf = df.assign(_fixtime=df['fixtime'].shift(-1),
                        _geometry=df['geometry'].shift(-1),
                        _filter_status=df['filter_status'].shift(-1))[:-1]

        straight_track = straighttrack_properties(gdf)
        gdf['speed_kmhr'] = straight_track.speed_kmhr

        gdf.loc[(gdf['filter_status'] == False) &
                (gdf['_filter_status'] == False) &
                (gdf['speed_kmhr'] > fix_filter.max_speed_kmhr), 'filter_status'] = True

        gdf.drop(['_fixtime', '_geometry', '_filter_status', 'speed_kmhr'], axis=1, inplace=True)
        return gdf

    @staticmethod
    def _apply_distfilter(df, fix_filter):
        gdf = df.assign(_filter_status=df['_filter_status'].shift(-1),
                        _geometry=df['geometry'].shift(-1))[:-1]

        _, _, distance_m = Geod(ellps="WGS84").inv(gdf['geometry'].x,
                                                   gdf['geometry'].y,
                                                   gdf['_geometry'].x,
                                                   gdf['_geometry'].y)
        gdf['distance_km'] = distance_m / 1000

        gdf.loc[(gdf['filter_status'] == False) &
                (gdf['_filter_status'] == False) &
                (gdf['distance_km'] > fix_filter.max_dist_km), 'filter_status'] = True

        gdf.drop(['_geometry', '_filter_status', 'distance_km'], axis=1, inplace=True)
        return gdf

    def apply_fix_filter(self, fix_filter=None):
        """Apply a given filter by marking the fix filter_status based on the conditions of a filter"""

        # Identify junk fixes based on location coordinate x,y ranges or that match specific coordinates
        if isinstance(fix_filter, RelocsCoordinateFilter):
            self._gdf.loc[(self._gdf['geometry'].x < fix_filter.min_x) |
                          (self._gdf['geometry'].x > fix_filter.max_x) |
                          (self._gdf['geometry'].y < fix_filter.min_y) |
                          (self._gdf['geometry'].y > fix_filter.max_y) |
                          (self._gdf['geometry'].isin(fix_filter.filter_point_coords)), 'filter_status'] = True

        # Mark fixes outside this date range as junk
        if isinstance(fix_filter, RelocsDateRangeFilter):
            if fix_filter.start is not None:
                self._gdf.loc[self._gdf['fixtime'] < fix_filter.start, 'filter_status'] = True

            if fix_filter.end is not None:
                self._gdf.loc[self._gdf['fixtime'] > fix_filter.end, 'filter_status'] = True

        # Mark fixes junk if object needed to move faster than the max_speed_kmhr value to reach next point
        if isinstance(fix_filter, RelocsSpeedFilter):
            self.sort_fixes(temporal_order='ASC')

            if self._gdf.crs == CRS.WGS84:
                self._gdf = self._apply_speedfilter(self._gdf, fix_filter)
            else:
                crs = self._gdf.crs
                self._gdf = self._gdf.to_crs(CRS.WGS84)
                self._gdf = self._apply_speedfilter(self._gdf, fix_filter)
                self._gdf = self._gdf.to_crs(crs)

                # Mark fixes junk if object needed to move greater than the max_dist_meters value to reach next point
        if isinstance(fix_filter, RelocsDistFilter):
            self.sort_fixes(temporal_order='ASC')

            if self._gdf.crs == CRS.WGS84:
                self._gdf = self._apply_distfilter(self._gdf, fix_filter)
            else:
                crs = self._gdf.crs
                self._gdf = self._gdf.to_crs(CRS.WGS84)
                self._gdf = self._apply_distfilter(self._gdf, fix_filter)
                self._gdf = self._gdf.to_crs(crs)

    def reset_fix_filter(self):
        self._gdf['filter_status'] = False


class MultiRelocations(Relocations):
    def apply_fix_filter(self, fix_filter=None):
        if isinstance(fix_filter, RelocsCoordinateFilter) or isinstance(fix_filter, RelocsDateRangeFilter):
            super().apply_fix_filter(fix_filter)

        if isinstance(fix_filter, RelocsSpeedFilter):
            if self._gdf.crs == CRS.WGS84:
                self._gdf = self._gdf.groupby('subject_id').apply(self._apply_speedfilter,
                                                                  fix_filter=fix_filter).droplevel(['subject_id'])
            else:
                crs = self._gdf.crs
                self._gdf = self._gdf.to_crs(CRS.WGS84)
                self._gdf = self._gdf.groupby('subject_id').apply(self._apply_speedfilter,
                                                                  fix_filter=fix_filter).droplevel(['subject_id'])
                self._gdf = self._gdf.to_crs(crs)

        if isinstance(fix_filter, RelocsDistFilter):
            if self._gdf.crs == CRS.WGS84:
                self._gdf = self._gdf.groupby('subject_id').apply(self._apply_distfilter,
                                                                  fix_filter=fix_filter,
                                                                  ).droplevel(['subject_id'])
            else:
                crs = self._gdf.crs
                self._gdf = self._gdf.to_crs(CRS.WGS84)
                self._gdf = self._gdf.groupby('subject_id').apply(self._apply_distfilter,
                                                                  fix_filter=fix_filter,
                                                                  ).droplevel(['subject_id'])

                self._gdf = self._gdf.to_crs(crs)


class Trajectory:
    """
    A trajectory represents a time-ordered collection of segments.
    Currently only straight track segments exist.
    It is based on an underlying relocs object that is the point representation
    """

    def __init__(self, relocs):
        _relocs_df = relocs.df() if isinstance(relocs, Relocations) else relocs
        _relocs_df['_fixtime'] = _relocs_df['fixtime'].shift(-1)
        _relocs_df['_geometry'] = _relocs_df['geometry'].shift(-1)
        self.crs = _relocs_df.crs
        self._other_columns = set(_relocs_df).difference(
            {'subject_id', 'fixtime', 'geometry', 'filter_status', 'additional', '_fixtime', '_geometry'})

        if _relocs_df.crs == CRS.WGS84:
            self._gdf = self._create_trajsegments(_relocs_df[:-1])
        else:
            _relocs_df = _relocs_df.to_crs(CRS.WGS84)  # explicitly project to WGS84 for creating traj segments
            self._gdf = self._create_trajsegments(_relocs_df[:-1])
            self._gdf = self._gdf.to_crs(self.crs)  # reproject back to original crs if different from WGS84

        self.relocs_df = relocs.df() if isinstance(relocs, Relocations) else relocs

    def _create_trajsegments(self, df):
        # TODO: future implementation: how can ew speed this up using a C dll?

        track_properties = straighttrack_properties(df)

        # pygeos.Geometry [LineStrings]
        coords = np.column_stack((np.column_stack(track_properties.start_fixes),
                                  np.column_stack(track_properties.end_fixes))).reshape(df.shape[0], 2, 2)
        geometry = pygeos.linestrings(coords)

        df = BaseMixin.add_col_metadata(dataframe=df, colnames=self._other_columns)

        # assemble results in new dataframe
        return gpd.GeoDataFrame(
            {
                'subject_id': df.subject_id,
                'segment_start': df.fixtime,
                'segment_end': df._fixtime,
                'timespan_seconds': track_properties.timespan_seconds,
                'dist_meters': track_properties.dist_meters,
                'speed_kmhr': track_properties.speed_kmhr,
                'heading': track_properties.heading,
                'x_displacement': track_properties.x_displacement,
                'y_displacement': track_properties.y_displacement,
                'geometry': geometry,
                'filter_status': df.filter_status,
                'additional': df.additional,
            },
            crs=4326,
            index=df.index)

    def df(self, temporal_order='ASC', filtered=False):
        ascending = True if temporal_order == 'ASC' else False
        return self._gdf[self._gdf.filter_status == filtered].sort_values(by='segment_start', ascending=ascending)

    _dataframe = property(df)

    def unpack_additional(self,
                          keyname: typing.Union[str, typing.List[str]],
                          colname: typing.Union[str, typing.List[str]] = None):
        """function to extract values from metadata (additional) column and create independent column"""
        self._gdf = BaseMixin.unpack_columns(dataframe=self._gdf,
                                             dict_column='additional',
                                             keyname=keyname,
                                             colname=colname)

    @property
    def relocs(self):
        """Return the relocs object that make up the trajectory"""
        return self.relocs_df

    def apply_traj_filter(self, traj_seg_filter):
        assert type(traj_seg_filter) is TrajSegFilter
        self._gdf.loc[
            (self._gdf['dist_meters'] < traj_seg_filter.min_length_meters) |
            (self._gdf['dist_meters'] > traj_seg_filter.max_length_meters) |
            (self._gdf['timespan_seconds'] < traj_seg_filter.min_time_secs) |
            (self._gdf['timespan_seconds'] > traj_seg_filter.max_time_secs) |
            (self._gdf['speed_kmhr'] < traj_seg_filter.min_speed_kmhr) |
            (self._gdf['speed_kmhr'] > traj_seg_filter.max_speed_kmhr), 'filter_status'] = True

    @property
    def traj_seg_counts(self):
        """A shortcut to getting the length of the trajectory segments array"""
        return len(self._dataframe.index)

    @property
    def tortuosity(self):
        # TODO Need to implement this property
        return 1.0

    @property
    def length_km(self):
        return sum(self._dataframe['dist_meters'].to_list()) * 1000

    @property
    def shapely_geometry(self):
        """Create MultiLineString object"""
        return shp.MultiLineString(self._dataframe['geometry'].to_list())

    @property
    def ogr_geometry(self):
        # Create an OGR multistring object
        return ogr.CreateGeometryFromWkt(self.wkt_geometry)

    @property
    def wkt_geometry(self):
        return self.shapely_geometry.wkt

    def resample(self):
        # TODO: Need to implement this method
        pass

    @property
    def earliest_segment(self):
        """Return the earliest trajectory segment"""
        _df = self._dataframe
        if not _df.empty:
            return _df.iloc[0]
        else:
            return None

    @property
    def latest_segment(self):
        """Return the latest trajectory segment"""
        _df = self._dataframe
        if not _df.empty:
            return _df.iloc[-1]
        else:
            return None

    def speed_percentiles(self, percentiles=None):
        speed_kmhr = self._dataframe['speed_kmhr']
        if percentiles is None:
            percentiles = [0.5]
        if not isinstance(percentiles, list):
            percentiles = [percentiles]
        return speed_kmhr.quantile(q=percentiles, interpolation='linear')


class MultiTrajectory(Trajectory):

    def __init__(self, multi_relocs):
        _multirelocs_df = multi_relocs.df()
        self.crs = _multirelocs_df.crs

        if _multirelocs_df.crs == CRS.WGS84:
            self._gdf = _multirelocs_df.groupby('subject_id').apply(self._create_multitraj).droplevel(['subject_id'])
        else:
            _relocs_df = _multirelocs_df.to_crs(CRS.WGS84)
            self._gdf = _multirelocs_df.groupby('subject_id').apply(self._create_multitraj).droplevel(['subject_id'])
            self._gdf = self._gdf.to_crs(self.crs)

        self.relocs_df = _multirelocs_df

    def _create_multitraj(self, df):
        df['_fixtime'] = df['fixtime'].shift(-1)
        df['_geometry'] = df['geometry'].shift(-1)
        return self._create_trajsegments(df[:-1])


class AnalysisParams:
    """ An abstract class that acts as a container for calculation parameters"""
    pass


class AnalysisResult:
    """An abstract class to act as a container for calculation results"""

    def __init__(self):
        self._analysis_start = dt.datetime.utcnow()
        self._analysis_end = dt.datetime.utcnow()
        self._errors = []

    @property
    def analysis_start(self):
        return self._analysis_start

    @analysis_start.setter
    def analysis_start(self, value):
        if type(value) is dt.datetime:
            self._analysis_start = value

    @property
    def analysis_end(self):
        return self._analysis_end

    @analysis_end.setter
    def analysis_end(self, value):
        if type(value) is dt.datetime:
            self._analysis_end = value

    @property
    def errors(self):
        return self._errors

    def add_error(self, value):
        self._errors.append(value)


@dataclass
class SpatialFeature:
    """
    A spatial geometry with an associated name and unique ID. Becomes a useful construct in several movdata calculations
    """
    name: str = ''
    unique_id: typing.Any = guid.uuid4()
    ogr_geometry: typing.Any = None

    def __post_init__(self):
        self.wkt_geometry = self.ogr_geometry.ExportToWkt()
        self.shapely_geometry = wkt.loads(self.wkt_geometry)


@dataclass
class Region:
    """
    A polygon with an associated name. Becomes a useful construct in several movdata calculations
    """
    region_name: str = ''
    unique_id: typing.Any = guid.uuid4()
    ogr_geometry: ogr.Geometry = None
    shapely_geometry: typing.Any = None
    crs: pyproj.CRS = CRS.WGS84

    def __post_init__(self):
        self.wkt_geometry = self.shapely_geometry.wkt

    @staticmethod
    def to_crs(self, crs):
        tranformer = pyproj_transformer(self.crs, crs)
        return ops.transform(tranformer.transform, self.shapely_geometry)


class PymetException(Exception):
    """ A custom exception type for movdata specific errors"""
    pass


