from datetime import datetime, timedelta, timezone


MAJOR_PHASES = {
    0: "New Moon",
    90: "First Quarter",
    180: "Full Moon",
    270: "Last Quarter",
}


def normalise_angle(angle):
    return angle % 360


def angular_distance(a, b):
    diff = abs(a - b)
    return min(diff, 360 - diff)


def get_phase(angle):

    angle = normalise_angle(angle)

    if angle < 22.5 or angle >= 337.5:
        return "New Moon"

    if angle < 67.5:
        return "Waxing Crescent"

    if angle < 112.5:
        return "First Quarter"

    if angle < 157.5:
        return "Waxing Gibbous"

    if angle < 202.5:
        return "Full Moon"

    if angle < 247.5:
        return "Waning Gibbous"

    if angle < 292.5:
        return "Last Quarter"

    return "Balsamic Moon"


def illumination(angle):

    import math

    fraction = (
        1 - math.cos(math.radians(angle))
    ) / 2

    return round(fraction * 100)


def is_major_phase_day(angle):

    angle = normalise_angle(angle)

    for phase_angle in MAJOR_PHASES:

        if angular_distance(angle, phase_angle) < 2:
            return MAJOR_PHASES[phase_angle]

    return None
