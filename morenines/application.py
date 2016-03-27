import click
import os
import sys

from morenines.index import Index
from morenines.ignores import Ignores
from morenines.remote import FakeRemote
from morenines.util import get_files, get_hash, get_new_and_missing
from morenines.output import warning, error, print_filelists

# Defining this on its own makes the _common_params definition a little cleaner and nicer
_root_path_type = click.Path( exists=True, file_okay=False, dir_okay=True, resolve_path=True)
_ignores_path_type = click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True)

_common_params = {
    'index': click.argument('index_file', type=click.File(), required=True),
}


def common_params(*param_names):
    def real_decorator(func):
        for param_name in param_names:
            func = _common_params[param_name](func)
        return func

    return real_decorator


@click.group()
def main():
    pass


@main.command()
@click.option('--ignores-file', 'ignores_path', type=_ignores_path_type)
@click.argument('root_path', required=True, default=os.getcwd(), type=_root_path_type)
def create(ignores_path, root_path):
    index = Index()

    index.headers['root_path'] = root_path

    if ignores_path:
        index.headers['ignores_file'] = ignores_path

        index.ignores = Ignores.read(ignores_path)

    files = get_files(index)

    index.add(files)

    index.write(sys.stdout)


@main.command()
@common_params('index')
@click.option('--remove/--no-remove', 'remove_missing', default=False)
@click.option('--new-root', 'new_root', type=_root_path_type)
def update(index_file, remove_missing, new_root):
    index = Index.read(index_file)

    if new_root:
        index.headers['root_path'] = new_root

    new_files, missing_files = get_new_and_missing(index)

    index.add(new_files)

    if remove_missing is True:
        index.remove(missing_files)

    index.write(sys.stdout)


@main.command()
@common_params('index')
def status(index_file):
    index = Index.read(index_file)

    new_files, missing_files = get_new_and_missing(index)

    print_filelists(new_files, None, missing_files)


@main.command()
@common_params('index')
def verify(index_file):
    index = Index.read(index_file)

    new_files, missing_files = get_new_and_missing(index)

    changed_files = []

    for path, old_hash in index.files.iteritems():
        if path in missing_files:
            continue

        current_hash = get_hash(os.path.join(index.headers['root_path'], path))

        if current_hash != old_hash:
            changed_files.append(path)

    print_filelists(new_files, changed_files, missing_files)


@main.command()
@common_params('index')
@click.option('--force/--no-force', 'force', default=False)
def push(index_file, force):
    index = Index.read(index_file)
    remotes = [FakeRemote(None)]

    # Check for new or missing files before pushing remotely
    new_files, missing_files = get_new_and_missing(index)

    if any([new_files, missing_files]):
        message = "Index file is out-of-date (there are new or missing files in the tree)"
        if force:
            warning(message + "\n" + "Pushing anyway because --force was used")
        else:
            error(message + "\n" + "(Use --force option to push anyway)")

    for remote in remotes:
        remote_blobs = remote.get_blob_list()

        files_to_upload = []

        for path, hash_ in index.files.iteritems():
            if hash_ not in remote_blobs:
                files_to_upload.append(path)

        for path in files_to_upload:
            remote.upload(path)


if __name__ == '__main__':
    main()

