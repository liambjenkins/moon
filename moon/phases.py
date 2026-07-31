from datetime import timedelta


def get_phase_from_events(day, events):

    current = day


    previous = None
    upcoming = None


    for event in events:

        event_date = event["time"].date()


        if event_date <= current:

            previous = event


        elif upcoming is None:

            upcoming = event
            break


    if previous is None:

        return "Waning Crescent"


    phase = previous["phase"]


    if phase == "New Moon":

        return "Waxing Crescent"


    if phase == "First Quarter":

        return "Waxing Gibbous"


    if phase == "Full Moon":

        return "Waning Gibbous"


    if phase == "Last Quarter":

        return "Waning Crescent"


    return phase



def get_illumination(angle):

    import math

    value = (
        1 - math.cos(
            math.radians(angle)
        )
    ) / 2

    return round(
        value * 100
    )
