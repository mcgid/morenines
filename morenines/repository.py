import os
import errno

from morenines import output
from morenines import util

from morenines.index import Index
from morenines.ignores import Ignores


NAMES = {
    'mn_dir': '.morenines',
    'index': 'index',
    'ignore': 'ignore',
    'new_index': 'new_index',
    'index_archive_dir': 'indexes',
}

DEFAULT_IGNORE_PATTERNS = [
    NAMES['mn_dir'],
]

class Repository(object):
    # Since click will try to instantiate this class for us with no args, we
    # put the __init__ code here instead
    def init(self, path):
        self.path = path
        self.index = Index(path)
        self.ignore = Ignores(DEFAULT_IGNORE_PATTERNS)

        # Other paths
        self.mn_dir_path = os.path.join(self.path, NAMES['mn_dir'])
        self.index_path = os.path.join(self.mn_dir_path, NAMES['index'])
        self.ignore_path = os.path.join(self.mn_dir_path, NAMES['ignore'])
        self.new_index_path = os.path.join(self.mn_dir_path, NAMES['new_index'])
        self.index_archive_dir = os.path.join(self.mn_dir_path, NAMES['index_archive_dir'])


    def create(self, path):
        repo_path = find_repo(path)

        if repo_path:
            output.error("Repository already exists: {}".format(repo_path))
            util.abort()

        self.init(path)

        os.mkdir(self.mn_dir_path)

        # Write an empty index file as a starter
        with open(self.index_path, 'w') as stream:
            self.index.write(stream)


    def open(self, path):
        if not os.path.exists(path):
            output.error("Repository path does not exist: {}".format(path))
            util.abort()
        elif not os.path.isdir(path):
            output.error("Repository path is not a directory: {}".format(path))
            util.abort()

        repo_path = find_repo(path)

        if not repo_path:
            output.error("Cannot find repository in '{}' or any parent dir".format(path))
            util.abort()

        self.init(repo_path)

        if os.path.isfile(self.index_path):
            self.index.read(self.index_path)

        if os.path.isfile(self.ignore_path):
            self.ignore.read(self.ignore_path)


    def normalize_paths(self, paths):
        """Make paths relative to the repo root.

        If a path is not a descendant of the repo root, raise an exception.
        """
        rel_paths = []

        for path in paths:
            # Remove any relative path weirdness
            path = os.path.abspath(path)

            if not path.startswith(self.path):
                output.error("Path not in repository: {}".format(path))
                util.abort()

            rel_paths.append(os.path.relpath(path, self.path))

        return rel_paths


    def expand_subdirs(self, paths):
        dirs = [p for p in paths if os.path.isdir(p)]

        not_dirs = [p for p in paths if p not in dirs]

        for root in dirs:
            for dir_path, dir_names, file_names in os.walk(root):
                # Assign dir_names in place with [:] so that os.walk doesn't traverse ignored dirs
                dir_names[:] = [d for d in dir_names if not self.ignores.match(d)]

                file_names = [f for f in file_names if not self.ignores.match(f)]
                file_paths = [os.path.join(dir_path, f) for f in file_names]

                not_dirs.extend(self.normalize_paths(file_paths))

        return not_dirs


    def expand_subdirs_from_index(self, paths):
        """Return the list of paths with directories replaced by all of their descendent
        children that are in the index.
        """
        dirs = [p for p in paths if os.path.isdir(p)]

        not_dirs = [p for p in paths if p not in dirs]

        for root in dirs:
            not_dirs.extend([path for path in self.index.files if path.startswith(root)])

        return not_dirs


    def add(self, paths):
        add_to_index = []

        for path in paths:
            if os.path.isdir(path):
                subdir_paths, ignored_subdir_paths = util.get_files(path, self.ignore, True)
                self.add(subdir_paths)
            elif not os.path.exists:
                output.error("Path does not exist: {}".format(path))
                util.abort()

            if path in self.index.files:
                continue

            add_to_index.append(path)

        self.index.add(add_to_index)


    def remove(self, paths):
        self.index.remove(paths)


    def write_index(self):
        """Rename the old index file and write the new one
        """
        self.check_index_sanity()

        # Figure out what we're going to rename the current index file to
        # We need to put this in the 'parent' header of the new index, so we
        # figure this out before we do anything
        archived_parent_name = self.get_archived_parent_name()

        self.index.parent = archived_parent_name

        # Write the new index
        with open(self.new_index_path, 'w') as new_index_stream:
            self.index.write(new_index_stream)

        self.archive_current_index(archived_parent_name)

        # Rename the new index file to be the current index
        try:
            os.rename(self.new_index_path, self.index_path)
        except OSError as e:
            output.error("Could not rename new index from {} to {}".format(self.new_index_path, self.index_path))
            util.abort()


    def check_index_sanity(self):
        """Try to ensure that the current repository state is expected and sensible.
        """

        if not os.path.isfile(self.index_path) and os.path.isfile(self.new_index_path):
            output.error("No current index file exists: {}".format(self.index_path))
            output.error("A new temporary index file exists, however: {}".format(self.new_index_path))
            output.error("To fix this problem, rename the newest valid index file (possibly the one listed above) to {}".format(self.index_path))
            output.error("(You may have to reattempt the last add or remove command)")

            util.abort()

        if os.path.isfile(self.new_index_path):
            output.error("A new temporary index file already exists: {}".format(self.new_index_path))

            output.error("To fix this problem, move this temporary index file out of its directory")
            output.error("(You may have to reattempt the last add or remove command)")

            util.abort()


    def archive_current_index(self, archived_name):
        # Get the path we're renaming the current index to
        archived_path = os.path.join(self.index_archive_dir, archived_name)

        # Create the index archive dir if possible - EAFP
        try:
            os.mkdir(self.index_archive_dir)
        except OSError as e:
            # When the dir already exists, ignore the exception
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

        # Archive the current index by renaming it into the archive dir
        try:
            os.rename(self.index_path, archived_path)
        except OSError as e:
            output.error("Could not rename current index from {} to {}".format(self.index_path, old_index_dest_path))
            output.error("(Does the latter already exist?)")
            util.abort()


    def get_archived_parent_name(self):
        old_index = Index(self.path)

        old_index.read(self.index_path)

        return "{}-{}".format(NAMES['index'], old_index.date)


def find_repo(start_path):
    if start_path == '/':
        return None

    mn_dir_path = os.path.join(start_path, NAMES['mn_dir'])

    if os.path.isdir(mn_dir_path):
        return start_path

    parent = os.path.split(start_path)[0]

    return find_repo(parent)
