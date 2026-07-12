import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'hybrid_forecast_orchestrator' / 'orchestrator.py'
SPEC = importlib.util.spec_from_file_location('hybrid_orchestrator', PATH)
ORCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ORCH)

class Task1380HybridOrchestratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = ROOT / 'hybrid_forecast_orchestrator' / 'tiny_synthetic_orchestrator_fixtures.json'
        cls.cases = {x['case_id']: x for x in json.loads(path.read_text())['cases']}

    def test_parallel_sources_are_preserved_without_combination(self):
        result = ORCH.build_route(self.cases['parallel-aligned'])
        self.assertTrue(result['valid'])
        self.assertEqual(2, len(result['route']['sources']))
        self.assertIsNone(result['route']['numeric_combination'])

    def test_stale_source_requires_and_preserves_human_review(self):
        result = ORCH.build_route(self.cases['stale-ai'])
        self.assertTrue(result['valid'])
        self.assertEqual('REQUIRED', result['route']['human_review_status'])

    def test_insufficient_sources_are_exposed(self):
        result = ORCH.build_route(self.cases['no-reference'])
        self.assertTrue(result['valid'])
        self.assertEqual('INSUFFICIENT_SOURCES', result['route']['disagreement_status'])

    def test_automatic_averaging_is_prohibited(self):
        with self.assertRaises(PermissionError): ORCH.average_sources([])

    def test_automatic_best_source_selection_is_prohibited(self):
        with self.assertRaises(PermissionError): ORCH.select_best_source([])

    def test_live_source_and_public_forecast_are_prohibited(self):
        with self.assertRaises(PermissionError): ORCH.call_live_source({})
        with self.assertRaises(PermissionError): ORCH.public_forecast({})

if __name__ == '__main__':
    unittest.main()
