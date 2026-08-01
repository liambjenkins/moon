from datetime import date, timedelta
import sys

from moon.astronomy import get_raw_moon_data
from moon.models import MoonDay
from moon.phases import get_illumination
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

def get_daily_phase(
    current,
    phase_lookup,
    previous_phase_lookup,
):

    if current in phase_lookup:
        return phase_lookup[current]

    tomorrow = current + timedelta(days=1)

    if (
        tomorrow in phase_lookup
        and phase_lookup[tomorrow] == "New Moon"
    ):
        return "Balsamic Moon"

    previous = previous_phase_lookup[current]

    if previous == "New Moon":
        return "Waxing Crescent"

    if previous == "First Quarter":
        return "Waxing Gibbous"

    if previous == "Full Moon":
        return "Waning Gibbous"

    return "Waning Crescent"

def build_day(     current,     phase_lookup,     previous_phase_lookup, ):

    raw = get_raw_moon_data(
        current
    )

    phase = get_daily_phase(
    current,
    phase_lookup,
    previous_phase_lookup,
)

    rise_set = get_rise_set(
        current
    )

    previous_day = (
        current - timedelta(days=1)
    )

    previous_raw = get_raw_moon_data(
        previous_day
    )

    transit = get_transit(
        previous_raw["longitude"],
        raw["longitude"],
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

        transit=transit,
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


    days = []

    current = start


    while current < end:

    days.append(
        build_day(
            current,
            phase_lookup,
            previous_phase_lookup,
        )
    )

    current += timedelta(
        days=1
    )

    phase_events = find_phase_events(
        start,
        end
    )

    phase_lookup = {}

for event in phase_events:

    phase_lookup[
        event["time"].date()
    ] = event["phase"]


previous_phase_lookup = {}

last_phase = "Last Quarter"

for current in (
    start + timedelta(days=i)
    for i in range((end - start).days)
):

    if current in phase_lookup:
        last_phase = phase_lookup[current]

    previous_phase_lookup[current] = last_phase


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
            f"moon-{day.date}@moon-calendar"
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
