# To-Do

## 0.0.1

Add:

- `mn list-tree`
- `mn status`

## Unassigned

Add:

- Definition of files and dirs in .morenines directory:
    - file structure?
        - How to track the directory trees over time?
        - Save the trees as header + file list and name as SHA-1? (like object
          files in git? except only saving tree files?)

    - file names: index? objects? trees?

    - The file format could be informed heavily by the git index file format,
      using the lessons git learned
        - This may be too heavyweight, though: readable text files that are
          slower to process are more desirable than inscrutable, highly
          efficient binary formats (at least, for now)

    Problems:
        - Will this support for file permissions, uid/gid, other stat(2) info?
            - The required info to perfectly recreate a file varies by platform:
              OS X requires xattr(1) extended attributes, and who knows what
              Windows requires.

            - This is a problem for the future.

        - This is already looking very similar to git, except it won't work
          exactly the same.

        - Will there be a `commit` verb? Or will `add`, `delete`, etc.
          immediately create a new treelist, and point the "HEAD" file to it?
          This could result in a LOT of treelists if files are specified
          individually. Particularly if another script calls those verbs for
          some reason.

    See:
        - https://git.io/v2STO

- `morenines init <path>`
  create:
    .morenines/
        HEAD
        config
        ...?
        index? (Put the file lists in the objects dir instead?)
        objects/ ? (Maybe better named 'trees' or something?)

- `morenines add <path> [<path> ...]`
    1. for each file `<path>` hash it (collect them into a temp file list?)
    2. for each directory `<path>`, generate current file list with that path
    3. for each file in each file list in 2., hash it
    4. gather all file hashes and create a new index/tree/whatever file
    5. update the 'HEAD' (or whatever) file

- `morenines status`
    1. generate current file list with path `<root_dir>`
    2. diff stored file list and current file list
    3. print

- `morenines remove` or `morenines delete` or `morenines rm` or whatever (probably `remove`)

- `morenines push`
    - Upload to configured remote

- `morenines pull <path>` or `morenines download <path>` or `morenines fetch <path>` or
  something (probably not "pull", since push/pull args would be asymmetrical)
    - Download a file ("path") from the primary configured remote

- `morenines config <something>`
    - Update the `config` file with whatever settings
    - Most importantly: the config info for `[remote]` key-value stores

- `morenines report` (or something)
    - subcommand that completely re-hashes all tracked files and compares the
    results to the stored hashes. Include per-file unmodified/modified info for
    each file in addition to `status` output. (I.e.  `report` output is a
    strict superset of `status` output.

- "plumbing" subcommands for use by "porcelain" commands:
    - `list-tree`: lists files in a directory tree
    - `hash-tree`: hashes everything in a directory tree

- `setup.py` file


## Future Ideas


    See:
        - https://git.io/v2STO


- Support for hashing only chunks of large files - e.g. verify each 100MB or
  1GB of a 10GB separately, so any corruption would only require a chunk-sized
  download.

    Problems:
        - Writing just one chunk to a file seems like a deceiptively tricky
          problem, and could completely corrupt the file.
