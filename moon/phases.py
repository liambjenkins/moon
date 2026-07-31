from math import cos, radians


def get_phase(angle):

    angle = angle % 360


    # Exact lunar turning points
    # These get their own single-day labels

    if angle < 6 or angle >= 354:
        return "New Moon"


    if 84 <= angle <= 96:
        return "First Quarter"


    if 174 <= angle <= 186:
        return "Full Moon"


    if 264 <= angle <= 276:
        return "Last Quarter"


    # Transitional phases

    if angle < 90:
        return "Waxing Crescent"


    if angle < 180:
        return "Waxing Gibbous"


    if angle < 270:
        return "Waning Gibbous"


    if angle < 315:
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
