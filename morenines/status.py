from morenines.index import Index
from morenines.util import get_files

def status(root_path, index_file):
    index = Index(root_path)

    index.read(index_file)

    return get_new_and_missing(root_path, index)
