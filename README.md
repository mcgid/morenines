# morenines: A simple content change detector

morenines hashes your files and, later, can tell you if they have changed.

## Usage

We have some files.

```bash
$ cd ~/photos
$ ls -1
DSC0001.jpg
DSC0002.jpg
notes.txt
TEMPFILE.dat
```

Let's track those files.

```bash
$ mn create
SUCCESS: Wrote index file /Users/example/photos/.mnindex
```

We'll make some changes, and then verify the index to see any changes.

```bash
$ rm TEMPFILE.dat
$ echo "lorem ipsum" >> notes.txt
$ touch a_new_file.txt
$ mn verify
New files (not in index):
  a_new_file.txt

Missing files:
  TEMPFILE.dat

Changed files (hash differs from index):
  notes.txt
```

## Full List of Options
```bash
$ mn  --help
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

  A tool to track whether the content of files has changed.

Options:
  --help  Show this message and exit.

Commands:
  create        Write a new index file
  edit-ignores  Open the ignores file in an editor
  init          Initialize a new morenines repository
  status        Show new, missing or ignored files
  update        Update an existing index file
```

```bash
$ mn create --help
Usage: __main__.py create [OPTIONS] [REPO_PATH]

  Write a new index file with the hashes of files under it.

Options:
  --help  Show this message and exit.
```

```bash
$ mn edit-ignores --help
Usage: __main__.py edit-ignores [OPTIONS] [REPO_PATH]

  Open an existing or a new ignores file in an editor.

Options:
  --help  Show this message and exit.
```

```bash
$ mn status --help
Usage: __main__.py status [OPTIONS] [REPO_PATH]

  Show any new files not in the index, index files that are missing, or
  ignored files.

Options:
  --color / --no-color          Enable/disable colorized output.
  -i, --ignored / --no-ignored  Enable/disable showing files ignored by the
                                ignores patterns.
  --verify / --no-verify        Re-hash all files in index and check for
                                changes
  --help                        Show this message and exit.
```

```bash
$ mn update --help
Usage: __main__.py update [OPTIONS] [REPO_PATH]

  Update an existing index file with new file hashes, missing files removed,
  etc.

Options:
  --add-new / --no-add-new        Hash and add any files that aren't in the
                                  index
  --remove-missing / --no-remove-missing
                                  Delete any the hashes of any files in the
                                  index that no longer exist.
  --help                          Show this message and exit.
```
