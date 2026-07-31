from datetime import date, timedelta

from moon.astronomy import get_raw_moon_data
from moon.models import MoonDay
from moon.phases import get_phase, get_illumination
from moon.phase_events import find_phase_event
from moon.rise_set import get_rise_set
from moon.feed import build_feed, save_feed
from moon.formatter import format_title, format_notes
from moon.config import START_DATE, YEARS_FORWARD


def get_sign(longitude):

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


def build_days():

    start = date.fromisoformat(START_DATE)

    end = date(
        start.year + YEARS_FORWARD,
        start.month,
        start.day,
    )

    days = []

    current = start

    while current < end:

        raw = get_raw_moon_data(current)

        angle = raw["angle"]

        phase_event = find_phase_event(current)

        rise_set = get_rise_set(current)

        day = MoonDay(
            date=current,

            # daily phase only
            phase=get_phase(angle),

            illumination=get_illumination(angle),

            sign=get_sign(
                raw["longitude"]
            ),

            # only populated on exact phase day
            phase_time=(
                phase_event["time"].time()
                if phase_event
                and phase_event["phase"] == get_phase(angle)
                else None
            ),

            moonrise=rise_set["moonrise"],

            moonset=rise_set["moonset"],
        )

        days.append(day)

        current += timedelta(days=1)

    return days


def build_events(days):

    from icalendar import Event

    events = []

    for day in days:

        event = Event()

        event.add(
            "summary",
            format_title(day)
        )

        event.add(
            "dtstart",
            day.date
        )

        event.add(
            "description",
            format_notes(day)
        )

        event.add(
            "uid",
            f"moon-{day.date}"
        )

        events.append(event)

    return events


if __name__ == "__main__":

    days = build_days()

    events = build_events(days)

    calendar = build_feed(events)

    save_feed(calendar)

    print("Moon calendar generated 🌙")
