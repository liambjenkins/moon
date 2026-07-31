from models import MoonDay


def format_title(day: MoonDay) -> str:
    return f"{day.phase} in {day.sign}"


def _time_string(value):
    if value is None:
        return None

    return value.strftime("%-I:%M%p").lower()


def format_notes(day: MoonDay) -> str:

    headline = f"{day.phase} ({day.illumination}%"

    if day.phase_time:
        headline += f", {_time_string(day.phase_time)}"

    headline += f") in {day.sign}"

    lines = [
        headline,
        "",
    ]

    if day.moonrise:
        lines.append(f"Moonrise: {_time_string(day.moonrise)}")

    if day.moonset:
        lines.append(f"Moonset: {_time_string(day.moonset)}")

    if day.moonrise or day.moonset:
        lines.append("")

    if day.transit_time:
        lines.append(
            f"Transit: {day.transit_from} → {day.transit_to} ({_time_string(day.transit_time)})"
        )
        lines.append("")

    lines.append("Location: Melbourne, Australia")

    return "\n".join(lines)
