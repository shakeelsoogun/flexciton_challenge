from datetime import datetime

from event_parser import parse_line


class TestParseLine:
    def test_parse_success(self):
        line = "2022/08/23 15:00 -> 2022/08/23 16:00 - Meet Jamie for coffee"
        start_date = datetime(year=2022, month=8, day=23, hour=15)
        end_date = datetime(year=2022, month=8, day=23, hour=16)
        name = "Meet Jamie for coffee"
        expected_result = {"start_date": start_date, "end_date": end_date, "name": name}

        assert parse_line(line) == expected_result
