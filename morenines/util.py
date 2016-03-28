import os
import hashlib


def get_files(index):
    paths = []

    for dirpath, dirnames, filenames in os.walk(index.headers['root_path']):
        # Remove ignored directories
        dirnames[:] = [d for d in dirnames if not index.ignores.match(d)]

        for filename in (f for f in filenames if not index.ignores.match(f)):
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


def get_new_and_missing(index):
    current_files = get_files(index)

    new_files = [path for path in current_files if path not in index.files]

    missing_files = [path for path in index.files.iterkeys() if path not in current_files]

    return new_files, missing_files
