import os

from morenines.index import Index
from morenines.util import get_files

def create(root_path):
    index = Index(root_path)

    files = get_files(root_path)

    index.add(files)

    return index
