from icalendar import Calendar, Event
from datetime import datetime, date
from pathlib import Path


CALENDAR_NAME = "Moon"


def create_calendar():
    cal = Calendar()

    cal.add("prodid", "-//Moon Calendar//OpenAI//")
    cal.add("version", "2.0")
    cal.add("X-WR-CALNAME", CALENDAR_NAME)
    cal.add("X-WR-TIMEZONE", "Australia/Melbourne")

    event = Event()

    event.add(
        "summary",
        "New Moon in Leo"
    )

    event.add(
        "dtstart",
        date(2027, 8, 2)
    )

    event.add(
        "dtend",
        date(2027, 8, 3)
    )

    event.add(
        "description",
        """Lunar phase: New Moon

Illumination: 0%

Moon sign: Leo

Location: Melbourne, Australia
Timezone: Australia/Melbourne

Exact new moon:
2 August 2027"""
    )

    event.add(
        "uid",
        "moon-test-event-001@moon-calendar"
    )

    event.add(
        "status",
        "CONFIRMED"
    )

    cal.add_component(event)

    return cal


calendar = create_calendar()

output = Path("Moon.ics")

with open(output, "wb") as file:
    file.write(calendar.to_ical())

print("Moon.ics created successfully 🌙")
