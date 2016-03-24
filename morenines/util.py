import os
import hashlib
import sys
import errno


def get_files(root_path):
    paths = []

    if not os.path.exists(root_path) or not os.path.isdir(root_path):
        print IOError(errno.ENOENT, os.strerror(errno.ENOENT), root_path)
        sys.exit(1)

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            # We want the path of the file, not its name
            path = os.path.join(dirpath, filename)

            # That path must be relative to the root, not absolute
            path = os.path.relpath(path, root_path)

            paths.append(path)

    return paths

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
