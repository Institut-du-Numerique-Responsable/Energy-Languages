#!/usr/bin/env python3
"""Compatibility entry point; scan the current directory using the shared runner."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parents[1] / 'compile_all.py'),
                   run_name='__main__')
