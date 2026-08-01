from datetime import datetime, timezone
from math import cos, radians
from skyfield.api import load
from skyfield.framelib import ecliptic_frame

from .config import MELBOURNE_TZ


ts = load.timescale()

eph = load("de421.bsp")

earth = eph["earth"]
moon = eph["moon"]
sun = eph["sun"]



def datetime_to_time(dt):

    if dt.tzinfo is None:
        dt = dt.replace(
            tzinfo=timezone.utc
        )

    return ts.from_datetime(dt)



def prepare_datetime(dt):

    if dt.tzinfo is None:
        dt = dt.replace(
            tzinfo=timezone.utc
        )

    return dt.astimezone(
        timezone.utc
    )



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

    return (
        get_moon_longitude(t)
        -
        get_sun_longitude(t)
    ) % 360



def get_phase_angle(dt):

    dt = prepare_datetime(dt)

    return get_phase_angle_at(
        datetime_to_time(dt)
    )



def get_moon_longitude_at(dt):

    dt = prepare_datetime(dt)

    return get_moon_longitude(
        datetime_to_time(dt)
    )



def get_sun_longitude_at(dt):

    dt = prepare_datetime(dt)

    return get_sun_longitude(
        datetime_to_time(dt)
    )



def get_raw_moon_data(day):

    local_time = datetime(
        day.year,
        day.month,
        day.day,
        0,
        1,
        tzinfo=MELBOURNE_TZ,
    )


    t = datetime_to_time(
        local_time.astimezone(
            timezone.utc
        )
    )


    angle = get_phase_angle_at(t)


    return {

        "angle": angle,

        "longitude": get_moon_longitude(t),

        "illumination": round(
            (
                1
                -
                cos(
                    radians(angle)
                )
            )
            /
            2
            *
            100
        ),

    }
