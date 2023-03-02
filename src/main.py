from datetime import datetime
import sys
from typing import Optional

import click
from event import Event

from event_parser import ParseMessageException, parse_into_events, date_format_str
from reschedule import adjust_event_schedule


def display_welcome() -> bool:
    click.echo(f"Welcome to the {click.style('Scheduler', bold=True)}!")
    click.echo("This is a tool to help you redesign your schedule.")

    click.echo("\nWe're about to open an editor for you to put all your entries in.")
    entry_form_text = click.style(
        "<start_date> -> <end_date> - <event_name>", fg="green"
    )
    click.echo(f"Please enter entries in the form: {entry_form_text}")
    date_form_text = click.style("YYYY/MM/DD HH:mm", fg="yellow")
    click.echo(f"Dates must be in the form: {date_form_text}.")

    should_proceed = click.confirm("\nReady to proceed?")
    if not should_proceed:
        click.echo("Ok, let me know when you're ready!")

    return should_proceed


def open_editor() -> Optional[str]:
    message = click.edit(
        "2022/08/23 15:00 -> 2022/08/23 16:00 - Example event, please replace with yours!"
    )
    if not message:
        click.echo("You didn't provide any events to process!")

    return message


def parse_events(message: str) -> list[Event]:
    try:
        events = parse_into_events(message)
    except ParseMessageException as exception:
        click.echo(f"There are errors with these lines of input:")
        for line, error in exception.lines_and_errors:
            click.echo(f'"{line}" - {error}')
        sys.exit(1)

    return events


def print_events(events: list[Event]):
    click.echo(f"Here are the {len(events)} that we've been able to schedule:")
    for event in events:
        start_date = date_to_str(event["start_date"])
        end_date = date_to_str(event["end_date"])
        click.echo(f'{start_date} -> {end_date} - {event["name"]}')


def date_to_str(date: datetime) -> str:
    return date.strftime(date_format_str)


@click.command()
def main():
    should_proceed = display_welcome()
    if not should_proceed:
        sys.exit(1)

    message = open_editor()
    if not message:
        sys.exit(1)

    events = parse_events(message)
    click.echo(f"You gave us {len(events)} events.")

    scheduled_events = adjust_event_schedule(events)
    print_events(scheduled_events)


if __name__ == "__main__":
    main()
