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
$
```

We'll make some changes, and then check the verify the index.

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
Usage: mn [OPTIONS] COMMAND [ARGS]...

  A tool to track whether the content of files has changed.

Options:
  --help  Show this message and exit.

Commands:
  create        Write a new index file
  edit-ignores  Open the ignores file in an editor
  status        Show new, missing or ignored files
  update        Update an existing index file
  verify        Re-hash all index files to show any changes

$ mn create --help
Usage: mn create [OPTIONS] ROOT_PATH

  Write a new index file with the hashes of files under it.

Options:
  --ignores-file PATH  The path to an existing ignores file.
  -o, --output PATH    The path where the index file should be written.
  --help               Show this message and exit.

$ mn edit-ignores --help
Usage: mn edit-ignores [OPTIONS]

  Open an existing or a new ignores file in an editor.

Options:
  --ignores-file PATH  The path to an existing ignores file, or the path to
                       which a new ignores file should be written.
  --help               Show this message and exit.

$ mn status --help
Usage: mn status [OPTIONS] [INDEX_FILE]

  Show any new files not in the index, index files that are missing, or
  ignored files.

Options:
  --color / --no-color          Enable/disable colorized output.
  -i, --ignored / --no-ignored  Enable/disable showing files ignored by the
                                ignores patterns.
  --help                        Show this message and exit.

$ mn update --help
Usage: mn update [OPTIONS] [INDEX_FILE]

  Update an existing index file with new file hashes, missing files removed,
  etc.

Options:
  --remove-missing / --no-remove-missing
                                  Delete any the hashes of any files in the
                                  index that no longer exist.
  --new-root DIRECTORY            New location of the root directory.
  --new-ignores-file PATH         New location of the ignores file.
  -o, --output PATH               The path where the updated index file should
                                  be written.
  --help                          Show this message and exit.

$ mn verify --help
Usage: mn verify [OPTIONS] [INDEX_FILE]

  Re-hash all files in the index and compare the index and current
  checksums.

Options:
  --color / --no-color          Enable/disable colorized output.
  -i, --ignored / --no-ignored  Enable/disable showing files ignored by the
                                ignores patterns.
  --help                        Show this message and exit.
```
