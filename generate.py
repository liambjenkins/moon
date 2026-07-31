from datetime import date, timedelta
import sys

from moon.astronomy import get_raw_moon_data
from moon.models import MoonDay
from moon.phases import get_phase_from_events, get_illumination
from moon.phase_events import find_phase_events
from moon.rise_set import get_rise_set
from moon.feed import build_feed, save_feed
from moon.formatter import format_title, format_notes
from moon.transits import get_transit


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

    return signs[
        int(longitude // 30)
    ]


def build_day(current, phase_events):

    raw = get_raw_moon_data(current)

    phase = get_phase_from_events(
        current,
        phase_events,
    )

    rise_set = get_rise_set(
        current
    )

    return MoonDay(
        date=current,

        phase=phase,

        illumination=get_illumination(
            raw["angle"]
        ),

        sign=get_sign(
            raw["longitude"]
        ),

        moonrise=rise_set.get(
            "moonrise"
        ),

        moonset=rise_set.get(
            "moonset"
        ),

        transit=get_transit(
            current
        ),
    )


def build_days(year):

    start = date(
        year,
        1,
        1
    )

    end = date(
        year + 1,
        1,
        1
    )


    phase_events = find_phase_events(
        start,
        end,
    )


    days = []

    current = start


    while current < end:

        days.append(
            build_day(
                current,
                phase_events
            )
        )

        current += timedelta(
            days=1
        )


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


        events.append(
            event
        )


    return events



if __name__ == "__main__":

    year = int(
        sys.argv[1]
    )


    days = build_days(
        year
    )


    events = build_events(
        days
    )


    calendar = build_feed(
        events
    )


    save_feed(
        calendar
    )


    print(
        f"Moon calendar generated for {year} 🌙"
    )
