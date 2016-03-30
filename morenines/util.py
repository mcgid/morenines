import os
import hashlib

from morenines.ignores import Ignores


def get_files(root_path, ignores, save_ignored_paths=False):
    paths = []
    ignored = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        ignored_dirs = [d for d in dirnames if ignores.match(d)]

        # Only walk ignored dirs if we're saving all ignored paths
        if save_ignored_paths:
            # Directories end in a slash
            ignored.extend([path + '/' for path in rel_paths_iter(ignored_dirs, dirpath, root_path)])

        # Prune ignored subdirs of current dir in-place
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs]

        for path in rel_paths_iter(filenames, dirpath, root_path):
            if ignores.match(path):
                if save_ignored_paths:
                    ignored.append(path)
                continue
            else:
                paths.append(path)

    return paths, ignored


def rel_paths_iter(names, parent_dir_path, root_path):
    for name in names:
        # We want the full path of the file/dir, not its name
        path = os.path.join(parent_dir_path, name)

        # That path must be relative to the root, not absolute
        path = os.path.relpath(path, root_path)

        yield path


def get_ignores(ignores_path=None):
    if not ignores_path:
        return Ignores()

    with open(ignores_path, 'r') as ignores_path:
        ignores = Ignores.read(ignores_path)

    return ignores


def get_hash(path):
    h = hashlib.sha1()

    with open(path, 'rb') as f:
        h.update(f.read())

    return h.hexdigest()


def get_new_and_missing(index, ignores, include_ignored=False):
    current_files, ignored_files = get_files(index.headers['root_path'], ignores, include_ignored)

    new_files = [path for path in current_files if path not in index.files]

    missing_files = [path for path in index.files.iterkeys() if path not in current_files]

    return new_files, missing_files, ignored_files
