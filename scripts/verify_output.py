#!/usr/bin/env python3
"""Verify a trusted benchmark command against a reference output, without RAPL."""
import argparse
import hashlib
from decimal import Decimal, InvalidOperation
import json
import math
import os
import signal
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


def compare(expected, actual, atol=0.0, rtol=0.0):
    """Compare whitespace-separated tokens; numeric tolerance is explicit."""
    left, right = expected.split(), actual.split()
    if len(left) != len(right):
        return False
    for a, b in zip(left, right):
        try:
            x, y = Decimal(a), Decimal(b)
        except InvalidOperation:
            if a != b:
                return False
        else:
            if not x.is_finite() or not y.is_finite():
                return False
            if atol == 0 and rtol == 0:
                if x != y:
                    return False
                continue
            if abs(x - y) > max(Decimal(str(atol)), Decimal(str(rtol)) * max(abs(x), abs(y))):
                return False
    return True


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError('must be finite and nonnegative')
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--atol', type=nonnegative, default=0.0)
    parser.add_argument('--rtol', type=nonnegative, default=0.0)
    parser.add_argument('--timeout', type=nonnegative, default=60.0)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command or args.timeout == 0:
        parser.error('a command and a positive timeout are required')
    try:
        expected = args.expected.read_bytes()
        expected_text = expected.decode('utf-8')
        report = {'command': command, 'cwd': str(Path.cwd()), 'platform': platform.platform(),
                  'python': platform.python_version(), 'expected_sha256': hashlib.sha256(expected).hexdigest(),
                  'atol': args.atol, 'rtol': args.rtol, 'timeout_s': args.timeout, 'passed': False}
        # Disk-backed capture avoids retaining arbitrarily large stdout during execution.
        with tempfile.TemporaryFile() as output:
            try:
                process = subprocess.Popen(command, stdout=output, start_new_session=os.name == 'posix')
                try:
                    process.wait(timeout=args.timeout)
                except subprocess.TimeoutExpired:
                    if os.name == 'posix':
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    else:
                        process.kill()
                    process.wait()
                    raise
                report['returncode'] = process.returncode
                output.seek(0)
                actual = output.read(1024 * 1024 + 1)
                report['output_exceeds_1MiB'] = len(actual) > 1024 * 1024
                if not report['output_exceeds_1MiB']:
                    report['actual_sha256'] = hashlib.sha256(actual).hexdigest()
                    report['passed'] = process.returncode == 0 and compare(
                        expected_text, actual.decode('utf-8'), args.atol, args.rtol)
            except subprocess.TimeoutExpired:
                report['error'] = 'timeout'
            except (OSError, UnicodeError) as error:
                report['error'] = str(error)
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    except (OSError, UnicodeError) as error:
        print(error, file=sys.stderr)
        return 1
    print('PASS' if report['passed'] else 'FAIL')
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
