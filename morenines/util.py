import os
import hashlib

from morenines.ignores import Ignores


def get_files(index, ignores=None):
    paths = []

    for dirpath, dirnames, filenames in os.walk(index.headers['root_path']):
        if ignores:
            # Remove ignored directories
            dirnames[:] = [d for d in dirnames if not ignores.match(d)]

        for filename in filenames:
            if ignores and ignores.match(filename):
                continue

            # We want the path of the file, not its name
            path = os.path.join(dirpath, filename)

            # That path must be relative to the root, not absolute
            path = os.path.relpath(path, index.headers['root_path'])

            paths.append(path)

    return paths


def get_ignores(ignores_path):
    with open(ignores_path, 'r') as ignores_file:
        ignores = [line.strip() for line in ignores_file]

    return ignores


def get_hash(path):
    h = hashlib.sha1()

    with open(path, 'rb') as f:
        h.update(f.read())

    return h.hexdigest()


def get_new_and_missing(index, include_ignored=False):
    ignores = None

    if not include_ignored and 'ignores_file' in index.headers:
        with open(index.headers['ignores_file'], 'r') as f:
            ignores = Ignores.read(f)

    current_files = get_files(index, ignores)

    new_files = [path for path in current_files if path not in index.files]

    missing_files = [path for path in index.files.iterkeys() if path not in current_files]

    if ignores:
        ignored_files = [path for path in new_files if not ignores.match(path)]
    else:
        ignored_files = []

    return new_files, missing_files, ignored_files
