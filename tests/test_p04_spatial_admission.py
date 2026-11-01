import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from tools.verify_p04_spatial_admission import EVIDENCE, load_verified, spatial_check, variable_check, verify


class P04AdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_verified(EVIDENCE)

    def test_real_metadata_has_312_labels_but_no_numeric_admission(self):
        result = variable_check(self.data['awra-dimensions.json'])
        self.assertEqual(result['sm_pct']['study_month_labels'], 312)
        self.assertFalse(result['sm_pct']['numeric_cell_completeness_verified'])

    def test_rendering_function_cannot_substitute_for_variable(self):
        data = copy.deepcopy(self.data['awra-dimensions.json'])
        for var in data['multidimensionalInfo']['variables']:
            if var['name'] == 'rain_day': var['name'] = 'precip_month'
        with self.assertRaises(ValueError): variable_check(data)

    def test_changed_unit_is_not_silently_converted(self):
        data = copy.deepcopy(self.data['awra-dimensions.json'])
        for var in data['multidimensionalInfo']['variables']:
            if var['name'] == 'sm_pct': var['unit'] = '%'
        with self.assertRaises(ValueError): variable_check(data)

    def test_missing_study_month_fails(self):
        data = copy.deepcopy(self.data['awra-dimensions.json'])
        data['multidimensionalInfo']['variables'] = [v for v in data['multidimensionalInfo']['variables'] if v['name'] in ('rain_day', 'sm_pct')]
        data['multidimensionalInfo']['variables'][0]['dimensions'][0]['values'] = []
        with self.assertRaises(ValueError): variable_check(data)

    def test_corrupt_snapshot_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p/'bad.json').write_text('{}')
            (p/'manifest.json').write_text(json.dumps({'files':[{'file':'bad.json','sha256':'0'*64}]}))
            with self.assertRaises(ValueError): load_verified(p)


@unittest.skipUnless(importlib.util.find_spec('shapely') and importlib.util.find_spec('pyproj'), 'Optional GIS audit dependencies')
class P04GeometryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.data = load_verified(EVIDENCE)

    def test_real_polygon_identity_topology_area_and_blocked_join(self):
        result = verify()
        self.assertTrue(result['geometry']['topology_valid'])
        self.assertAlmostEqual(result['geometry']['computed_area_km2'],1902.459811,places=4)
        self.assertEqual(result['status'],'BLOCKED_NUMERIC_JOIN')
        self.assertIsNone(result['environmental_conclusion'])

    def test_wrong_node_join_fails(self):
        poly = copy.deepcopy(self.data['catchment410033.geojson'])
        poly['features'][0]['properties']['netnodeid'] = -1
        with self.assertRaises(ValueError): spatial_check(poly,self.data['station410033.json'])

    def test_invalid_polygon_is_not_repaired(self):
        poly = copy.deepcopy(self.data['catchment410033.geojson'])
        poly['features'][0]['geometry']['coordinates'] = [[[[0,0],[1,1],[1,0],[0,1],[0,0]]]]
        with self.assertRaises(ValueError): spatial_check(poly,self.data['station410033.json'])

    def test_truncated_station_response_fails(self):
        station = copy.deepcopy(self.data['station410033.json']); station['exceededTransferLimit'] = True
        with self.assertRaises(ValueError): spatial_check(self.data['catchment410033.geojson'],station)
