import os
import collections
import datetime
import itertools


class Index(object):
    version = 1

    def __init__(self, root_path):
        self.headers = collections.OrderedDict()
        self.files = collections.OrderedDict()

        # Default to version in class; if reading file, this will get overwritten
        self.headers['version'] = Index.version
        self.headers['root_path'] = root_path

    def itercontent(self):
        """Return an iterator over the content,
        converted to strings for writing to disk"""

        header_strings = ("{}: {}\n".format(k, v) for k, v in self.headers.iteritems())
        separator = ("\n",)
        file_strings = ("{} {}\n".format(hash_, path) for path, hash_ in self.files.iteritems())

        return itertools.chain(header_strings, separator, file_strings)

    def add(self, path, hash_):
        self.files[path] = hash_

    def remove(self, path):
        del self.files[path]

    def read(self, path):
        with open(path, 'r') as f:
            self.headers = parse_headers(f)

            if 'version' not in self.headers:
                raise Exception("Invalid file format: no version header")

            if self.headers['version'] != str(Index.version):
                raise Exception("Unsupported file format version: file is {}, parser is {}".format(self.headers['version'], Index.version))

            self.files = parse_files(f)

    def write(self, file_handle):
        # The date header is the moment the index is written to disk
        self.headers['date'] = datetime.datetime.utcnow().isoformat()

        # Write headers -- but sort the keys before writing
        for key in sorted(self.headers):
            file_handle.write("{}: {}\n".format(key, self.headers[key]))

        # Separate the headers from the files list with a blank line
        file_handle.write("\n")

        # Write files and hashes -- but sort the paths before writing
        for path in sorted(self.files):
            file_handle.write("{} {}\n".format(self.files[path], path))


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
