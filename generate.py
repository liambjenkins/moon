from icalendar import Calendar, Event
from datetime import datetime

calendar = Calendar()
calendar.add("prodid", "-//Moon Calendar//")
calendar.add("version", "2.0")

event = Event()
event.add("summary", "New Moon in Leo")
event.add("dtstart", datetime(2027, 8, 2))
event.add("description", """
Phase:
New Moon

Illumination:
0%

Moon Sign:
Leo

Exact New Moon:
2 August 2027
""")

calendar.add_component(event)

with open("Moon.ics", "wb") as file:
    file.write(calendar.to_ical())

print("Moon.ics created 🌙")
