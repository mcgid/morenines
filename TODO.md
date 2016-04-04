# To-Do

# 1.0.0

## Final Changes

- [ ] Centralize default file names for .mnindex and .mnignore

## Administration

- [ ] Remove existing git tags
- [ ] Finish writing setup.py
- [ ] Install and configure tox
- [ ] Install and configure Sphinx

## Documentation
- [ ] Add (click) help text for each command
- [ ] Write Sphinx documentation
    - [ ] for commands
    - [ ] for Index/Ignores
    - [ ] for output and util
    - [ ] for modules
- [ ] Update README.md
    - [ ] with new text
    - [ ] with a simple class diagram

## Packaging and Shipping
- [ ] Publish to PyPI
    - [ ] Look up how to do this again


# Post-1.0.0 New Features and Changes

- [ ] Add --all option to status (to print each file in index with its status)
- [ ] Add --all option to verify (would this print out the hash for each file
      as they're traversed?)
- [ ] Review variable names again
- [ ] Move MNContext, Index and Ignores to a single file (e.g. model.py? context.py?)
- [ ] Convert `@common_params()` to separate decorators for each param, to make
      it more obvious which ones are being used?
- [ ] Move `get_context()`, `get_index()`, `get_ignores` to util.py?
- [ ] Create `util.abort()` or something, to centralize failure exiting?
- [ ] Do a better job of dealing with file writing in create and update
      commands? Including rewriting 'path/to/-' to just '-', to facilitate
      writing to stdout
- [ ] Rename `get_new_and_missing()` because ew
- [ ] Rethink the interaction between `find_file()`, `get_ignores()`, etc -- it
      seems like the current structure is somewhat haphazard. Does it need a
      Repo class or something to manage things in an objecty way?

---

# Future Ideas

## Add `push` command
1. Get list of blobs from remote
2. Open index file
3. For path in index, if hash not in remote blobs: add path to upload list
4. For path in upload list, [GCS: generate md5], upload [with md5]


## Add `pull` command

Download a file from the primary configured remote.

1. Look up `<path>` in index to get the desired `hash`
2. Ask remote for blob for key `hash`
3. Write blob to temp file using `<hash>.download` as its name
    - Where to store temp file? In `root_path`? In `dirname(<path>)`?
3. Rename current `<path>` (if present) to `<path>.old`, and `<hash>.download`

Possible names:

``` bash
$ mn pull <path>     # Bad?: not the same arguments or semantics to "mn push"
$ mn download <path>
$ mn fetch <path>
```

## Add `config` file and command

Similar to `git config`. Most immediate use: writing configuration info for
remote blob storage.


## Check file perms are read-only during `verify`


## Add special status/verify error message for when all indexed files are missing

If everything's gone, the index file might have been moved. So the error
message could include something like, '(All files are missing; was the index
file moved?)'


## Hash chunks of files
Support for hashing only chunks of large files - e.g. verify each 100MB or
1GB of a 10GB separately, so any corruption would only require a chunk-sized
download.

Problems:

- Writing just one chunk to a file seems like a deceiptively tricky problem,
  and could completely corrupt the file.
- In general I'm trying to do things atomically (like renaming files in two
  stages, instead of overwriting them). This is the opposite of that.
