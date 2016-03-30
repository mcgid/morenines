import os
import collections
import datetime

from morenines.util import get_hash


class Index(object):
    reader_version = 1

    def __init__(self, stream=None):
        self.headers = collections.OrderedDict()
        self.files = collections.OrderedDict()

        if stream:
            self.headers = parse_headers(stream)

            if 'version' not in self.headers:
                raise Exception("Invalid file format: no version header")

            if self.headers['version'] != str(self.reader_version):
                raise Exception("Unsupported file format version: file is {}, parser is {}".format(self.headers['version'], self.reader_version))

            self.files = parse_files(stream)
        else:
            self.headers['version'] = self.reader_version

    def add(self, paths):
        for path in paths:
            # To hash the file, we need its absolute path
            abs_path = os.path.join(self.headers['root_path'], path)

            # We store the relative path in the index, not the absolute
            self.files[path] = get_hash(abs_path)

    def remove(self, paths):
        for path in paths:
            del self.files[path]

    def write(self, stream):
        # The date header is the moment the index is written to disk
        self.headers['date'] = datetime.datetime.utcnow().isoformat()

        # Write headers -- but sort the keys before writing
        for key in sorted(self.headers):
            stream.write("{}: {}\n".format(key, self.headers[key]))

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
