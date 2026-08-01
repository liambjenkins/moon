from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from moon.astronomy import get_moon_longitude_at


MELBOURNE = ZoneInfo(
    "Australia/Melbourne"
)


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



def get_boundary_degree(sign):

    index = SIGNS.index(
        sign
    )

    return (
        index * 30
    )



def find_sign_events(
    start_date,
    end_date,
):

    events = []

    current = start_date


    while current < end_date:

        start = datetime(
            current.year,
            current.month,
            current.day,
            0,
            1,
            tzinfo=MELBOURNE,
        )


        end = datetime(
            current.year,
            current.month,
            current.day,
            23,
            59,
            tzinfo=MELBOURNE,
        )


        start_longitude = get_moon_longitude_at(
            start
        )

        end_longitude = get_moon_longitude_at(
            end
        )


        start_sign = get_sign(
            start_longitude
        )

        end_sign = get_sign(
            end_longitude
        )


        if start_sign != end_sign:

            events.append(
                {
                    "from": start_sign,

                    "to": end_sign,

                    "time": refine_sign_change(
                        start,
                        end,
                        start_sign,
                    ),
                }
            )


        current += timedelta(
            days=1
        )


    return events



def refine_sign_change(
    start,
    end,
    start_sign,
):

    boundary = get_boundary_degree(
        SIGNS[
            (SIGNS.index(start_sign) + 1) % 12
        ]
    )


    for _ in range(30):

        midpoint = start + (
            end - start
        ) / 2


        longitude = get_moon_longitude_at(
            midpoint
        )


        if crossed_boundary(
            get_moon_longitude_at(start),
            longitude,
            boundary,
        ):

            end = midpoint

        else:

            start = midpoint


    return start + (
        end - start
    ) / 2



def crossed_boundary(
    previous,
    current,
    boundary,
):

    previous = previous % 360
    current = current % 360
    boundary = boundary % 360


    if previous <= current:

        return (
            previous <= boundary <= current
        )

    else:

        return (
            boundary >= previous
            or boundary <= current
        )
