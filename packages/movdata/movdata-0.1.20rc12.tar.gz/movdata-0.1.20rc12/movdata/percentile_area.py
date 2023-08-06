import movdata.base as base
import datetime as dt
import os
import numpy as np
import fiona
import typing
import rasterio
import rasterio.features
import pandas as pd
import geopandas as gp
from dataclasses import dataclass, field
from shapely.geometry import shape, mapping
from shapely.geometry.multipolygon import MultiPolygon


@dataclass
class PercentileAreaProfile(base.AnalysisParams):
    input_raster: typing.Union[str, bytes, os.PathLike]
    percentile_levels: typing.List = field(default_factory=[50.])
    subject_id: str = ''


@dataclass
class PercentileAreaAnalysisResults(base.AnalysisResult):
    percentile: float = 100.
    area: float = 0.
    geo: typing.Any = None


class PercentileArea:

    @staticmethod
    def _multipolygon(shapes, percentile):
        return MultiPolygon([shape(geom) for geom, value in shapes if value == percentile])

    @classmethod
    def calculate_percentile_area(cls, profile: PercentileAreaProfile):

        # create result object
        result = PercentileAreaAnalysisResults()
        result.analysis_start = dt.datetime.utcnow()

        try:
            assert type(profile) is PercentileAreaProfile
            shapes = []

            # open raster
            with rasterio.open(profile.input_raster) as src:
                crs = src.crs.to_wkt()

                for percentile in profile.percentile_levels:
                    data_array = src.read(1).astype(np.float32)

                    # Mask no-data values
                    data_array[data_array == src.nodata] = np.nan

                    # calculate percentile value
                    percentile_val = np.percentile(data_array[~np.isnan(data_array)], 100.0 - percentile)

                    # TODO: make a more explicit comparison for less than and greater than

                    # Set any vals less than the cutoff to be nan
                    data_array[data_array < percentile_val] = np.nan

                    # Mask any vals that are less than the cutoff percentile
                    data_array[data_array >= percentile_val] = percentile

                    shapes.extend(rasterio.features.shapes(data_array, transform=src.transform))

            data = [[profile.subject_id, percentile, cls._multipolygon(shapes, percentile)]
                    for percentile in sorted(profile.percentile_levels, reverse=True)]
            df = pd.DataFrame(data, columns=['subject_id', 'percentile', 'geometry'])

            return gp.GeoDataFrame(df, geometry=df.geometry, crs=crs)

        except Exception as e:
            result.add_error(e)


