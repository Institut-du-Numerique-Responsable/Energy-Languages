# Energy Languages — INR edition

**An improved derivative of [Green Software Lab's Energy-Languages](https://github.com/greensoftwarelab/Energy-Languages), maintained by the Institut du Numérique Responsable (INR).**

This edition adds targeted reliability and safety fixes to the energy measurement runner, regression tests and clearer documentation. The original research and benchmark implementations remain credited to their authors. This is an independent derivative, not an official upstream release.

**En français :** cette version améliorée est maintenue par l'Institut du Numérique Responsable. Elle corrige trois défauts prioritaires du programme de mesure et ajoute des tests. Elle reprend les travaux de Green Software Lab ; elle ne constitue pas une nouvelle validation scientifique du classement des langages.

## What INR improved

- Failed benchmark commands now stop the measurement run with a nonzero status; failed samples are not appended to the CSV. Previously completed samples are retained.
- Command-line arguments and output-file errors are checked. Unbounded argument copies were removed; initialization errors stop execution. A temporary file stages each sample to prevent sensor failures from leaving partial result rows.
- The RAPL executable is built with permissions `755`, replacing the previous world-writable `777` mode.
- Automated regression tests exercise the real command runner with simulated hardware readings.
- This README, the [changelog](CHANGELOG.md) and [known limitations](docs/KNOWN_LIMITATIONS.md) distinguish completed improvements from remaining work.

These changes do **not** establish that any language is more energy efficient. Existing CSV files are inherited results, not measurements produced or revalidated by INR. No new hardware energy measurements accompany this edition.

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

These tests validate runner behavior with simulated RAPL functions. They do not validate physical energy readings or all benchmark algorithms.

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

## Input datasets and legacy build recipes

The documented root `compile_all.py` is absent from the imported snapshot. Language-specific copies and Makefiles remain available but are not uniformly functional.

For a fresh checkout, `gen-input.sh` references a generated `.py` file that does not yet exist. To generate the datasets explicitly with Python 3 from the root:

```sh
python3 Python/fasta/fasta.python3-3.python3 25000000 > knucleotide-input25000000.txt
cp knucleotide-input25000000.txt revcomp-input25000000.txt
python3 Python/fasta/fasta.python3-3.python3 5000000 > regexredux-input5000000.txt
```

These are large benchmark datasets. Compiler versions, flags, input sizes, thread counts and machine configuration affect results. Some targets and sources are missing; see [known limitations](docs/KNOWN_LIMITATIONS.md).

## Contributing

Report reproducible problems with the command, runtime/compiler version, operating system and hardware details. For measurement changes, include regression tests and distinguish simulated checks from hardware validation. Keep upstream attribution and document INR changes in `CHANGELOG.md`.
