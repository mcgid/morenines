import os

import morenines.status

from morenines.index import Index
from morenines.util import get_files


def update(root_path, index_file, remove_missing):
    index = Index.read(index_file)

    new_files, missing_files = morenines.status.status(root_path, index_file)

    index.add(new_files)

    if remove_missing is True:
        index.remove(missing_files)

    return index
