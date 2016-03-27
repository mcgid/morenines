import click
import os
import sys

from morenines.index import Index
from morenines.remote import FakeRemote
from morenines.util import get_files, get_hash, get_new_and_missing
from morenines.output import warning, error, print_filelists

# Defining this on its own makes the _common_params definition a little cleaner and nicer
_root_path_type = click.Path( exists=True, file_okay=False, dir_okay=True, resolve_path=True)

_common_params = {
    'index': click.option('--index', 'index_file', type=click.File(), required=True),
    'force': click.option('--force/--no-force', 'force', default=False),
    'root_path': click.argument('root_path', nargs=1, default=os.getcwd(), type=_root_path_type),
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
@common_params('root_path')
def create(root_path):
    index = Index()

    index.headers['root_path'] = root_path

    files = get_files(root_path)

    index.add(files)

    index.write(sys.stdout)


@main.command()
@common_params('index', 'root_path')
@click.option('--remove/--no-remove', 'remove_missing', default=False)
def update(root_path, index_file, remove_missing):
    index = Index.read(index_file)

    new_files, missing_files = get_new_and_missing(root_path, index)

    index.add(new_files)

    if remove_missing is True:
        index.remove(missing_files)

    index.write(sys.stdout)


@main.command()
@common_params('index', 'root_path')
def status(root_path, index_file):
    index = Index.read(index_file)

    new_files, missing_files = get_new_and_missing(root_path, index)

    print_filelists(new_files, None, missing_files)


@main.command()
@common_params('index', 'root_path')
def verify(root_path, index_file):
    index = Index.read(index_file)

    new_files, missing_files = get_new_and_missing(root_path, index)

    changed_files = []

    for path, old_hash in index.files.iteritems():
        if path in missing_files:
            continue

        current_hash = get_hash(os.path.join(root_path, path))

        if current_hash != old_hash:
            changed_files.append(path)

    print_filelists(None, changed_files, missing_files)


@main.command()
@common_params('index', 'root_path', 'force')
def push(root_path, index_file, force):
    index = Index.read(index_file)
    remotes = [FakeRemote(None)]

    # Check for new or missing files before pushing remotely
    new_files, missing_files = get_new_and_missing(root_path, index)

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

