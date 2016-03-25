import os

from morenines.index import Index
from morenines.util import get_files, get_new_and_missing


def update(root_path, index_file, remove_missing):
    index = Index.read(index_file)

    new_files, missing_files = get_new_and_missing(root_path, index)

    index.add(new_files)

    if remove_missing is True:
        index.remove(missing_files)

    return index
