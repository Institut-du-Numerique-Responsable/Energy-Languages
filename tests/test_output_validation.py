import importlib.util
import os
import time
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify_output', ROOT / 'scripts/verify_output.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class OutputTests(unittest.TestCase):
    def test_numeric_tolerance_and_invalid_values(self):
        self.assertTrue(module.compare('label 1.0', 'label 1.00001', atol=0.0001))
        for expected, actual in [('1', '2'), ('label 1', 'other 1'), ('1 2', '1'),
                                 ('nan', 'nan'), ('inf', 'inf'), ('9007199254740992', '9007199254740993')]:
            self.assertFalse(module.compare(expected, actual))

    def test_real_command_success_failure_and_timeout(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            expected = folder / 'expected'
            expected.write_text('42\n')
            base = [sys.executable, str(ROOT / 'scripts/verify_output.py'),
                    '--expected', str(expected), '--report', str(folder / 'report.json')]
            for code, timeout, passed in [('print(42)', '10', True), ('print(41)', '10', False),
                                          ('print(42); exit(7)', '10', False),
                                          ('import time; time.sleep(2)', '0.01', False)]:
                with self.subTest(code=code):
                    result = subprocess.run(base + ['--timeout', timeout, '--', sys.executable, '-c', code],
                                            capture_output=True)
                    self.assertEqual(result.returncode == 0, passed)

    @unittest.skipUnless(os.name == 'posix', 'process groups require POSIX')
    def test_timeout_stops_descendants(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            expected = folder / 'expected'
            expected.write_text('42')
            marker = folder / 'child-survived'
            child = "import time; from pathlib import Path; time.sleep(0.6); Path(" + repr(str(marker)) + ").touch()"
            wrapper = "import subprocess,sys,time; subprocess.Popen([sys.executable, '-c', " + repr(child) + "]); time.sleep(5)"
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/verify_output.py'),
                                     '--expected', str(expected), '--report', str(folder / 'report.json'),
                                     '--timeout', '0.2', '--', sys.executable, '-c', wrapper], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            time.sleep(0.7)
            self.assertFalse(marker.exists())
