# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
This file adopts the suggestions of [Keep a CHANGELOG](http://keepachangelog.com);
GNU would call this file `NEWS.md`.

## [1.1.0] - 2016-05-01

With this release, we now write the updated index as a new file and archive
(rename into a subdir in the repo) the old one, instead of overwriting the
index.

### Added
- [#10](https://github.com/mcgid/morenines/issues/10): `add` and `remove`
  commands, to replace the `update` command. These allow you to tell morenines
  which specific paths you want to track in the repository, instead of the
  all-or-nothing of `update`.
- [#2](https://github.com/mcgid/morenines/issues/2): `help` command. Since we
  already look an awful lot like Git, this will smooth things over when
  someone is trying to figure out usage.

### Removed
- [#4](https://github.com/mcgid/morenines/issues/4): the `create` command; it's
  redundant given the `init` command.

### Changed
- [#8](https://github.com/mcgid/morenines/issues/8): `add`, `remove`, `status`
  and `edit-ignores` commands must be run inside a repository now. This allows
  the first three to accept path arguments that act on specific files in the
  repository tree. The old method was from the time before repositories, in the
  flexible but messy just-pass-an-index-file-path days.

## [1.0.1] - 2016-04-15
### Fixed
- [#1](https://github.com/mcgid/morenines/issues/1): Fix exceptions on Python
  3.x due to use of `dict.iter_()` in version 1.0.0

## [1.0.0] - 2016-04-15 [YANKED]
### Added
- Initial version


[1.1.0]: https://github.com/mcgid/morenines/compare/1.0.1...1.1.0
[1.0.1]: https://github.com/mcgid/morenines/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/mcgid/morenines/releases/tag/1.0.0
