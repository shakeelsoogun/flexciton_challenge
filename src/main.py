import click


def parse(line: str) -> list[str]:
    return line.split("\n")


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


@click.command()
def main():
    display_welcome()
    message = click.edit(
        "2022/08/23 15:00 -> 2022/08/23 16:00 - Example event, please replace with yours!"
    )
    if not message:
        click.echo("You didn't provide any events to process!")
        return

    lines = parse(message)
    click.echo(f"You gave us {len(lines)} lines.")


if __name__ == "__main__":
    main()
