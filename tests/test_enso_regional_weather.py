"""Synthetic QC tests and real acquisition-failure tests; no synthetic probabilities."""
import unittest
from cczps_lite.integration import enso_regional_weather as e

class ENSORegionalWeatherTests(unittest.TestCase):
    def test_fixed_failure_has_no_probabilities(self):
        v=e.evaluate(e.request()); self.assertEqual(v['status'],'DATA_NOT_READY')
        self.assertEqual(v['probabilities'],[]);self.assertIsNone(v['numerical_output'])
    def test_no_fallback_to_index_persistence(self):
        v=e.evaluate(e.request()); self.assertEqual(v['paired_years'],0)
        self.assertTrue(v['atlas_trace_context']['does_not_supply_rain_probability'])
    def test_science_gates(self):
        v=e.evaluate(e.request());self.assertEqual(v['scientific_admission'],'PENDING')
        self.assertFalse(v['deployed']);self.assertFalse(v['certified'])
    def test_missing_ecoengine_is_low(self):
        v=e.evaluate(e.request())['ecoengine_evidence']
        self.assertEqual(v['strength'],'low');self.assertEqual(v['indicators'],[])
    def test_unknown_territory_not_state_average(self):
        r=e.request();r['spatial_support']='all_NSW';self.assertRaises(ValueError,e.validate_request,r)
    def test_wrong_index_version(self):
        r=e.request();r['index_version']='ONI';self.assertRaises(ValueError,e.validate_request,r)
    def test_utc_instant_rejected(self):
        r=e.request();r['temporal_support']='UTC_midnight';self.assertRaises(ValueError,e.validate_request,r)
    def test_wrong_season(self):
        r=e.request();r['mode']=['SON','JJA'];self.assertRaises(ValueError,e.validate_request,r)
    def test_missing_zero_imputation_rejected(self):
        r=e.request();r['missing_policy']='ZERO';self.assertRaises(ValueError,e.validate_request,r)
    def test_causal_claim_rejected(self):
        r=e.request();r['claim']='ENSO_CAUSED_DROUGHT';self.assertRaises(ValueError,e.validate_request,r)
    def test_certification_rejected(self):
        r=e.request();r['authority']='CERTIFY';self.assertRaises(ValueError,e.validate_request,r)
    def test_policy_score_not_physics(self):
        r=e.request();r['policy_score']=50;self.assertRaises(ValueError,e.validate_request,r)
    def test_wrong_rain_unit(self):
        self.assertRaises(ValueError,e.monthly_qc,50,unit='mm')
    def test_qc_flag_excludes(self):
        self.assertIsNone(e.monthly_qc(100,quality='O')['mm'])
    def test_missing_days_excludes(self):
        self.assertFalse(e.monthly_qc(100,measurement='A')['eligible'])
    def test_trace_not_zero(self):
        self.assertIsNone(e.monthly_qc(-1)['mm'])
    def test_missing_sentinel_not_zero(self):
        self.assertIsNone(e.monthly_qc(-9999)['mm'])
    def test_blank_flag_does_not_prove_daily_complete(self):
        v=e.monthly_qc(123);self.assertEqual(v['mm'],12.3);self.assertEqual(v['daily_completeness'],'UNKNOWN')
    def test_true_zero_allowed(self): self.assertEqual(e.monthly_qc(0)['mm'],0)
    def test_unknown_flags_reject(self):
        for kw in ({'source':'Q'},{'quality':'Z'},{'measurement':'F'}): self.assertRaises(ValueError,e.monthly_qc,100,**kw)
    def test_nan_rejected(self): self.assertRaises(ValueError,e.monthly_qc,float('nan'))
    def test_fixed_weights_no_available_case_reweight(self):
        self.assertIsNone(e.fixed_panel([10,None,20],3));self.assertEqual(e.fixed_panel([10,20,30],3),20)
    def test_station_support_rejected(self): self.assertRaises(ValueError,e.fixed_panel,[10,20],3)
    def test_all_months_required(self):
        self.assertIsNone(e.seasonal_total({6:10,7:None,8:20},'JJA'))
    def test_month_alignment(self): self.assertRaises(ValueError,e.seasonal_total,{5:10,6:10,7:10},'JJA')
    def test_tie_is_neither(self): self.assertEqual(e.event(10,10),'neither')
    def test_missing_event_stays_null(self): self.assertIsNone(e.event(None,10))
    def test_fips_country_regression(self):
        line=e.read(e.TASK/'REGIONS.json')['regions'][0]['stations'][0]['inventory_line']
        self.assertTrue(e.inventory_row(line)['id'].startswith('AS'))
        self.assertRaises(ValueError,e.inventory_row,'AU'+line[2:])
    def test_selected_before_rain_attempt(self):
        a=e.read(e.TASK/'REGIONS.json');b=e.read(e.TASK/'evidence/archive-receipt.json')
        self.assertLess(a['selected_utc'],b['started_utc']);self.assertTrue(a['before_rain_values'])
    def test_plan_was_frozen(self):
        a=e.read(e.TASK/'evidence/inventory-receipt.json');b=e.read(e.TASK/'evidence/archive-receipt.json')
        self.assertEqual(a['plan_sha256'],b['plan_sha256']);self.assertEqual(a['preregistration_sha256'],b['preregistration_sha256'])
    def test_repeat_is_deterministic(self): self.assertEqual(e.evaluate(e.request()),e.evaluate(e.request()))
    def test_no_temperature_inference(self): self.assertEqual(e.evaluate(e.request())['hot'],'NOT_ASSESSED')

if __name__=='__main__': unittest.main()
