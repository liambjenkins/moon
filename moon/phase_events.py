from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from moon.astronomy import get_phase_angle


MELBOURNE = ZoneInfo("Australia/Melbourne")


TARGETS = {
    0: "New Moon",
    90: "First Quarter",
    180: "Full Moon",
    270: "Last Quarter",
}


def normalise(angle):
    return angle % 360


def angular_distance(a, b):
    return min(
        abs(a - b),
        360 - abs(a - b)
    )


def crossed(previous, current, target):

    return (
        angular_distance(current, target)
        <
        angular_distance(previous, target)
    )


def refine_event_time(
    start,
    end,
    target
):

    for _ in range(20):

        midpoint = start + (
            end - start
        ) / 2

        start_distance = angular_distance(
            get_phase_angle(start),
            target
        )

        mid_distance = angular_distance(
            get_phase_angle(midpoint),
            target
        )

        if mid_distance < start_distance:
            end = midpoint
        else:
            start = midpoint

    return start + (
        end - start
    ) / 2



def find_phase_events(
    start_date,
    end_date
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


    previous_angle = normalise(
        get_phase_angle(current)
    )

    previous_time = current


    step = timedelta(hours=6)


    while current <= end:

        current += step

        angle = normalise(
            get_phase_angle(current)
        )


        for target, name in TARGETS.items():

            if crossed(
                previous_angle,
                angle,
                target
            ):

                event_time = refine_event_time(
                    previous_time,
                    current,
                    target
                )

                events.append(
                    {
                        "phase": name,
                        "time": event_time.astimezone(
                            MELBOURNE
                        ),
                    }
                )


        previous_angle = angle
        previous_time = current


    return events
