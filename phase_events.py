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


def angle_difference(a, b):

    diff = abs(a - b)

    return min(
        diff,
        360 - diff
    )


def find_phase_time(day):

    start = datetime(
        day.year,
        day.month,
        day.day,
        tzinfo=timezone.utc,
    )

    best_time = None
    best_distance = 999

    for hour in range(24):

        moment = start + timedelta(
            hours=hour
        )

        angle = normalise(
            get_phase_angle(moment)
        )

        for target, name in TARGETS.items():

            distance = angle_difference(
                angle,
                target
            )

            if distance < best_distance:

                best_distance = distance
                best_time = moment


    if best_distance < 2:

        return {
            "phase": TARGETS[
                min(
                    TARGETS,
                    key=lambda x: angle_difference(
                        x,
                        get_phase_angle(best_time)
                    )
                )
            ],
            "time": best_time,
        }


    return None
