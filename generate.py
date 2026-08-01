from datetime import date, timedelta
import sys

from moon.astronomy import get_raw_moon_data
from moon.models import MoonDay
from moon.phases import get_illumination
from moon.lunar_days import get_lunar_day
from moon.phase_events import find_phase_events
from moon.sign_events import find_sign_events
from moon.feed import build_feed, save_feed
from moon.formatter import format_title, format_notes



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

        return phase_lookup[current]["phase"]


    tomorrow = current + timedelta(days=1)


    if (
        tomorrow in phase_lookup
        and phase_lookup[tomorrow]["phase"] == "New Moon"
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



def build_day(
    current,
    phase_lookup,
    previous_phase_lookup,
    sign_lookup,
    sign_transition_lookup,
):

    raw = get_raw_moon_data(
        current
    )


    phase = get_daily_phase(
        current,
        phase_lookup,
        previous_phase_lookup,
    )


    phase_time = None

    if current in phase_lookup:

        phase_time = phase_lookup[current]["time"]



    return MoonDay(

        date=current,

        phase=phase,

        illumination=get_illumination(
            raw["angle"]
        ),

        lunar_day=get_lunar_day(
            raw["angle"]
        ),

        sign=sign_lookup.get(
            current,
            "Unknown"
        ),

        phase_time=phase_time,

        sign_transition=sign_transition_lookup.get(
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



    # PHASE EVENTS

    phase_events = find_phase_events(
        start,
        end
    )


    phase_lookup = {}


    for event in phase_events:

        phase_lookup[
            event["date"]
        ] = event



    previous_phase_lookup = {}


    last_phase = "Last Quarter"


    current = start


    while current < end:


        if current in phase_lookup:

            last_phase = phase_lookup[current]["phase"]


        previous_phase_lookup[current] = last_phase


        current += timedelta(
            days=1
        )



    # SIGN EVENTS

    sign_events = find_sign_events(
        start,
        end
    )


    sign_lookup = {}

    sign_transition_lookup = {}



    first_longitude = get_raw_moon_data(
        start
    )["longitude"]


    last_sign = get_sign(
        first_longitude
    )



    current = start


    while current < end:


        if current in [
            event["date"]
            for event in sign_events
        ]:

            for event in sign_events:

                if event["date"] == current:

                    last_sign = event["to"]

                    sign_transition_lookup[current] = event



        sign_lookup[current] = last_sign


        current += timedelta(
            days=1
        )



    # BUILD DAYS

    days = []


    current = start


    while current < end:


        days.append(

            build_day(

                current,

                phase_lookup,

                previous_phase_lookup,

                sign_lookup,

                sign_transition_lookup,

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
