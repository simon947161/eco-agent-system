import unittest
import audit_observations as a

class AuditTests(unittest.TestCase):
    def test_missing_and_finite(self):
        for value in ('nan', 'inf', '-999.999', '-99'):
            self.assertFalse(a.valid(value))
        self.assertTrue(a.valid('0'))
        self.assertTrue(a.valid('-27', -273.14))
        self.assertFalse(a.valid('-999.9', -273.14))

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            a.unique([('2024-01-01T00:00:00Z', 1)] * 2)

    def test_non_utc_and_mid_hour_rejected(self):
        for time in ('2024-01-01T00:00:00+01:00','2024-01-01T00:30:00Z'):
            with self.assertRaises(ValueError):
                a.unique([(time, 1)])

    def test_unknown_precision_stops(self):
        self.assertFalse(a.precision_gate({}))
        self.assertFalse(a.precision_gate({'pressure_uncertainty': 1}))

    def test_real_data_waterfall_and_gate(self):
        r = a.audit((a.HERE/'evidence/ch4_brw_2024_subset.txt').read_text(),
                    (a.HERE/'evidence/met_brw_2024.txt').read_text())
        self.assertEqual(r['exact_utc_overlap'], sum(r['exclusive_losses'].values()) + r['complete_background_timestamp_matches'])
        self.assertEqual(r['expected_hours'],r['met_absent_hours']+r['met_rows'])
        self.assertEqual(r['science_eligible_pairs'],0)
        self.assertFalse(r['numerical_comparison_run'])
        self.assertEqual(set(r['intake_heights_m']), {'9.9','35.05'})

if __name__ == '__main__':
    unittest.main()
