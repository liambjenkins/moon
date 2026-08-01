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

    return ts.from_datetime(
        dt.astimezone(
            timezone.utc
        )
    )



def get_moon_position(t):

    position = (
        earth
        .at(t)
        .observe(moon)
        .apparent()
    )

    latitude, longitude, _ = position.frame_latlon(
        ecliptic_frame
    )

    return {
        "longitude": longitude.degrees % 360,
        "latitude": latitude.degrees,
    }



def get_sun_position(t):

    position = (
        earth
        .at(t)
        .observe(sun)
        .apparent()
    )

    latitude, longitude, _ = position.frame_latlon(
        ecliptic_frame
    )

    return {
        "longitude": longitude.degrees % 360,
        "latitude": latitude.degrees,
    }



def get_moon_longitude(t):

    return get_moon_position(t)["longitude"]



def get_moon_latitude(t):

    return get_moon_position(t)["latitude"]



def get_sun_longitude(t):

    return get_sun_position(t)["longitude"]



def get_phase_angle_at(t):

    return (
        get_moon_longitude(t)
        -
        get_sun_longitude(t)
    ) % 360



def prepare_datetime(dt):

    if dt.tzinfo is None:
        dt = dt.replace(
            tzinfo=timezone.utc
        )

    return dt.astimezone(
        timezone.utc
    )



def get_phase_angle(dt):

    return get_phase_angle_at(
        datetime_to_time(
            prepare_datetime(dt)
        )
    )



def get_moon_longitude_at(dt):

    return get_moon_longitude(
        datetime_to_time(
            prepare_datetime(dt)
        )
    )



def get_moon_latitude_at(dt):

    return get_moon_latitude(
        datetime_to_time(
            prepare_datetime(dt)
        )
    )



def get_sun_longitude_at(dt):

    return get_sun_longitude(
        datetime_to_time(
            prepare_datetime(dt)
        )
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
        local_time
    )


    angle = get_phase_angle_at(
        t
    )


    moon_position = get_moon_position(
        t
    )


    return {

        "angle": angle,

        "longitude": moon_position["longitude"],

        "latitude": moon_position["latitude"],

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
