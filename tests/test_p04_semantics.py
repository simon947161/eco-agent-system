import copy
import json
import tempfile
import unittest
from pathlib import Path
from tools.inspect_awra_netcdf_header import BLOCK, HeaderRanges, validate_range
from tools.verify_p04_semantics import load_verified, inspect_semantics


class P04SemanticsTests(unittest.TestCase):
    def test_native_metadata_remains_blocked(self):
        result = inspect_semantics(load_verified())
        self.assertEqual(result['status'], 'BLOCKED_NUMERIC_JOIN')
        soil = result['variables']['sm_pct']
        self.assertIn('cell_methods', soil['absent_attributes'])
        self.assertIn('scale_factor', soil['absent_attributes'])
        self.assertEqual(soil['units'], 'fraction of fullness')
        self.assertEqual(soil['sampled_months'][1]['days'], 29)
        self.assertEqual(soil['sampled_months'][-1]['end_boundary'], '2026-10-01')

    def test_changed_calendar_refused(self):
        data = load_verified()
        data['rain_day']['variables']['time']['attributes']['calendar'] = '360_day'
        with self.assertRaises(ValueError): inspect_semantics(data)

    def test_percent_not_silently_converted(self):
        data = load_verified()
        data['sm_pct']['variables']['sm_pct']['attributes']['units'] = '%'
        with self.assertRaises(ValueError): inspect_semantics(data)

    def test_incomplete_month_refused(self):
        data = load_verified()
        data['sm_pct']['coordinate_sample']['time_bounds'][0][1] -= 1
        with self.assertRaises(ValueError): inspect_semantics(data)

    def test_corrupt_evidence_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p/'bad.json').write_text('{}')
            (p/'manifest.json').write_text(json.dumps({'files':[{'file':'bad.json','sha256':'0'*64}]}))
            with self.assertRaises(ValueError): load_verified(p)

    def test_full_response_refused(self):
        with self.assertRaises(ValueError): validate_range(200, None, 0, b'')

    def test_oversized_or_wrong_range_refused(self):
        for body, start in ((b'x'*(BLOCK+1), 0), (b'x'*BLOCK, BLOCK)):
            with self.assertRaises(ValueError): validate_range(206, f'bytes 0-{BLOCK-1}/100000', start, body)

    def test_revision_size_change_refused(self):
        with self.assertRaises(ValueError): validate_range(206, f'bytes 0-{BLOCK-1}/100000', 0, b'x'*BLOCK, 99999)

    def test_valid_bounded_range(self):
        self.assertEqual(validate_range(206, f'bytes 0-{BLOCK-1}/100000', 0, b'x'*BLOCK), 100000)

    def test_unapproved_variable_refused_before_network(self):
        with self.assertRaises(ValueError): HeaderRanges('other')
