import unittest
from validate_intake import audit

class IntakeEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.q,cls.rows=audit()
    def test_measured_export_same_source_not_independent(self):
        self.assertTrue(self.q['plotting_input_exact_match'])
        self.assertEqual(self.q['independent_dataset_count'],1)
        self.assertEqual(len(self.rows),23)
    def test_published_flow_summary_reproduced_but_not_time_mean(self):
        self.assertAlmostEqual(self.q['flow']['row_arithmetic_mean_lps'],18.02925980951026,places=10)
        self.assertEqual(self.q['flow']['unique_timestamps'],311)
        self.assertGreater(self.q['flow']['excess_rows_on_repeated_time'],0)
        self.assertFalse(self.q['flow']['physical_time_mean_established'])
        self.assertFalse(self.q['flow']['join_to_methane_performed'])
    def test_missing_timezone_prevents_utc_claim(self):
        self.assertIsNone(self.q['timezone'])
        self.assertFalse(self.q['utc_conversion_performed'])
    def test_descriptive_statistics_independent_sum(self):
        values=[v for t,v in self.rows]
        self.assertAlmostEqual(sum(values)/23,9.898099434782608,places=10)
        self.assertEqual(sorted(values)[11],self.q['median'])
        self.assertEqual(self.q['elapsed_hours'],23)
    def test_measurement_phases_and_science_gates(self):
        self.assertIn('dissolved',self.q['unit'])
        self.assertEqual(self.q['D3'],'DATA_NOT_READY')
        self.assertEqual(self.q['P1-A'],'PENDING')
        methane=[s for s in self.q['feed_schema'] if s['label']=='Methane (SCH4)'][0]
        self.assertIn('mg COD/L',methane['unit_or_header'])
        self.assertNotEqual(methane['unit_or_header'],self.q['unit'])

if __name__=='__main__': unittest.main(verbosity=2)
