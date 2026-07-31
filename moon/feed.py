from pathlib import Path


def build_feed(events):

    from icalendar import Calendar

    calendar = Calendar()

    calendar.add(
        "prodid",
        "-//Moon Calendar//"
    )

    calendar.add(
        "version",
        "2.0"
    )

    for event in events:
        calendar.add_component(event)

    return calendar


def save_feed(calendar):

    output = Path("Moon.ics")

    with open(
        output,
        "wb"
    ) as file:

        file.write(
            calendar.to_ical()
        )

    print(
        f"Saved calendar: {output}"
    )
