from datetime import datetime, timezone
from skyfield import almanac

from moon.astronomy import ts, eph


def find_seasonal_events(start_date, end_date):

    events = []


    start = ts.utc(
        start_date.year,
        start_date.month,
        start_date.day
    )


    end = ts.utc(
        end_date.year,
        end_date.month,
        end_date.day
    )


    times, seasons = almanac.find_discrete(
        start,
        end,
        almanac.seasons(eph)
    )


    names = {
        0: "March Equinox",
        1: "June Solstice",
        2: "September Equinox",
        3: "December Solstice",
    }


    for time, season in zip(
        times,
        seasons
    ):

        events.append(
            {
                "type": names[season],
                "time": time.utc_datetime()
            }
        )


    return events
