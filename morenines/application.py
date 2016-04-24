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


@main.command(short_help="Hash and add any files that aren't in the index")
@pass_repository
@click.argument("paths", required=False, nargs=-1, type=click.Path(resolve_path=True))
def add(repo, paths):
    """Update an existing index wtih new file hashes.

    Must be called from inside an existing repository.
    """
    repo.open(default_repo_path())

    if not paths:
        warning("No action taken (supply one or more PATHS to files to add to the repository)")
        return

    paths = repo.normalize_paths(paths)

    for path in paths:
        if not os.path.exists(path):
            error("Path does not exist: {}".format(path))
            abort()

    paths = repo.expand_subdirs(paths)

    # If dirs were the only supplied paths, and walking them produced no valid files
    # TODO this could really benefit from a --verbose option, to see what is ignored
    if not paths:
        warning("No action taken (if supplied PATHS were subdirs, walking them produced no files)")
        return

    repo.add(paths)
    repo.write_index()
    success("Wrote index file {}".format(repo.index_path))


@main.command(short_help="Remove the hashes of supplied paths from the index.")
@pass_repository
@click.argument("paths", required=False, nargs=-1, type=click.Path(resolve_path=True))
def remove(repo, paths):
    """Update the repository to remove paths from it.

    Must be run while inside a repository.
    """
    repo.open(default_repo_path())

    if not paths:
        warning("No action taken (supply one or more PATHS to files to add to the repository)")
        return

    paths = repo.normalize_paths(paths)

    for path in paths:
        if path not in repo.index.files:
            error("Path not in repository: {}".format(path))
            abort()

    paths = repo.expand_subdirs_from_index(paths)

    # If dirs were the only supplied paths, and walking them produced no valid files
    # TODO this could really benefit from a --verbose option, to see what is ignored
    if not paths:
        warning("No action taken (if supplied PATHS were subdirs, no tracked files are in them)")
        return

    repo.remove(paths)
    repo.write_index()
    success("Wrote index file {}".format(repo.index_path))


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
