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
    'color': click.option('--color/--no-color', 'show_color', default=True),
}


def common_params(*param_names):
    def real_decorator(func):
        for param_name in param_names:
            func = _common_params[param_name](func)
        return func

    return real_decorator


class MNContext(object):
    def __init__(self, config, index, ignores):
        self.config = config
        self.index = index
        self.ignores = ignores


def get_index_path(config):
    if 'index_path' in config:
        return config['index_path']
    else:
        return find_file('.mnindex')


def get_ignores_path(config):
    if 'ignores_file' in config:
        path = config['ignores_file']
    elif 'root_path' in config:
        path = os.path.join(config['root_path'], '.mnignore')
    else:
        return None

    if os.path.isfile(path):
        return path
    else:
        return None


def get_default_config(cwd):
    INDEX_FILENAME = '.mnindex'
    IGNORES_FILENAME = '.mnignore'

    default_config = {
        'default_index_filename': INDEX_FILENAME,
        'default_ignores_filename': IGNORES_FILENAME,
        'default_index_path': os.path.join(cwd, INDEX_FILENAME),
        'default_ignores_path': os.path.join(cwd, IGNORES_FILENAME),
    }

    return default_config


def get_context(index_path, index_required=True):
    config = get_default_config(os.getcwd())

    if index_path:
        config['index_path'] = index_path

    index_path = get_index_path(config)

    if index_path:
        config['index_path'] = index_path

        index = Index.read(index_path)

        config['root_path'] = index.root_path
        config['ignores_file'] = index.ignores_file
    elif not index_path and index_required:
        error("Cannot find index file '.mnindex' in this or any parent dir")
        # XXX XXX TODO write util.abort() or something, to exit centrally
        import sys
        sys.exit(1)
    else:
        index = None

    ignores_path = get_ignores_path(config)

    if ignores_path:
        config['ignores_file'] = ignores_path

        ignores = Ignores.read(ignores_path)
    else:
        ignores = Ignores()

    return MNContext(config, index, ignores)


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

    context = get_context(None, index_required=False)

    index = Index(root_path, ignores_path)

    files, ignored = get_files(index.root_path, context.ignores)

    index.add(files)

    with click.open_file(output_path, mode='w') as stream:
        index.write(stream)

    success('Wrote index file {}'.format(output_path))


@main.command()
@common_params('index')
@click.option('--remove-missing/--no-remove-missing', default=False)
@click.option('--new-root', 'new_root', type=_path_type['existing dir'])
@click.option('--new-ignores-file', type=_path_type['existing file'])
@click.option('-o', '--output', 'output_path', type=_path_type['file'])
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

    if output_path:
        if os.path.basename(output_path) == '-':
            output_path = '-'
    else:
        output_path = context.config['index_path']

    with click.open_file(output_path, mode='w') as stream:
        context.index.write(stream)


@main.command()
@common_params('index', 'ignored', 'color')
@click.pass_context
def status(ctx, index_file, show_ignored, show_color):
    context = get_context(index_file)

    new_files, missing_files, ignored_files = get_new_and_missing(context.index, context.ignores, show_ignored)

    ctx.color = show_color

    print_filelists(new_files, None, missing_files, ignored_files)


@main.command()
@common_params('index', 'ignored', 'color')
@click.pass_context
def verify(ctx, index_file, show_ignored, show_color):
    context = get_context(index_file)

    new_files, missing_files, ignored_files = get_new_and_missing(context.index, context.ignores, show_ignored)

    changed_files = []

    for path, old_hash in context.index.files.iteritems():
        if path in missing_files:
            continue

        current_hash = get_hash(os.path.join(context.index.root_path, path))

        if current_hash != old_hash:
            changed_files.append(path)

    ctx.color = show_color

    print_filelists(new_files, changed_files, missing_files, ignored_files)


@main.command(name='edit-ignores')
@click.option('--ignores-file', 'ignores_path', type=_path_type['file'])
def edit_ignores(ignores_path):
    context = get_context(None, index_required=False)

    if 'ignores_file' in context.config:
        path = context.config['ignores_file']
    else:
        path = context.config['default_ignores_file']

    click.edit(filename=path)

if __name__ == '__main__':
    main()
