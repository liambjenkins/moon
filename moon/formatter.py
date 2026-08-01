from moon.models import MoonDay


def format_time(value):

    if value is None:
        return None

    return value.strftime("%-I:%M%p").lower()



def format_title(day: MoonDay):

    return f"{day.phase} in {day.sign}"



def format_notes(day: MoonDay):

    lines = []

    lines.append(
        f"{day.phase} in {day.sign}"
    )

    lines.append("")

    lines.append(
        f"Lunar Day {day.lunar_day}, "
        f"{day.illumination}% Illumination"
    )

    lines.append("")

    lines.append(
        "Melbourne, Australia"
    )

    return "\n".join(lines)
