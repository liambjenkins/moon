from skyfield.api import load, wgs84
from skyfield import almanac

from .config import MELBOURNE


ts = load.timescale()

eph = load("de421.bsp")

moon = eph["moon"]


location = wgs84.latlon(
    MELBOURNE.latitude,
    MELBOURNE.longitude,
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
            location,
        ),
    )


    moonrise = None
    moonset = None


    for time, event in zip(t, events):

        local_time = (
            time
            .utc_datetime()
            .replace(tzinfo=None)
            .astimezone(MELBOURNE)
        )


        if event == 1 and moonrise is None:

            moonrise = local_time


        elif event == 0 and moonset is None:

            moonset = local_time


    return {
        "moonrise": moonrise,
        "moonset": moonset,
    }
