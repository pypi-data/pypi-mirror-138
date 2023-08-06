<!--
SPDX-FileCopyrightText: 2021-2 Galagic Limited, et. al. <https://galagic.com>

SPDX-License-Identifier: CC-BY-SA-4.0

figular generates visualisations from flexible, reusable parts

For full copyright information see the AUTHORS file at the top-level
directory of this distribution or at
[AUTHORS](https://gitlab.com/thegalagic/figular/AUTHORS.md)

This work is licensed under the Creative Commons Attribution 4.0 International
License. You should have received a copy of the license along with this work.
If not, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
-->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.3 - 2022-02-15](https://gitlab.com/thegalagic/figular/-/releases/v0.0.3)

### Added

* New figure `org/orgchart` for organisational charts. See
  [orgchart](docs/figures/org/orgchart.md) in the docs for details.
* All Figure documentation has been expanded to cover website usage.
* README: direct contributors to our new wiki.

### Fixed

* Figures can accept and cope with all ASCII printable characters as input. We
  apply fuzz testing to this.
* Don't set CORS in the app, better set on network applicances.
* Build: clear out old built packages otherwise twine will try and upload them
  and fail.

### Changed

* Dependencies updated to latest.

## [0.0.2 - 2021-11-10](https://gitlab.com/thegalagic/figular/-/releases/v0.0.2)

### Added

* More detail on the deployment instructions.

### Fixed

* Quick patch to increase asy timeout to 3s which was hitting 1s limit on prod

## [0.0.1 - 2021-11-08](https://gitlab.com/thegalagic/figular/-/releases/v0.0.1)

### Added

* New cmdline flag `--help` to show usage.
* An API using FastAPI so Figular can be hosted and accessible over HTTP.
* GOVERNANCE.md was missing, added benevolent dictator.

### Fixed

* Bugs in figure `concept/circle`:
  * Crash when not given any blobs. Now we will skip drawing.
  * Crash when one blob and middle=true
  * Blobs were drawn on top of each other when only two blobs and middle=true

## [0.0.0 - 2020-04-01](https://gitlab.com/thegalagic/figular/-/releases/v0.0.0)

First version, basic cmdline usage and docs.

### Added

* New figure `concept/circle`, see docs for details.
