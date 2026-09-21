# Changelog

## INR initial edition — 2026-09-21

Based on a local snapshot of Green Software Lab's Energy-Languages; exact upstream revision unknown.

### Fixed

- Stop on failed benchmark commands and propagate their exit status instead of recording failed runs as successful measurements.
- Stage sample output until command execution and sensor reads complete successfully.
- Validate required arguments, language filename components and benchmark labels; eliminate fixed-buffer argument copies.
- Check output-file opening, RAPL initialization and output errors.
- Build the measurement executable with mode 755 instead of 777.

### Added

- Runner regression tests using a simulated RAPL backend.
- CI for those tests, attribution, usage guidance and a limitations register.
- Git exclusions for local assistant state, dependencies, compiled objects and generated benchmark output.

### Validation limits

No new physical RAPL measurements or exhaustive cross-language algorithm validation. Existing measurement data is inherited and has not been revalidated.
