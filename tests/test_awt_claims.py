"""Meaningful boundary/oracle tests for Issue162, no real emission experiments."""
import copy
import importlib.util
import json
import math
from pathlib import Path
import unittest

T = Path(__file__).resolve().parents[1]/'docs/tasks/climateos_awt_001'
spec = importlib.util.spec_from_file_location('awt_under_test', T/'engine.py')
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)


class AWTTests(unittest.TestCase):
    def f(self, s='B'): return e.read('fixtures/'+s+'.json')
    def p(self, s='B'): return e.read('examples/'+s+'.json')

    def test_schema_valid_all_four_and_nine_types(self):
        for s in 'ABCD':
            e.validate(self.p(s))
            self.assertEqual({n['type'] for n in self.p(s)['entities']},e.TYPES)

    def test_hand_oracle_baseline_and_AD(self):
        r=e.calculate(self.f())
        # Independent longhand: uncollected remainder, pipe loss, combustion slip.
        self.assertAlmostEqual(r['physical_ledger']['landfill']['emitted_kg_CH4'],28350+185+366.3)
        self.assertAlmostEqual(r['physical_ledger']['AD']['emitted_kg_CH4'],1200+588+1164.24)
        self.assertAlmostEqual(r['physical_ledger']['residue_landfill']['emitted_kg_CH4'],7200+20+39.6)
        self.assertAlmostEqual(r['baseline_t_CO2e'],806.11536)
        self.assertAlmostEqual(r['project_t_CO2e'],331.762048)
        self.assertAlmostEqual(r['estimated_net_abatement_t_CO2e'],469.353312)

    def test_physical_CH4_and_carbon_closure(self):
        for c in [0,.24,.37,.75,1]:
            r=e.methane_path(50000,c,.1,.01,.98)
            f=r['flows']
            self.assertAlmostEqual(50000, r['emitted_kg_CH4']+f['oxidized']+f['destroyed'])
            self.assertTrue(all(abs(v)<1e-8 for v in r['residuals'].values()))

    def test_capture_monotonic_given_fixed_assumptions(self):
        vals=[e.calculate(dict(self.f(),capture_fraction=c))['baseline_t_CO2e'] for c in [0,.37,.75,1]]
        self.assertEqual(vals,sorted(vals,reverse=True))

    def test_A_common_baseline_identity_not_independent_uncertainty(self):
        r=e.sensitivity(self.f('A'))
        self.assertEqual(r['bounds'],[0,0])
        self.assertEqual(r['runs'],128)

    def test_corner_envelope_contains_center_and_sign_change(self):
        f=self.f(); r=e.sensitivity(f); v=e.calculate(f)['estimated_net_abatement_t_CO2e']
        self.assertLess(r['bounds'][0],0)
        self.assertLessEqual(r['bounds'][0],v)
        self.assertGreaterEqual(r['bounds'][1],v)
        self.assertEqual(r['runs'],128)

    def test_missing_residual_never_zero(self):
        r=e.assess(self.p('D')); c=r['calculation']
        for k in ['project_t_CO2e','leakage_t_CO2e','estimated_net_abatement_t_CO2e']:
            self.assertIsNone(c[k])
        self.assertEqual(e.sensitivity(self.f('D'))['runs'],0)
        self.assertIn('BASELINE_EVIDENCE_MISSING',r['reasons'])

    def test_missing_leakage_blocks_net(self):
        c=e.calculate(dict(self.f(),leakage_known='UNKNOWN'))
        self.assertIsNone(c['estimated_net_abatement_t_CO2e'])

    def test_omitting_residue_is_not_accepted(self):
        f=self.f(); del f['residue_N2O_kg']
        with self.assertRaises(ValueError): e.calculate(f)

    def test_invalid_physical_parameters(self):
        for v in [-.1,1.1,None,math.nan,math.inf,True,'0.5']:
            with self.subTest(value=v),self.assertRaises((ValueError,TypeError)):
                e.calculate(dict(self.f(),capture_fraction=v))

    def test_carbon_allocation_cannot_exceed_DOC(self):
        with self.assertRaisesRegex(ValueError,'DOUBLE_USE'):
            e.calculate(dict(self.f(),ad_decomposed_fraction=.9,residue_decomposed_fraction=.2))

    def test_outside_authorized_mass_unit_time_real_data(self):
        for k,v in [('waste_t',1001),('waste_unit','t_dry'),('interval','ONE_DAY'),('mode','OBSERVED')]:
            with self.subTest(field=k),self.assertRaises(ValueError): e.calculate(dict(self.f(),**{k:v}))

    def test_no_double_subtraction_energy_or_capture(self):
        r=e.calculate(self.f())
        self.assertEqual(r['energy_export_credit_t_CO2e'],0)
        self.assertAlmostEqual(sum(v for k,v in r['component_t_CO2e'].items() if k!='offsite_only_leakage'),r['project_t_CO2e'])
        self.assertAlmostEqual(r['baseline_t_CO2e']-r['project_t_CO2e']-r['leakage_t_CO2e'],r['estimated_net_abatement_t_CO2e'])

    def test_known_expired_rule_narrow_ineligibility(self):
        r=e.legal_screen(self.p()['legal'])
        self.assertEqual(r['eligibility'],'NOT_ELIGIBLE')
        self.assertEqual(r['reason'],'EXPIRED_METHOD_NEW_REGISTRATION_ONLY')
        self.assertEqual(r['additionality'],'INSUFFICIENT_EVIDENCE')

    def test_legacy_method_not_blanket_disqualified(self):
        r=e.legal_screen(dict(self.p()['legal'],registration='LEGACY_UNVERIFIED'))
        self.assertEqual(r['eligibility'],'INSUFFICIENT_EVIDENCE')

    def test_consultation_never_enacted(self):
        r=e.legal_screen(self.p('C')['legal'])
        self.assertEqual(r['reason'],'CONSULTATION_IS_NOT_ENACTED_METHOD')
        self.assertFalse(r['formal_legal_determination'])

    def test_FOGO_effective_date_exemptions_and_processing_separate(self):
        x=self.p('C')['legal']
        before=e.legal_screen(dict(x,assessment_date='2030-06-30'))
        after=e.legal_screen(x)
        self.assertTrue(before['collection'].startswith('NOT_YET'))
        self.assertTrue(after['collection'].startswith('CONDITIONALLY'))
        self.assertIn('UNKNOWN',e.legal_screen(dict(x,exemption='UNKNOWN'))['collection'])
        self.assertEqual(after['required_processing_pathway'],'AD_SPECIFIC_REQUIREMENT_NOT_ESTABLISHED')
        self.assertEqual(e.legal_screen(dict(x,jurisdiction='OTHER'))['collection'],'UNKNOWN_OUTSIDE_IMPLEMENTED_SCOPE')

    def test_duplicate_risk_not_fraud_or_credit(self):
        d=e.assess(self.p('D'))
        self.assertEqual(len(d['duplicate_risks']),1)
        self.assertIn('NOT_PROVEN',d['duplicate_risks'][0]['status'])
        links=self.p('D')['rights_links'];links[1]['batch']='DIFFERENT_BATCH'
        self.assertEqual(e.overlap(links),[])
        self.assertEqual(len(e.overlap([links[0],links[0]])),1)

    def test_hash_tamper_fail_closed(self):
        for field in ['input_sha256','dataset','output_provenance']:
            p=self.p()
            if field=='dataset':p[field]['sha256']='0'*64
            elif field=='output_provenance':p[field]['engine_sha256']='0'*64
            else:p[field]='0'*64
            r=e.assess(p)
            self.assertEqual(r['assurance'],'CONDITIONS_NOT_MET')
            self.assertIsNone(r['calculation'])

    def test_schema_unknown_extra_or_approval_promotion(self):
        for change in ['extra','mode','approval','entity','code','licence']:
            p=self.p()
            if change=='extra':p['external_endpoint']='https://example.com'
            elif change=='mode':p['mode']='OBSERVED'
            elif change=='approval':p['review']['scientifically_admitted']=True
            elif change=='entity':p['entities'][0]['type']='CERTIFIED'
            elif change=='code':p['output_provenance']['engine']='../../other.py'
            else:p['dataset']['licence']='UNKNOWN'
            self.assertEqual(e.assess(p)['assurance'],'CONDITIONS_NOT_MET')

    def test_no_fake_instrument_or_measurement(self):
        p=self.p();p['observation']['instrument']='Invented flux tower'
        self.assertEqual(e.assess(p)['assurance'],'CONDITIONS_NOT_MET')

    def test_cycles_duplicate_and_dangling_links(self):
        for kind in ['cycle','duplicate','dangling']:
            p=self.p()
            if kind=='cycle':p['entities'][0]['depends_on']=['PHYSICAL_ESTIMATE']
            elif kind=='duplicate':p['entities'][1]['id']=p['entities'][0]['id']
            else:p['entities'][0]['depends_on']=['ABSENT']
            self.assertEqual(e.assess(p)['assurance'],'CONDITIONS_NOT_MET')

    def test_append_revision_preserves_original_and_event_chain(self):
        p=self.p();old=copy.deepcopy(p);changed=copy.deepcopy(p)
        changed['review']['human_notes']=['Proposed note; not independent approval.']
        new=e.revision(p,changed)
        self.assertEqual(p,old);self.assertEqual(new['revision'],2)
        self.assertEqual(new['previous_revision_sha256'],e.prior.digest(old))
        events=e.prior.append_event([],'SUBMITTED','SYNTHETIC_SUBMITTER',e.prior.digest(new))
        self.assertEqual(e.prior.verify_events(events,events[-1]['event_sha256']),'SUBMITTED')
        events[0]['package_sha256']='0'*64
        with self.assertRaises(ValueError):e.prior.verify_events(events,events[-1]['event_sha256'])

    def test_all_science_credits_and_assurance_remain_unapproved(self):
        for s in 'ABCD':
            r=e.assess(self.p(s))
            self.assertEqual(r['science'],'PENDING')
            self.assertEqual(r['assurance'],'INSUFFICIENT_EVIDENCE')
            self.assertEqual(r['credit_quantity'],'NOT_DETERMINED')

    def test_replay_and_saved_output_match(self):
        saved=e.read('evidence/results.json')
        for s in 'ABCD':
            self.assertEqual(e.assess(self.p(s)),saved[s])
            self.assertEqual(e.prior.canonical(e.assess(self.p(s))),e.prior.canonical(e.assess(self.p(s))))

    def test_schema_finite_and_unknown_keyword(self):
        p=self.p();p['revision']=math.nan
        self.assertEqual(e.assess(p)['assurance'],'CONDITIONS_NOT_MET')
        with self.assertRaises(ValueError):e.schema_validate('x',dict(type='string',unknown=True))


if __name__=='__main__': unittest.main()
