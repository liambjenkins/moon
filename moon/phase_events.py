from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from moon.astronomy import (
    get_phase_angle,
    get_moon_longitude_at,
)


MELBOURNE = ZoneInfo(
    "Australia/Melbourne"
)


TARGETS = {
    0: "New Moon",
    90: "First Quarter",
    180: "Full Moon",
    270: "Last Quarter",
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



def normalise(angle):

    return angle % 360



def forward_angle_difference(
    start,
    end,
):

    return (
        end - start
    ) % 360



def crossed(
    previous,
    current,
    target,
):

    movement = forward_angle_difference(
        previous,
        current,
    )

    distance = forward_angle_difference(
        previous,
        target,
    )

    return distance <= movement



def refine_event_time(
    start,
    end,
    target,
):

    for _ in range(30):

        midpoint = start + (
            end - start
        ) / 2


        start_distance = forward_angle_difference(
            get_phase_angle(start),
            target,
        )


        mid_distance = forward_angle_difference(
            get_phase_angle(midpoint),
            target,
        )


        if mid_distance < start_distance:

            end = midpoint

        else:

            start = midpoint



    return start + (
        end - start
    ) / 2



def add_event(
    events,
    event,
):

    for existing in events:

        same_phase = (
            existing["phase"]
            ==
            event["phase"]
        )


        close_time = (
            abs(
                existing["time"]
                -
                event["time"]
            )
            <
            timedelta(minutes=10)
        )


        if same_phase and close_time:

            return


    events.append(
        event
    )



def find_phase_events(
    start_date,
    end_date,
):

    events = []


    current = datetime(
        start_date.year,
        start_date.month,
        start_date.day,
        tzinfo=timezone.utc,
    )


    end = datetime(
        end_date.year,
        end_date.month,
        end_date.day,
        tzinfo=timezone.utc,
    )


    previous_time = current


    previous_angle = normalise(
        get_phase_angle(current)
    )


    step = timedelta(
        hours=6
    )



    while current < end:

        current += step


        current_angle = normalise(
            get_phase_angle(current)
        )


        for target, name in TARGETS.items():

            if crossed(
                previous_angle,
                current_angle,
                target,
            ):

                event_time = refine_event_time(
                    previous_time,
                    current,
                    target,
                )


                local_time = event_time.astimezone(
                    MELBOURNE
                )


                longitude = get_moon_longitude_at(
                    event_time
                )


                add_event(
                    events,
                    {
                        "phase": name,

                        "sign": get_sign(
                            longitude
                        ),

                        "time": local_time,

                        "date": local_time.date(),
                    }
                )


        previous_time = current

        previous_angle = current_angle



    return sorted(
        events,
        key=lambda event: event["time"]
    )
