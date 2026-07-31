from datetime import datetime, timezone

from skyfield.api import load
from skyfield.framelib import ecliptic_frame

from moon.config import MELBOURNE


ts = load.timescale()

eph = load("de421.bsp")

earth = eph["earth"]
moon = eph["moon"]
sun = eph["sun"]


def get_time(day):

    dt = datetime(
        day.year,
        day.month,
        day.day,
        12,
        tzinfo=timezone.utc,
    )

    return ts.from_datetime(dt)


def moon_longitude(t):

    position = earth.at(t).observe(moon)

    _, longitude, _ = position.frame_latlon(
        ecliptic_frame
    )

    return longitude.degrees % 360


def moon_sun_angle(t):

    moon_position = earth.at(t).observe(moon)
    sun_position = earth.at(t).observe(sun)

    return moon_position.separation_from(
        sun_position
    ).degrees


def get_raw_moon_data(day):

    t = get_time(day)

    return {
        "longitude": moon_longitude(t),
        "angle": moon_sun_angle(t),
    }
