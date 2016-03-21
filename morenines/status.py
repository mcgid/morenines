from morenines.index import Index
from morenines.util import get_files

def status(root_path, index_path):
    index = Index(root_path)

    index.read(index_path)

    current_files = get_files(root_path)

    new_files = [path for path in current_files if path not in index.files]
    
    missing_files = [path for path in index.files.iterkeys() if path not in current_files]

    return new_files, missing_files
