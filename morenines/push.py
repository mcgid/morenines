import morenines.remote as remote
from morenines.index import Index

def push(root_path, index_path, remotes):
    # XXX: DO SANITY CHECK: run a local status() check

    for remote in remotes:
        remote_blobs = remote.get_blob_list()

        index = Index(root_path)

        index.read(index_path)

        files_to_upload = []

        for path, hash_ in index.files.iteritems():
            if hash_ not in remote_blobs:
                files_to_upload.append(path)

        for path in files_to_upload:
            remote.upload(path)
