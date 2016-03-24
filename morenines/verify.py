import os

import morenines.status

from morenines.index import Index
from morenines.util import get_files, get_hash

def verify(root_path, index_path):
    index = Index(root_path)

    index.read(index_path)

    new_files, missing_files = morenines.util.get_new_and_missing(root_path, index)

    changed_files = []

    for path, old_hash in index.files.iteritems():
        if path in missing_files:
            continue

        current_hash = get_hash(os.path.join(root_path, path))

        if current_hash != old_hash:
            changed_files.append(path)

    return changed_files, missing_files
