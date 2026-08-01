from math import cos, radians


def get_illumination(angle):

    value = (
        1 - cos(
            radians(angle)
        )
    ) / 2

    return round(
        value * 100
    )
