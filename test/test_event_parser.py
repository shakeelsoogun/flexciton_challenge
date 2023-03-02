from datetime import datetime

import pytest

from event_parser import (
    ParseLineException,
    ParseMessageException,
    parse_into_events,
    parse_line,
)


class TestParseLine:
    def test_parse_success(self):
        line = "2022/08/23 15:00 -> 2022/08/23 16:00 - Meet Jamie for coffee"
        start_date = datetime(year=2022, month=8, day=23, hour=15)
        end_date = datetime(year=2022, month=8, day=23, hour=16)
        name = "Meet Jamie for coffee"
        expected_result = {"start_date": start_date, "end_date": end_date, "name": name}

        assert parse_line(line) == expected_result

    @pytest.mark.parametrize(
        "line",
        [
            # incorrect start date - year format
            "22/08/23 15:00 -> 2022/08/23 16:00 - Meet Jamie for coffee",
            # incorrect end date - year format
            "2022/08/23 15:00 -> 22/08/23 16:00 - Meet Jamie for coffee",
            # incorrect structure - no arrow between dates
            "2022/08/23 15:00 22/08/23 16:00 - Meet Jamie for coffee",
            # incorrect structure - no dash between end date and event name
            "2022/08/23 15:00 -> 22/08/23 16:00 Meet Jamie for coffee",
            # incorrect structure - no name
            "2022/08/23 15:00 -> 22/08/23 16:00 - ",
        ],
    )
    def test_raise_when_incorrect(self, line: str):
        with pytest.raises(ParseLineException):
            parse_line(line)


class TestParseIntoEvents:
    def test_parse_success(self):
        message = """2022/08/23 15:00 -> 2022/08/23 16:00 - Meet Jamie for coffee
        2022/08/23 15:00 -> 2022/08/23 16:00 - Meet Jamie for coffee
        """
        start_date = datetime(year=2022, month=8, day=23, hour=15)
        end_date = datetime(year=2022, month=8, day=23, hour=16)
        name = "Meet Jamie for coffee"
        expected_result = {"start_date": start_date, "end_date": end_date, "name": name}

        assert parse_into_events(message) == [expected_result, expected_result]

    @pytest.mark.parametrize(
        "message",
        [
            # Incorrect first line
            """22/08/23 15:00 -> 2022/08/23 16:00 - Meet Jamie for coffee
            2022/08/23 15:00 -> 2022/08/23 16:00 - Meet Jamie for coffee
            """,
            # Incorrect second line
            """2022/08/23 15:00 -> 22/08/23 16:00 - Meet Jamie for coffee
            2022/08/23 15:00 -> 2022/08/23 16:00 - Meet Jamie for coffee
            """,
            # Incorrect both lines
            """22/08/23 15:00 -> 22/08/23 16:00 - Meet Jamie for coffee
            2022/08/23 15:00 -> 22/08/23 16:00 - Meet Jamie for coffee
            """,
        ],
    )
    def test_parse_fail(self, message: str):
        with pytest.raises(ParseMessageException):
            parse_into_events(message)
