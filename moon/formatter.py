from moon.models import MoonDay



def format_time(value):

    if value is None:
        return None

    return value.strftime(
        "%-I:%M%p"
    ).lower()



def format_title(day: MoonDay):

    title = (
        f"{day.phase} "
        f"in "
        f"{day.sign}"
    )


    if (
        day.phase_time
        and day.phase in [
            "New Moon",
            "Full Moon",
            "Balsamic Moon",
        ]
    ):

        title += (
            f", "
            f"{format_time(day.phase_time)}"
        )


    return title



def format_notes(day: MoonDay):

    lines = []


    lines.append(
        f"Lunar Day {day.lunar_day}, "
        f"{day.illumination}% Illumination"
    )


    if day.sign_transition:

        lines.append("")

        lines.append(
            f"{day.sign_transition['from']}"
            f" → "
            f"{day.sign_transition['to']}"
            f", "
            f"{format_time(day.sign_transition['time'])}"
        )


    lines.append("")


    lines.append(
        "Melbourne, Australia"
    )


    return "\n".join(lines)
