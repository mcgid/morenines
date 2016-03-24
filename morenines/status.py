from morenines.index import Index
from morenines.util import get_files

def status(root_path, index_path):
    index = Index(root_path)

    index.read(index_path)

    return get_new_and_missing(root_path, index)
