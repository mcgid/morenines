import os
import collections
import datetime
import itertools


class Index(object):
    def __init__(self, root_path):
        self.headers = collections.OrderedDict()
        self.files = collections.OrderedDict()

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


class IndexParser():
    def __init__(self):
        self.preamble = {
            'version': "1",
        }

    def read(self, path):
        index = Index(path)

        with open(path, 'r') as f:
            version = parse_preamble(f)

            if version != self.preamble['version']:
                raise Exception("Incorrect IndexParser for file: {} (version {} parser required)".format(path, version))

            index.headers = parse_headers(f)
            index.files = parse_files(f)

        return index

    def write(self, index, file_handle):
        # The date header is the moment the index is written to disk
        index.headers['date'] = datetime.datetime.utcnow().isoformat()

        # The preamble is at the start of the file, to identify and version the
        # file format
        # TODO: make IndexParser just read the preamble, and then call another
        # version-specific class according to the version in the preamble
        for key, value in self.preamble.iteritems():
            file_handle.write("{}: {}\n".format(key, value))

        for line in index.itercontent():
            file_handle.write(line)


##############################
# Index file parsing functions
##############################

def parse_preamble(file_):
    version_line = file_.readline()

    version_key, version_value = [e.strip() for e in version_line.split(':', 1)]

    if version_key != 'version' or version_value == '':
        raise Exception("Invalid file format: invalid preamble (no version)")

    return version_value

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
