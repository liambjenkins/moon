from datetime import datetime, timezone


def get_zodiac_sign(longitude):

    signs = [
        "Aries",
        "Taurus",
        "Gemini",
        "Cancer",
        "Leo",
        "Virgo",
        "Libra",
        "Scorpio",
        "Sagittarius",
        "Capricorn",
        "Aquarius",
        "Pisces",
    ]

    return signs[int(longitude // 30)]


def get_transit(previous_longitude, current_longitude):

    previous_sign = get_zodiac_sign(previous_longitude)
    current_sign = get_zodiac_sign(current_longitude)

    if previous_sign == current_sign:
        return None

    return {
        "from": previous_sign,
        "to": current_sign,
    }
