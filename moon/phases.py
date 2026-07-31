import math


MAJOR_PHASES = {
    0: "New Moon",
    90: "First Quarter",
    180: "Full Moon",
    270: "Last Quarter",
}


def normalise(angle):
    return angle % 360


def distance(a, b):

    difference = abs(a - b)

    return min(
        difference,
        360 - difference
    )


def get_phase(angle):

    angle = normalise(angle)

    if angle < 22.5:
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

    if angle < 337.5:
        return "Balsamic Moon"

    return "New Moon"


def get_illumination(angle):

    illuminated = (
        1 - math.cos(math.radians(angle))
    ) / 2

    return round(illuminated * 100)


def get_major_phase(angle):

    for phase_angle, name in MAJOR_PHASES.items():

        if distance(angle, phase_angle) < 1:

            return name

    return None
