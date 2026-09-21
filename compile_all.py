#!/usr/bin/env python3
"""Run a benchmark Makefile target recursively, reporting every failure."""
import argparse
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ACTIONS = ('compile', 'run', 'measure', 'mem', 'clean')
EXCLUDED = {'node_modules', 'obj', 'bin', 'target', 'RAPL', '__pycache__'}


def benchmark_makefiles(root):
    """Find benchmark recipes, excluding dependencies and the RAPL tool itself."""
    def on_error(error):
        raise error

    for directory, subdirs, files in os.walk(root, onerror=on_error):
        subdirs[:] = sorted(name for name in subdirs
                            if not name.startswith('.') and name not in EXCLUDED)
        if 'Makefile' in files and Path(directory).name not in EXCLUDED:
            yield Path(directory) / 'Makefile'


def declared_targets(makefile):
    """Read literal rule names in this suite's standalone Makefiles.

    This is an inventory, not a general Make parser: included, generated and
    variable-expanded target names are not resolved.
    """
    targets = set()
    for line in makefile.read_text().splitlines():
        if not line or line[0].isspace() or line.startswith('#'):
            continue
        match = re.match(r'^([^:=#]+):(?!=)', line)
        if match:
            targets.update(match.group(1).split())
    return targets


def nonnegative_seconds(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError('delay must be a finite, nonnegative number')
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=ACTIONS, nargs='?', default='compile')
    parser.add_argument('--root', type=Path, default=Path('.'),
                        help='directory to scan (default: current directory)')
    parser.add_argument('--check', action='store_true',
                        help='list literal target availability without running recipes')
    parser.add_argument('--delay', type=nonnegative_seconds, default=5.0,
                        help='seconds between measurement commands (default: 5)')
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        parser.error(f'not a directory: {args.root}')
    try:
        makefiles = list(benchmark_makefiles(args.root.resolve()))
    except OSError as error:
        print(f'Cannot scan benchmarks: {error}', file=sys.stderr)
        return 1
    if not makefiles:
        print('No benchmark Makefiles found.', file=sys.stderr)
        return 1

    succeeded = failed = missing = 0
    measurement_started = False
    for makefile in makefiles:
        folder = makefile.parent
        try:
            if args.action not in declared_targets(makefile):
                print(f'[MISSING] {folder}: target {args.action}', flush=True)
                missing += 1
                continue
            if args.check:
                print(f'[AVAILABLE] {folder}: target {args.action}', flush=True)
                succeeded += 1
                continue
            if args.action == 'measure' and measurement_started:
                time.sleep(args.delay)
            print(f'[RUN] {folder}: make {args.action}', flush=True)
            status = subprocess.run(['make', args.action], cwd=folder).returncode
            if args.action == 'measure':
                measurement_started = True
            if status:
                print(f'[FAILED] {folder}: exit status {status}', flush=True)
                failed += 1
            else:
                print(f'[OK] {folder}', flush=True)
                succeeded += 1
        except (OSError, UnicodeError) as error:
            print(f'[FAILED] {folder}: {error}', file=sys.stderr, flush=True)
            failed += 1
    label = 'available' if args.check else 'succeeded'
    print(f'Summary: {succeeded} {label}, {failed} failed, {missing} missing.', flush=True)
    return 1 if failed or missing else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print('\nInterrupted.', file=sys.stderr)
        sys.exit(130)
