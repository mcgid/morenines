import os

from morenines.index import Index
from morenines.util import get_files, get_hash

def create(root_path):
    index = Index(root_path)

    files = get_files(root_path)

    for path in files:
        # To hash the file, we need its absolute path
        abs_path = os.path.join(root_path, path)

        hash_ = get_hash(abs_path)

        # We store the relative path in the index
        index.add(path, hash_)

    return index
