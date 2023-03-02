from datetime import datetime, timedelta
from operator import itemgetter
from event import Event


def adjust_event_schedule(events: list[Event]) -> list[Event]:
    """Filter for all events that validly fit within the time schedule
    (Mon-Fri 09:00-18:00) and don't overlap, and then try to refit all other
    events around these valid ones.

    Args:
        events (list[Event]): The events to readjust

    Returns:
        list[Event]: A new list of events that fit within Mon-Fri 09:00-18:00
        and don't overlap
    """
    # First pass - find all the events that are already valid (prioritising first encountered)
    # Invalid states:
    #  - Outside of hours (Mon-Fri 9:00-18:00)
    #  - Events overlap each other
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

    # Sort the events and then find where we can slot them in one by one
    sorted_events = sorted(valid_events, key=itemgetter("start_date"))
    to_be_rescheduled = sorted(to_be_rescheduled, key=itemgetter("start_date"))
    for event in to_be_rescheduled:
        sorted_events = slot_into_schedule(event, sorted_events)

    return sorted_events


def slot_into_schedule(event: Event, valid_events: list[Event]) -> list[Event]:
    """Takes an event and existing valid schedule of events and finds the next
    available space where it can fit, as close to its original time as possible.

    Args:
        event (Event): The event to fit in
        valid_events (list[Event]): A valid schedule of events. We assume these
        are:
            - sorted in asc order
            - within the time constraints
            - don't overlap each other. 

    Returns:
        list[Event]: A new schedule of events with the event slotted in.
    """
    if not valid_events:
        return [event]

    event_duration = event["end_date"] - event["start_date"]

    for index, valid_event in enumerate(valid_events):
        previous_event = valid_events[index - 1] if index > 0 else None
        if (
            event["start_date"] >= valid_event["start_date"]
            or event["start_date"] >= valid_event["end_date"]
            or not previous_event
        ):
            continue

        # valid_event is after our event, so try scheduling it in between
        # previous_event and valid_event
        end_of_day = previous_event["end_date"].replace(hour=18, minute=0)
        if end_of_day > valid_event["start_date"]:
            # previous and next events are on the same day, so check the slot between these
            slot_duration = valid_event["start_date"] - previous_event["end_date"]
            if event_duration > slot_duration:
                continue

            slot_start = previous_event["end_date"]

        else:
            # The next event is on the next day, so there's 3 potential slots:
            #  - Up to the end of day 1 (just after previous event)
            day_1_slot_duration = end_of_day - previous_event["end_date"]

            #  - At the start of day 2 (just before next event)
            start_of_day_2 = valid_event["start_date"].replace(hour=9, minute=0)
            day_2_slot_duration = valid_event["start_date"] - start_of_day_2

            #  - Any free days that occur between day 1 and day 2
            days_between = find_days_between_dates(
                previous_event["end_date"], valid_event["start_date"]
            )

            if event_duration <= day_1_slot_duration:
                slot_start = previous_event["end_date"]
            if days_between:
                # We have some free days in between, so just pick the first day
                slot_start = days_between[0].replace(hour=9, minute=0)
            elif event_duration <= day_2_slot_duration:
                slot_start = start_of_day_2
            else:
                # Can't fit into either slot, so move on
                continue

        # Found a slot, so fit the event in
        new_event: Event = {
            "start_date": slot_start,
            "end_date": slot_start + event_duration,
            "name": event["name"],
        }
        all_previous = valid_events[0:index]
        all_next = valid_events[index:]
        return all_previous + [new_event] + all_next

    # Fit our event after all the others
    last_valid_event = valid_events[-1]
    end_of_day = last_valid_event["end_date"].replace(hour=18, minute=0)
    slot_duration = end_of_day - last_valid_event["end_date"]

    last_event_time = last_valid_event["end_date"]
    next_start = last_valid_event["end_date"]
    if slot_duration < event_duration:
        # Can't fit on same day, so fit on next week if Friday, else next day
        days_to_increment = 3 if last_event_time.isoweekday() == 5 else 1
        next_start = next_start.replace(hour=9, minute=0) + timedelta(
            days=days_to_increment
        )
    new_event: Event = {
        "start_date": last_valid_event["end_date"],
        "end_date": last_valid_event["end_date"] + event_duration,
        "name": event["name"],
    }
    return valid_events + [new_event]


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


def find_days_between_dates(date_1: datetime, date_2: datetime) -> list[datetime]:
    duration = date_2 - date_1
    if duration.days <= 1:
        return []

    dates_in_between = []
    for day_count in range(2, duration.days):
        date_to_check = date_1 + timedelta(days=day_count)
        if date_to_check.isoweekday() in [6, 7]:
            continue
        dates_in_between.append(date_to_check)

    return dates_in_between
