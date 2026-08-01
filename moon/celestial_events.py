from skyfield import almanac
from skyfield import eclipselib

from moon.astronomy import ts, eph


SEASON_NAMES = {
    0: "Autumn Equinox",
    1: "Winter Solstice",
    2: "Spring Equinox",
    3: "Summer Solstice",
}



def find_seasonal_events(
    start_date,
    end_date,
):

    events = []


    start = ts.utc(
        start_date.year,
        start_date.month,
        start_date.day,
    )


    end = ts.utc(
        end_date.year,
        end_date.month,
        end_date.day,
    )


    times, seasons = almanac.find_discrete(
        start,
        end,
        almanac.seasons(eph),
    )


    for time, season in zip(
        times,
        seasons,
    ):

        events.append(
            {
                "type": SEASON_NAMES[season],

                "time": time.utc_datetime(),
            }
        )


    return events



def find_lunar_eclipses(
    start_date,
    end_date,
):

    events = []


    start = ts.utc(
        start_date.year,
        start_date.month,
        start_date.day,
    )


    end = ts.utc(
        end_date.year,
        end_date.month,
        end_date.day,
    )


    times, kinds, details = eclipselib.lunar_eclipses(
        start,
        end,
        eph,
    )


    for time, kind in zip(
        times,
        kinds,
    ):

        events.append(
            {
                "type": "Lunar Eclipse",

                "time": time.utc_datetime(),

                "kind": str(kind),
            }
        )


    return events



def find_solar_eclipses(
    start_date,
    end_date,
):

    events = []


    start = ts.utc(
        start_date.year,
        start_date.month,
        start_date.day,
    )


    end = ts.utc(
        end_date.year,
        end_date.month,
        end_date.day,
    )


    if hasattr(
        eclipselib,
        "solar_eclipses"
    ):

        times, kinds, details = eclipselib.solar_eclipses(
            start,
            end,
            eph,
        )


        for time, kind in zip(
            times,
            kinds,
        ):

            events.append(
                {
                    "type": "Solar Eclipse",

                    "time": time.utc_datetime(),

                    "kind": str(kind),
                }
            )


    return events



def find_celestial_events(
    start_date,
    end_date,
):

    events = []


    events.extend(
        find_seasonal_events(
            start_date,
            end_date,
        )
    )


    events.extend(
        find_lunar_eclipses(
            start_date,
            end_date,
        )
    )


    events.extend(
        find_solar_eclipses(
            start_date,
            end_date,
        )
    )


    return sorted(
        events,
        key=lambda event: event["time"]
    )
