"""Numerical and data-quality checks for the published historical analysis."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/analyze_results.py'
SPEC = importlib.util.spec_from_file_location('analysis', SCRIPT)
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


class AnalysisTests(unittest.TestCase):
    def test_mixed_delimiters_and_missing_domains(self):
        row = analysis.parse_row('n-body ; 20, 10, , , 2000', 'C/C.csv', 1, 1)
        self.assertEqual(row['package_j'], 20)
        self.assertEqual(row['time_s'], 2)
        self.assertIsNone(row['dram_j'])
        self.assertEqual(row['issues'], [])

    def test_invalid_readings_are_flagged_not_corrected(self):
        for raw in ['n-body; -2; 1; 0; 0; 1000',
                    'n-body; nan; 1; 0; 0; 1000',
                    'n-body; 2; 1; 0; 0; 0',
                    'n-body; ; 1; 0; 0; 1000']:
            with self.subTest(raw=raw):
                row = analysis.parse_row(raw, 'C/C.csv', 1, 1)
                self.assertFalse(row['numeric_valid'])
                self.assertTrue(row['issues'])

    def test_power_is_median_of_paired_row_ratios(self):
        rows = [analysis.parse_row(f'x; {energy}; 1; 0; 0; {ms}', 'C/C.csv', i, 1)
                for i, (energy, ms) in enumerate([(10, 1000), (100, 2000), (30, 3000)], 1)]
        series = analysis.summarize_series(rows)
        self.assertEqual(series['package_j_median'], 30)
        self.assertEqual(series['time_s_median'], 2)
        self.assertEqual(series['power_w_median'], 10)
        self.assertNotEqual(series['power_w_median'], 30 / 2)
        self.assertEqual(series['edp_js_median'], 90)

    def test_blocks_are_not_silently_pooled_when_they_shift(self):
        rows = [analysis.parse_row('x; 20; 1; 0; 0; 1000', 'C/C.csv', 1, 1),
                analysis.parse_row('x; 200; 1; 0; 0; 10000', 'C/C.csv', 2, 2)]
        series = analysis.summarize_series(rows)
        self.assertEqual(series['block_time_ratio'], 10)
        self.assertIn('block_shift', series['flags'])
        self.assertFalse(series['exploratory_eligible'])

    def test_short_readings_are_visible_but_not_comparison_candidates(self):
        row = analysis.parse_row('x; .01; .005; 0; 0; 1', 'C/C.csv', 1, 1)
        self.assertTrue(row['numeric_valid'])
        self.assertIn('short_time', row['issues'])
        self.assertFalse(analysis.summarize_series([row])['exploratory_eligible'])

    def test_spearman_handles_ties(self):
        self.assertAlmostEqual(analysis.spearman([1, 1, 2], [2, 2, 4]), 1)
        self.assertAlmostEqual(analysis.spearman([1, 2, 3], [3, 2, 1]), -1)
        self.assertIsNone(analysis.spearman([1, 1], [1, 2]))

    def test_variants_and_headers_are_retained_separately(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'C').mkdir()
            (root / 'C/C.csv').write_text('x; 20; 1; 0; 0; 1000\ny; 30; 1; 0; 0; 1000\nx; 40; 1; 0; 0; 2000\n')
            (root / 'C/xC.csv').write_text('benchmark-name, PKG (Joules), CPU (J), DRAM (J), Time (ms)\nx; 20; 1; 0; 0; 1000\n')
            rows, inventory, rejected = analysis.load_sources(root)
            self.assertEqual(len(rows), 4)
            self.assertEqual([r['block'] for r in rows[:3]], [1, 2, 3])
            self.assertEqual(sum(r['variant'] for r in rows), 1)
            self.assertEqual(inventory[1]['duplicate_primary_rows'], 1)
            self.assertEqual(inventory[1]['header_rows'], 1)
            self.assertEqual(rejected, [])


if __name__ == '__main__':
    unittest.main()
