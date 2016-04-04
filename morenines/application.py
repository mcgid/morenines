import click
import os
import sys

from morenines.index import Index
from morenines.ignores import Ignores
from morenines.util import get_files, get_hash, get_new_and_missing, find_file
from morenines.output import success, warning, error, print_filelists

_path_type = {
    'file':click.Path(file_okay=True, dir_okay=False, resolve_path=True),
    'existing file':click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True),
    'new file':click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True),
    'existing dir':click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
}

_common_params = {
    'index': click.argument('index_file', required=False, type=_path_type['file']),
    'ignored': click.option('-i', '--ignored/--no-ignored', 'show_ignored', default=False),
}


def common_params(*param_names):
    def real_decorator(func):
        for param_name in param_names:
            func = _common_params[param_name](func)
        return func

    return real_decorator


class MNContext(object):
    def __init__(self, index, ignores):
        self.index = index
        self.ignores = ignores


def get_index(index_path):
    if not index_path:
        index_path = find_file('.mnindex')

    if index_path:
        index = Index.read(index_path)
    else:
        index = None

    return index


def get_ignores(index):
    if index.ignores_file:
        ignores_path = index.ignores_file
    else:
        ignores_path = os.path.join(index.root_path, '.mnignore')

    if os.path.isfile(ignores_path):
        ignores = Ignores.read(ignores_path)
    else:
        ignores = Ignores()

    return ignores


def get_context(index_path, index_required=True):
    index = get_index(index_path)

    if not index and index_required:
        error("Cannot find index file '.mnindex' in this or any parent dir")
        # XXX XXX TODO write util.abort() or something, to exit centrally
        import sys
        sys.exit(1)

    if index:
        ignores = get_ignores(index)
    else:
        ignores = Ignores()

    return MNContext(index, ignores)


@click.group()
def main():
    pass


@main.command()
@click.option('--ignores-file', 'ignores_path', type=_path_type['existing file'])
@click.option('-o', '--output', 'output_path', default=os.path.join(os.getcwd(), '.mnindex'), type=_path_type['new file'])
@click.argument('root_path', required=True, default=os.getcwd(), type=_path_type['existing dir'])
def create(ignores_path, root_path, output_path):
    if os.path.exists(output_path):
        error("Index file {} already exists".format(output_path))
        error("(To update an existing index file, use the 'update' command)")
        sys.exit(1)

    if os.path.basename(output_path) == '-':
        output_path = '-'

    index = Index(root_path, ignores_path)

    ignores = get_ignores(index)

    files, ignored = get_files(index.root_path, ignores)

    index.add(files)

    with click.open_file(output_path, mode='w') as stream:
        index.write(stream)

    success('Wrote index file {}'.format(output_path))


@main.command()
@common_params('index')
@click.option('--remove-missing/--no-remove-missing', default=False)
@click.option('--new-root', 'new_root', type=_path_type['existing dir'])
@click.option('--new-ignores-file', type=_path_type['existing file'])
@click.option('-o', '--output', 'output_path', default=os.path.join(os.getcwd(), '.mnindex'), type=_path_type['file'])
def update(index_file, remove_missing, new_root, new_ignores_file, output_path):
    context = get_context(index_file)

    if new_root:
        context.index.root_path = new_root

    # Just update the ignores file header, without trying to read that new file
    # This seems least surprising, since we're creating the new index based on
    # the current one, and the current one is influenced by the current ignores file.
    if new_ignores_file:
        context.index.ignores_file = new_ignores_file

    new_files, missing_files, ignored_files = get_new_and_missing(context.index, context.ignores)

    context.index.add(new_files)

    if remove_missing is True:
        context.index.remove(missing_files)

    if os.path.basename(output_path) == '-':
        output_path = '-'

    with click.open_file(output_path, mode='w') as stream:
        context.index.write(stream)


@main.command()
@common_params('index', 'ignored')
def status(index_file, show_ignored):
    context = get_context(index_file)

    new_files, missing_files, ignored_files = get_new_and_missing(context.index, context.ignores, show_ignored)

    print_filelists(new_files, None, missing_files, ignored_files)


@main.command()
@common_params('index', 'ignored')
def verify(index_file, show_ignored):
    context = get_context(index_file)

    new_files, missing_files, ignored_files = get_new_and_missing(context.index, context.ignores, show_ignored)

    changed_files = []

    for path, old_hash in context.index.files.iteritems():
        if path in missing_files:
            continue

        current_hash = get_hash(os.path.join(context.index.root_path, path))

        if current_hash != old_hash:
            changed_files.append(path)

    print_filelists(new_files, changed_files, missing_files, ignored_files)


@main.command(name='edit-ignores')
@click.option('--ignores-file', 'ignores_path', type=_path_type['file'])
def edit_ignores(ignores_path):
    context = get_context(None, index_required=False)

    # TODO Make get_ignores_path() and call it from here and from get_ignores() ?
    if context.index:
        if context.index.ignores_file:
            path = context.index.ignores_file
        else:
            path = os.path.join(context.index.root_path, '.mnignore')
    else:
        path = os.path.join(os.getcwd(), '.mnignore')

    click.edit(filename=path)

if __name__ == '__main__':
    main()
