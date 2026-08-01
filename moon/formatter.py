from moon.models import MoonDay



def format_time(value):

    if value is None:
        return None

    return value.strftime(
        "%-I:%M%p"
    ).lower()



def format_title(
    day: MoonDay
):

    return (
        f"{day.phase} "
        f"in {day.sign}"
    )



def format_notes(
    day: MoonDay
):

    lines = []


    #
    # Moon event detail
    #

    title = (
        f"{day.phase} "
        f"in {day.sign}"
    )


    if day.phase_time:

        title += (
            f", "
            f"{format_time(day.phase_time)}"
        )


    lines.append(
        title
    )


    lines.append(
        ""
    )


    #
    # Lunar information
    #

    lines.append(
        f"Lunar Day {day.lunar_day}, "
        f"{day.illumination}% Illumination"
    )


    #
    # Moon sign transition
    #

    if day.sign_transition:

        lines.append(
            ""
        )


        lines.append(
            f"{day.sign_transition['from']} "
            f"→ "
            f"{day.sign_transition['to']}, "
            f"{format_time(day.sign_transition['time'])}"
        )


    #
    # Coming events
    #

    if day.coming:

        lines.append(
            ""
        )

        lines.append(
            "Coming:"
        )


        for event in day.coming:

            lines.append(
                event
            )


    lines.append(
        ""
    )


    lines.append(
        "Melbourne, Australia"
    )


    return "\n".join(lines)
