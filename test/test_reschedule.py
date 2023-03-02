from datetime import datetime

import pytest
from event import Event

from reschedule import date_is_inside_hours, does_events_overlap, slot_into_schedule


test_date = datetime(year=2023, month=3, day=2)


class TestDateIsInsideHours:
    @pytest.mark.parametrize(
        "date",
        [
            # Monday 6th March 9:00 (Monday 9am boundary)
            test_date.replace(day=6, hour=9, minute=0),
            # Friday 3rd March 18:00 (Friday 18:00 boundary)
            test_date.replace(day=3, hour=18, minute=0),
        ],
    )
    def test_true(self, date: datetime):
        assert date_is_inside_hours(date) is True

    @pytest.mark.parametrize(
        "date",
        [
            # Saturday 4th
            test_date.replace(day=4, hour=9, minute=0),
            # Sunday 5th
            test_date.replace(day=5, hour=18, minute=0),
            # Before 9
            test_date.replace(hour=8, minute=59),
            # outside of 18
            test_date.replace(hour=19, minute=59),
            # 18, but 1min past
            test_date.replace(hour=18, minute=1),
        ],
    )
    def test_false(self, date: datetime):
        assert date_is_inside_hours(date) is False


class TestDoesEventsOverlap:
    @pytest.mark.parametrize(
        ["times_1", "times_2"],
        [
            [
                (
                    test_date.replace(hour=9, minute=0),
                    test_date.replace(hour=10, minute=0),
                ),
                (
                    test_date.replace(hour=10, minute=0),
                    test_date.replace(hour=11, minute=0),
                ),
            ],
            [
                (
                    test_date.replace(hour=9, minute=30),
                    test_date.replace(hour=10, minute=30),
                ),
                (
                    test_date.replace(hour=10, minute=30),
                    test_date.replace(hour=11, minute=30),
                ),
            ],
        ],
    )
    def test_no_overlap(self, times_1, times_2):
        (start_date_1, end_date_1) = times_1
        (start_date_2, end_date_2) = times_2

        event_1: Event = {
            "name": "Event 1",
            "start_date": start_date_1,
            "end_date": end_date_1,
        }
        event_2: Event = {
            "name": "Event 2",
            "start_date": start_date_2,
            "end_date": end_date_2,
        }
        assert does_events_overlap(event_1, event_2) is False

    @pytest.mark.parametrize(
        ["times_1", "times_2"],
        [
            # Overlap start date
            [
                (
                    test_date.replace(hour=9, minute=0),
                    test_date.replace(hour=10, minute=0),
                ),
                (
                    test_date.replace(hour=9, minute=30),
                    test_date.replace(hour=10, minute=0),
                ),
            ],
            # Overlap end date
            [
                (
                    test_date.replace(hour=9, minute=0),
                    test_date.replace(hour=10, minute=30),
                ),
                (
                    test_date.replace(hour=8, minute=29),
                    test_date.replace(hour=9, minute=30),
                ),
            ],
            # Encompassing
            [
                (
                    test_date.replace(hour=9, minute=0),
                    test_date.replace(hour=10, minute=30),
                ),
                (
                    test_date.replace(hour=8, minute=29),
                    test_date.replace(hour=11, minute=30),
                ),
            ],
        ],
    )
    def test_overlap(self, times_1, times_2):
        (start_date_1, end_date_1) = times_1
        (start_date_2, end_date_2) = times_2

        event_1: Event = {
            "name": "Event 1",
            "start_date": start_date_1,
            "end_date": end_date_1,
        }
        event_2: Event = {
            "name": "Event 2",
            "start_date": start_date_2,
            "end_date": end_date_2,
        }
        assert does_events_overlap(event_1, event_2) is True


class TestSlotIntoSchedule:
    def test_no_events(self):
        event: Event = {
            "start_date": test_date.replace(hour=9, minute=0),
            "end_date": test_date.replace(hour=10, minute=0),
            "name": "Event 1",
        }
        events = slot_into_schedule(event, [])
        assert events == [event]

    def test_slot_event_after_everything(self):
        event: Event = {
            "start_date": test_date.replace(hour=10, minute=0),
            "end_date": test_date.replace(hour=11, minute=10),
            "name": "Event 1",
        }
        event_2: Event = {
            "start_date": test_date.replace(hour=9, minute=0),
            "end_date": test_date.replace(hour=10, minute=10),
            "name": "Event 2",
        }
        readjusted_event: Event = {
            "start_date": test_date.replace(hour=10, minute=10),
            "end_date": test_date.replace(hour=11, minute=20),
            "name": "Event 1",
        }
        events = slot_into_schedule(event, [event_2])
        assert events == [event_2, readjusted_event]

    def test_slot_event_before_everything(self):
        event: Event = {
            "start_date": test_date.replace(hour=9, minute=0),
            "end_date": test_date.replace(hour=10, minute=0),
            "name": "Event 1",
        }
        event_2: Event = {
            "start_date": test_date.replace(hour=11, minute=0),
            "end_date": test_date.replace(hour=12, minute=10),
            "name": "Event 2",
        }
        readjusted_event: Event = {
            "start_date": test_date.replace(hour=10, minute=0),
            "end_date": test_date.replace(hour=11, minute=0),
            "name": "Event 1",
        }
        events = slot_into_schedule(event, [event_2])
        assert events == [readjusted_event, event_2]
