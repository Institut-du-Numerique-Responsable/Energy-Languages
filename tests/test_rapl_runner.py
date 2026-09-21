"""Runner integration tests; only the hardware-specific RAPL functions are stubbed."""
import os
from pathlib import Path
import subprocess
import shutil
import stat
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.build = tempfile.TemporaryDirectory()
        build = Path(cls.build.name)
        stub = build / 'stub.c'
        stub.write_text('''#include <stdio.h>
#include <stdlib.h>
int rapl_init(int core) { return getenv("FAIL_INIT") ? -1 : 0; }
void rapl_before(FILE *fp, int core) {}
void rapl_after(FILE *fp, int core) {
    fprintf(fp, "1, 2, , , ");
    if (getenv("FAIL_AFTER")) exit(127);
}
''')
        cls.binary = build / 'runner'
        subprocess.run([os.environ.get('CC', 'cc'), '-include', 'sys/time.h',
                        str(ROOT / 'RAPL/main.c'), str(stub), '-o', str(cls.binary)], check=True)

    @classmethod
    def tearDownClass(cls):
        cls.build.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cwd = self.root / 'benchmark'
        self.cwd.mkdir()
        self.csv = self.root / 'Audit.csv'

    def run_command(self, *args, **env):
        return subprocess.run([str(self.binary), *args], cwd=self.cwd,
                              env={**os.environ, **env}, capture_output=True, timeout=10)

    def rows(self):
        return self.csv.read_text().splitlines() if self.csv.exists() else []

    def test_success_records_ten_samples(self):
        result = self.run_command('true', 'Audit', 'sample')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(self.rows()), 10)

    def test_failure_preserves_existing_results(self):
        self.csv.write_text('existing\n')
        result = self.run_command('exit 7', 'Audit', 'sample')
        self.assertEqual(result.returncode, 7)
        self.assertEqual(self.rows(), ['existing'])

    def test_missing_arguments_are_rejected_without_crash(self):
        result = self.run_command()
        self.assertGreater(result.returncode, 0)
        self.assertIn(b'Usage:', result.stderr)

    def test_long_command_does_not_overflow(self):
        result = self.run_command('true #' + 'x' * 1000, 'Audit', 'sample')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(self.rows()), 10)

    def test_signal_failure_discards_sample(self):
        result = self.run_command('kill -TERM $$', 'Audit', 'sample')
        self.assertGreater(result.returncode, 0)
        self.assertEqual(self.rows(), [])

    def test_oversized_language_is_rejected(self):
        result = self.run_command('true', 'A' * 1000, 'sample')
        self.assertGreater(result.returncode, 0)
        self.assertEqual(self.rows(), [])

    def test_invalid_labels_are_rejected(self):
        for language, label in [('../escape', 'sample'), ('Audit', 'bad\nrow'), ('', 'sample')]:
            with self.subTest(language=language, label=label):
                result = self.run_command('true', language, label)
                self.assertGreater(result.returncode, 0)
        self.assertEqual(self.rows(), [])

    def test_output_open_failure_is_reported(self):
        self.csv.mkdir()
        result = self.run_command('touch executed', 'Audit', 'sample')
        self.assertGreater(result.returncode, 0)
        self.assertFalse((self.cwd / 'executed').exists())

    def test_initialization_failure_does_not_execute(self):
        result = self.run_command('touch executed', 'Audit', 'sample', FAIL_INIT='1')
        self.assertGreater(result.returncode, 0)
        self.assertFalse((self.cwd / 'executed').exists())
        self.assertEqual(self.rows(), [])

    def test_sensor_failure_does_not_append_partial_row(self):
        result = self.run_command('true', 'Audit', 'sample', FAIL_AFTER='1')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.rows(), [])

    def test_build_removes_world_write_permission(self):
        for name in ['main.c', 'rapl.c', 'rapl.h', 'Makefile']:
            shutil.copy2(ROOT / 'RAPL' / name, self.cwd / name)
        executable = self.cwd / 'main'
        executable.write_text('old executable')
        executable.chmod(0o777)
        subprocess.run(['make', '-B'], cwd=self.cwd, check=True, capture_output=True)
        self.assertEqual(stat.S_IMODE(executable.stat().st_mode), 0o755)


if __name__ == '__main__':
    unittest.main()
