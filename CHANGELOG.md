# Changelog

## Public website — 2026-09-21

- Publish three lightweight French pages presenting findings, searchable historical results and methodology.
- Highlight energy–time correlations and the scoped n-body comparison in the website and README, generated from the same CSV exports.
- Add canonical URLs, a sitemap, structured software/dataset metadata and downloadable data, with GitHub Pages deployment after regression checks.
- Preserve complete HTML tables without JavaScript and document provenance and limitations beside the findings.

## Historical results documentation — 2026-09-21

- Publish a reproducible descriptive analysis of the inherited CSV files, with source hashes and line references.
- Separate alternate files and flag invalid readings, very short runs and shifts between contiguous measurement blocks.
- Add per-benchmark tables, coverage and energy–time figures, derived power and energy–delay metrics, dispersion and within-benchmark Spearman correlations.
- Document missing experimental metadata and propose controlled cross-analyses without presenting a validated language ranking or invented memory/carbon measurements.
- Add numerical and parsing regression tests for the analysis script.

## INR orchestration fixes — 2026-09-21

- Restore the documented root `compile_all.py` as a shared Python 3 runner; migrate the JavaScript, Fortran, FSharp and Java-GraalVM entry points and remove the `lazyme` dependency.
- Report failures for `compile`, `run`, `measure`, `mem` and `clean`, continue the remaining available recipes, and return a nonzero aggregate status.
- Use subprocess argument lists and working directories instead of interpolated shell commands; stream output instead of retaining entire benchmark output in memory.
- Add target availability checks without recipe execution, explicit root selection and configurable measurement spacing.
- Generate input data from the existing FASTA source using Python 3, independent of the current directory. Stage all datasets before publication and generate the shared nucleotide data once.
- Add integration tests for orchestration and input generation. Missing benchmark implementations remain explicitly unsupported.

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
