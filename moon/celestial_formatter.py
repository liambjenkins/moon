def format_title(event):

    event_type = event["type"]

    sign = event.get(
        "sign"
    )


    if sign:

        return (
            f"{event_type} "
            f"in {sign}"
        )


    return event_type



def format_notes(event):

    return (
        "Melbourne, Australia"
    )
