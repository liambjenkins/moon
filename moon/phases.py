def phase_name(angle):

    angle = angle % 360

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


def illumination(angle):

    import math

    fraction = (
        1 - math.cos(math.radians(angle))
    ) / 2

    return round(fraction * 100)
