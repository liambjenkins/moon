from math import floor


def get_lunar_day(angle):

    angle = angle % 360

    day = floor(
        angle / 12
    ) + 1

    return min(
        day,
        30
    )
