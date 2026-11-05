"""Real archive replay and synthetic refusal mutations."""
import copy
import json
import unittest
import tempfile
import shutil
from cczps_lite.integration import facility_spatial_evidence as f


class FacilitySpatialEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((f.EVIDENCE/'waste-points.json').read_bytes())

    def test_real_archive_identity_and_colocation(self):
        out = f.replay()
        self.assertEqual(len(out['records']), 6)
        self.assertEqual(out['coincident_register_points'], [['waste:668', 'waste:2397', 'waste:3319']])
        self.assertEqual([r['name'] for r in out['records'] if 'LANDFILL' in r['category']], ['COOMA LANDFILL'])
        self.assertEqual(out['methane'], 'DATA_NOT_READY')
        self.assertEqual(out['temporal_comparison'], 'NOT_ADMITTED_NO_COMMON_OBSERVATION_INTERVAL')

    def test_refuse_truncation_error_crs_and_geometry(self):
        for change in [{'exceededTransferLimit': True}, {'error': {}}, {'spatialReference': {'wkid': 4326}}, {'geometryType': 'esriGeometryPolygon'}, {'features': None}]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                f.parse_points({**self.payload, **change}, 'waste')

    def test_refuse_bad_location_and_identity(self):
        for field, value in [('x', float('nan')), ('x', True), ('y', 0), ('x', None)]:
            data = copy.deepcopy(self.payload)
            data['features'][0]['geometry'][field] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                f.parse_points(data, 'waste')
        data = copy.deepcopy(self.payload)
        data['features'].append(data['features'][0])
        with self.assertRaisesRegex(ValueError, 'DUPLICATE'):
            f.parse_points(data, 'waste')

    def test_empty_is_not_no_facilities_conclusion(self):
        self.assertEqual(f.parse_points({**self.payload, 'features': []}, 'waste'), [])

    def test_tampered_archive_and_missing_receipts_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = __import__('pathlib').Path(tmp)
            for path in f.EVIDENCE.glob('*.json'):
                shutil.copyfile(path, folder/path.name)
            path = folder/'waste-points.json'
            path.write_bytes(path.read_bytes() + b' ')
            with self.assertRaisesRegex(ValueError, 'HASH_MISMATCH'):
                f.replay(folder)
            (folder/'receipts.json').write_text('[]', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'INCOMPLETE_RECEIPTS'):
                f.replay(folder)


if __name__ == '__main__':
    unittest.main()
