from datetime import date, timedelta
import sys

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


def build_day(current):

    raw = get_raw_moon_data(current)

    angle = raw["angle"]

    rise_set = get_rise_set(current)

    phase_event = find_phase_event(current)

    return MoonDay(
        date=current,
        phase=get_phase(angle),
        illumination=get_illumination(angle),
        sign=get_sign(raw["longitude"]),
        phase_time=(
            phase_event["time"].time()
            if phase_event
            and phase_event["phase"] == get_phase(angle)
            else None
        ),
        moonrise=rise_set["moonrise"],
        moonset=rise_set["moonset"],
    )


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

        days.append(
            build_day(current)
        )

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

    if len(sys.argv) > 1:

        test_date = date.fromisoformat(
            sys.argv[1]
        )

        day = build_day(test_date)

        print(day)

        print()

        print(format_title(day))

        print()

        print(
            format_notes(day)
        )

        exit()


    days = build_days()

    events = build_events(days)

    calendar = build_feed(events)

    save_feed(calendar)

    print(
        "Moon calendar generated 🌙"
    )
