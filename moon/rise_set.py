from skyfield.api import load, Topos
from skyfield import almanac

from moon.config import MELBOURNE


ts = load.timescale()

eph = load("de421.bsp")

earth = eph["earth"]
moon = eph["moon"]


observer = earth + Topos(
    latitude_degrees=MELBOURNE.latitude,
    longitude_degrees=MELBOURNE.longitude,
)


def get_rise_set(day):

    start = ts.utc(
        day.year,
        day.month,
        day.day,
        0,
    )

    end = ts.utc(
        day.year,
        day.month,
        day.day,
        23,
    )

    t, events = almanac.find_discrete(
        start,
        end,
        almanac.risings_and_settings(
            eph,
            moon,
            observer,
        ),
    )

    moonrise = None
    moonset = None

    for time, event in zip(t, events):

        if event == 1:
            moonrise = time.utc_datetime()

        else:
            moonset = time.utc_datetime()

    return {
        "moonrise": moonrise,
        "moonset": moonset,
    }
