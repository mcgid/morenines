#   There would be a separate class for GCSRemote, AWSRemote, B2Remote, etc.
#
#   And then maybe a remotes.py module, which would have functions for
#   iterremotes() or something? That would let us just have a list of configured
#   remotes, and dump stuff up to them, doing it in parallel?
#
#   But that complexity will come later.
#

class FakeRemote(object):
    def __init__(self, config):
        pass

    def get_blob_list(self):
        return [
            '7631a5d4eecd9d7eab7b811f37a02300f057c54d',
            '4783859b6b834ba7807ee25b89ce7ae57eafd14e',
        ]

    def upload(self, path):
        print "Upload: {}".format(path)
        pass
