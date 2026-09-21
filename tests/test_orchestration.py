"""Integration tests for the command-line tools, using small temporary benchmarks."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='energy tools ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def benchmark(self, name, recipe):
        folder = self.root / name
        folder.mkdir(parents=True)
        (folder / 'Makefile').write_text(recipe)
        return folder

    def run_tool(self, *args, entry='compile_all.py'):
        return subprocess.run([sys.executable, str(ROOT / entry), *args],
                              cwd=self.root, capture_output=True, text=True, timeout=10)

    def test_all_actions_report_failure_and_continue(self):
        self.benchmark('a-failure', '')
        self.benchmark('z-success', '')
        for action in ['compile', 'run', 'measure', 'mem', 'clean']:
            with self.subTest(action=action):
                (self.root / 'a-failure/Makefile').write_text(f'{action}:\n\t@false\n')
                (self.root / 'z-success/Makefile').write_text(f'{action}:\n\t@echo executed > {action}\n')
                result = self.run_tool(action, '--delay', '0')
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertTrue((self.root / f'z-success/{action}').exists())
                self.assertIn('failed', result.stdout.lower())

    def test_paths_are_not_shell_code(self):
        folder = self.benchmark('space ; touch injected', 'compile:\n\t@echo output\n')
        result = self.run_tool('--root', str(folder))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / 'injected').exists())
        self.assertIn('output', result.stdout)

    def test_check_lists_missing_targets_without_execution(self):
        self.benchmark('available', 'measure:\n\t@touch executed\n')
        self.benchmark('unavailable', 'xmeasure:\n\t@touch executed\n')
        result = self.run_tool('measure', '--check')
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('unavailable', result.stdout)
        self.assertIn('MISSING', result.stdout)
        self.assertEqual(list(self.root.rglob('executed')), [])

    def test_missing_target_is_not_success(self):
        self.benchmark('unavailable', 'compile:\n\t@true\n')
        result = self.run_tool('mem')
        self.assertEqual(result.returncode, 1)
        self.assertIn('MISSING', result.stdout)

    def test_python3_legacy_entry_points_support_mem(self):
        self.benchmark('available', 'mem:\n\t@echo memory-result\n')
        for language in ['JavaScript', 'Fortran', 'FSharp', 'Java-GraalVM']:
            with self.subTest(language=language):
                result = self.run_tool('mem', entry=f'{language}/compile_all.py')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('memory-result', result.stdout)

    def test_prunes_non_benchmark_directories(self):
        self.benchmark('real', 'compile:\n\t@true\n')
        for excluded in ['.hidden', 'node_modules', 'obj', 'RAPL']:
            self.benchmark(f'{excluded}/nested', 'compile:\n\t@touch should-not-run\n')
        result = self.run_tool()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.root.rglob('should-not-run')), [])

    def test_empty_directory_reports_error(self):
        result = self.run_tool()
        self.assertEqual(result.returncode, 1)
        self.assertIn('No benchmark Makefiles', result.stderr)

    def test_invalid_root_is_rejected(self):
        result = self.run_tool('--root', str(self.root / 'absent'))
        self.assertEqual(result.returncode, 2)
        self.assertIn('not a directory', result.stderr)

    def test_invalid_action_is_rejected_before_execution(self):
        result = self.run_tool('compile; touch injected')
        self.assertEqual(result.returncode, 2)
        self.assertIn('invalid choice', result.stderr)
        self.assertFalse((self.root / 'injected').exists())


class InputGenerationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='energy inputs ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'Python/fasta/fasta.python3-3.python3'
        self.source.parent.mkdir(parents=True)
        shutil.copy2(ROOT / 'Python/fasta/fasta.python3-3.python3', self.source)
        shutil.copy2(ROOT / 'gen-input.sh', self.root / 'gen-input.sh')
        self.outside = self.root / 'elsewhere'
        self.outside.mkdir()

    def run_generator(self, *sizes, python=sys.executable):
        return subprocess.run(['bash', str(self.root / 'gen-input.sh'), *sizes],
                              cwd=self.outside, env={**os.environ, 'PYTHON': python},
                              capture_output=True, timeout=10)

    def test_small_datasets_match_fasta_from_any_directory(self):
        result = self.run_generator('10', '5')
        self.assertEqual(result.returncode, 0, result.stderr)
        expected = subprocess.check_output([sys.executable, str(self.source), '10'])
        self.assertEqual((self.root / 'knucleotide-input10.txt').read_bytes(), expected)
        self.assertEqual((self.root / 'revcomp-input10.txt').read_bytes(), expected)
        expected_regex = subprocess.check_output([sys.executable, str(self.source), '5'])
        self.assertEqual((self.root / 'regexredux-input5.txt').read_bytes(), expected_regex)
        self.assertEqual(list(self.outside.iterdir()), [])

    def test_failed_generation_preserves_existing_outputs(self):
        names = ['knucleotide-input10.txt', 'revcomp-input10.txt', 'regexredux-input5.txt']
        for name in names:
            (self.root / name).write_text('existing')
        fake_python = self.root / 'failing-python'
        fake_python.write_text('#!/bin/sh\nprintf partial\nexit 7\n')
        fake_python.chmod(0o755)
        result = self.run_generator('10', '5', python=str(fake_python))
        self.assertEqual(result.returncode, 7)
        for name in names:
            self.assertEqual((self.root / name).read_text(), 'existing')
        self.assertEqual(list(self.root.glob('.inputs.*')), [])

    def test_second_generator_failure_preserves_all_outputs(self):
        names = ['knucleotide-input10.txt', 'revcomp-input10.txt', 'regexredux-input5.txt']
        for name in names:
            (self.root / name).write_text('existing')
        fake_python = self.root / 'fail-second-python'
        fake_python.write_text('#!/bin/sh\n'
                               'if [ -e first-call ]; then printf partial; exit 7; fi\n'
                               'touch first-call\nprintf generated\n')
        fake_python.chmod(0o755)
        result = self.run_generator('10', '5', python=str(fake_python))
        self.assertEqual(result.returncode, 7)
        for name in names:
            self.assertEqual((self.root / name).read_text(), 'existing')
        self.assertEqual(list(self.root.glob('.inputs.*')), [])

    def test_invalid_sizes_do_not_create_datasets(self):
        for sizes in [('0', '5'), ('-1', '5'), ('abc', '5'), ('1', '2', '3')]:
            with self.subTest(sizes=sizes):
                result = self.run_generator(*sizes)
                self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.root.glob('*-input*.txt')), [])


if __name__ == '__main__':
    unittest.main()
