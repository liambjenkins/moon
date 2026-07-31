import math


def get_phase(angle):

    angle = angle % 360


    if angle < 22.5:
        return "New Moon"

    elif angle < 67.5:
        return "Waxing Crescent"

    elif angle < 112.5:
        return "First Quarter"

    elif angle < 157.5:
        return "Waxing Gibbous"

    elif angle < 202.5:
        return "Full Moon"

    elif angle < 247.5:
        return "Waning Gibbous"

    elif angle < 292.5:
        return "Last Quarter"

    elif angle < 337.5:
        return "Waning Crescent"

    else:
        return "New Moon"


def get_illumination(angle):

    illumination = (
        1 - math.cos(
            math.radians(angle)
        )
    ) / 2

    return round(
        illumination * 100
    )
