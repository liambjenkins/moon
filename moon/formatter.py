from .models import MoonDay


def format_time(value):

    if value is None:
        return None

    return (
        value
        .strftime("%I:%M%p")
        .lstrip("0")
        .lower()
    )


def format_title(day: MoonDay):

    return f"{day.phase} Moon in {day.sign}"


def format_notes(day: MoonDay):

    lines = []


    title = (
        f"{day.phase} "
        f"({day.illumination}% illuminated"
    )


    if day.phase_time:

        title += (
            f", exact phase: "
            f"{format_time(day.phase_time)}"
        )


    title += f") in {day.sign}"


    lines.append(title)

    lines.append("")


    if day.moonrise:

        lines.append(
            f"Moonrise: {format_time(day.moonrise)}"
        )


    if day.moonset:

        lines.append(
            f"Moonset: {format_time(day.moonset)}"
        )

    
    if day.transit:

    lines.append("")

    lines.append(
        f"Transit: "
        f"{day.transit['from']} → "
        f"{day.transit['to']} "
        f"({format_time(day.transit_time) if day.transit_time else ''})"
    )

    
    if day.transit_time:

        lines.append("")

        lines.append(
            f"Transit: "
            f"{format_time(day.transit_time)}"
        )


    lines.append("")


    lines.append(
        "Location: Melbourne, Australia"
    )


    return "\n".join(lines)
