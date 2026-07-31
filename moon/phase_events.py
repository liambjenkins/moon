from datetime import datetime, timedelta, timezone

from moon.astronomy import get_phase_angle


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


def find_phase_event(day):

    start = datetime(
        day.year,
        day.month,
        day.day,
        tzinfo=timezone.utc,
    )

    best = None
    best_distance = 999

    for minute in range(0, 1440, 30):

        moment = start + timedelta(
            minutes=minute
        )

        angle = normalise(
            get_phase_angle(moment)
        )

        for target, name in TARGETS.items():

            distance = angular_distance(
                angle,
                target
            )

            if distance < best_distance:

                best_distance = distance

                best = {
                    "phase": name,
                    "time": moment,
                }

    if best_distance < 3:

        return best

    return None
