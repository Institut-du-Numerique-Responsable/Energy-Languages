# COBOL benchmarks (GnuCOBOL)

**En français :** sept benchmarks réécrits en COBOL par l’INR pour représenter un langage des grands systèmes (mainframe). Ils sont compilés avec GnuCOBOL sur Linux ou macOS et validés contre des implémentations indépendantes. Aucune mesure d’énergie n’a encore été réalisée. Ces programmes ne mesurent pas la consommation d’un mainframe IBM Z avec Enterprise COBOL.

COBOL is the most widely used language on mainframes (IBM Z, z/OS). This directory adds seven Benchmarks Game programs written in COBOL by INR, compiled with [GnuCOBOL](https://gnucobol.sourceforge.io/) 3.x. They follow the sequential reference algorithms and the output formats of the other implementations in this suite.

| Benchmark | Source | Standard argument | Notes |
|---|---|---|---|
| n-body | `n-body/nbody.cob` | 50000000 | `COMP-2` (double precision) |
| spectral-norm | `spectral-norm/spectralnorm.cob` | 5500 | `COMP-2`, exact integer denominators |
| mandelbrot | `mandelbrot/mandelbrot.cob` | 16000 | `COMP-2`, binary PBM output |
| fannkuch-redux | `fannkuch-redux/fannkuchredux.cob` | 12 | binary integers (`COMP-5`), single thread |
| fasta | `fasta/fasta.cob` | 25000000 | integer generator; thresholds of the C program `fasta.gcc-2` |
| reverse-complement | `reverse-complement/revcomp.cob` | `< revcomp-input25000000.txt` | buffer grown by doubling, `INSPECT CONVERTING` |
| binary-trees | `binary-trees/binarytrees.cob` | 21 | one C `calloc`/`free` per node, explicit stack |

Not implemented: k-nucleotide (hash table), pidigits (arbitrary-precision arithmetic) and regex-redux (regular expressions) have no practical COBOL equivalent without external libraries.

## Build and run

```sh
cd COBOL/n-body
make compile      # cobc -x -O2 -o nbody.cobol_run nbody.cob
./nbody.cobol_run 1000
```

On Debian or Ubuntu, install `gnucobol`; on macOS, `brew install gnucobol`. The `measure` targets follow the suite’s RAPL convention and require Linux with Intel MSR access.

## Validation

`tests/test_cobol.py` compiles each program and compares a small run byte for byte with an independent reference:

- n-body (n=1000), fannkuch-redux (n=7), fasta (n=1000), reverse-complement and binary-trees (depth 10): the Python programs of this suite;
- spectral-norm (n=100): the published value 1.274219991;
- mandelbrot (n=200): a sequential C implementation of the reference algorithm.

Larger sizes were also checked during development: fasta and reverse-complement up to n=2,500,000, fannkuch-redux n=10, spectral-norm n=500, mandelbrot n=1000 and binary-trees depth 21.

## Expected run times

Single runs on an Apple M4 Pro, GnuCOBOL 3.2, `-O2`; standard sizes are extrapolated from smaller runs unless stated.

| Benchmark | Observed | Standard size (estimate) |
|---|---|---|
| binary-trees | 10 s at depth 21 | 10 s (measured) |
| fasta | 2.9 s at n=2.5M | about 30 s |
| reverse-complement | 1.1 s for 25 MB of input | about 11 s |
| fannkuch-redux | 1.2 s at n=10 | about 2.5 min |
| spectral-norm | 10 s at n=500 | about 20 min |
| n-body | 3.8 s at 20,000 steps | about 2.7 h |
| mandelbrot | 116 s at n=1000 | about 8 h |

GnuCOBOL evaluates `COMP-2` expressions through its decimal arithmetic library (GMP) instead of native floating-point instructions. The three floating-point benchmarks therefore run about 50 times slower than the Python programs of this suite, whereas the integer programs run faster than Python. These durations describe GnuCOBOL, not COBOL on a mainframe.

## Limits

- **Not mainframe measurements.** IBM Enterprise COBOL compiles to z/Architecture instructions, with hardware decimal and floating-point units. GnuCOBOL translates COBOL to C and runs on x86 or ARM. An energy reading of these programs does not describe the consumption of a COBOL application on IBM Z.
- **No historical data.** These programs are absent from the inherited CSV files. Comparing them with other languages requires a new campaign on the same machine, with reference languages measured again under the same conditions.
- **Single thread.** The reference C programs of several benchmarks use several threads.
- **Long runs.** The RAPL backend reads the counters only at the start and end of a run; runs of several hours need periodic sampling before their readings can be trusted (see [known limitations](../docs/KNOWN_LIMITATIONS.md)).
- PL/I, RPG, Natural and High Level Assembler are not included: they have no maintained open-source compiler for Linux, or would only run through an emulator, which would measure the emulation. REXX could be added with the open-source Regina interpreter.
