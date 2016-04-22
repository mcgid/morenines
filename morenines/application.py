import click
import os
import sys

from morenines.index import Index
from morenines.ignores import Ignores
from morenines.repository import Repository
from morenines.util import get_files, get_hash, get_new_and_missing, abort
from morenines.output import info, success, warning, error, print_filelists


pass_repository = click.make_pass_decorator(Repository, ensure=True)

def default_repo_path():
    return os.getcwd()

_common_params = {
    'ignored': click.option('-i', '--ignored/--no-ignored', 'show_ignored', default=False, help="Enable/disable showing files ignored by the ignores patterns."),
    'color': click.option('--color/--no-color', 'show_color', default=True, help="Enable/disable colorized output."),
}

def common_params(*param_names):
    def real_decorator(func):
        for param_name in param_names:
            func = _common_params[param_name](func)
        return func

    return real_decorator


@click.group()
def main():
    """A tool to track whether the content of files has changed."""
    pass


@main.command(short_help="Initialize a new morenines repository")
@click.argument("repo_path", required=False, type=click.Path(resolve_path=True))
@pass_repository
def init(repo, repo_path):
    """Create the morenines repository (the .morenines directory and associated
       files) in REPO_PATH, the parent directory containing all files (including
       in subdirs) that will be tracked.

    Must not be called inside an existing repository.
    """
    if not repo_path:
        repo_path = default_repo_path()

    repo.create(repo_path)

    success("Initialized empty morenines repository in {}".format(repo.mn_dir_path))


@main.command(short_help="Update an existing index file")
@pass_repository
@click.option('--add-new/--no-add-new', default=False, help="Hash and add any files that aren't in the index")
@click.option('--remove-missing/--no-remove-missing', default=False, help="Delete any the hashes of any files in the index that no longer exist.")
def update(repo, add_new, remove_missing):
    """Update an existing index file with new file hashes, missing files removed, etc.

    Must be called from inside an existing repository.
    """
    repo.open(default_repo_path())
    new_files, missing_files, ignored_files = get_new_and_missing(repo)

    if add_new:
        repo.index.add(new_files)

    if remove_missing is True:
        repo.index.remove(missing_files)

    if not any([new_files, missing_files]):
        info("Index is up-to-date (no new or missing files)")
    elif add_new or remove_missing:
        repo.write_index()
        success("Wrote index file {}".format(repo.index_path))
    else:
        warning("No action taken (use '--add-new' or '--remove-missing' to change the index)")


@main.command(short_help="Show new, missing or ignored files")
@common_params('ignored', 'color')
@click.option('--verify/--no-verify', default=False, help="Re-hash all files in index and check for changes")
@pass_repository
@click.pass_context
def status(ctx, repo, show_ignored, show_color, verify):
    """Show any new files not in the index, index files that are missing, or ignored files.

    Must be called from inside an existing repository.
    """
    repo.open(default_repo_path())

    new_files, missing_files, ignored_files = get_new_and_missing(repo, show_ignored)

    changed_files = []

    if verify:
        for path, old_hash in repo.index.files.items():
            if path in missing_files:
                continue

            current_hash = get_hash(os.path.join(repo.path, path))

            if current_hash != old_hash:
                changed_files.append(path)

    ctx.color = show_color

    print_filelists(new_files, changed_files, missing_files, ignored_files)


@main.command(name='edit-ignores', short_help="Open the ignores file in an editor")
@pass_repository
def edit_ignores(repo):
    """Open an existing or a new ignores file in an editor.

    Must be called from inside an existing repository.
    """
    repo.open(default_repo_path())

    click.edit(filename=repo.ignore_path)


if __name__ == '__main__':
    main()
