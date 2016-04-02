import os
from fnmatch import fnmatchcase
import click

from morenines.util import find_file


class Ignores(object):
    @classmethod
    def read(cls, path):
        if not path:
            path = find_file('.mnignore')

        ignores = cls()

        if path:
            with click.open_file(path, 'r') as stream:
                ignores.patterns = [line.strip() for line in stream]

        return ignores
    
    def __init__(self):
        self.patterns = []

    def match(self, path):
        filename = os.path.basename(path)

        if any(fnmatchcase(filename, pattern) for pattern in self.patterns):
            return True
        else:
            return False
