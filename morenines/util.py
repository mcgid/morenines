import os
import hashlib

from fnmatch import fnmatchcase


def get_files(root_path):
    paths = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            # We want the path of the file, not its name
            path = os.path.join(dirpath, filename)

            # That path must be relative to the root, not absolute
            path = os.path.relpath(path, root_path)

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


def get_new_and_missing(path, index):
    current_files = get_files(path)

    new_files = [path for path in current_files if path not in index.files]

    missing_files = [path for path in index.files.iterkeys() if path not in current_files]

    return new_files, missing_files


def filter_ignores(files, ignores):
    included_files = []
    ignored_files = []

    for f in files:
        if any(fnmatchcase(os.path.basename(f), pattern) for pattern in ignores):
            ignored_files.append(f)
        else:
            included_files.append(f)

    return included_files, ignored_files
