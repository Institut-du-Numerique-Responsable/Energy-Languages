# Known limitations

The INR edition addresses the three high-priority runner findings and the orchestration/input-generation defects from the local audit. It does not certify the complete suite.

## Remaining audit findings

- A static inventory of 294 benchmark Makefiles found 26 without a `measure` target, 8 without `run`, 17 without `mem`, and 1 without `compile`. Some recipes deliberately use `xmeasure`; missing targets are not implemented by this release. The shared runner reports them as missing and returns a nonzero status. Use `python3 compile_all.py measure --check` to inspect current availability without running benchmarks.
- Target discovery recognizes literal rules in the current standalone Makefiles. It does not resolve includes, variables or generated target names. Rule presence does not validate the command, dependencies or benchmark output.
- Input generation preserves existing outputs if a generator fails, and replaces each completed file individually. The three replacements are not a single transaction against disk failures or interruption.

The [historical results report](BENCHMARK_RESULTS.md) quantifies data-quality issues and documents the filters used for descriptive comparisons. It does not validate the inherited measurements.

## Measurement and portability

- RAPL support uses legacy Linux/Intel MSR access and CPU-model checks. Hardware validation is required; native macOS and Apple Silicon are unsupported.
- The inherited backend subtracts counter readings without wraparound correction, opens MSR descriptors without closing them, and measures only the selected CPU package. Those issues remain outside the initial fixes.
- Timing still uses wall-clock time, includes runner overhead and does not isolate the benchmark from other system activity.
- A successful exit status does not prove a benchmark's output is correct. No complete expected-output comparison framework is included.
- Temporary-file staging prevents failed commands or sensor reads from appending a sample. It does not make the final CSV append transactional against disk failures or simultaneous writers. Use one writer per output file.
- Existing CSV files mix delimiters and contain inherited measurements; they are not new INR results.
- Existing Makefiles contain hard-coded runtime paths, legacy dependencies and machine-specific options. GNU `/usr/bin/time -v` and `modprobe` recipes are Linux-specific.
- Build products and bundled compiled dependencies are excluded from the Git publication. Install/rebuild external libraries as needed, including GMP for recipes that reference a local library archive.

## Scope of tests

Automated tests compile the real RAPL command runner against a simulated backend, execute temporary Makefile recipes through the orchestrator, and compare small generated datasets with the FASTA source. The physical backend, all language toolchains and the full benchmark workloads have not been validated by these tests.
