import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'model_comparison_divergence'/'comparison.py'
SPEC=importlib.util.spec_from_file_location('comparison',PATH)
CMP=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CMP)

class Task1420ComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=ROOT/'model_comparison_divergence'/'tiny_synthetic_comparison_fixtures.json'
        cls.cases={x['comparison_id']:x for x in json.loads(path.read_text())['cases']}

    def test_agreement_preserves_sources_without_combination(self):
        result=CMP.evaluate_fixture(self.cases['cmp-agree'])
        self.assertTrue(result['valid'])
        self.assertIsNone(result['comparison']['combined_value'])

    def test_event_divergence_requires_human_review(self):
        result=CMP.evaluate_fixture(self.cases['cmp-diverge'])
        self.assertTrue(result['valid'])
        self.assertEqual('REQUIRED',result['comparison']['human_review_status'])

    def test_single_event_does_not_claim_systematic_bias(self):
        result=CMP.evaluate_fixture(self.cases['cmp-diverge'])
        self.assertEqual('INSUFFICIENT_WINDOWS',result['comparison']['systematic_bias_status'])

    def test_ood_exclusion_is_preserved(self):
        result=CMP.evaluate_fixture(self.cases['cmp-ood'])
        self.assertTrue(result['valid'])
        self.assertEqual('OOD',result['comparison']['excluded_sources'][0]['reason'])

    def test_ranking_and_averaging_are_prohibited(self):
        with self.assertRaises(PermissionError): CMP.rank_models([])
        with self.assertRaises(PermissionError): CMP.average_disagreement([])

    def test_public_forecast_is_prohibited(self):
        with self.assertRaises(PermissionError): CMP.make_public_forecast({})

if __name__=='__main__': unittest.main()
