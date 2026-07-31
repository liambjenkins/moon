from datetime import datetime, timezone

from skyfield.api import load
from skyfield.framelib import ecliptic_frame


ts = load.timescale()

loader = load

eph = loader("de421.bsp")

earth = eph["earth"]
moon = eph["moon"]
sun = eph["sun"]


def datetime_to_time(dt):
    return ts.from_datetime(dt)


def melbourne_day_to_datetime(day):

    return datetime(
        day.year,
        day.month,
        day.day,
        12,
        tzinfo=timezone.utc,
    )


def moon_sun_angle(t):

    moon_position = earth.at(t).observe(moon)
    sun_position = earth.at(t).observe(sun)

    return moon_position.separation_from(
        sun_position
    ).degrees


def moon_ecliptic_longitude(t):

    position = earth.at(t).observe(moon)

    _, longitude, _ = position.frame_latlon(
        ecliptic_frame
    )

    return longitude.degrees % 360


def get_illumination(angle):

    import math

    illuminated = (
        1 - math.cos(math.radians(angle))
    ) / 2

    return round(illuminated * 100)


def get_raw_moon_data(day):

    dt = melbourne_day_to_datetime(day)

    t = datetime_to_time(dt)

    angle = moon_sun_angle(t)

    return {
        "angle": angle,
        "illumination": get_illumination(angle),
        "longitude": moon_ecliptic_longitude(t),
    }
