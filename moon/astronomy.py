from datetime import datetime, timezone

from skyfield.api import load
from skyfield.framelib import ecliptic_frame


ts = load.timescale()

eph = load("de421.bsp")

earth = eph["earth"]
moon = eph["moon"]
sun = eph["sun"]


def datetime_to_time(dt):
    return ts.from_datetime(dt)


def get_moon_longitude(t):

    position = earth.at(t).observe(moon)

    _, longitude, _ = position.frame_latlon(
        ecliptic_frame
    )

    return longitude.degrees % 360


def get_sun_longitude(t):

    position = earth.at(t).observe(sun)

    _, longitude, _ = position.frame_latlon(
        ecliptic_frame
    )

    return longitude.degrees % 360


def get_phase_angle_at(t):

    moon_longitude = get_moon_longitude(t)

    sun_longitude = get_sun_longitude(t)

    return (
        moon_longitude
        - sun_longitude
    ) % 360


def get_raw_moon_data(day):

    dt = datetime(
        day.year,
        day.month,
        day.day,
        12,
        tzinfo=timezone.utc,
    )

    t = datetime_to_time(dt)

    return {
        "angle": get_phase_angle_at(t),
        "longitude": get_moon_longitude(t),
    }


def get_phase_angle(dt):

    t = datetime_to_time(dt)

    return get_phase_angle_at(t)
