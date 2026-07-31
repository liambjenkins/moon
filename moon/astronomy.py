from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from skyfield.api import load
from skyfield.framelib import ecliptic_frame


MELBOURNE = ZoneInfo("Australia/Melbourne")

ts = load.timescale()

eph = load("de421.bsp")

earth = eph["earth"]
moon = eph["moon"]
sun = eph["sun"]


def datetime_to_time(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return ts.from_datetime(dt)


def get_moon_longitude(t):

    position = (
        earth
        .at(t)
        .observe(moon)
        .apparent()
    )

    _, longitude, _ = position.frame_latlon(
        ecliptic_frame
    )

    return longitude.degrees % 360


def get_sun_longitude(t):

    position = (
        earth
        .at(t)
        .observe(sun)
        .apparent()
    )

    _, longitude, _ = position.frame_latlon(
        ecliptic_frame
    )

    return longitude.degrees % 360


def get_phase_angle_at(t):

    moon_lon = get_moon_longitude(t)
    sun_lon = get_sun_longitude(t)

    return (
        moon_lon - sun_lon
    ) % 360


def get_raw_moon_data(day):

    local_time = datetime(
        day.year,
        day.month,
        day.day,
        12,
        tzinfo=MELBOURNE,
    )

    utc_time = local_time.astimezone(
        timezone.utc
    )

    t = datetime_to_time(
        utc_time
    )

    angle = get_phase_angle_at(t)

    return {
        "angle": angle,
        "longitude": get_moon_longitude(t),
        "illumination": round(
            (1 - __import__("math").cos(
                __import__("math").radians(angle)
            )) / 2 * 100
        )
    }


def get_phase_angle(dt):

    if dt.tzinfo is None:
        dt = dt.replace(
            tzinfo=timezone.utc
        )

    return get_phase_angle_at(
        datetime_to_time(dt)
    )
