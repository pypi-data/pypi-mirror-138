import datetime
import typing
import numpy as np
import pandas as pd
import astropy.time
import astropy.coordinates
from dataclasses import dataclass, field


class Lunar:

    def __init__(self, ):
        pass

    @classmethod
    def angle(cls, time):
        """Calculate lunar orbital phase in degrees"""
        sun = astropy.coordinates.get_sun(time=time)
        moon = astropy.coordinates.get_moon(time=time)
        # angular separation from moon to sun
        elongation = moon.separation(sun)
        return elongation

    @classmethod
    def illumination(cls, time):
        """
        Calculate fraction of the moon illumination;
        moon is fully illuminated at the full moon (fraction = 1.00)
        during crescent visible fraction ranges from 0.00 to 0.5
        """
        elongation = cls.angle(time)
        # degree of illumination is given by (1 - cos e) /2 = sin^2(e/2) where e is elongation
        return (1 - np.cos(elongation)) / 2.


@dataclass
class Sun:
    """
    Equations used in calculating sunrise & sunset are taken from NOAA solar calculation excel sheet at this url.
    [https://gml.noaa.gov/grad/solcalc/calcdetails.html]
    """
    latitude: typing.Union[float, np.ndarray]
    longitude: typing.Union[float, np.ndarray]
    time: datetime.datetime
    utc_offset: int = 0
    sun_radius: float = field(init=False, repr=False, default=695800000.)  # radiation at suns surface (W/m^2)
    sun_surface_radion: float = field(init=False, repr=False, default=63156942.6)  # radius of the sun in meters
    orbital_period: float = field(init=False, repr=False, default=365.2563630)  # days it takes earth to revolve

    def __post_init__(self):
        self.abs_julian_date = astropy.time.Time(self.time).jd
        self.abs_julian_century = jc = (self.abs_julian_date - 2451545) / 36525.0

        # # oblique mean elliptic of earth orbit
        self.oblique_mean_elip = 23 + (26 + (21.448 - jc * (46.815 + jc * (0.00059 - jc * 0.001813))) / 60) / 60
        # the oblique correction
        self.oblique_correction = self.oblique_mean_elip + 0.00256 * np.cos(np.radians(125.04 - 1934.136 * jc))
        # geometric mean longitude of the sun
        self.geomean_longitude = (280.46646 + jc * (36000.76983 + jc * 0.0003032)) % 360
        # precise eccentricity of earths orbit at referece datetime
        self.earth_eccent = 0.016708634 - jc * (4.2037e-5 + 1.267e-7 * jc)
        # eometric mean anomoly of the sun
        self.geomean_anomoly = (357.52911 + jc * (35999.05029 - 0.0001537 * jc))

    def equation_of_time(self):
        oc = np.radians(self.oblique_correction)
        gml = np.radians(self.geomean_longitude)
        gma = np.radians(self.geomean_anomoly)
        ec = self.earth_eccent

        vary = np.tan(oc / 2) ** 2

        return 4 * np.degrees(vary * np.sin(2 * gml) - 2 * ec * np.sin(gma) +
                              4 * ec * vary * np.sin(gma) * np.cos(2 * gml) -
                              0.5 * vary * vary * np.sin(4 * gml) -
                              1.25 * ec * ec * np.sin(2 * gma))

    def get_sun_eq_of_center(self):
        """ :return sun_eq_of_center: the suns equation of center"""
        gma = np.radians(self.geomean_anomoly)

        return np.sin(gma) * (1.914602 - self.abs_julian_century *
                              (0.004817 + 0.000014 * self.abs_julian_century)) + \
               np.sin(2 * gma) * (0.019993 - 0.000101 * self.abs_julian_century) + \
               np.sin(3 * gma) * 0.000289

    def apparent_longitude(self):
        stl = self.true_long()
        return stl - 0.00569 - 0.00478 * np.sin(np.radians(125.04 - 1934.136 * self.abs_julian_century))

    def true_long(self):
        # true longitude of the sun
        return self.geomean_longitude + self.get_sun_eq_of_center()

    def get_declination(self):
        sal = np.radians(self.apparent_longitude())
        oc = np.radians(self.oblique_correction)
        return np.degrees(np.arcsin(np.sin(oc) * np.sin(sal)))

    def solar_noon(self):
        eqn_time = self.equation_of_time()
        lon = self.longitude
        tz = self.utc_offset
        solar_noon = (720 - 4 * lon - eqn_time + tz * 60) / 1440
        # solar_noon_time = dt.timedelta(days=solar_noon)
        return solar_noon

    def hour_angle_sunrise(self):
        declination = np.radians(self.get_declination())
        lat = np.radians(self.latitude)

        return np.degrees(np.arccos((np.cos(np.radians(90.833)) /
                                     (np.cos(lat) * np.cos(declination)) - np.tan(lat) * np.tan(declination))))

    def sunrise_time(self):
        solar_noon = self.solar_noon()
        hour_angle_sunrise = self.hour_angle_sunrise()
        sunrise = (solar_noon * 1440 - hour_angle_sunrise * 4) / 1440
        sunrise_time = datetime.timedelta(days=sunrise)
        return sunrise_time

    def sunset_time(self):
        solar_noon = self.solar_noon()
        hour_angle_sunrise = self.hour_angle_sunrise()
        sunset = (solar_noon * 1440 + hour_angle_sunrise * 4) / 1440
        sunset_time = datetime.timedelta(days=sunset)
        return sunset_time

    def sunlight(self):
        hour_angle_sunrise = self.hour_angle_sunrise()
        daylight_hours = 8 * hour_angle_sunrise / 1440
        return daylight_hours


def lunar_luminosity(multirelocations):
    fixtime = astropy.time.Time(multirelocations.fixtime)
    illumination = Lunar.illumination(fixtime)
    return illumination


def day_night(multirelocations, utcoffset=0):
    # 0 means night & 1 means day
    fixtime = astropy.time.Time(multirelocations.fixtime)
    ndarray = np.column_stack([multirelocations.geometry.x,
                               multirelocations.geometry.y,
                               fixtime])

    def _is_day_or_night(m):
        ycoord, xcoord, time = m
        sun = Sun(latitude=ycoord, longitude=xcoord, time=time, utc_offset=utcoffset)
        sunset = sun.sunset_time()
        sunrise = sun.sunrise_time()

        f = time.to_datetime()
        fixtime_date = f.date()
        sunrise_time = datetime.datetime(fixtime_date.year, fixtime_date.month, fixtime_date.day) + sunrise
        sunset_time = datetime.datetime(fixtime_date.year, fixtime_date.month, fixtime_date.day) + sunset

        return 'day' if sunrise_time <= f < sunset_time else 'night'
    vfunc = np.vectorize(_is_day_or_night, signature='(n)->()', otypes=['object'])
    _dayornight = vfunc(ndarray)
    return _dayornight


def daynight_ratio(trajectory_df, daynight_colname):
    colname = daynight_colname.split('.')
    df = trajectory_df
    if 'additional' in colname:
        daynight_colname = colname[1]
        df = pd.json_normalize(trajectory_df.additional)
    val_count = df[daynight_colname].value_counts(normalize=True)
    return val_count.day / val_count.night

