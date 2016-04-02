import os
import collections
import datetime
import click

from morenines.util import get_hash, find_file
from morenines.output import error


class Index(object):
    reader_version = 1

    @classmethod
    def _check_version(cls, headers):
        try:
            version = headers['version']
        except KeyError as e:
            missing_key = e.args[0]
            raise Exception("Invalid file format: missing required header '{}'".format(missing_key))

        if version != str(cls.reader_version):
            raise Exception("Unsupported file format version: file is {}, parser is {}".format(version, cls.reader_version))

    @classmethod
    def read(cls, path):
        if not path:
            path = find_file('.mnindex')

            if not path:
                error("Cannot find index file '.mnindex' in this or any parent dir")
                # XXX XXX TODO write util.abort() or something, to exit centrally
                import sys
                sys.exit(1)

        with click.open_file(path, 'r') as stream:
            headers = parse_headers(stream)

            cls._check_version(headers)

            index = cls(headers['root_path'])

            if 'ignores_file' in headers:
                index.ignores_file = headers['ignores_file']

            index.files = parse_files(stream)

            return index

    def __init__(self, root_path, ignores_file=None):
        self.root_path = root_path
        self.ignores_file = ignores_file
        self.files = collections.OrderedDict()

    def add(self, paths):
        for path in paths:
            # To hash the file, we need its absolute path
            abs_path = os.path.join(self.root_path, path)

            # We store the relative path in the index, not the absolute
            self.files[path] = get_hash(abs_path)

    def remove(self, paths):
        for path in paths:
            del self.files[path]

    def write(self, stream):
        headers = [
            ('version', self.reader_version),
            ('root_path', self.root_path),
            ('date', datetime.datetime.utcnow().isoformat()),
        ]

        if self.ignores_file:
            headers.append(('ignores_file', self.ignores_file))

        for key, value in headers:
            stream.write("{}: {}\n".format(key, value))

        # Separate the headers from the files list with a blank line
        stream.write("\n")

        # Write files and hashes -- but sort the paths before writing
        for path in sorted(self.files):
            stream.write("{} {}\n".format(self.files[path], path))


##############################
# Index file parsing functions
##############################

def split_lines(lines, delim, num_fields):
    """Split each element in the sequence 'lines' into its component fields."""
    for line in lines:
        if line == '\n':
            return

        yield [field.strip() for field in line.split(delim, num_fields - 1)]

def parse_headers(file_):
    """Parse header lines of the form 'key: value'"""
    return {key: value for key, value in split_lines(file_, ':', 2)}

def parse_files(file_):
    """Parse file lines of the form 'HASHVALUE /path/to/file"""
    return {path:hash_ for hash_, path in split_lines(file_, ' ', 2)}
