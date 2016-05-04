# morenines: A simple content change detector

morenines hashes your files and, later, can tell you if they have changed.

Much like Git, information about your files is stored in a **repository**, in
a hidden directory named `.morenines`.

To start using morenines, you initialize a repository and then add paths to it.
Later, you can verify that your files have not changed.

Morenines does not modify your files. It just tells you if they have changed.

## Short Usage

```bash
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
```

If you haven't edited it, a JPEG should not change. So now you know that you
need to restore `DSC0003.jpg` from a backup.

## Usage

#### Starting out

We have some files.

```bash
$ cd ~/photos
$ ls -1
DSC0001.jpg
DSC0002.jpg
TEMPFILE.dat
notes.txt
```

Let's track those files. First, initialize the repository:

```bash
$ mn init
SUCCESS: Initialized empty morenines repository in /home/mnuser/photos/.morenines
```

And then, add the files to the repository:

```bash
$ mn add DSC0001.jpg DSC0002.jpg TEMPFILE.dat notes.txt
SUCCESS: Files added to repository:
  DSC0001.jpg
  DSC0002.jpg
  TEMPFILE.dat
  notes.txt
```

#### Adding and removing files

Now the files are tracked in the repository by their content. We can get the
status of the repository:

```bash
$ mn status
Index is up-to-date (no changes)
```

If we add a file, we can then run `mn status` to see the change:

```bash
$ echo "a new file" > new_file.txt
$ mn status
New files (not in index):
  new_file.txt
```

We can add the new file:

```bash
$ mn add new_file.txt 
SUCCESS: Files added to repository:
  new_file.txt
```

Note that this **does not do anything to `new_file.txt`**; it merely reads
`new_file.txt`, computes information about it, and stores that information in
the repository.

We can also use `status` to seesee if a file is missing:

```bash
$ rm TEMPFILE.dat 
remove TEMPFILE.dat? y
$ mn status
Missing files:
  TEMPFILE.dat
```

If this is intentional, we can tell `morenines` to forget about that file:

```bash
$ mn remove TEMPFILE.dat
SUCCESS: Files removed from repository:
  TEMPFILE.dat
```

Note that this **does not do anything to `TEMPFILE.dat`**; it merely removes the
information about `TEMPFILE.dat` from the repository.

#### Detecting changed files

Here's the meat of it. We can use the `--verify` option of the `status` command
to re-hash the tracked files and see if their content has changed:

```bash
$ echo "some new content" >> notes.txt 
$ mn status
Index is up-to-date (no changes)
$ mn status --verify
Changed files (hash differs from index):
  notes.txt
```

Now you know that the content of `notes.txt` has changed. If this is
unexpected, you know that you need to restore `notes.txt` from a backup.

If it was expected, however, you can communicate this to morenines by using
`remove` and then `add` on that path:

```bash
$ mn remove notes.txt
SUCCESS: Files removed from repository:
  notes.txt
$ mn add notes.txt
SUCCESS: Files added to repository:
  notes.txt
```
