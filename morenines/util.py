import os
import hashlib

from morenines.ignores import Ignores


def get_files(root_path, ignores, save_ignored_paths=False):
    paths = []
    ignored = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        # If we aren't saving ignored paths, we can prune the tree as we walk
        if not save_ignored_paths:
            # Prune ignored subdirs of current dir in-place
            dirnames[:] = [d for d in dirnames if not ignores.match(d)]

        for filename in filenames:
            # We want the path of the file, not its name
            path = os.path.join(dirpath, filename)

            # That path must be relative to the root, not absolute
            path = os.path.relpath(path, root_path)

            if ignores.match(filename):
                if save_ignored_paths:
                    ignored.append(path)
                continue
            else:
                paths.append(path)

    return paths, ignored


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
