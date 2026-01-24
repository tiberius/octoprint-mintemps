# Changelog
All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows
semantic versioning.

## [Unreleased]

## [0.2.6] - 2026-01-24
### Added
- Avoid overwriting higher manual target temperatures when applying minimums.
### Changed
- Default per-tool minimums now mirror the configured bed minimum.

## [0.2.5] - 2026-01-21
### Changed
- Raised firmware minimum check threshold to 6 C.
### Added
- Require multiple consecutive safe readings before applying minimum temps.

## [0.2.4] - 2026-01-21
### Fixed
- Skip applying minimums when a heater has no temperature reading.
- Use each heater's actual temperature reading for min-temp checks.

## [0.2.3] - 2026-01-20
### Fixed
- Default tool count/bed values in the settings template to avoid Jinja errors.

## [0.2.2] - 2026-01-20
### Fixed
- Removed custom settings JS bindings to restore normal save behavior.
### Changed
- Removed the disable checkbox from the settings UI.

## [0.2.1] - 2026-01-20
### Added
- Skip applying minimum temperatures when actual temperature is below 5 C.

## [0.2.0] - 2026-01-20
### Added
- Periodic minimum temperature enforcement while idle.
- Per-tool minimum temperature settings derived from the printer profile.
### Changed
- Expanded settings to include tool count, bed availability, and interval.

## [0.1.0] - 2026-01-20
### Added
- Initial MVP with post-print minimum temperature enforcement.
