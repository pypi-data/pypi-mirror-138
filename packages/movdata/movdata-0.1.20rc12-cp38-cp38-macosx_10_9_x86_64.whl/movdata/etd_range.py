import math
import os
import tempfile
import typing
from dataclasses import dataclass

import geopandas
import numpy as np
import pandas
from joblib import Parallel, delayed
from joblib import load, dump
from pyproj import Geod
import scipy
from scipy.integrate import quad
from scipy.optimize import minimize
from scipy.stats import weibull_min

import movdata.raster as rst
from movdata import base
from movdata import _etd
import warnings
from numba import cuda, float32, float64


class Geometry:

    @classmethod
    def get_distant(cls, x1: float, y1: float, x2: float, y2: float):
        # by the Pythagorean Theorem get the length of the vector ||V|| of points P(x1, y1) and Q(x2, y2)
        # coordinates should be projected or this is not a valid approach
        return math.sqrt(math.pow((y2 - y1), 2) + math.pow((x2 - x1), 2))

    @classmethod
    def great_circle_distant(cls,
                             lons1: typing.Any,
                             lats1: typing.Any,
                             lons2: typing.Any,
                             lats2):
        _, _, distance = Geod(ellps="WGS84").inv(lons1=lons1, lats1=lats1, lons2=lons2, lats2=lats2)
        return distance


class WeibullPDF:

    @staticmethod
    def fit(data, floc=0):
        # returns estimates of shape and scale parameters from data; keeping the location fixed
        shape, _, scale = weibull_min.fit(data, floc=floc)
        return shape, scale

    @staticmethod
    def pdf(data, shape, location=0, scale=1):
        # probability density function.
        return weibull_min.pdf(x=data, c=shape, loc=location, scale=scale)

    @staticmethod
    def cdf(data, shape, location=0, scale=1):
        # cumulative distribution function.
        return weibull_min.cdf(x=data, c=shape, loc=location, scale=scale)

    @staticmethod
    def nelder_mead(func, x0, args=(), **kwargs):
        # minimization of scalar function of one or more variables using the Nelder-Mead algorithm.
        return minimize(fun=func, x0=x0, args=args, method='Nelder-Mead', **kwargs)

    @staticmethod
    def expected_func(speed, shape, scale, time, distance):
        # time-density expectation function for two-parameter weibull distribution.
        _funcs = [4 * shape / (math.pi * scale * speed),
                  math.pow((speed / scale), shape - 1),
                  math.exp(-1 * math.pow(speed / scale, shape)) / math.sqrt(np.square(speed) * np.square(time)
                                                                            - np.square(distance)
                                                                            )]
        return math.prod(_funcs)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)


@dataclass
class Weibull2Parameter(WeibullPDF):
    shape: float = 1.
    scale: float = 1.


@dataclass
class Weibull3Parameter(WeibullPDF):
    # Weibull parameterization using scale=a(t^b)(c^t)
    shape: float = 1.
    a: float = 1.
    b: float = 1.
    c: float = 1.


@dataclass(init=True, repr=True)
class ETDProfile(base.AnalysisParams):
    output_path: typing.Union[str, bytes, os.PathLike]
    max_datagap_secs: int = 14400
    max_speed_kmhr: float = 0.
    max_speed_percentage: float = 0.9999
    intstep_kmhr: float = 0.001
    prob_dens_cutoff: float = 1E-10
    raster_profile: rst.RasterProfile = None
    expansion_factor: float = 1.3
    threadsperblock: int = 32
    weibull_pdf: typing.Union[Weibull2Parameter, Weibull3Parameter] = Weibull2Parameter()


# time-density expectation lowlevel callable function for two-parameter weibull distribution.
expect_value_integrand = scipy.LowLevelCallable.from_cython(_etd, 'expected_fn')
CENTROID_SIZE = 0


class ETD:

    @classmethod
    def calculate_etd_range(cls, trajectory_gdf: geopandas.GeoDataFrame, etd_profile: ETDProfile, gpu_parallel=False):
        folder = tempfile.mkdtemp()
        weibull_pdf = etd_profile.weibull_pdf

        # if two-parameter weibull have default values; run an optimization routine to auto-determine parameters
        if isinstance(weibull_pdf, Weibull2Parameter) and all([weibull_pdf.shape == 1., weibull_pdf.scale == 1.]):
            speed_kmhr = trajectory_gdf.speed_kmhr
            shape, scale = weibull_pdf.fit(speed_kmhr)

            # update the shape/scale parameters
            weibull_pdf.shape = shape
            weibull_pdf.scale = scale

        # reproject trajseg to desired crs
        trajectory_gdf = trajectory_gdf.to_crs(etd_profile.raster_profile.crs)

        # determine envelope of trajectory
        x_min, y_min, x_max, y_max = trajectory_gdf.geometry.total_bounds

        # apply expansion factor on the trajectory total bound.
        if etd_profile.expansion_factor > 1.0:
            dx = (x_max - x_min) * (etd_profile.expansion_factor - 1.0) / 2.0
            dy = (y_max - y_min) * (etd_profile.expansion_factor - 1.0) / 2.0
            x_min -= dx
            x_max += dx
            y_min -= dy
            y_max += dy

        # update the raster extent for the raster profile
        etd_profile.raster_profile.raster_extent = rst.RasterExtent(x_min=x_min,
                                                                    x_max=x_max,
                                                                    y_min=y_min,
                                                                    y_max=y_max)

        # determine the output raster size
        num_rows, num_columns = etd_profile.raster_profile.rows, etd_profile.raster_profile.columns

        # determine overall data times-span
        total_time = np.sum(trajectory_gdf.timespan_seconds) / 3600  # hours

        # maximum trajectory segment speed value
        max_trajseg_speed = trajectory_gdf.speed_kmhr.max()

        # determine max-speed value
        if etd_profile.max_speed_kmhr > 0.:
            maxspeed = etd_profile.max_speed_kmhr
        else:
            # Use a value calculated from the CDF
            maxspeed = weibull_pdf.scale * math.pow(-1 * math.log(1. - etd_profile.max_speed_percentage),
                                                    1. / weibull_pdf.shape)
        if maxspeed <= max_trajseg_speed:
            raise ValueError(f"ETD maximum speed value: {maxspeed} should be greater than "
                             f"trajectory maximum speed value {max_trajseg_speed}")
        print('Using {0} as the max_speed_kmhr value'.format(maxspeed))

        # Define the affine transform to get grid pixel centroids as geographic coordinates.
        grid_centroids = np.array(etd_profile.raster_profile.transform.to_gdal()).reshape(2, 3)
        grid_centroids[0, 0] = x_min + etd_profile.raster_profile.pixel_size * 0.5
        grid_centroids[1, 0] = y_max - etd_profile.raster_profile.pixel_size * 0.5

        # all grid centroids
        pixel_coords = np.array([[1, k, r] for r in range(num_rows) for k in range(num_columns)])
        pixel_coords = pixel_coords.reshape([len(pixel_coords), 3, 1])
        centroids = np.dot(grid_centroids, pixel_coords)

        if gpu_parallel:
            # trajectory coords
            def _trajectory_coords(geom):
                pointx, pointy = geom.coords[0]
                point2x, point2y = geom.coords[1]
                return pointx, pointy, point2x, point2y

            trvfunc = np.vectorize(_trajectory_coords)
            coords = np.column_stack(trvfunc(trajectory_gdf.geometry))
            # timespan
            timespan = (trajectory_gdf.timespan_seconds.to_numpy()).reshape((trajectory_gdf.shape[0], 1))
            # append timespan to coords to create relevant matrix.
            matrix = np.append(coords, timespan, axis=1)
            raster_ndarray = np.zeros(shape=(num_rows * num_columns), dtype=np.float64)
            global CENTROID_SIZE
            CENTROID_SIZE = num_rows * num_columns

            # Initialise the kernel
            blockpergrid = (trajectory_gdf.shape[0] + (etd_profile.threadsperblock - 1)) // etd_profile.threadsperblock
            _calc_raster_gpu[blockpergrid, etd_profile.threadsperblock](matrix,
                                                                        centroids,
                                                                        weibull_pdf.shape,
                                                                        weibull_pdf.scale,
                                                                        total_time,
                                                                        maxspeed,
                                                                        etd_profile.intstep_kmhr,
                                                                        raster_ndarray)
        else:
            # create a temporary file for storing memmap files.
            centroid_coord_tmp = os.path.join(folder, 'centroid_coord_tmp.mmap')
            raster_ndarray_tmp = os.path.join(folder, 'raster_ndarray.mmap')

            # Create a blank grid array and dump the data array to memmap to speedup the parallel process.
            # To-Do: this seems inefficient. Is there a better way
            raster_ndarray = np.zeros(shape=(num_rows, num_columns), dtype=np.float64)
            dump(raster_ndarray, raster_ndarray_tmp)
            raster_ndarray = load(raster_ndarray_tmp, mmap_mode='w+')

            # Dump the pixel centroids coordinates to disk to free the memory
            dump(centroids, centroid_coord_tmp)

            # Release the reference on the original in memory array and replace it
            # by a reference to the memmap array so that the garbage collector can
            # release the memory before forking. gc.collect() is internally called
            # in Parallel just before forking.
            centroids_coords = load(centroid_coord_tmp, mmap_mode='r')

            # Fork the worker processes to perform computation concurrently
            parameters = ((row,
                           weibull_pdf.shape,
                           weibull_pdf.scale,
                           maxspeed,
                           num_rows,
                           num_columns,
                           raster_ndarray,
                           total_time,
                           centroids_coords,
                           ) for index, row in trajectory_gdf.iterrows())

            Parallel(n_jobs=-1, verbose=8)(delayed(cls._raster_calc)(*p) for p in parameters)

        # Normalize the grid values
        sum = np.sum(raster_ndarray)
        raster_ndarray = raster_ndarray / sum

        # Set the null data values
        no_data_mask = raster_ndarray == 0.
        raster_ndarray[no_data_mask] = etd_profile.raster_profile.nodata_value

        # write raster_ndarray to GeoTIFF file.
        rst.RasterPy.write(ndarray=raster_ndarray, fp=etd_profile.output_path, **etd_profile.raster_profile)

    @classmethod
    def _raster_calc(cls,
                     trajectory_segment: pandas.Series,
                     shape: float,
                     scale: float,
                     max_speed_kmhr: float,
                     row: int,
                     column: int,
                     raster_ndarray,
                     total_time,
                     centroids_coords
                     ):

        # if trajectory_segment.timespan_seconds < max_datagap: can lose this since should filter straight away
        coords = trajectory_segment.geometry.coords

        # get the coordinate (x, y) for the first and last point from MultiLinestring
        pointx, pointy = coords[0]
        point2x, point2y = coords[1]

        # the fraction of time of this segment compared to all segments
        tfrac = (trajectory_segment.timespan_seconds / 3600) / total_time

        # calculate distance from Point P -> Z
        coordinate_distance = np.sqrt(np.subtract(pointx, centroids_coords[0]) ** 2 +
                                      np.subtract(pointy, centroids_coords[1]) ** 2)

        # calculate distance from Point Z -> P2
        coordinate_distance2 = np.sqrt(np.subtract(centroids_coords[0], point2x) ** 2 +
                                       np.subtract(centroids_coords[1], point2y) ** 2)

        # total distance from point P -> Z -> P2
        distance = np.sum([coordinate_distance, coordinate_distance2], axis=0) * 0.001

        # calculate speed of travel to reach every grid cell centroid from P1->Z->P2
        time = trajectory_segment.timespan_seconds / 3600
        _speeds = distance / time
        speeds = _speeds.reshape(row, column)

        # Set flag for elements that meet out max-speed criteria.
        # ...and then eliminate the grids outside that threshold
        lte_mask = speeds <= max_speed_kmhr
        evs = np.zeros_like(speeds)

        def expected_value(minspeed):
            return quad(expect_value_integrand, a=minspeed, b=max_speed_kmhr, args=(shape,
                                                                                    scale,
                                                                                    time,
                                                                                    minspeed * time  # distance
                                                                                    ))[0]
        vfunc = np.vectorize(expected_value)

        expected_value = 0.
        if speeds[lte_mask].size > 0:
            evs[lte_mask] = vfunc(speeds[lte_mask])
            expected_value = np.sum(evs)
        else:
            message = 'None of grid centroids are reachable; either increase maxspeed value or decrease ' \
                      'the grid size to reflect data correctly.'
            warnings.warn(message=message, category=UserWarning)

        if expected_value > 0.:
            raster_ndarray += (evs / expected_value) * tfrac


@cuda.jit
def _calc_raster_gpu(traj_matrix: np.ndarray,
                     centroids: np.ndarray,
                     shape: typing.Union[int, float],
                     scale: typing.Union[int, float],
                     total_time: typing.Union[int, float],
                     maxspeed: typing.Union[int, float],
                     intstep_kmhr: typing.Union[int, float],
                     raster_ndarray: np.ndarray,
                     ):
    # absolute position of the current thread in the grid of blocks.
    pos = cuda.grid(1)
    px, py, p1x, p1y, timespan = traj_matrix[pos]
    time, expected_value = timespan / 3600, 0

    # Allocate a local array of size centroids.
    # The array is private to current thread.
    # shape of array must be constant expression.
    evs = cuda.local.array(shape=(CENTROID_SIZE), dtype=float64)
    delta = intstep_kmhr

    for index in range(centroids.shape[1]):
        # calculate distance from Point P -> Z
        coord_distance = math.sqrt((px - centroids[0, index][0]) ** 2 + (py - centroids[1, index][0]) ** 2)
        # calculate distance from Point Z -> P2
        coord_distance2 = math.sqrt((centroids[0, index][0] - p1x) ** 2 + (centroids[1, index][0] - p1y) ** 2)
        # total distance from point P -> Z -> P2
        distance = (coord_distance + coord_distance2) * 0.001
        # calculate speed of travel to reached from P1->Z->P2
        s = distance / time
        mu = s + delta / 2
        minspeed = s + delta
        evsum = 0
        if mu < maxspeed:
            while mu < maxspeed:
                if minspeed <= maxspeed:
                    _delta = delta
                else:
                    _speed = minspeed - delta
                    rem = _delta = maxspeed - _speed
                    mu = rem / 2 + _speed

                evsum += delta * (4 * shape * math.pow((mu / scale), shape - 1) *
                                  math.exp(-1 * math.pow((mu / scale), shape))) / \
                         (scale * math.pi * mu * math.sqrt((mu * mu) * (time * time) - (distance * distance)))
                mu += delta
                minspeed += delta
        evs[index] = evsum
        expected_value += evsum

    # the fraction of time of this segment compared to all segments
    tfrac = time / total_time

    for i in range(CENTROID_SIZE):
        raster_ndarray[i] += (evs[i] / expected_value) * tfrac
