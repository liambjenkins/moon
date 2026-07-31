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

    diff = abs(a - b)

    return min(
        diff,
        360 - diff
    )


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


    previous_angle = None
    previous_time = None


    while current <= end:

        angle = normalise(
            get_phase_angle(current)
        )


        if previous_angle is not None:

            for target, name in TARGETS.items():

                before = angular_distance(
                    previous_angle,
                    target,
                )

                after = angular_distance(
                    angle,
                    target,
                )


                if after > before:

                    continue


                if before < 2:

                    events.append(
                        {
                            "phase": name,
                            "time": previous_time.astimezone(
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
