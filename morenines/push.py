import morenines.remote as remote
from morenines.index import Index

def push(root_path, index_file, remotes):
    # XXX: DO SANITY CHECK: run a local status() check

    for remote in remotes:
        remote_blobs = remote.get_blob_list()

        index = Index.read(index_file)

        files_to_upload = []

        for path, hash_ in index.files.iteritems():
            if hash_ not in remote_blobs:
                files_to_upload.append(path)

        for path in files_to_upload:
            remote.upload(path)
