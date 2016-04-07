# To-Do

# 1.0.0

## Final Changes

- [x] Fix bug: update does not overwrite the index file it read
    - [x] Add the detected `index_path` to the context object
    - [x] Make update base its decision based on the index path
- [x] Centralize default file names for .mnindex and .mnignore

## Administration

- [ ] Remove existing git tags
- [ ] Tag for release

## Documentation
- [x] Add (click) help text for each command
- [x] Update README.md
    - [x] with new text

## Packaging and Shipping
- [x] Finish writing setup.py
- [ ] Publish to PyPI
    - [x] Look up how to do this again
    - [x] Write `DESCRIPTION.rst`
    - [ ] Test whether package can be installed


# POSTPONED
- [ ] Update README.md
    - [ ] with a simple class diagram
- [ ] Write Sphinx documentation
    - [ ] for commands
    - [ ] for Index/Ignores
    - [ ] for output and util
    - [ ] for modules


# Post-1.0.0 New Features and Changes

## Good Citizenship

- [ ] Move code [into `src` dir][1]
- [ ] Start using tox
- [ ] Consider using Sphinx

1: https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure

## General

- [ ] Add --all option to status (to print each file in index with its status)
- [ ] Add --all option to verify (would this print out the hash for each file
      as they're traversed?)
- [ ] Review variable names again
- [ ] Convert `@common_params()` to separate decorators for each param, to make
      it more obvious which ones are being used?
- [ ] Create `util.abort()` or something, to centralize failure exiting?
- [ ] Rename `get_new_and_missing()` because ew
- [ ] Make output consistent and logical across commands
    - [ ] Use logging (or something) to record all state and decisions: found
          files, selected options (via command line, config file, program
          default, etc.)
    - [ ] Add -q|--quiet options
    - [ ] Set sane defaults for output

## Things related to configuration

The way things are configured right now (`get_context()`) is essentially
haphazard, and not terribly well-planned. A handful of functions accept a
`config` object, others don't, and there's not a lot of consistency. This needs
to be consistent and reliable if the whole thing isn't going to fall in on
itself.

- [ ] Figure out a comprehensive way to structure configuration and state
    - [ ] Separate Index headers from files? So that headers like `root_path`
          get pulled out and kept in a single config object?
    - [ ] Find some way to make default config values guaranteed?
- [ ] Move MNContext, Index and Ignores to a single file (e.g. model.py? context.py?)
- [ ] Move `get_context()`, `get_index()`, `get_ignores` to util.py?
- [ ] Do a better job of dealing with file writing in create and update
      commands? Including rewriting 'path/to/-' to just '-', to facilitate
      writing to stdout
- [ ] Rethink the interaction between `find_file()`, `get_ignores()`, etc -- it
      seems like the current structure is somewhat haphazard. Does it need a
      Repo class or something to manage things in an objecty way?

### UPDATE

It looks like a Repository class, and having the universal `<repo_path>`
parameter to all commands, is the way to go. Simplifies a lot of things.

Further analysis is in the (private) `design/PLANS.txt` file.

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
