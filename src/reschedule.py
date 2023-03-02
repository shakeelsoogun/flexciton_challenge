from datetime import datetime
from operator import itemgetter
from event import Event


# Potential invalid states:
#  - Outside of hours (Mon-Fri 9:00-18:00)
#  - Events overlap each other
def reschedule(events: list[Event]) -> list[Event]:
    # first pass - find all the events that are already valid (prioritising first encountered)
    valid_events = []
    to_be_rescheduled = []
    for event in events:
        # Check for inside correct hours
        if not is_inside_hours(event):
            to_be_rescheduled.append(event)
            continue

        # Check for overlaps
        is_overlapping = any(x for x in valid_events if does_events_overlap(x, event))
        if is_overlapping:
            to_be_rescheduled.append(event)
        else:
            valid_events.append(event)

    sorted_initial_events = sorted(valid_events, key=itemgetter("start_date"))

    return sorted_initial_events


def is_inside_hours(event: Event) -> bool:
    return date_is_inside_hours(event["start_date"]) and date_is_inside_hours(
        event["end_date"]
    )


def date_is_inside_hours(date: datetime) -> bool:
    is_on_weekday = date.isoweekday() not in [6, 7]
    is_on_or_after_9 = date.hour >= 9
    is_before_or_on_18 = date.hour < 18 or (date.hour == 18 and date.minute == 0)

    return is_on_weekday and is_on_or_after_9 and is_before_or_on_18


#  - Overlapping:
#    - start_date occurs within the time of another event (after start_date and before end_date)
#    - end_date occurs within the time of another event (after start_date and before end_date)
#    - event has another event occurring within it (1.start_date is before 2.start_date, and 1.end_date is after 2.end_date)
def does_events_overlap(event_1: Event, event_2: Event) -> bool:
    is_start_date_2_in_time_1 = (
        event_2["start_date"] >= event_1["start_date"]
        and event_2["start_date"] < event_1["end_date"]
    )
    is_end_date_2_in_time_1 = (
        event_2["end_date"] > event_1["start_date"]
        and event_2["end_date"] <= event_1["end_date"]
    )
    is_event_2_encompassing_event_1 = (
        event_2["start_date"] <= event_1["start_date"]
        and event_2["end_date"] >= event_1["end_date"]
    )

    return (
        is_start_date_2_in_time_1
        or is_end_date_2_in_time_1
        or is_event_2_encompassing_event_1
    )
