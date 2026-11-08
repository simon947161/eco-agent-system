"""Focused fail-closed tests. No real-data physical calculation or simulation."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from audit_profile import ROOT, audit, finite, summary


class AdmissionTests(unittest.TestCase):
    def test_missing_is_not_zero(self):
        self.assertIsNone(finite('NaN'))
        self.assertIsNone(finite('inf'))
        self.assertIsNone(finite(''))
        self.assertEqual(finite('0'), 0)
        self.assertEqual(summary(['NaN', '0'])['missing_or_nonfinite'], 1)

    def test_original_identity_and_global_vs_row_gate(self):
        result = audit()
        self.assertEqual(result['profile_rows'], 2137)
        self.assertEqual(result['row_structural_failures'], {})
        self.assertEqual(result['structurally_usable_rows'], 2137)
        self.assertEqual(result['globally_admitted_comparison_rows'], 0)
        self.assertIn('ambient_temperature_uncertainty', result['global_metadata_blockers'])
        self.assertEqual(result['stage2_status'], 'NO_VALID_VERTICAL_PROFILE')
        self.assertFalse(result['p1_executed'])

    def test_clock_representation_is_not_silent_deduplication(self):
        result = audit()
        self.assertEqual(result['duplicate_formatted_timestamps'], 138)
        self.assertEqual(result['duplicate_fractional_seconds'], 0)
        self.assertLess(result['maximum_formatted_clock_difference_seconds'], 1)
        self.assertEqual(result['profile_rows'], 2137)

    def test_tampered_bytes_fail_before_analysis(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'task'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('__pycache__'))
            manifest = json.loads((root/'INPUT_MANIFEST.json').read_text())
            with (root/manifest['profile_path']).open('ab') as f:
                f.write(b'\n')
            with self.assertRaisesRegex(ValueError, 'Input identity mismatch'):
                audit(root)

    def test_even_completed_metadata_does_not_run_or_admit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'task'
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('__pycache__'))
            gates = json.loads((root/'METADATA_GATES.json').read_text())
            for item in gates.values():
                item['status'] = 'VERIFIED'
            (root/'METADATA_GATES.json').write_text(json.dumps(gates))
            result = audit(root)
            self.assertEqual(result['stage2_status'], 'REQUIRES_SEPARATE_SCIENTIFIC_REVIEW')
            self.assertEqual(result['globally_admitted_comparison_rows'], 0)
            self.assertFalse(result['counterfactual_executed'])


if __name__ == '__main__':
    unittest.main()
