import copy
import json
from pathlib import Path
import sys
import unittest

T=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(T))
import reviewer as r
import check_open_fragment as fragment

class ReviewTests(unittest.TestCase):
    def setUp(self): self.a=r.load('examples/A.json')
    def assert_block(self,p,reason=None):
        out=r.review(p)
        self.assertEqual(out['status'],'MATERIAL_CONTRADICTION')
        self.assertEqual(out['REGULATORY_CERTIFICATION'],'NOT_PROVIDED')
        if reason: self.assertIn(reason,json.dumps(out))
    def test_three_outcomes(self):
        for name,status in [('A','METHOD_ALIGNED'),('B','MATERIAL_CONTRADICTION'),('C','EVIDENCE_INSUFFICIENT')]:
            self.assertEqual(r.review(r.load('examples/'+name+'.json'))['status'],status)
    def test_manual_mass_oracles(self):
        results=r.review(self.a)['claims']
        for c,emitted,consumed,lateral in zip(results,[95,32.7,31.08],[0,62.3,58.92],[0,0,5]):
            v=c['calculation']; self.assertAlmostEqual(v['emitted_kg_CH4'],emitted)
            self.assertAlmostEqual(110,15+emitted+consumed+lateral)
            self.assertAlmostEqual(v['carbon_in_kg_C'],82.5)
            self.assertAlmostEqual(v['carbon_out_plus_stock_kg_C'],82.5)
            self.assertEqual(c['arithmetic'],'RECALCULATED')
            self.assertEqual(c['effect'],'NOT_ASSESSED')
    def test_correct_arithmetic_not_evidence(self):
        out=r.review(r.load('examples/C.json'))
        self.assertTrue(all(c['arithmetic']=='RECALCULATED' and c['evidence']=='EVIDENCE_INSUFFICIENT' for c in out['claims']))
    def test_unit(self): self.a['DATA']['unit']='ppm'; self.assert_block(self.a,'DATA_UNIT')
    def test_phase(self): self.a['DATA']['phase']='aqueous'; self.assert_block(self.a,'DATA_PHASE')
    def test_gas(self): self.a['DATA']['gas']='CO2'; self.assert_block(self.a,'DATA_GAS')
    def test_time(self): self.a['DATA']['time_window']='YEAR_2026'; self.assert_block(self.a,'DATA_TIME_WINDOW')
    def test_timezone(self): self.a['DATA']['timezone']='UTC'; self.assert_block(self.a,'DATA_TIMEZONE')
    def test_space(self): self.a['DATA']['spatial_boundary']='OTHER_SITE'; self.assert_block(self.a,'DATA_SPATIAL_BOUNDARY')
    def test_reference_volume(self): self.a['DATA']['volume_reference']='Nm3_0C'; self.assert_block(self.a,'DATA_VOLUME_REFERENCE')
    def test_wet_dry(self): self.a['DATA']['wet_dry']='dry_ppm'; self.assert_block(self.a,'DATA_WET_DRY')
    def test_jurisdiction(self): self.a['METHOD']['jurisdiction']='AU_NGER'; self.assert_block(self.a,'JURISDICTION_VERSION')
    def test_version(self): self.a['METHOD']['version']='2026-C21'; self.assert_block(self.a,'JURISDICTION_VERSION')
    def test_reporting_year(self): self.a['METHOD']['reporting_year']='2025-26'; self.assert_block(self.a,'REPORTING_YEAR')
    def test_double_oxidation(self): self.a['CALCULATION']['oxidation_applications']=2; self.assert_block(self.a,'DOUBLE_OXIDATION')
    def test_lateral(self): self.a['CALCULATION']['lateral_fate']='DESTROYED'; self.assert_block(self.a,'BOUNDARY_OMISSION')
    def test_licence_missing(self):
        self.a['SOURCE_LICENCE'][0]['licence']='UNKNOWN'
        self.assertEqual(r.review(self.a)['status'],'EVIDENCE_INSUFFICIENT')
    def test_calibration_missing(self):
        self.a['DATA']['calibration']='UNKNOWN'; self.assertEqual(r.review(self.a)['status'],'EVIDENCE_INSUFFICIENT')
    def test_raw_flow_missing(self):
        self.a['DATA']['raw_flow_evidence']='UNKNOWN'; self.assertEqual(r.review(self.a)['status'],'EVIDENCE_INSUFFICIENT')
    def test_synthetic_as_real(self): self.a['SOURCE_LICENCE'][0]['origin']='REAL'; self.assert_block(self.a,'SYNTHETIC_AS_REAL')
    def test_effect(self): self.a['OUTCOME']['requested_effect']='EFFECT_VERIFIED'; self.assert_block(self.a,'UNAUTHORIZED_CERTIFICATION')
    def test_certification(self): self.a['OUTCOME']['regulatory_certification']='ISO_CERTIFIED'; self.assert_block(self.a,'UNAUTHORIZED_CERTIFICATION')
    def test_self_review(self): self.a['REVIEW']['reviewer_id']='SYNTHETIC_SUBMITTER'; self.assert_block(self.a,'ROLE_CONFLICT')
    def test_approval(self): self.a['REVIEW']['authority']='FOUNDER_APPROVED'; self.assert_block(self.a,'UNAUTHORIZED_APPROVAL')
    def test_unknown_role(self):
        self.a['REVIEW']['reviewer_id']='MADE_UP'; self.assertEqual(r.review(self.a)['status'],'EVIDENCE_INSUFFICIENT')
    def test_hash_tamper(self): self.a['SOURCE_LICENCE'][0]['payload']['cases'][0]['flows']['generated']['value']=999; self.assert_block(self.a,'HASH_TAMPER')
    def test_self_rehashed_payload(self):
        s=self.a['SOURCE_LICENCE'][0]; s['payload']['cases'][0]['flows']['generated']['value']=999; s['sha256']=r.digest(s['payload'])
        self.assert_block(self.a,'HASH_TAMPER')
    def test_changed_core_hash(self): self.a['CALCULATION']['code_sha256']='0'*64; self.assert_block(self.a,'CODE_HASH')
    def test_unknown_field(self): self.a['DATA']['allow_override']=True; self.assert_block(self.a,'SCHEMA_FIELDS')
    def test_unknown_schema(self): self.a['schema_version']='future'; self.assert_block(self.a,'SCHEMA_VERSION')
    def test_nan(self): self.a['CLAIM'][0]['reported_emitted_kg_CH4']=float('nan'); self.assert_block(self.a,'SCHEMA_TYPE')
    def test_bool_number(self): self.a['CLAIM'][0]['reported_emitted_kg_CH4']=True; self.assert_block(self.a,'SCHEMA_TYPE')
    def test_mass_failure(self): self.a['CLAIM'][2]['flows']['lateral_out']['value']=0; self.assert_block(self.a,'MASS_NOT_CONSERVED')
    def test_false_output(self): self.a['CLAIM'][0]['reported_emitted_kg_CH4']=90; self.assert_block(self.a,'OUTPUT_MISMATCH')
    def test_raw_input_link(self):
        # Preserve conservation while changing numbers: arithmetic alone must not pass provenance.
        c=self.a['CLAIM'][0]; c['flows']['generated']['value']+=1; c['flows']['stock_end']['value']+=1
        self.assert_block(self.a,'RAW_INPUT_MISMATCH')
    def test_claim_evidence_missing(self):
        self.a['CLAIM'][0]['supporting_evidence_ids']=['UNREGISTERED']
        self.assertEqual(r.review(self.a)['claims'][0]['status'],'EVIDENCE_INSUFFICIENT')
    def test_duplicate_source(self): self.a['SOURCE_LICENCE'].append(copy.deepcopy(self.a['SOURCE_LICENCE'][0])); self.assert_block(self.a,'DUPLICATE_EVIDENCE')
    def test_duplicate_claim(self): self.a['CLAIM'].append(copy.deepcopy(self.a['CLAIM'][0])); self.assert_block(self.a,'DUPLICATE_CLAIM')
    def test_per_claim_local_failure(self):
        self.a['CLAIM'][1]['reported_emitted_kg_CH4']=0
        self.assertEqual([c['status'] for c in r.review(self.a)['claims']],['METHOD_ALIGNED','MATERIAL_CONTRADICTION','METHOD_ALIGNED'])
    def test_open_raw_hash(self):
        raw=(T/'evidence/raw/SL1.zip').read_bytes(); _,rows=fragment.read_rows(raw); self.assertEqual(len(rows),23)
        with self.assertRaises(AssertionError): fragment.read_rows(raw+b'tamper')
    def test_open_fragment_inverse(self):
        from decimal import Decimal
        for row in r.load('evidence/open-fragment-results.json')['rows']:
            self.assertEqual(Decimal(row['derived_kg_m3'])/Decimal('0.001'),Decimal(row['original_mg_L']))

class LifecycleTests(unittest.TestCase):
    def history(self):
        out=[]
        for action,actor,sha in [('SUBMITTED','SYNTHETIC_SUBMITTER','a'*64),('REVIEWED','TECHNICAL_REVIEW_FIXTURE','a'*64),('OBJECTED','SYNTHETIC_SUBMITTER','a'*64),('CORRECTED','SYNTHETIC_SUBMITTER','b'*64),('REREVIEWED','TECHNICAL_REVIEW_FIXTURE','b'*64),('WITHDRAWN','SYNTHETIC_SUBMITTER','b'*64)]:
            old=copy.deepcopy(out); out=r.append_event(out,action,actor,sha); self.assertEqual(out[:-1],old)
        return out
    def test_lifecycle(self):
        events=self.history(); self.assertEqual(r.verify_events(events,events[-1]['event_sha256']),'WITHDRAWN')
    def test_deleted_event(self):
        events=self.history()
        with self.assertRaises(ValueError): r.verify_events(events[:-1],events[-1]['event_sha256'])
    def test_rewrite(self):
        events=self.history(); events[1]['actor']='SYNTHETIC_SUBMITTER'
        with self.assertRaises(ValueError): r.verify_events(events,events[-1]['event_sha256'])
    def test_role(self):
        with self.assertRaises(ValueError): r.append_event([], 'SUBMITTED','TECHNICAL_REVIEW_FIXTURE','a'*64)
    def test_after_withdrawal(self):
        with self.assertRaises(ValueError): r.append_event(self.history(),'REVIEWED','TECHNICAL_REVIEW_FIXTURE','b'*64)
    def test_same_revision_correction(self):
        e=self.history()[:3]
        with self.assertRaises(ValueError): r.append_event(e,'CORRECTED','SYNTHETIC_SUBMITTER','a'*64)

if __name__=='__main__': unittest.main()
