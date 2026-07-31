from moon.models import MoonDay


def format_time(value):

    if value is None:
        return None

    return value.strftime("%-I:%M%p").lower()


def format_title(day: MoonDay):

    return f"{day.phase} in {day.sign}"


def format_notes(day: MoonDay):

    lines = []

    title = (
        f"{day.phase} "
        f"({day.illumination}%"
    )

    if day.phase_time:
        title += (
            f", {format_time(day.phase_time)}"
        )

    title += f") in {day.sign}"

    lines.append(title)

    lines.append("")

    if day.moonrise:

        lines.append(
            f"Moonrise: {format_time(day.moonrise)}"
        )

    elif day.moonrise is not None:

        lines.append(
            "Moonrise: —"
        )


    if day.moonset:

        lines.append(
            f"Moonset: {format_time(day.moonset)}"
        )

    elif day.moonset is not None:

        lines.append(
            "Moonset: —"
        )


    if day.transit_time:

        lines.append("")

        lines.append(
            f"Transit: "
            f"{day.transit_from} → "
            f"{day.transit_to} "
            f"({format_time(day.transit_time)})"
        )


    lines.append("")

    lines.append(
        "Location: Melbourne, Australia"
    )

    return "\n".join(lines)
