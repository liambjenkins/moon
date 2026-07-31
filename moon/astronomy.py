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


def get_moon_sun_angle(t):

    moon_position = earth.at(t).observe(moon)
    sun_position = earth.at(t).observe(sun)

    return moon_position.separation_from(
        sun_position
    ).degrees


def get_moon_longitude(t):

    position = earth.at(t).observe(moon)

    _, longitude, _ = position.frame_latlon(
        ecliptic_frame
    )

    return longitude.degrees % 360


def get_raw_moon_data(day):

    dt = datetime(
        day.year,
        day.month,
        day.day,
        12,
        tzinfo=timezone.utc,
    )

    t = datetime_to_time(dt)

    angle = get_moon_sun_angle(t)

    return {
        "angle": angle,
        "longitude": get_moon_longitude(t),
    }


def get_phase_angle(dt):

    t = datetime_to_time(dt)

    return get_moon_sun_angle(t)
