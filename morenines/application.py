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
    changed_files, missing_files = morenines.verify.verify(root_path, index_path)

    morenines.output.print_filelists(None, changed_files, missing_files)


@main.command()
@click.option('--index', 'index_path', required=True)
@click.argument('root_path', nargs=1, default=os.getcwd())
def status(root_path, index_path):
    new_files, missing_files = morenines.status.status(root_path, index_path)
    morenines.output.print_filelists(new_files, None, missing_files)


@main.command()
@click.option('--index', 'index_path', required=True)
@click.argument('root_path', nargs=1, default=os.getcwd())
def push(root_path, index_path):
    remotes = [morenines.remote.FakeRemote(None)]
    morenines.push.push(root_path, index_path, remotes)

if __name__ == '__main__':
    main()

