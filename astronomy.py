from datetime import datetime, timezone

from skyfield.api import load, wgs84
from skyfield.framelib import ecliptic_frame

from .config import MELBOURNE


ts = load.timescale()

eph = load("de421.bsp")

earth = eph["earth"]
moon = eph["moon"]
sun = eph["sun"]


def moon_illumination(t):
    earth_pos = earth.at(t)
    moon_pos = earth_pos.observe(moon)
    sun_pos = earth_pos.observe(sun)

    angle = moon_pos.separation_from(sun_pos).degrees

    illumination = (1 - (angle / 180)) * 100

    return round(max(0, min(100, illumination)))


def moon_sign(t):

    astrometric = earth.at(t).observe(moon)

    ecliptic = astrometric.frame_latlon(ecliptic_frame)

    longitude = ecliptic[1].degrees % 360

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


def moon_phase_name(illumination):

    if illumination < 2:
        return "New Moon"

    if illumination > 98:
        return "Full Moon"

    if illumination < 50:
        return "Waxing Crescent"

    if illumination < 55:
        return "First Quarter"

    if illumination < 98:
        return "Waxing Gibbous"

    return "Waning Gibbous"


def get_moon_data(date):

    dt = datetime(
        date.year,
        date.month,
        date.day,
        12,
        tzinfo=timezone.utc,
    )

    t = ts.from_datetime(dt)

    illumination = moon_illumination(t)

    return {
        "phase": moon_phase_name(illumination),
        "illumination": illumination,
        "sign": moon_sign(t),
    }
