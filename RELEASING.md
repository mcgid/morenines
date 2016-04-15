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
5. Merge changes from new branch into `dev` **as a merge commit, not a
   fast-forward** (see discussion after)

```bash
$ git checkout dev
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

1. Make necessary changes...

2. Go to previous phase, make another release candidate, test, rinse, repeat

### Make Final Release Version

1. Bump version number to `X.Y.Z` in `setup.py` **and ACTUALLY COMMIT this time**

2. Merge changes from `dev` into `master`

    ```bash
    $ git checkout master
    $ git merge --no-ff dev
    ```

3. Tag the release

    ```bash
    $ git tag X.Y.Z
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

- `master` holds full released versions
- `dev` is for:
    - collecting and preparing finished features, bug fixes
    - tooling and environment changes
    - project resource changes (README, etc.)
- separate feature and bugfix branches are for actual development and
  testing

There isn't one right way to do this, and this isn't an issue of dogma; if this
branching model starts to be a problem, we can do things differently. This is
just what we're doing for now.

### Merging

Merges from feature branches to `dev`, and from `dev` to `master`, are done as
`--no-ff` merges.  While these could be fast-forwards, for now, they're being
kept visible as separate merges.

There isn't one right way to do this, and this isn't an issue of dogma; if
`--no-ff` starts to be a problem, we can do things differently. This is just
what we're doing for now.

### Version Numbering

Versions follow the usual Semantic Versioning pattern of `X.Y.Z(rcN)`, where
`X` is usually backwards-incompatible, `Y` is major feature changes, `Z` is
bug/security/etc. fixes.

Versions don't start with a `v` prefix.
