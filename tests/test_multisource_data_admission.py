"""Real payload checks plus explicitly synthetic negative fixtures; no network."""
import copy, importlib.util, unittest
from unittest.mock import patch
from cczps_lite.integration import multisource_data_admission as m

class AdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qc,cls.monthly,cls.seasons,cls.roni=m.intake()
        cls.pairs,cls.results,cls.counter=m.analyse(cls.seasons,cls.roni)
        cls.son=cls.results[1];cls.lag=cls.results[2]
        spec=importlib.util.spec_from_file_location('independent_audit',m.TASK/'scripts/independent_audit.py')
        a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a);cls.exact=a.audit()
    def good(self):return {'source_id':'fixture','research_use_permitted':True,'geographic_coverage':['Australia'],'baseline_years_available':30,'payload_available':True}
    def reject_request(self,k,v):
        r=m.request();r[k]=v
        with self.assertRaises(ValueError):m.contract(r)
    def test_404_fallback(self):
        a=dict(self.good(),source_id='failed',http_status=404);r=m.fallback([a,self.good()])
        self.assertEqual(r['candidate'],'fixture');self.assertEqual(r['trace'][0]['decision'],'NOT_FOUND_404')
    def test_403_no_bypass(self):
        r=m.fallback([dict(self.good(),http_status=403)]);self.assertIsNone(r['candidate']);self.assertFalse(r['trace'][0]['network_executed'])
    def test_499_no_bypass(self):self.assertEqual(m.source_gate(dict(self.good(),http_status=499)),'ACCESS_RESTRICTED')
    def test_auth_missing(self):self.assertEqual(m.source_gate(dict(self.good(),auth_required=True)),'AUTH_REQUIRED')
    def test_license_unknown(self):self.assertEqual(m.source_gate(dict(self.good(),research_use_permitted=False)),'LICENCE_UNCLEAR')
    def test_china_not_australia(self):self.assertEqual(m.source_gate(dict(self.good(),geographic_coverage=['China'])),'TIME_SUPPORT_MISMATCH')
    def test_nasa_short_baseline(self):self.assertEqual(m.source_gate(dict(self.good(),baseline_years_available=10)),'TIME_SUPPORT_MISMATCH')
    def test_payload_unavailable(self):self.assertEqual(m.source_gate(dict(self.good(),payload_available=False)),'PAYLOAD_INVALID')
    def test_registry_fallback_real(self):self.assertEqual(m.fallback(m.read(m.TASK/'SOURCE_REGISTRY.json'))['candidate'],m.SOURCE)
    def test_roni_wrong_version(self):self.reject_request('index_version','ONI_v5')
    def test_wrong_rain_unit(self):self.reject_request('unit','mm/day')
    def test_wrong_time_basis(self):self.reject_request('time_basis','UTC_00_00')
    def test_interpolated_not_observed(self):self.reject_request('data_kind','interpolated_grid')
    def test_source_version_switch(self):self.reject_request('source_id','latest_other_source')
    def test_synthetic_not_observed(self):self.reject_request('authorship','SYNTHETIC')
    def test_no_zero_imputation(self):self.reject_request('missing_policy','ZERO')
    def test_no_causal_claim(self):self.reject_request('claim','ENSO_CAUSES_LOCAL_RAIN')
    def test_no_certification(self):self.reject_request('authority','SCIENTIFICALLY_ADMITTED')
    def test_no_added_authority(self):self.reject_request('deployment',True)
    def one(self,**kw):
        row=['ASN00072150','Wagga','-35.1583','147.4573','212','196101','100','','','D','1']
        for k,v in kw.items():row[int(k)]=v
        return (','.join(row)+'\n').encode()
    def test_country_as_not_au(self):
        with self.assertRaisesRegex(ValueError,'FIPS'):m.parse_station(self.one(**{'0':'AUN00072150'}),m.STATIONS[0])
    def test_station_outside_region(self):
        with self.assertRaisesRegex(ValueError,'REGION_SUPPORT'):m.parse_station(self.one(**{'2':'35'}),m.STATIONS[0])
    def test_invalid_month(self):
        with self.assertRaisesRegex(ValueError,'MONTH_RANGE'):m.parse_station(self.one(**{'5':'196113'}),m.STATIONS[0])
    def test_duplicate_month(self):
        with self.assertRaisesRegex(ValueError,'DUPLICATE'):m.parse_station(self.one()*2,m.STATIONS[0])
    def test_unknown_flag(self):
        with self.assertRaisesRegex(ValueError,'UNKNOWN'):m.parse_station(self.one(**{'8':'?'}),m.STATIONS[0])
    def test_trace_not_zero(self):self.assertIsNone(m.parse_station(self.one(**{'6':'-1'}),m.STATIONS[0])[0][1961,1]['rain_mm'])
    def test_measurement_flag_excluded(self):self.assertIsNone(m.parse_station(self.one(**{'7':'A'}),m.STATIONS[0])[0][1961,1]['rain_mm'])
    def test_quality_flag_excluded(self):self.assertIsNone(m.parse_station(self.one(**{'8':'S'}),m.STATIONS[0])[0][1961,1]['rain_mm'])
    def test_units_conversion(self):self.assertEqual(m.parse_station(self.one(),m.STATIONS[0])[0][1961,1]['rain_mm'],10)
    def test_blank_flag_not_daily_complete(self):self.assertEqual(m.parse_station(self.one(),m.STATIONS[0])[1]['daily_completeness'],'UNKNOWN_for_blank_M')
    def test_missing_station_not_renormalized(self):self.assertIsNone(m.previous.fixed_panel([1,None,2],3))
    def test_season_months_mismatch(self):
        with self.assertRaisesRegex(ValueError,'MONTH_SEASON'):m.previous.seasonal_total({6:1,7:2,9:3},'JJA')
    def test_year_alignment(self):
        s=copy.deepcopy(self.seasons);s['SON'][0]['year']=1962
        with self.assertRaisesRegex(ValueError,'ANNUAL_ALIGNMENT'):m.analyse(s,self.roni,repeats=1)
    def test_season_alignment(self):
        s=copy.deepcopy(self.seasons);s['SON'][0]['season']='JJA'
        with self.assertRaisesRegex(ValueError,'SEASON_ALIGNMENT'):m.analyse(s,self.roni,repeats=1)
    def test_missing_index(self):
        r=dict(self.roni);del r[1992,'SON']
        with self.assertRaisesRegex(ValueError,'RONI_ALIGNMENT'):m.analyse(self.seasons,r,repeats=1)
    def test_real_station_qc(self):self.assertEqual([q['present_months'] for q in self.qc],[691,700,667]);self.assertEqual(sum(r['rain_mm'] is not None for r in self.monthly),585)
    def test_jja_blocked_23(self):self.assertEqual(self.results[0]['gate']['valid_baseline_seasons'],23);self.assertIsNone(self.results[0]['probabilities'])
    def test_son_admitted_26_46(self):self.assertEqual(self.son['gate']['valid_baseline_seasons'],26);self.assertEqual(self.son['gate']['valid_analysis_seasons'],46)
    def test_raw_rational_recomputation(self):
        for result in self.results:
            exact=self.exact[result['mode']]
            self.assertEqual(exact['valid_baseline'],result['gate']['valid_baseline_seasons'])
            if not exact['gate']:continue
            self.assertAlmostEqual(exact['threshold_mm'],result['thresholds_mm']['median_1961_1990'])
            for p in m.PHASES:
                for event in ('dry','wet'):
                    v=result['events'][event]['primary']['phase'][p]
                    self.assertEqual((v['k'],v['n']),(exact['counts'][p][event],exact['counts'][p]['n']))
            for row in (r for r in self.pairs if r['mode']==result['mode'] and r['rain_mm'] is not None):
                self.assertAlmostEqual(row['rain_mm'],exact['exact_rain_mm'][row['year']]);self.assertEqual(row['phase'],exact['phases'][row['year']])
    def test_real_son_counts(self):self.assertEqual([(self.son['events']['dry']['primary']['phase'][p]['k'],self.son['events']['dry']['primary']['phase'][p]['n']) for p in m.PHASES],[(13,17),(3,10),(9,19)])
    def test_extreme_threshold_ties_exact(self):
        for result in (self.son,self.lag):
            for p in m.PHASES:
                for event in ('extreme_dry','extreme_wet'):
                    self.assertEqual(result[event]['phase'][p]['k'],self.exact[result['mode']]['counts'][p][event])
    def test_historical_adapter_not_recent(self):
        result=m.evaluate(m.request(),verify_hashes=False,repeats=2)
        self.assertNotIn('recent rainfall',result['ecoengine']['indicators'])
        self.assertEqual(result['scientific_admission'],'PENDING');self.assertFalse(result['deployed'])
    def test_same_weather_not_92_independent_years(self):self.assertEqual(len({r['year'] for r in self.pairs if r['rain_mm'] is not None}),46);self.assertEqual(sum(r['rain_mm'] is not None for r in self.pairs),92)
    def test_1992_only_lag_counterexample(self):
        rows=[r for r in self.counter if r['year']==1992];self.assertEqual(len(rows),1);self.assertEqual(rows[0]['mode'],'JJA_SON');self.assertAlmostEqual(rows[0]['rain_mm'],267.3666666666667)
    def test_small_sample_not_certain(self):
        s=m.summary([{'rain_mm':0,'phase':'warm'}],1,'dry')['phase']['warm'];self.assertEqual(s['sample_warning'],'LOW_N');self.assertLess(s['wilson95'][0],1)
    def test_zero_group_no_probability(self):self.assertIsNone(m.summary([],1,'dry')['phase']['cold']['p'])
    def test_tie_neither(self):self.assertEqual(m.previous.event(1,1),'neither');self.assertEqual(m.event_number(1,1,'dry'),0);self.assertEqual(m.event_number(1,1,'wet'),0)
    def test_year_blocks_keep_adjacency(self):
        for sample in m.block_samples(60,3,10):
            self.assertEqual(len(sample),60)
            for i in range(0,60,3):self.assertEqual([(sample[i]+j)%60 for j in range(3)],sample[i:i+3])
    def test_unstable_bootstrap_not_certain(self):self.assertEqual(m.interval([.5]*5,2000)['status'],'UNSTABLE_SUPPORT')
    def test_block5_warm_cold_includes_zero(self):self.assertLess(self.son['events']['dry']['blocks'][1]['warm_minus_cold']['percentile95'][0],0)
    def test_holdout_no_training_leakage(self):
        rows=[r.copy() for r in self.pairs if r['mode']=='SON_SON'];old=m.holdout(rows)
        for r in rows:
            if r['year']>=1991 and r['rain_mm'] is not None:r['rain_mm']*=100
        new=m.holdout(rows);self.assertEqual(old['threshold_mm'],new['threshold_mm']);self.assertEqual(old['events']['dry']['training_probability'],new['events']['dry']['training_probability'])
    def test_holdout_brier_independent(self):
        h=self.son['holdout']['events']['dry'];pred=h['predictions'];self.assertEqual(len(pred),20)
        self.assertAlmostEqual(sum((r['p']-r['event'])**2 for r in pred)/20,h['brier_phase'])
    def test_registry_hash_drift(self):
        actual=m.read
        def read(p):
            x=actual(p)
            if p.name=='SOURCE_REGISTRY.json':next(s for s in x if s['source_id']==m.SOURCE)['raw_bytes_sha256'][m.STATIONS[0]]='0'*64
            return x
        with patch.object(m,'read',side_effect=read),self.assertRaisesRegex(ValueError,'REGISTRY_HASH'):m.intake()
    def test_raw_hash_drift(self):
        with patch.object(m,'parse_station',side_effect=AssertionError('must not parse')):
            actual=m.read
            def read(p):
                x=actual(p)
                if p.name=='DOWNLOAD_RECEIPTS.json':x[0]['sha256']='0'*64
                if p.name=='SOURCE_REGISTRY.json':next(s for s in x if s['source_id']==m.SOURCE)['raw_bytes_sha256'][m.STATIONS[0]]='0'*64
                return x
            with patch.object(m,'read',side_effect=read),self.assertRaisesRegex(ValueError,'RAW_HASH'):m.intake()
    def test_manifest_and_preregistration(self):
        m.verify();manifest=m.read(m.TASK/'evidence/manifest.json')
        for station in m.STATIONS:
            self.assertIn((m.TASK/'evidence/raw'/f'{station}.csv').relative_to(m.ROOT).as_posix(),manifest['byte_exact'])
    def test_legacy_gate_unchanged(self):self.assertEqual(m.previous.evaluate(m.previous.request())['status'],'DATA_NOT_READY')

if __name__=='__main__':unittest.main()
