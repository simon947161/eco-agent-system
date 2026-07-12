import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'forecast_source_registry' / 'registry.py'
SPEC = importlib.util.spec_from_file_location('source_registry', PATH)
REGISTRY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REGISTRY)

class Task1300SourceRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / 'forecast_source_registry' / 'tiny_synthetic_source_fixtures.json'
        cls.cases = {x['source_id']: x for x in json.loads(path.read_text())['cases']}

    def test_all_eight_states_are_preserved(self):
        self.assertEqual(8, len(REGISTRY.STATES))

    def test_complete_candidate_is_valid(self):
        result = REGISTRY.validate_source(self.cases['synthetic-complete'])
        self.assertTrue(result['valid'])

    def test_customer_experiment_blocked_without_controls(self):
        result = REGISTRY.validate_source(self.cases['synthetic-customer'])
        self.assertFalse(result['valid'])
        self.assertEqual('customer_experiment_controls_missing', result['blockers'][0]['code'])

    def test_source_connection_is_prohibited(self):
        with self.assertRaises(PermissionError):
            REGISTRY.connect_source({})

    def test_customer_activation_is_prohibited(self):
        with self.assertRaises(PermissionError):
            REGISTRY.activate_customer_experiment({})

    def test_controlled_candidates_are_structurally_valid(self):
        path = ROOT / 'forecast_source_registry' / 'controlled_candidate_registry.json'
        results = REGISTRY.load_registry(path)
        self.assertEqual(5, len(results))
        self.assertTrue(all(item['valid'] for item in results))

if __name__ == '__main__':
    unittest.main()
