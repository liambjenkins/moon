from icalendar import Calendar, Event


def build_feed(events):

    calendar = Calendar()

    calendar.add(
        "prodid",
        "-//Moon Calendar//"
    )

    calendar.add(
        "version",
        "2.0"
    )

    calendar.add(
        "X-WR-CALNAME",
        "Moon"
    )

    for event in events:
        calendar.add_component(event)

    return calendar


def save_feed(calendar, filename="moon.ics"):

    with open(filename, "wb") as file:
        file.write(calendar.to_ical())
