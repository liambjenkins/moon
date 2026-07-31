from icalendar import Calendar, Event
from datetime import datetime, timedelta
from pathlib import Path

from .models import MoonDay
from .formatter import format_title, format_notes


def build_calendar(days: list[MoonDay]):

    cal = Calendar()

    cal.add("prodid", "-//Moon Calendar//")
    cal.add("version", "2.0")
    cal.add("X-WR-CALNAME", "Moon")
    cal.add("X-WR-TIMEZONE", "Australia/Melbourne")

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
            "dtend",
            day.date + timedelta(days=1)
        )

        event.add(
            "description",
            format_notes(day)
        )

        event.add(
            "uid",
            f"moon-{day.date}@moon-calendar"
        )

        event.add(
            "status",
            "CONFIRMED"
        )

        event.add(
            "transp",
            "TRANSPARENT"
        )

        cal.add_component(event)

    return cal


def save_calendar(calendar):

    output = Path("Moon.ics")

    with open(output, "wb") as file:
        file.write(calendar.to_ical())

    return output
