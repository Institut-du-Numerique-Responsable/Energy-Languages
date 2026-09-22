"""Exercise the real backend with fake MSR reads, including a counter rollover."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BackendTests(unittest.TestCase):
    def test_rollover_and_descriptor_lifetime(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            harness = folder / 'backend.c'
            harness.write_text(r'''
#include "rapl.h"
#include <stdarg.h>
static int opened, closed, phase;
int fake_open(const char *name, int flags, ...) { opened++; return 17; }
int fake_close(int fd) { closed++; return 0; }
ssize_t fake_pread(int fd, void *buf, size_t count, off_t offset) {
    uint64_t value = phase ? 3 : UINT32_MAX - 1;
    memcpy(buf, &value, sizeof value);
    return sizeof value;
}
#define open fake_open
#define close fake_close
#define pread fake_pread
#include "rapl.c"
int main(void) {
    cpu_model = 60;
    energy_units = 0.5;
    rapl_before(stdout, 0);
    phase = 1;
    rapl_after(stdout, 0);
    fprintf(stderr, "%d %d", opened, closed);
    return 0;
}
''')
            binary = folder / 'backend'
            subprocess.run([os.environ.get('CC', 'cc'), '-I', str(ROOT / 'RAPL'),
                            str(harness), '-lm', '-o', str(binary)], check=True,
                           capture_output=True)
            result = subprocess.run([str(binary)], check=True, capture_output=True, text=True)
            values = [float(value) for value in result.stdout.split(',') if value.strip()]
            self.assertEqual(values, [2.5] * 4)
            self.assertEqual(result.stderr, '2 2')
