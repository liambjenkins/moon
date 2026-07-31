from datetime import datetime, timezone

from skyfield.api import load
from skyfield import almanac
from moon.config import MELBOURNE


ts = load.timescale()

eph = load("de421.bsp")

earth = eph["earth"]
moon = eph["moon"]


def get_rise_set(day):

    start = ts.utc(
        day.year,
        day.month,
        day.day,
        0
    )

    end = ts.utc(
        day.year,
        day.month,
        day.day,
        23
    )

    observer = (
        earth
        + earth.topos(
            latitude_degrees=MELBOURNE.latitude,
            longitude_degrees=MELBOURNE.longitude
        )
    )

    t, events = almanac.find_discrete(
        start,
        end,
        almanac.risings_and_settings(
            eph,
            moon,
            observer
        )
    )

    moonrise = None
    moonset = None

    for time, event in zip(t, events):

        dt = time.utc_datetime()

        if event == 1:
            moonrise = dt

        else:
            moonset = dt


    return {
        "moonrise": moonrise,
        "moonset": moonset,
    }
