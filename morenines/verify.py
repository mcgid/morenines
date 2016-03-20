import os

from morenines.index import Index
from morenines.util import get_files, get_hash

def verify(root_path, index_path):
    index = Index(root_path)

    index.read(index_path)

    current_files = get_files(root_path)

    changed_files = []

    missing_files = []

    for path, old_hash in index.files.iteritems():
        if path not in current_files:
            missing_files.append(path)
            continue

        current_hash = get_hash(os.path.join(root_path, path))

        if current_hash != old_hash:
            changed_files.append(path)


    new_files = [path for path in current_files if path not in index.files]

    print_files("New Files", new_files)
    print_files("Changed Files", changed_files)
    print_files("Missing Files", missing_files)


def print_files(name, files):
    print "{}:".format(name)

    for path in files:
        print "  {}".format(path)
