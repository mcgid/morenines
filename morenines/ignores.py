import os
from fnmatch import fnmatchcase

class Ignores(object):
    @classmethod
    def read(cls, stream):
        ignores = cls()

        for line in stream:
            ignores.patterns.append(line.strip())

        return ignores
    
    def __init__(self):
        self.patterns = []

    def match(self, path):
        filename = os.path.basename(path)

        if any(fnmatchcase(filename, pattern) for pattern in self.patterns):
            return True
        else:
            return False
