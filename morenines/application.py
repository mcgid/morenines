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

_common_params = {
    'index': click.option('--index', 'index_path', required=True),
    'root_path': click.argument('root_path', nargs=1, default=os.getcwd()),
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
    index = morenines.create.create(root_path)

    index.write(sys.stdout)

@main.command()
@common_params('index', 'root_path')
def verify(root_path, index_path):
    changed_files, missing_files = morenines.verify.verify(root_path, index_path)

    morenines.output.print_filelists(None, changed_files, missing_files)


@main.command()
@common_params('index', 'root_path')
def status(root_path, index_path):
    new_files, missing_files = morenines.status.status(root_path, index_path)
    morenines.output.print_filelists(new_files, None, missing_files)


@main.command()
@common_params('index', 'root_path')
def push(root_path, index_path):
    remotes = [morenines.remote.FakeRemote(None)]
    morenines.push.push(root_path, index_path, remotes)

if __name__ == '__main__':
    main()

