from moon.models import MoonDay


def format_time(value):
    if value is None:
        return None

    return value.strftime("%-I:%M%p").lower()


def format_title(day: MoonDay) -> str:
    return f"{day.phase} in {day.sign}"


def format_notes(day: MoonDay) -> str:

    lines = []

    title = f"{day.phase} ({day.illumination}%"

    if day.phase_time:
        title += f", {format_time(day.phase_time)}"

    title += f") in {day.sign}"

    lines.append(title)
    lines.append("")

    if day.moonrise:
        lines.append(f"Moonrise: {format_time(day.moonrise)}")

    if day.moonset:
        lines.append(f"Moonset: {format_time(day.moonset)}")

    if day.moonrise or day.moonset:
        lines.append("")

    if day.transit_time:
        lines.append(
            f"Transit: {day.transit_from} → {day.transit_to} ({format_time(day.transit_time)})"
        )
        lines.append("")

    lines.append("Location: Melbourne, Australia")

    return "\n".join(lines)
