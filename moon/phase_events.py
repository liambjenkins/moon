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


def forward_angle_difference(start, end):
    """
    Returns clockwise movement from start to end.
    Example:
    350 -> 10 = 20 degrees
    """

    return (end - start) % 360


def crossed(previous, current, target):
    """
    Checks whether the phase angle crossed a target
    between two observations.
    """

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
    """
    Binary search the exact moment
    the phase angle crosses target.
    """

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


    step = timedelta(hours=6)


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

                events.append(
                    {
                        "phase": name,
                        "time": event_time.astimezone(
                            MELBOURNE
                        ),
                    }
                )


        previous_time = current
        previous_angle = current_angle


    return events
