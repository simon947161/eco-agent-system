import copy
import json
import math
import shutil
import struct
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.reproduce_awra_month import (
    EVIDENCE, CELL, START, END, PRODUCTS, Capture, NoRedirect,
    analyse, comparison, decode, load, plan, reproduce, validate_sample,
)


class AWRAMonthReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest, cls.data, cls.receipts = load(EVIDENCE)

    def test_real_sample_mean_matches_and_month_end_does_not(self):
        result = reproduce()
        self.assertEqual(result['status'], 'PARTIAL')
        soil = result['comparisons']['sm_pct']
        self.assertTrue(soil['daily_mean']['agrees'])
        self.assertFalse(soil['final_day']['agrees'])
        self.assertAlmostEqual(soil['daily_mean']['reference'], 0.13241835275003988, places=14)
        self.assertGreater(abs(soil['final_day']['difference']), 0.028)
        self.assertEqual(result['metadata']['day-sm_pct']['valid_samples'], 31)
        self.assertEqual(result['metadata']['day-sm_pct']['masked_samples'], 0)
        self.assertFalse(result['provider_general_semantics_proven'])
        self.assertFalse(result['scientific_admission'])
        self.assertEqual(result['cross_source_numeric_join'], 'BLOCKED')

    def test_absent_rain_stays_missing_not_zero(self):
        result = reproduce()
        self.assertEqual(self.receipts['day-rain_day.dds']['http_status'], 404)
        self.assertNotIn('day-rain_day', result['samples'])
        self.assertNotIn('daily_sum', result['comparisons']['rain_day'])
        self.assertEqual(result['samples']['month-rain_day']['rain_day'], [struct.unpack('>f', struct.pack('>f', 11.3))[0]])
        self.assertNotIn(b'name="rain_day_2000.nc"', self.data['awral-catalog.xml'])
        self.assertNotIn(b'name="rain_day_2000.nc"', self.data['day-catalog.xml'])

    def test_ieee_float32_values_and_date_coordinates(self):
        sample = decode(self.data['day-sm_pct.dods'], 'day-sm_pct')
        self.assertEqual(sample['time'], list(range(START, END)))
        self.assertEqual(sample['sm_pct'][0], 0.15876387059688568)
        self.assertEqual(sample['latitude'], [CELL['latitude']])
        self.assertEqual(sample['longitude'], [CELL['longitude']])

    def test_fill_nan_and_out_of_range_are_rejected(self):
        for value in (-999, math.nan, math.inf, -0.01, 1.1):
            with self.subTest(value=value):
                sample = decode(self.data['day-sm_pct.dods'], 'day-sm_pct')
                sample['sm_pct'][3] = value
                with self.assertRaises(ValueError):
                    validate_sample(sample, self.data['day-sm_pct.das'], 'day-sm_pct')

    def test_incomplete_duplicate_or_shifted_days_are_rejected(self):
        for times in (list(range(START, END-1)), [START] * 31, list(range(START+1, END+1))):
            sample = decode(self.data['day-sm_pct.dods'], 'day-sm_pct')
            sample['time'] = times
            with self.assertRaises(ValueError):
                validate_sample(sample, self.data['day-sm_pct.das'], 'day-sm_pct')

    def test_wrong_cell_and_month_bounds_are_rejected(self):
        for field, value in (('longitude', [149.15]), ('latitude', [-36.3]), ('time_bounds', [START, END-1])):
            sample = decode(self.data['month-sm_pct.dods'], 'month-sm_pct')
            sample[field] = value
            with self.assertRaises(ValueError):
                validate_sample(sample, self.data['month-sm_pct.das'], 'month-sm_pct')

    def test_unit_calendar_and_packing_changes_are_rejected(self):
        sample = decode(self.data['day-sm_pct.dods'], 'day-sm_pct')
        for old, new in ((b'fraction of fullness', b'%'), (b'gregorian', b'360_day'), (b'degrees_east', b'radians'),
                         (b'Float32 _FillValue -999.0;', b'Float32 _FillValue -999.0; Float32 scale_factor 100.0;'),
                         (b'Float32 _FillValue -999.0;', b'Float32 _FillValue -999.0; Float32 valid_range 0.0, 1.0;')):
            with self.assertRaises(ValueError):
                validate_sample(sample, self.data['day-sm_pct.das'].replace(old, new), 'day-sm_pct')

    def test_bad_dap_count_shape_identity_and_trailing_bytes_rejected(self):
        raw = self.data['day-sm_pct.dods']
        header, payload = raw.split(b'\nData:\n', 1)
        bad_count = header + b'\nData:\n' + struct.pack('>I', 30) + payload[4:]
        for body in (bad_count, raw.replace(b'time = 31', b'time = 32'), raw.replace(b'sm_pct_2000.nc;', b'sm_pct_2001.nc;'), raw + b'x'):
            with self.assertRaises(ValueError):
                decode(body, 'day-sm_pct')

    def test_revision_change_blocks_comparison(self):
        receipts = copy.deepcopy(self.receipts)
        receipts['day-sm_pct-after.head']['headers']['last-modified'] = 'changed'
        result = analyse(self.data, receipts)
        self.assertIn('revision changed', result['failures']['day-sm_pct'])
        self.assertNotIn('daily_mean', result['comparisons']['sm_pct'])

    def test_corrupt_response_bytes_and_source_url_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / 'evidence'
            shutil.copytree(EVIDENCE, directory)
            p = directory / 'day-sm_pct.dods'
            original = p.read_bytes()
            p.write_bytes(original + b'x')
            with self.assertRaises(ValueError):
                load(directory)
            p.write_bytes(original)
            manifest = json.loads((directory / 'manifest.json').read_text())
            manifest['files'][0]['url'] = 'https://other.example/data'
            (directory / 'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                load(directory)

    def test_no_network_on_default_replay(self):
        with patch('urllib.request.OpenerDirector.open', side_effect=AssertionError('unexpected network')):
            reproduce()

    def test_live_plan_cannot_get_whole_physical_file_or_large_subset(self):
        for name, (url, method, cap) in plan().items():
            self.assertTrue(url.startswith('https://thredds.nci.org.au/thredds/'))
            if url.endswith('.nc'):
                self.assertEqual(method, 'HEAD')
                self.assertEqual(cap, 0)
            if '.dods?' in url:
                self.assertIn('%5B525:1:525%5D%5B742:1:742%5D', url)
                self.assertLessEqual(cap, 16384)
        with tempfile.TemporaryDirectory() as tmp:
            capture = Capture(Path(tmp) / 'capture')
            with self.assertRaises(KeyError):
                capture.get('https://other.example/data')
            with self.assertRaises(FileExistsError):
                Capture(capture.directory)
        with self.assertRaises(ValueError):
            NoRedirect().redirect_request(None)

    def test_rounding_tolerance_does_not_hide_material_difference(self):
        self.assertTrue(comparison(31.000001, 31, 1e-5)['agrees'])
        self.assertFalse(comparison(1, 31, 1e-5)['agrees'])

    def test_rain_sum_branch_with_explicit_synthetic_fixture(self):
        data, receipts = copy.deepcopy(self.data), copy.deepcopy(self.receipts)
        key = 'day-rain_day'
        header = f"""Dataset {{
    Grid {{
     ARRAY:
        Float32 rain_day[time = 31][latitude = 1][longitude = 1];
     MAPS:
        Int32 time[time = 31];
        Float64 latitude[latitude = 1];
        Float64 longitude[longitude = 1];
    }} rain_day;
}} {PRODUCTS[key]};
""".encode()
        payload = b''
        for fmt, values in (('f', [11.3] + [0.0]*30), ('i', list(range(START, END))),
                            ('d', [-36.25]), ('d', [149.1])):
            payload += struct.pack('>II', len(values), len(values))
            payload += struct.pack('>' + str(len(values)) + fmt, *values)
        data[key + '.dods'] = header + b'\nData:\n' + payload
        data[key + '.das'] = self.data['month-rain_day.das']
        for suffix in ('.dds', '.das', '.dods', '-before.head', '-after.head'):
            receipts[key + suffix] = copy.deepcopy(self.receipts['month-rain_day' + suffix])
        result = analyse(data, receipts)
        self.assertTrue(result['comparisons']['rain_day']['daily_sum']['agrees'])
        self.assertFalse(result['scientific_admission'])
        self.assertEqual(result['cross_source_numeric_join'], 'BLOCKED')

    def test_live_response_caps_retain_failure_without_full_download(self):
        class Response:
            status = 200
            def __init__(self, headers, body):
                self.headers, self.body, self.read_calls = headers, body, []
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, n):
                self.read_calls.append(n)
                return self.body[:n]
        for length in (None, '999999999'):
            with tempfile.TemporaryDirectory() as tmp:
                capture = Capture(Path(tmp) / 'capture')
                response = Response({'Content-Length': length} if length else {}, b'x' * 16385)
                with patch.object(capture.opener, 'open', return_value=response):
                    self.assertFalse(capture.get('day-sm_pct.dds'))
                self.assertFalse(capture.receipts[0]['complete'])
                self.assertIn('cap', capture.receipts[0]['error'])
                self.assertEqual(response.read_calls, [] if length else [16385])
