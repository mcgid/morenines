import os

from morenines import output
from morenines import util

from morenines.index import Index
from morenines.ignores import Ignores


NAMES = {
    'repo_dir': '.morenines',
    'index': 'index',
    'ignore': 'ignore',
}


class Repository(object):
    def __init__(self):
        self.path = None
        self.index = None
        self.ignores = None

    def open(self, path):
        repo_dir_path = find_repo(path)

        if not repo_dir_path:
            output.error("Cannot find repository in '{}' or any parent dir".format(path))
            util.abort()

        self.path = repo_dir_path

        self.index = Index.read(os.path.join(self.path, NAMES['index']))

        self.ignores = Ignores.read(os.path.join(self.path, NAMES['ignore']))


def find_repo(start_path):
    if start_path == '/':
        return None

    path = os.path.join(start_path, NAMES['repo_dir'])

    if os.path.isdir(path):
        return path

    parent = os.path.split(start_path)[0]

    return find_repo(parent)
