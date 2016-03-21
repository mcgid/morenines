import click
import os
import sys

import morenines.create
import morenines.verify
import morenines.remote
import morenines.push
import morenines.output

#root_path_type = click.Path(
#    exists=True,
#    file_okay=False,
#    dir_okay=True,
#    resolve_path=True,
#)

@click.group()
def main():
    pass


@main.command()
@click.argument('root_path', nargs=1, default=os.getcwd())
def create(root_path):
    index = morenines.create.create(root_path)

    index.write(sys.stdout)

@main.command()
@click.option('--index', 'index_path', required=True)
@click.argument('root_path', nargs=1, default=os.getcwd())
def verify(root_path, index_path):
    changed_files = morenines.verify.verify(root_path, index_path)

    if changed_files:
        morenines.output.print_filelist("Changed files (hash differs from index):", changed_files)
    else:
        morenines.output.print_message("Index is up-to-date (no changes)")


@main.command()
@click.option('--index', 'index_path', required=True)
@click.argument('root_path', nargs=1, default=os.getcwd())
def status(root_path, index_path):
    new_files, missing_files = morenines.status.status(root_path, index_path)

    if new_files:
        morenines.output.print_filelist("Added files (not in index):", new_files)

    if missing_files:
        morenines.output.print_filelist("Missing files:", missing_files)

    if not new_files and not missing_files:
        morenines.output.print_message("Index is up-to-date (no changes)")


@main.command()
@click.option('--index', 'index_path', required=True)
@click.argument('root_path', nargs=1, default=os.getcwd())
def push(root_path, index_path):
    remotes = [morenines.remote.FakeRemote(None)]
    morenines.push.push(root_path, index_path, remotes)

if __name__ == '__main__':
    main()

