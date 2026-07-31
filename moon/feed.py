from pathlib import Path

from icalendar import Calendar


def build_feed(events):

    calendar = Calendar()

    calendar.add(
        "prodid",
        "-//Moon Calendar//Lunar Engine//"
    )

    calendar.add(
        "version",
        "2.0"
    )

    calendar.add(
        "X-WR-CALNAME",
        "Moon Calendar"
    )

    calendar.add(
        "X-WR-TIMEZONE",
        "Australia/Melbourne"
    )


    for event in events:

        calendar.add_component(
            event
        )


    return calendar



def save_feed(
    calendar,
    filename="Moon.ics"
):

    output = Path(filename)


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


    return output
