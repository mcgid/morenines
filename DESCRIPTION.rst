morenines: A simple content change detector
===========================================

``morenines`` hashes your files and, later, can tell you if they have changed.

Much like Git, information about your files is stored in a **repository**, in
a hidden directory named ``.morenines``.

To start using morenines, you initialize a repository and then add paths to it.
Later, you can verify that your files have not changed.

Morenines does not modify your files. It just tells you if they have changed.

Short Usage
-----------

This is a brief demonstration of how you would use ``morenines``::

    $ cd ~/photos
    $ mn init .
    SUCCESS: Initialized empty morenines repository in /home/mnuser/photos/.morenines
    $ mn add 2016/camping_trip
    SUCCESS: Files added to repository:
      2016/camping_trip/DSC0003.jpg
      2016/camping_trip/DSC0003.jpg
      2016/camping_trip/DSC0003.jpg

    # (time passes...)
    $ mn status --verify
    Changed files (hash differs from index):
      2016/camping_trip/DSC0003.jpg

If you haven't edited it, a JPEG should not change. So now you know that you
need to restore `DSC0003.jpg` from a backup.

You can find more details and a longer explanation on the `project page`_.

.. _project page: https://github.com/mcgid/morenines
