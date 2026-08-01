from moon.upcoming import build_upcoming


def format_time(value):

    if value is None:
        return None

    return value.strftime("%-I:%M%p").lower()



def format_title(day):

    title = (
        f"{day.phase} "
        f"in {day.sign}"
    )


    if day.phase_time:

        title += (
            f", {format_time(day.phase_time)}"
        )


    return title



def format_notes(
    day,
    phase_events,
    celestial_events,
):

    lines = []


    lines.append(
        f"Lunar Day {day.lunar_day}, "
        f"{day.illumination}% Illumination"
    )


    if day.sign_transition:

        lines.append(
            ""
        )

        lines.append(
            f"{day.sign_transition['from']} → "
            f"{day.sign_transition['to']}, "
            f"{format_time(day.sign_transition['time'])}"
        )


    upcoming = build_upcoming(
        day.date,
        phase_events,
        celestial_events,
    )


    if upcoming:

        lines.append(
            ""
        )

        lines.append(
            "Coming:"
        )


        for event in upcoming:

            lines.append(
                event
            )


    return "\n".join(lines)
