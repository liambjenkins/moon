from datetime import datetime


def format_time(value):

    if value is None:
        return None

    return value.strftime("%-I:%M%p").lower()



def format_title(event):

    event_type = event["type"]

    sign = event.get(
        "sign"
    )


    if sign:

        return f"{event_type} in {sign}"


    return event_type



def format_notes(event):

    lines = []


    event_type = event["type"]


    if event_type in (
        "Lunar Eclipse",
        "Solar Eclipse",
    ):

        lines.append(
            event_type
        )

        lines.append("")


        if event.get("kind"):

            lines.append(
                event["kind"]
            )

            lines.append("")


    elif event_type in (
        "Autumn Equinox",
        "Winter Solstice",
        "Spring Equinox",
        "Summer Solstice",
    ):

        lines.append(
            event_type
        )

        lines.append("")


    lines.append(
        "Melbourne, Australia"
    )


    return "\n".join(lines)
