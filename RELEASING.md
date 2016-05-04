# Releasing

This will walk through the process of cutting a new release of the project. It
is divided into phases, each of which has a number of steps.

Discsusion about particular decisions follows afterwards.

## Phases

### Make Code Changes

1. Create a new feature/bugfix branch

```bash
$ git checkout -b new_branch
```

2. Edit files and commit until done/fixed
3. Run tests with tox
4. Run coverage with cov.sh


### Update Master and Merge

1. Update `master`

```bash
$ git checkout master
$ git fetch origin
$ git diff master origin/master
$ git merge origin/master
```

2. Rebase the feature branch onto the tip of `master` (see discussion after)

```bash
$ git checkout new_branch
$ git rebase master
```

3. Merge changes from new branch into `master` **as a merge commit, not a
   fast-forward** (see discussion after)

```bash
$ git checkout master
$ git merge --no-ff new_branch
```

### Update Project Resources

1. Update as necessary and commit separately:

   - `CHANGELOG.md`
   - `README.md`
   - `DESCRIPTION.rst`
   - etc.

### Make Release Candidate Version

1. Bump version number to `X.Y.Zrc1` in `setup.py`; **do NOT commit**

2. Build `X.Y.Zrc1`

    ```bash
    $ python setup.py sdist bdist_wheel
    ```

3. If necessary: re-register project with PyPI test server

    ```bash
    $ python setup.py register -r test
    ```

4. Upload `X.Y.Zrc1` to test PyPI server

    ```bash
    $ twine upload -r test dist/morenines-X.Y.Zrc1*
    ```

5. Test install and/or upgrade of `X.Y.Zrc1` in a test virtualenv

    ```bash
    $ pip install --pre [--upgrade] --extra-index-url https://testpypi.python.org/pypi morenines
    ```

### Fix Any Problems with Release Candidate Version

1. Make necessary changes.

2. Go to previous phase, make another release candidate, test, rinse, repeat

### Make Final Release Version

1. Bump version number to `X.Y.Z` in `setup.py` **and ACTUALLY COMMIT this time**

2. Tag the release

    ```bash
    $ git tag X.Y.Z
    ```

3. Push `master` and the new tag

    ```bash
    $ git push origin master
    $ git push --tags
    ```

4. Build final release version

    ```bash
    $ python setup.py sdist bdist_wheel
    ```

5. Upload final release version

    ```bash
    $ twine upload dist/morenines-X.Y.Z.tar.gz dist/morenines-X.Y.Z-py2.py3-none-any.whl
    ```

Note that we do not specify `dist/morenines-X.Y.Z*` because that would upload the `X.Y.ZrcN` versions.

## Discussion

### Branching

In this project:

- feature branches contain:
    - new features, changes, improvements and bug fixes that are:
    - non-trivial, cohesive code changes that exist as a logical atomic changeset
- `master` contains:
    - tagged release versions
    - feature branch merge commits
    - reasonably small bug fixes/typo fixes/etc. commits
    - tooling and environment change commits
    - project resource changes (README, etc.)

There isn't one right way to do this, and this isn't an issue of dogma; if this
branching model starts to be a problem, we can do things differently. This is
just what we're doing for now.

### Rebasing

We use rebase for local, non-shared work, following the standard dogma about
not modifying published history. It is cleaner to rebase feature branches onto
the tip of master and resolving any resulting issues before pushing.

### Merging

Merges from feature branches to `master` are done as `--no-ff` merges.  While
these could be fast-forwards, for now, they're being kept visible as separate
merges. This is both to make it obvious where the development occurred, instead
of it springing forth Athena-like, as well as to make the progression in the
feature branch obvious.

There isn't one right way to do this, and this isn't an issue of dogma; if
`--no-ff` starts to be a problem, we can do things differently. This is just
what we're doing for now.

### Version Numbering

Versions follow the usual Semantic Versioning pattern of `X.Y.Z(rcN)`, where
`X` is usually backwards-incompatible, `Y` is major feature changes, `Z` is
bug/security/etc. fixes.

Versions don't start with a `v` prefix.
