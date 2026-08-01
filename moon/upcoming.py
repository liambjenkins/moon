from datetime import date


INCLUDED_PHASES = [
    "New Moon",
    "Full Moon",
]


INCLUDED_CELESTIAL = [
    "Solar Eclipse",
    "Lunar Eclipse",
    "Autumn Equinox",
    "Winter Solstice",
    "Spring Equinox",
    "Summer Solstice",
]



def format_days(days):

    if days == 1:
        return "tomorrow"

    return f"{days} days"



def days_until(
    event_date,
    current,
):

    return (
        event_date - current
    ).days



def build_upcoming(
    current,
    phase_events,
    celestial_events,
):

    upcoming = []


    #
    # MOON PHASE EVENTS
    #

    for event in phase_events:

        if event["phase"] not in INCLUDED_PHASES:
            continue


        event_date = event["date"]


        days = days_until(
            event_date,
            current,
        )


        # Only future events within 30 days
        if days <= 0 or days > 30:
            continue


        sign = event.get(
            "sign"
        )


        if sign:

            text = (
                f"{event['phase']} "
                f"in {sign} "
                f"({format_days(days)})"
            )

        else:

            text = (
                f"{event['phase']} "
                f"({format_days(days)})"
            )


        upcoming.append(
            {
                "date": event_date,
                "text": text,
            }
        )



    #
    # CELESTIAL EVENTS
    #

    for event in celestial_events:

        if event["type"] not in INCLUDED_CELESTIAL:
            continue


        event_date = event["time"].date()


        days = days_until(
            event_date,
            current,
        )


        # Only future events within 30 days
        if days <= 0 or days > 30:
            continue



        if (
            event["type"]
            in [
                "Solar Eclipse",
                "Lunar Eclipse",
            ]
            and "sign" in event
        ):

            text = (
                f"{event['type']} "
                f"in {event['sign']} "
                f"({format_days(days)})"
            )

        else:

            text = (
                f"{event['type']} "
                f"({format_days(days)})"
            )


        upcoming.append(
            {
                "date": event_date,
                "text": text,
            }
        )



    #
    # SORT CHRONOLOGICALLY
    #

    upcoming.sort(
        key=lambda item: item["date"]
    )


    return [
        item["text"]
        for item in upcoming
    ]
