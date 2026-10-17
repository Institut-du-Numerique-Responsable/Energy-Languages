"""Compile the COBOL benchmarks and compare small runs with independent references.

References come from the Python programs of this suite (n-body, fannkuch-redux,
fasta, reverse-complement, binary-trees), from the published spectral-norm value
for n=100 and from a sequential C implementation for mandelbrot.
"""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests' / 'fixtures' / 'cobol'
CASES = [
    ('n-body', 'nbody', ['1000'], None, 'n-body-1000.out'),
    ('spectral-norm', 'spectralnorm', ['100'], None, 'spectral-norm-100.out'),
    ('mandelbrot', 'mandelbrot', ['200'], None, 'mandelbrot-200.pbm'),
    ('fannkuch-redux', 'fannkuchredux', ['7'], None, 'fannkuch-redux-7.out'),
    ('fasta', 'fasta', ['1000'], None, 'fasta-1000.out'),
    ('reverse-complement', 'revcomp', [], 'reverse-complement-input.fa',
     'reverse-complement.out'),
    ('binary-trees', 'binarytrees', ['10'], None, 'binary-trees-10.out'),
]


@unittest.skipUnless(shutil.which('cobc'), 'GnuCOBOL (cobc) is not installed')
class CobolBenchmarkTests(unittest.TestCase):
    def test_outputs_match_references(self):
        with tempfile.TemporaryDirectory(prefix='cobol ') as temp:
            for benchmark, program, args, stdin, expected in CASES:
                with self.subTest(benchmark=benchmark):
                    executable = Path(temp) / program
                    source = ROOT / 'COBOL' / benchmark / f'{program}.cob'
                    build = subprocess.run(['cobc', '-x', '-O2', '-o', str(executable), str(source)],
                                           capture_output=True, text=True, timeout=120)
                    self.assertEqual(build.returncode, 0, build.stderr)
                    input_bytes = (FIXTURES / stdin).read_bytes() if stdin else None
                    result = subprocess.run([str(executable), *args], input=input_bytes,
                                            capture_output=True, timeout=120)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(result.stdout, (FIXTURES / expected).read_bytes())

    def test_makefiles_declare_every_action(self):
        for benchmark, program, *_ in CASES:
            with self.subTest(benchmark=benchmark):
                makefile = (ROOT / 'COBOL' / benchmark / 'Makefile').read_text()
                for target in ['compile:', 'run:', 'measure:', 'mem:', 'clean:']:
                    self.assertIn(target, makefile)
                self.assertIn(f'{program}.cob', makefile)


if __name__ == '__main__':
    unittest.main()
