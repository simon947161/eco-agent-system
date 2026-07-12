import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'common_weather_data' / 'validator.py'
SPEC = importlib.util.spec_from_file_location('common_weather_validator', PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

class Task1340CommonWeatherDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / 'common_weather_data' / 'tiny_synthetic_common_weather_fixtures.json'
        cls.records = {x['record_id']: x for x in json.loads(path.read_text())['records']}

    def test_complete_deterministic_record_is_valid(self):
        self.assertTrue(VALIDATOR.validate_record(self.records['synthetic-deterministic'])['valid'])

    def test_ensemble_member_id_is_required(self):
        result = VALIDATOR.validate_record(self.records['synthetic-ensemble-missing-member'])
        self.assertFalse(result['valid'])
        self.assertIn('ensemble_member_id_required', {x['code'] for x in result['blockers']})

    def test_valid_time_must_equal_run_plus_lead(self):
        result = VALIDATOR.validate_record(self.records['synthetic-time-mismatch'])
        self.assertFalse(result['valid'])
        self.assertIn('valid_time_lead_mismatch', {x['code'] for x in result['blockers']})

    def test_grid_spacing_does_not_supply_effective_resolution(self):
        record = dict(self.records['synthetic-deterministic'])
        record['spatial'] = dict(record['spatial'])
        record['spatial']['effective_resolution_status'] = ''
        self.assertFalse(VALIDATOR.validate_record(record)['valid'])

    def test_live_ingestion_is_prohibited(self):
        with self.assertRaises(PermissionError):
            VALIDATOR.ingest_live_data({})

    def test_task1380_orchestration_is_prohibited(self):
        with self.assertRaises(PermissionError):
            VALIDATOR.orchestrate_sources({})

if __name__ == '__main__':
    unittest.main()
