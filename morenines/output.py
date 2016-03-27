import click
import sys

GOOD_COLOUR = 'green'
WARN_COLOUR = 'yellow'
BAD_COLOUR = 'red'

def set_output_colour(colour):
    # Print nothing except the ANSI escape sequence
    click.secho('', nl=False, fg=colour, reset=False)


def clear_output_colour():
    # Print nothing except the reset escape sequence
    click.secho('', nl=False, reset=True)


def output(message, items=[], colour=None):
    if colour:
        set_output_colour(colour)

    click.echo(message)

    for item in sorted(items):
        click.echo("  " + item)

    clear_output_colour()


def warning(message, items=[]):
    output("WARNING: " + message, items, WARN_COLOUR)


def error(message, items=[]):
    output("ERROR: " + message, items, BAD_COLOUR)
    sys.exit(1)


def print_filelists(new_files, changed_files, missing_files):
    if not any([new_files, changed_files, missing_files]):
        output("Index is up-to-date (no changes)", GOOD_COLOUR)
        return

    if new_files:
        output("Added files (not in index):", new_files, WARN_COLOUR)

        # Print a blank space between sections
        if changed_files or missing_files:
            click.echo()

    if changed_files:
        output("Changed files (hash differs from index):", changed_files, BAD_COLOUR)

        # Print a blank space between sections
        if missing_files:
            click.echo()

    if missing_files:
        output("Missing files:", missing_files, WARN_COLOUR)

