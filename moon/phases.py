from math import cos, radians


def get_phase(angle):

    angle = angle % 360


    if angle < 22.5:
        return "New Moon"

    if angle < 45:
        return "Waxing Crescent"

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
        return "Waning Crescent"

    return "Balsamic Moon"


def get_illumination(angle):

    value = (
        1 - cos(
            radians(angle)
        )
    ) / 2

    return round(
        value * 100
    )
