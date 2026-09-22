# Energy Languages — INR edition

**An improved derivative of [Green Software Lab's Energy-Languages](https://github.com/greensoftwarelab/Energy-Languages), maintained by the Institut du Numérique Responsable (INR).**

This edition adds targeted reliability and safety fixes to the energy measurement runner, a shared Python 3 orchestrator, reliable input generation, regression tests and clearer documentation. The original research and benchmark implementations remain credited to their authors. This is an independent derivative, not an official upstream release.

**En français :** cette version améliorée est maintenue par l'Institut du Numérique Responsable. Elle corrige trois défauts prioritaires du programme de mesure et ajoute des tests. Elle reprend les travaux de Green Software Lab ; elle ne constitue pas une nouvelle validation scientifique du classement des langages.

[**Explore the public website**](https://institut-du-numerique-responsable.github.io/Energy-Languages/) · [Results](https://institut-du-numerique-responsable.github.io/Energy-Languages/resultats.html) · [Methodology](https://institut-du-numerique-responsable.github.io/Energy-Languages/methode.html)

<!-- BEGIN GENERATED FINDINGS -->
## Key findings from the historical observations

**Read energy together with execution time and power.**

- **Energy and runtime are strongly associated:** within-benchmark Spearman correlations range from 0.938 to 0.996 in the retained exploratory series.
- **Modest differences in power can accompany large differences in energy:** the n-body example below illustrates the role of duration.
- **The evidence can be checked:** all 253 series, source lines, quality flags and calculations are published, including series excluded from exploratory comparisons.

| n-body observation | Python / C ratio |
|---|---:|
| Median package energy | 157.5× |
| Median execution time | 133.5× |
| Median package power | 1.18× |

These ratios describe the inherited sample, **not universal language characteristics**. Hardware and execution metadata are incomplete; correlation does not establish causation. [Read the results, filters and limitations](docs/BENCHMARK_RESULTS.md).
<!-- END GENERATED FINDINGS -->

## What INR improved

- Failed benchmark commands now stop the measurement run with a nonzero status; failed samples are not appended to the CSV. Previously completed samples are retained.
- Command-line arguments and output-file errors are checked. Unbounded argument copies were removed; initialization errors stop execution. A temporary file stages each sample to prevent sensor failures from leaving partial result rows.
- The RAPL executable is built with permissions `755`, replacing the previous world-writable `777` mode.
- A shared Python 3 orchestrator reports failed and missing targets for all five operations. The four legacy entry points delegate to it.
- Input generation works from any directory, reuses the identical nucleotide dataset and preserves existing inputs when generation fails.
- Automated regression tests exercise the command runner with simulated hardware readings, orchestration with real Makefiles and input generation with small FASTA datasets.
- This README, the [changelog](CHANGELOG.md) and [known limitations](docs/KNOWN_LIMITATIONS.md) distinguish completed improvements from remaining work.

These changes do **not** establish that any language is more energy efficient. Existing CSV files are inherited results, not measurements produced or revalidated by INR. No new hardware energy measurements accompany this edition.

## Historical benchmark results

Read the [results and cross-analyses](docs/BENCHMARK_RESULTS.md) (French), with [detailed tables for every benchmark](docs/results/TABLES.md), coverage and energy–time charts, and downloadable CSV exports.

The analysis separates alternate files, reports anomalous readings, and documents every filter. It compares energy, duration, derived package power, variability and energy–delay product descriptively. It also proposes controlled follow-up analyses for memory, input size, parallelism and runtime warm-up. These are inherited observations with incomplete experimental metadata, not a new INR ranking of programming languages.

Reproduce the numerical report with `python3 scripts/analyze_results.py`; add `--plots` when Matplotlib is installed to regenerate the figures.

## Origin and attribution

Upstream project: [greensoftwarelab/Energy-Languages](https://github.com/greensoftwarelab/Energy-Languages).

Original authors: Rui Pereira, Marco Couto, Francisco Ribeiro, Rui Rua, Jácome Cunha, João Paulo Fernandes and João Saraiva.

Research: *Energy Efficiency across Programming Languages: How does Energy, Time and Memory Relate?*, SLE 2017. See the [original project and research links](https://github.com/greensoftwarelab/Energy-Languages#further-reading).

The suite contains implementations originating from the Computer Language Benchmark Game, grouped by language. Preserve individual source-file attribution notices when redistributing them. The original [MIT license](LICENSE) and copyright notice are retained.

This repository was initialized from a local source snapshot without Git history. Its exact upstream commit is not established. The [README supplied with that snapshot](docs/README-imported.md) is retained for reference; some instructions there are obsolete or incomplete.

## Try a small benchmark

Python 3 is sufficient for this example; no RAPL device or administrator access is required:

```sh
python3 Python/n-body/nbody.python3 1000
```

## Run the regression tests

Requires Python 3 and a C compiler (`cc`, or set `CC`):

```sh
python3 -m unittest discover -s tests -v
```

These tests validate runner behavior with simulated RAPL functions, orchestration and input generation. They do not validate physical energy readings or all benchmark algorithms. They also require `make` and Bash.

## Verify benchmark output before measuring

A zero exit code is insufficient. Use an independently reviewed expected output with the same input size and configuration:

```sh
python3 scripts/verify_output.py --expected reference.txt --report validation.json --atol 1e-9 -- python3 Python/n-body/nbody.python3 1000
```

The command must be trusted. The tool compares whitespace-separated tokens, checks numeric tolerances, rejects non-finite numbers and failed commands, and records output hashes and execution context. Choose tolerances for the algorithm and printed precision; the example tolerance is not universal. Legacy `measure` targets do not enforce this preflight. See [validation guidance](docs/VALIDATION.md).

## Measure energy on supported hardware

The inherited backend requires **Linux and a compatible Intel CPU with accessible MSR devices**. It does not support native macOS/Apple Silicon measurement. Its CPU/domain detection is legacy; check the [limitations](docs/KNOWN_LIMITATIONS.md) before interpreting readings.

```sh
make -B -C RAPL
```

Compile a benchmark using its `Makefile`, adapting compiler paths and dependencies to your environment. From that benchmark's directory, the runner interface is:

```text
../../RAPL/main "command" Language benchmark-name
```

The command is interpreted by a shell, allowing the existing input-redirection recipes to work. It must be trusted. Existing `measure` targets use `sudo`; that also runs the benchmark command with elevated privileges. Only run reviewed commands from a trusted, appropriately owned checkout.

Ten successful repetitions append ten rows to `../Language.csv`. The inherited row format mixes a semicolon after the benchmark name with commas between energy fields; time is in milliseconds. It is not a uniform delimiter-separated table. Errors stop the run; already completed rows remain.

## Run or inspect benchmark targets

The root orchestrator requires Python 3 and `make`. It scans the current directory recursively; use `--root` to select a language or benchmark:

```sh
# Check target availability only; no benchmark command is executed.
python3 compile_all.py measure --check
python3 compile_all.py compile --root C --check

# Execute a target after adapting its compiler paths and dependencies.
python3 compile_all.py compile --root C/n-body
```

Supported actions: `compile` (default), `run`, `measure`, `mem`, `clean`.
Existing language-specific `compile_all.py` entry points use the same runner and scan the current working directory, preserving their previous scope.

A failed command or missing target produces a nonzero final status. Other available benchmarks continue, and a final summary counts successes, failures and missing targets. Output is streamed; redirect it when running benchmarks that generate large outputs. For `measure`, the runner waits five seconds between executed benchmark commands; adjust with `--delay SECONDS`.

The inventory recognizes literal targets in the suite's standalone Makefiles. It does not resolve generated rules, included Makefiles or variable-expanded target names. Availability only means that a rule exists, not that its compiler, input files or implementation are usable. Dependencies, build directories, hidden directories and the RAPL tool are excluded from discovery. Build RAPL separately as shown above.

## Generate input datasets

From a fresh checkout, no preliminary compilation is needed:

```sh
bash gen-input.sh
```

This generates the default nucleotide/reverse-complement inputs with `n=25000000` and regex-redux input with `n=5000000` in the repository root. The source path and output directory are independent of the current working directory. Set `PYTHON` to select a Python 3 executable.

For a small check:

```sh
bash gen-input.sh 10 5
```

Custom sizes are reflected in filenames (`knucleotide-input10.txt`, `revcomp-input10.txt`, `regexredux-input5.txt`); default benchmark recipes still expect the default sizes.

All datasets are generated in a temporary directory before replacing outputs. A generator failure preserves existing files. Each final replacement is atomic on the same filesystem, but replacing all three files is not a single transaction against interruption or disk errors.

Default datasets are large. Compiler versions, flags, input sizes, thread counts and machine configuration affect results. Some targets and sources are missing; see [known limitations](docs/KNOWN_LIMITATIONS.md).

## Contributing

Report reproducible problems with the command, runtime/compiler version, operating system and hardware details. For measurement changes, include regression tests and distinguish simulated checks from hardware validation. Keep upstream attribution and document INR changes in `CHANGELOG.md`.
