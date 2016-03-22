import os

import morenines.status

from morenines.index import Index
from morenines.util import get_files, get_hash


def update(root_path, index_path, remove_missing):
    index = Index(root_path)

    index.read(index_path)

    new_files, missing_files = morenines.status.status(root_path, index_path)

    for path in new_files:
        abs_path = os.path.join(root_path, path)

        hash_ = get_hash(abs_path)

        index.add(path, hash_)

    if remove_missing is True:
        for path in missing_files:
            index.remove(path)

    return index
