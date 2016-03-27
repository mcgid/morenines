import click
import sys

def info(message):
    click.echo(message)

def good(message):
    click.secho("Warning: " + message, fg='green')

def warning(message):
    click.secho("WARNING: " + message, fg='yellow')

def error(message):
    click.secho("ERROR: " + message, fg='red')
    sys.exit(1)


def print_filelist(header, filelist, colour=None):
    click.echo(header)

    for line in sorted(filelist):
        if colour:
            line = click.style(line, fg=colour)

        click.echo("  {}".format(line))


def print_filelists(new_files, changed_files, missing_files):
    if not any([new_files, changed_files, missing_files]):
        good("Index is up-to-date (no changes)")
        return

    if new_files:
        print_filelist("Added files (not in index):", new_files, 'green')

        # Print a blank space between sections
        if changed_files or missing_files:
            click.echo()

    if changed_files:
        print_filelist("Changed files (hash differs from index):", changed_files, 'red')

        # Print a blank space between sections
        if missing_files:
            click.echo()

    if missing_files:
        print_filelist("Missing files:", missing_files, 'red')

