"""Independent arithmetic anchors and adversarial research-admission boundaries."""
import copy
import hashlib
import math
import unittest
from unittest.mock import patch
from cczps_lite.integration import physical_process_trajectory as t

class TrajectoryTests(unittest.TestCase):
    def request(self,example='CH4'):
        return dict(version=t.VERSION,example=example,authority='BOUNDED_RESEARCH_ONLY',scope='FROZEN_EVIDENCE_NO_CAUSAL_EXTRAPOLATION')

    def test_noaa_published_rounding_anchor(self):
        r=t.radiation()
        self.assertEqual(round(r['ERF_W_m2'],3),.569)
        self.assertLess(abs(r['rounding_residual_W_m2']),.0005)
        self.assertIsNone(r['temperature_K'])

    def test_preindustrial_zero_and_domain(self):
        self.assertEqual(t.ch4_erf(729.2,338.86)['ERF_W_m2'],0)
        for M,N in [(0,338),(1936,-1),(5000,338),(float('nan'),338)]:
            with self.assertRaises(ValueError): t.ch4_erf(M,N)

    def test_ppm_and_local_basis_refused(self):
        for unit in ('ppm','ppb_local','kg/m3','W/m2'):
            with self.assertRaisesRegex(ValueError,'UNIT'): t.ch4_erf(1936,338,unit=unit)

    def test_liquid_or_wet_basis_refused(self):
        for phase in ('dissolved','wet_air_mole_fraction'):
            with self.assertRaisesRegex(ValueError,'PHASE'): t.ch4_erf(1936,338,phase=phase)

    def test_derivatives_vs_independent_central_difference(self):
        M,N=1936.03,338.86; h=.01; r=t.ch4_erf(M,N)
        dm=(t.ch4_erf(M+h,N)['ERF_W_m2']-t.ch4_erf(M-h,N)['ERF_W_m2'])/(2*h)
        dn=(t.ch4_erf(M,N+h)['ERF_W_m2']-t.ch4_erf(M,N-h)['ERF_W_m2'])/(2*h)
        self.assertAlmostEqual(dm,r['dF_dM'],places=12); self.assertAlmostEqual(dn,r['dF_dN'],places=12)
        self.assertLess(dn,0) # N2O overlap, not an unqualified positive sum.

    def test_model_error_not_measurement_ci(self):
        r=t.radiation()
        self.assertGreater(r['formula_10_percent_scale_W_m2'],100*r['propagated_abundance_u_if_independent_W_m2'])
        self.assertTrue(r['model_scale_not_CI'])

    def test_synthetic_energy_conservation_and_imbalance(self):
        self.assertEqual(t.energy_residual(10,8,60,120),0)
        self.assertEqual(t.energy_residual(10,8,60,100),20)
        with self.assertRaisesRegex(ValueError,'ENERGY_UNITS'): t.energy_residual(10,8,60,120,units=('W','s','K'))

    def test_frozen_methane_mass_and_carbon(self):
        old=t.legacy()
        self.assertEqual(old['PR143']['status'],'SYNTHETIC_ONLY')
        for fixture,expected in [('uncaptured',95),('capture_flare',32.7),('oxidation_leaks',31.08)]:
            r=old['PR144'][fixture]; self.assertAlmostEqual(r['emitted_kg_CH4'],expected)
            self.assertEqual(r['carbon_in_kg_C'],r['carbon_out_plus_stock_kg_C'])
            self.assertTrue(all(abs(v)<1e-12 for v in r['residuals'].values()))

    def test_roni_raw_hash_and_fixed_window(self):
        raw=(t.TASK/'evidence/RONI.ascii.txt').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),'1297887f581b6190e459cbbf8bdec9a703ff65c1a229e2de4dd94285254f35c8')
        rows=t.parse_roni(raw)
        self.assertEqual(sum(1961<=y<=2020 for y,s in rows),720)

    def test_duplicate_missing_and_sentinel_index(self):
        raw=(t.TASK/'evidence/RONI.ascii.txt').read_bytes()
        with self.assertRaisesRegex(ValueError,'DUPLICATE'): t.parse_roni(raw+b'\nSON 1961 -0.2\n')
        lines=raw.splitlines(); missing=b'\n'.join(l for l in lines if not (b'SON' in l and b'1961' in l))
        with self.assertRaisesRegex(ValueError,'MISSING'): t.parse_roni(missing)
        with self.assertRaisesRegex(ValueError,'INDEX_QC'): t.parse_roni(raw+b'\nSON 3000 -99.99\n')

    def test_threshold_inclusive_not_five_event_rule(self):
        self.assertEqual([t.phase(v) for v in (-.5,-.49,.49,.5)],['cold','neutral','neutral','warm'])

    def test_independent_historical_count_and_lag(self):
        # Direct row filter independent of enso() grouping/bootstrapping code.
        rows=t.parse_roni((t.TASK/'evidence/RONI.ascii.txt').read_bytes())
        warm=[y for y in range(1961,2021) if rows[y,'JJA']>=.5]
        successes=[y for y in warm if rows[y,'SON']>=.5]
        self.assertEqual((len(warm),len(successes)),(14,13))
        self.assertEqual(set(warm)-set(successes),{1992})
        # JJA and SON do not overlap. Retrospective smoothing is still a caveat.
        self.assertTrue(set((6,7,8)).isdisjoint((9,10,11)))

    def test_bootstrap_degeneracy_not_certainty(self):
        b=t.enso(); cold=b['JJA_to_SON_persistence']['cold']
        self.assertEqual((cold['k'],cold['n']),(10,10))
        self.assertLess(cold['nominal_iid_Wilson95'][0],.73)
        self.assertEqual(cold['block_bootstrap'][0]['p_interval'],[1,1])
        self.assertIsNone(b['weather_probability'])

    def test_bootstrap_reproducible_and_block_lengths(self):
        pairs=[('warm','warm'),('neutral','cold'),('warm','neutral'),('cold','cold')]*15
        self.assertEqual(t.block_intervals(pairs,'warm',3),t.block_intervals(pairs,'warm',3))
        self.assertEqual(t.block_intervals(pairs,'warm',5)['valid'],2000)

    def test_wilson_not_probability_one(self):
        lo,hi=t.wilson(10,10); self.assertLess(lo,1); self.assertAlmostEqual(hi,1)
        with self.assertRaises(ValueError): t.wilson(0,0)

    def test_known_water_ledger_and_covariance_cancellation(self):
        nodes,v,sd=t.water_fixture(); r=t.water_balance(nodes,v,sd)
        self.assertEqual(r['residual_m3'],0)
        # Eight independent external rate terms, nine P/E/storage terms.
        self.assertAlmostEqual(r['whole_chain_u_m3'],math.sqrt(8*8640**2+9*100**2))
        self.assertLess(r['whole_chain_u_m3'],r['incorrect_independent_node_u_m3'])
        self.assertEqual(set(r['cancelled_internal_terms']),{'q12','q23'})

    def test_internal_flow_perturbation_cancels_not_nodes(self):
        nodes,v,sd=t.water_fixture(); v['q12']+=123
        r=t.water_balance(nodes,v,sd)
        self.assertEqual([n['residual_m3'] for n in r['nodes']],[-123,123,0])
        self.assertEqual(r['residual_m3'],0)

    def test_external_residual_not_evaporation(self):
        nodes,v,sd=t.water_fixture(); v['q3']+=8640
        r=t.water_balance(nodes,v,sd); self.assertEqual(r['residual_m3'],-8640)
        self.assertIsNone(r['attribution'])

    def test_unknown_lateral_and_storage_never_zero_filled(self):
        for key in ('l2','s1'):
            nodes,v,sd=t.water_fixture(); v[key]=None; r=t.water_balance(nodes,v,sd)
            self.assertEqual(r['status'],'BLOCKED_MISSING_DATA'); self.assertIsNone(r['residual_m3'])

    def test_water_unit_and_time_mismatch(self):
        for field,value,error in [('unit','mm/day','WATER_UNIT'),('interval','LOCAL_DST_UNKNOWN','TIME_SUPPORT')]:
            nodes,v,sd=t.water_fixture(); nodes[0][field]=value
            with self.assertRaisesRegex(ValueError,error): t.water_balance(nodes,v,sd)

    def test_hrs_unreliable_complete_is_not_validated_flow(self):
        r=t.hydro()['real_fragment']; self.assertEqual(r['quality_counts'],{'E':31})
        self.assertEqual(r['absent_dates'],[]); self.assertIsNone(r['physical_volume_sum'])
        self.assertEqual(r['balance_status'],'BLOCKED_MISSING_DATA')

    def test_scorecard_not_reproduced_and_not_sent(self):
        r=t.scorecard(); self.assertEqual((r['diagnostic_score'],r['published_historical_label']),(40,50))
        self.assertFalse(r['score_wrong_proven']); self.assertEqual(r['contact_status'],'NOT_SENT')

    def test_extra_policy_score_cannot_enter_physics(self):
        r=self.request(); r['score']=50
        with self.assertRaisesRegex(ValueError,'REQUEST_SCHEMA'): t.evaluate(r)

    def test_no_sample_extrapolation_or_causal_claim(self):
        for scope in ('GLOBAL_FORECAST','ENSO_CAUSES_DROUGHT','NILE_FROM_COOMA'):
            r=self.request('ENSO'); r['scope']=scope
            with self.assertRaisesRegex(ValueError,'SCOPE_CAUSALITY'): t.evaluate(r)

    def test_no_authority_or_version_expansion(self):
        for key,value,error in [('authority','SCIENCE_APPROVED','UNAUTHORIZED'),('version','old','VERSION')]:
            r=self.request(); r[key]=value
            with self.assertRaisesRegex(ValueError,error): t.evaluate(r)

    def test_missing_version_fake_citation_and_false_completion(self):
        original=t.read
        for mutation,error in [
            (lambda d:d[0]['source_version_locator'][0].update(id='FAKE_DOI'),'SOURCE_VERSION'),
            (lambda d:d[0]['source_version_locator'][0].update(version='invented'),'SOURCE_VERSION'),
            (lambda d:d[0].update(source_version_locator=[]),'MISSING_SOURCE'),
            (lambda d:d[3].update(numerical_output=1.2),'FALSE_NUMERIC_COMPLETION')]:
            data=copy.deepcopy(original(t.TASK/'TRAJECTORIES.json')); mutation(data)
            def reader(path): return data if path.name=='TRAJECTORIES.json' else original(path)
            with patch.object(t,'read',side_effect=reader):
                with self.assertRaisesRegex(ValueError,error): t.load(False)

    def test_all_five_examples_and_original_atlas_trace(self):
        for key in ('CH4','ENSO','HYDRO','CROSS','SCORECARD'):
            r=t.evaluate(self.request(key)); self.assertEqual(r['scientific_admission'],'PENDING')
            self.assertFalse(r['certification']); self.assertFalse(r['deployed'])
        for key in ('CH4','ENSO','HYDRO'):
            r=t.trace(key); self.assertFalse(r['whole_chain_calculable']); self.assertTrue(r['trajectory'])

if __name__=='__main__': unittest.main()
