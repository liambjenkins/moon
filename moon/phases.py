from math import cos, radians


PHASES = [
    (22.5, "New Moon"),
    (67.5, "Waxing Crescent"),
    (112.5, "First Quarter"),
    (157.5, "Waxing Gibbous"),
    (202.5, "Full Moon"),
    (247.5, "Waning Gibbous"),
    (292.5, "Last Quarter"),
    (337.5, "Waning Crescent"),
    (360, "Balsamic Moon"),
]


def get_phase(angle):
    """
    Convert lunar elongation angle into a named moon phase.
    Angle: degrees between 0-360.
    """

    angle %= 360

    for threshold, phase in PHASES:
        if angle < threshold:
            return phase

    return "New Moon"


def get_illumination(angle):
    """
    Calculate illuminated fraction as a percentage.

    Angle should be the Sun-Moon elongation:
    0° = New Moon
    180° = Full Moon
    """

    angle %= 360

    value = (1 - cos(radians(angle))) / 2

    return round(value * 100)
