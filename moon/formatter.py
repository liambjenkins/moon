from moon.models import MoonDay



def format_time(value):

    if value is None:
        return None

    return value.strftime(
        "%-I:%M%p"
    ).lower()



def format_title(day: MoonDay):

    return (
        f"{day.phase} "
        f"in "
        f"{day.sign}"
    )



def format_notes(day: MoonDay):

    lines = []


    phase_line = (
        f"{day.phase} "
        f"in "
        f"{day.sign}"
    )


    if day.phase_time:

        phase_line += (
            f", "
            f"{format_time(day.phase_time)}"
        )


    lines.append(
        phase_line
    )


    lines.append("")


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


    # Coming will be added here


    lines.append("")


    lines.append(
        "Melbourne, Australia"
    )


    return "\n".join(lines)
