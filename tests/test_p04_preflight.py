import unittest
from tools.p04_water_soil_climate_preflight import preflight


class P04PreflightTests(unittest.TestCase):
    def test_calendar_quality_audit_does_not_create_a_scientific_result(self):
        result=preflight()
        self.assertEqual(len(result['monthly_water_availability']),312)
        self.assertEqual(next(m for m in result['monthly_water_availability'] if m['year_month']=='2000-02')['expected_calendar_labels'],29)
        for month in result['monthly_water_availability']:
            self.assertEqual(sum(month['quality_counts'].values()),month['records'])
            self.assertLessEqual(month['a_b_nonnull_days'],month['records'])
        self.assertIsNone(result['environmental_conclusion'])
        self.assertIsNone(result['causal_conclusion'])
        self.assertTrue(result['missing_dependencies'])


if __name__=='__main__':unittest.main()
