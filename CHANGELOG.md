# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- n/a

## [2.2.0] - 2021-09-29

### Added

- `populate_ubi_dot_repos` - drives population of ubi DOT repositories

## Changed

- Definitions data objects are now immutable.

## [2.1.0] - 2021-03-30

### Added

- `rhel_open_dist` - listing RHEL versions which are still expecting new minor releases

## [2.0.0] - 2021-03-04

### Changed

- The concept of the project has changed significantly. The `cdn-definitions` project
  now contains only placeholder data, a schema and a small convenience API for loading
  data. When used in production, it is now necessary to combine `cdn-definitions` with a
  separately maintained (e.g. private) data set.

### Added

- `load_data`, `load_schema` functions were added.

### Deprecated

- `rhui_aliases`, `origin_aliases` and `PathAlias` are now deprecated.

## [1.3.0] - 2020-06-30

### Added

- Define RHEL8 AUS RHUI mapping

## [1.2.0] - 2020-05-22

### Added

- Define RHEL8 EUS RHUI mapping

## [1.1.0] - 2020-05-13

### Added

- Define RHEL8 E4S RHUI mapping

## [1.0.0] - 2020-04-07

### Removed

- Dropped an incorrect fastrack RHUI alias

## [0.2.0] - 2020-03-24

### Added

- Support loading data from `/usr/share/cdn-definitions`

## [0.1.1] - 2020-03-24

### Fixed

- Fixed missing files from source distribution

## 0.1.0 - 2020-03-24

- Initial release

[Unreleased]: https://github.com/release-engineering/cdn-definitions/compare/v2.2.0...HEAD
[2.2.0]: https://github.com/release-engineering/cdn-definitions/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/release-engineering/cdn-definitions/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/release-engineering/cdn-definitions/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/release-engineering/cdn-definitions/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/release-engineering/cdn-definitions/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/release-engineering/cdn-definitions/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/release-engineering/cdn-definitions/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/release-engineering/cdn-definitions/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/release-engineering/cdn-definitions/compare/v0.1.0...v0.1.1
