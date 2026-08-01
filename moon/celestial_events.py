from skyfield import almanac

from moon.astronomy import (
    ts,
    eph,
    get_moon_longitude_at,
    get_sun_longitude_at,
)

from moon.phase_events import find_phase_events



SEASON_NAMES = {
    0: "Autumn Equinox",
    1: "Winter Solstice",
    2: "Spring Equinox",
    3: "Summer Solstice",
}


SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]



def get_sign(longitude):

    return SIGNS[
        int(longitude // 30)
    ]



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

    from skyfield import eclipselib


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

        dt = time.utc_datetime()


        events.append(
            {
                "type": "Lunar Eclipse",

                "sign": get_sign(
                    get_moon_longitude_at(dt)
                ),

                "time": dt,

                "kind": str(kind),
            }
        )


    return events



def find_solar_eclipses(
    start_date,
    end_date,
):

    events = []


    new_moons = find_phase_events(
        start_date,
        end_date,
    )


    for moon in new_moons:

        if moon["phase"] != "New Moon":
            continue


        dt = moon["time"]


        moon_lon = get_moon_longitude_at(
            dt
        )

        sun_lon = get_sun_longitude_at(
            dt
        )


        separation = abs(
            moon_lon - sun_lon
        )


        if separation > 180:
            separation = 360 - separation


        # Placeholder eclipse threshold:
        # New Moon must be close to the Sun
        # and near an eclipse node.
        #
        # Refined once we add lunar latitude.

        if separation < 1:

            events.append(
                {
                    "type": "Solar Eclipse",

                    "sign": get_sign(
                        moon_lon
                    ),

                    "time": dt,

                    "kind": "Solar",
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
