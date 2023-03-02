from datetime import datetime
from event import Event


def parse_into_events(message: str) -> list[Event]:
    """Parses a multiline string into structured dicts for Event details. See
    parse_line for details on the structure needed for each line.

    Args:
        message (str): The message containing lines of events

    Raises:
        ParseMessageError: Raised for any lines that are not in the correct
        structure

    Returns:
        list[Event]: A list of Event dicts of processed data
    """
    lines = message.splitlines()

    errors = []
    events = []
    for line in lines:
        try:
            events.append(parse_line(line))
        except ParseLineException as e:
            errors.append(line)

    if errors:
        raise ParseMessageException(lines_and_errors=errors)

    return events


def parse_line(line: str) -> Event:
    """Parses a single line of the format <start_date> -> <end_date> - <name>
    into a structured dict of properties. Dates must be in format
    YYYY/MM/DD HH:mm.

    Args:
        line (str): The line to parse

    Raises:
        ParseLineException: Raised if the line does not match the structure (
        or the date is in the incorrect format).

    Returns:
        Event: A structured dict of Event properties
    """
    raw_start_date, *first_split_parts = line.split(" -> ", maxsplit=1)
    if not raw_start_date or not first_split_parts:
        raise ParseLineException("Line is not structured correctly")

    raw_end_date, *second_split_parts = first_split_parts[0].split(" - ", maxsplit=1)
    if not raw_end_date or not second_split_parts:
        raise ParseLineException("Line is not structured correctly")

    try:
        str_format = "YYYY/MM/DD HH:mm"
        start_date = datetime.strptime(raw_start_date, str_format)
        end_date = datetime.strptime(raw_end_date, str_format)
    except Exception as exception:
        raise ParseLineException("Dates are not formatted correctly") from exception

    return {
        "start_date": start_date,
        "end_date": end_date,
        "name": second_split_parts[0],
    }


class ParseLineException(Exception):
    pass


class ParseMessageException(Exception):
    lines_and_errors: list[tuple[str, str]]

    def __init__(self, *args: object, lines_and_errors: list[tuple[str, str]]) -> None:
        super().__init__(*args)
        self.lines_and_errors = lines_and_errors
