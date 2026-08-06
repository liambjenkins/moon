import swisseph as swe


def get_sun_position(julian_day):
    position, _ = swe.calc_ut(
        julian_day,
        swe.SUN
    )

    return position[0]
