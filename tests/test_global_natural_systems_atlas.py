"""Admission boundary tests: real metadata, wrong claims and missing evidence."""
import copy
import tempfile
import unittest
from pathlib import Path
from cczps_lite.integration import global_natural_systems_atlas as atlas

class AtlasTests(unittest.TestCase):
    def setUp(self):
        self.data=atlas.load_atlas(verify=False)

    def reject(self, edit, expected):
        data=copy.deepcopy(self.data); edit(data)
        with self.assertRaisesRegex(ValueError,expected): atlas.validate(data)

    def test_m49_and_many_to_many(self):
        result=atlas.validate(self.data)
        self.assertEqual(result['countries'],248)
        self.assertEqual(result['deep_cases'],12)
        links=self.data['graph']['country_links']
        self.assertEqual({l['country_id'] for l in links if l['unit_id']=='BASIN_NILE'},{'M49:231','M49:818','M49:729'})
        self.assertGreater(len([l for l in links if l['country_id']=='M49:036']),1)
        self.assertEqual(result['geometry_coverage_fraction'],0)

    def test_missing_country_and_duplicate(self):
        self.reject(lambda d:d['coverage']['countries'].pop(),'GLOBAL_COVERAGE')
        self.reject(lambda d:d['coverage']['countries'].append(d['coverage']['countries'][0]),'DUPLICATE_ID')

    def test_false_geometry_crs_and_area_fraction(self):
        self.reject(lambda d:d['graph']['units'][0].update(CRS='EPSG:4326'),'GEOMETRY_OR_CRS')
        self.reject(lambda d:d['graph']['units'][0].update(geometry_ref='made_up.geojson'),'GEOMETRY_OR_CRS')
        self.reject(lambda d:d['graph']['country_links'][0].update(fraction=0.9),'SPATIAL_OVERLAY')

    def test_license_and_hash(self):
        self.reject(lambda d:d['sources'][0].update(raw_redistributed=True),'RAW_REDISTRIBUTION')
        self.reject(lambda d:d['evidence'][0].update(rights='CC0'),'RIGHTS_OR_VERSION')
        self.reject(lambda d:d['evidence'][0].update(sha_if_downloaded='0'*64),'HASH_MISMATCH')

    def test_manifest_detects_mutated_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp); (path/'evidence').mkdir()
            (path/'evidence/manifest.json').write_text('{"files":{"README.md":"bad"}}')
            with self.assertRaisesRegex(ValueError,'HASH_OR_PATH'): atlas.verify_manifest(path)

    def test_global_hash_manifest(self):
        self.assertGreater(atlas.verify_manifest(),10)

    def test_score_not_invented_or_duplicated_to_missing_country(self):
        self.reject(lambda d:d['policies'][0].update(score=99),'FABRICATED_SCORE')
        self.reject(lambda d:next(p for p in d['policies'] if p['country_id']=='M49:458').update(score=0),'SCORE_WITHOUT_COVERAGE')
        self.reject(lambda d:d['policies'][0].update(unit='kg_CH4/year'),'POLICY_AS_PHYSICS')

    def test_original_score_labels_and_missingness(self):
        countries={p['display_name']:p for p in self.data['policies']}
        self.assertEqual(countries['Australia']['score'],50)
        self.assertEqual(countries['China']['score'],20)
        self.assertEqual(countries['Germany']['score'],100)
        self.assertIsNone(countries['Fiji']['score'])
        self.assertEqual(countries['Australia']['review_state'],'MATERIAL_CONTRADICTION')

    def test_policy_is_not_observation_or_causal_parameter(self):
        self.reject(lambda d:next(e for e in d['evidence'] if e['source_id']=='SCORE').update(evidence_type='PHYSICAL_OBSERVATION'),'POLICY_AS_OBSERVATION')
        self.reject(lambda d:d['graph']['edges'][0].update(evidence_ids=['EV:POLICY:156']),'POLICY_USED_AS_PHYSICAL')
        self.reject(lambda d:d['graph']['edges'][0].update(numeric_weight=0.8),'UNADMITTED_COEFFICIENT')

    def test_causality_hypothesis_and_river_direction(self):
        self.reject(lambda d:d['graph']['edges'][3].update(causality='DETERMINISTIC'),'FALSE_DETERMINISTIC')
        self.reject(lambda d:d['graph']['edges'][-1].update(causality='PROVEN'),'HYPOTHESIS_AS_CAUSE')
        self.reject(lambda d:d['graph']['edges'][0].update(from_id='BLUE_LOWER',to_id='BLUE_UPPER'),'RIVER_DIRECTION')

    def test_dangling_links(self):
        self.reject(lambda d:d['graph']['edges'][0].update(to_id='imaginary'),'DANGLING_EDGE')
        self.reject(lambda d:d['graph']['edges'][0].update(evidence_ids=['imaginary']),'MISSING_EDGE_EVIDENCE')
        self.reject(lambda d:d['graph']['country_links'][0].update(country_id='M49:999'),'DANGLING_COUNTRY_UNIT')

    def test_units_timezone_order_and_legal_version(self):
        self.reject(lambda d:next(e for e in d['evidence'] if e['claim_id']=='BRW_EXISTING').update(unit='kg/year'),'OBSERVATION_UNIT')
        self.reject(lambda d:next(e for e in d['evidence'] if e['claim_id']=='BRW_EXISTING')['time_support'].update(timezone='Australia/Sydney'),'TIME_WINDOW_OR_ZONE')
        self.reject(lambda d:next(e for e in d['evidence'] if e['claim_id']=='BRW_EXISTING')['time_support'].update(end='2023-01-01T00:00:00Z'),'TIME_ORDER')
        self.reject(lambda d:next(e for e in d['evidence'] if e['claim_id']=='AU_TARGET').update(method_id='US/2026/foo'),'WRONG_JURISDICTION')
        self.reject(lambda d:next(e for e in d['evidence'] if e['claim_id']=='GML_GLOBAL').update(unit='kg_CH4/year'),'UNIT_BOUNDARY')
        self.reject(lambda d:next(e for e in d['evidence'] if e['claim_id']=='BRW_EXISTING')['time_support'].update(start='2024-01-01T00:00:00+10:00'),'UTC_OFFSET_CONFLICT')

    def test_no_synthetic_as_real_or_science_promotion(self):
        self.reject(lambda d:d['evidence'][-1].update(origin='FIELD_MEASUREMENT'),'SYNTHETIC_AS_REAL')
        self.reject(lambda d:d['coverage']['countries'][0].update(science_status='ADMITTED'),'SCIENTIFIC_PROMOTION')
        self.reject(lambda d:next(e for e in d['evidence'] if e['claim_id']=='OUTCOME_GAP').update(review_state='SOURCE_VERIFIED'),'OUTCOME_PROMOTION')

    def test_query_filters_and_unknown_time(self):
        q=atlas.query(self.data,country='USA',system='ATM_BOUNDARY',at='2024-06-01T00:00:00Z',evidence_type='PHYSICAL_OBSERVATION')
        self.assertEqual([e['claim_id'] for e in q['evidence']],['BRW_EXISTING'])
        self.assertFalse(atlas.query(self.data,at='2025-01-01T00:00:00Z')['evidence'])
        self.assertFalse(atlas.query(self.data,country='not_a_country')['evidence'])
        self.assertFalse(atlas.query(self.data,country='ETH',system='ocean')['evidence'])
        self.assertEqual(len(atlas.query(self.data,evidence_type='POLICY_ASSESSMENT')['policies']),8)
        self.assertTrue(atlas.query(self.data,text='conditional')['evidence'])

    def test_transboundary_paths(self):
        self.assertEqual([e['id'] for e in atlas.trace(self.data,'BLUE_UPPER','MAIN_NILE')],['N1','N2'])
        self.assertFalse(atlas.trace(self.data,'MAIN_NILE','BLUE_UPPER'))
        self.assertEqual([e['id'] for e in atlas.trace(self.data,'CH4_SOURCE','CLIMATE_RESPONSE')],['M1','M2','M3'])
        self.assertEqual(atlas.trace(self.data,'CH4_SOURCE','CLIMATE_RESPONSE')[-1]['status'],'BLOCKED')

    def test_end_to_end_preserves_internal_arithmetic_boundary(self):
        output=atlas.end_to_end(self.data)
        self.assertFalse(output['policy_sent_to_model'])
        self.assertEqual(output['scientific_admission'],'PENDING')
        for record in output['scenario_interface']['records']:
            self.assertEqual(record['approval_support_status'],'not_ready_for_approval')
            self.assertEqual(record['comparison_status'],'insufficient_evidence_for_comparison')
        self.assertEqual(output['review_results']['A']['status'],'METHOD_ALIGNED')
        self.assertEqual(output['review_results']['B']['status'],'MATERIAL_CONTRADICTION')
        self.assertEqual(output['review_results']['C']['status'],'EVIDENCE_INSUFFICIENT')
        for result in output['review_results'].values():
            self.assertEqual(result['arithmetic_interpretation'],'INTERNAL_FIXTURE_REPLAY_ONLY')
            self.assertEqual(result['human_review'],'PENDING')
            self.assertEqual(result['REGULATORY_CERTIFICATION'],'NOT_PROVIDED')
        self.assertTrue(any(c['arithmetic']=='RECALCULATED' for c in output['review_results']['B']['claims']))

if __name__=='__main__': unittest.main()
