import os

from morenines import output
from morenines import util

from morenines.index import Index
from morenines.ignores import Ignores


NAMES = {
    'mn_dir': '.morenines',
    'index': 'index',
    'ignore': 'ignore',
}


class Repository(object):
    def __init__(self):
        self.path = None
        self.index = None
        self.ignore = None

    def init_paths(self, repo_path):
        self.path = repo_path
        self.mn_dir_path = os.path.join(self.path, NAMES['mn_dir'])
        self.index_path = os.path.join(self.mn_dir_path, NAMES['index'])
        self.ignore_path = os.path.join(self.mn_dir_path, NAMES['ignore'])

    def open(self, path):
        repo_path = find_repo(path)

        if not repo_path:
            output.error("Cannot find repository in '{}' or any parent dir".format(path))
            util.abort()

        self.init_paths(repo_path)

        if os.path.isfile(self.index_path):
            self.index = Index.read(self.index_path)
        else:
            self.index = Index(self.path)

        if os.path.isfile(self.ignore_path):
            self.ignore = Ignores.read(self.ignore_path)
        else:
            self.ignore = Ignores()


def find_repo(start_path):
    if start_path == '/':
        return None

    mn_dir_path = os.path.join(start_path, NAMES['mn_dir'])

    if os.path.isdir(mn_dir_path):
        return start_path

    parent = os.path.split(start_path)[0]

    return find_repo(parent)
