import click

def print_message(message):
    print message


def print_filelist(header, filelist, colour=None):
    click.echo(header)

    for line in filelist:
        if colour:
            line = click.style(line, fg=colour)

        click.echo("  {}".format(line))


def print_filelists(new_files, changed_files, missing_files):
    if not any([new_files, changed_files, missing_files]):
        print_message("Index is up-to-date (no changes)")
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

