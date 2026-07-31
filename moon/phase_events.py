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

    previous_distance = angular_distance(
        previous,
        target
    )

    current_distance = angular_distance(
        current,
        target
    )

    return current_distance < previous_distance



def find_phase_events(start_date, end_date):

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


    current += timedelta(
        hours=6
    )


    while current <= end:

        angle = normalise(
            get_phase_angle(current)
        )


        for target, name in TARGETS.items():

            if crossed(
                previous_angle,
                angle,
                target
            ):

                events.append(
                    {
                        "phase": name,
                        "time": current.astimezone(
                            MELBOURNE
                        ),
                    }
                )


        previous_angle = angle
        previous_time = current

        current += timedelta(
            hours=6
        )


    return events
