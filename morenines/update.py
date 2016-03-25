import os

import morenines.status

from morenines.index import Index
from morenines.util import get_files


def update(root_path, index_path, remove_missing):
    index = Index(root_path)

    index.read(index_path)

    new_files, missing_files = morenines.status.status(root_path, index_path)

    index.add(new_files)

    if remove_missing is True:
        index.remove(missing_files)

    return index
