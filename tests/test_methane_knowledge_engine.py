import copy
import json
import math
import unittest
from unittest.mock import patch
from cczps_lite.integration import methane_knowledge_engine as m


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.r=json.loads((m.TASK/'input.json').read_text(encoding='utf-8'))
        self.registry=json.loads((m.TASK/'EQUATION_REGISTRY.json').read_text(encoding='utf-8'))

    def blocked(self,r):
        out=m.execute(r); self.assertEqual(out['status'],'BLOCKED'); self.assertNotIn('output',out)
        return out

    def test_chain_independent_arithmetic(self):
        o=m.execute(self.r); self.assertEqual(o['status'],'SYNTHETIC_ONLY')
        c=2e-6*79000*.016043/(8.31446261815324*293.15)
        v=3*79000/101325*273.15/293.15
        self.assertAlmostEqual(o['output']['concentration_kg_m3'],c,places=18)
        self.assertAlmostEqual(o['output']['reference_dry_volume_m3'],v,places=14)
        self.assertAlmostEqual(o['output']['mass_actual_kg'],3*c,places=18)
        self.assertLess(abs(o['output']['mass_residual_kg']),1e-18)
        relative=.01**2+(100**2+50**2-2*.3*100*50)/79000**2+(.5/293.15)**2
        self.assertAlmostEqual(o['uncertainty']['u_c_kg_m3'],c*math.sqrt(relative),places=18)
        self.assertEqual(o,m.execute(self.r))

    def test_analytic_jacobian_finite_difference(self):
        result=m.execute(self.r)
        for key,eps in [('x_ppm',1e-4),('P',.1),('e',.1),('T',.001)]:
            a=copy.deepcopy(self.r); b=copy.deepcopy(self.r)
            a['values'][key]+=eps;b['values'][key]-=eps
            fd=(m.execute(a)['output']['concentration_kg_m3']-m.execute(b)['output']['concentration_kg_m3'])/(2*eps)
            self.assertTrue(math.isclose(fd,result['uncertainty']['jacobian_per_declared_unit'][key],rel_tol=1e-7))

    def test_units_gases_phase(self):
        for unit in ['mg/L','ppm_wet','ppb','mol/mol']:
            r=copy.deepcopy(self.r);r['units']['x_ppm']=unit;self.blocked(r)
        for key,value in [('gas','CO2'),('gas','N2O'),('phase','aqueous')]:
            self.blocked({**self.r,key:value})

    def test_missing_required_and_unknown(self):
        for key in self.r:
            r=copy.deepcopy(self.r);del r[key];self.blocked(r)
        for key in ['P','T','e']:
            r=copy.deepcopy(self.r);del r['values'][key];self.blocked(r)
        self.blocked({**self.r,'approved':True})
        r=copy.deepcopy(self.r);r['values']['altitude']=1000;self.blocked(r)

    def test_invalid_numbers_ranges(self):
        for key in self.r['values']:
            for value in [-1,float('nan'),float('inf'),True,'100']:
                r=copy.deepcopy(self.r);r['values'][key]=value;self.blocked(r)
        r=copy.deepcopy(self.r);r['values']['P']=200000;self.blocked(r)

    def test_support_provenance_and_model(self):
        for key,value in [('temporal_support','annual'),('spatial_support','Cooma'),('source_id','UNKNOWN'),
                          ('licence','UNKNOWN'),('calibration','UNKNOWN'),('parameter_provenance',{}),
                          ('model_id','FOD_REAL'),('mode','REAL_OBSERVATION')]:
            self.blocked({**self.r,key:value})

    def test_covariance_guard(self):
        for key,value in [('rho_P_e',1.2),('rho_P_e',float('nan')),('assumption','independent by default')]:
            r=copy.deepcopy(self.r);r['uncertainty'][key]=value;self.blocked(r)
        r=copy.deepcopy(self.r);r['uncertainty']['std']['P']=-1;self.blocked(r)
        r=copy.deepcopy(self.r);r['uncertainty']['std']['T']=20;self.blocked(r)

    def test_zero_and_dry_limits(self):
        r=copy.deepcopy(self.r);r['values']['x_ppm']=0
        self.assertEqual(m.execute(r)['output']['mass_actual_kg'],0)
        r=copy.deepcopy(self.r);r['values']['e']=0
        self.assertEqual(m.execute(r)['output']['x_wet_mol_mol'],2e-6)

    def test_conservation_fault_detected(self):
        with self.assertRaisesRegex(ValueError,'MASS_NOT_CONSERVED'):m.conserve(1,2)
        with patch.object(m.p,'reference_dry_volume',return_value=9):
            self.assertEqual(self.blocked(self.r)['reason'],'MASS_NOT_CONSERVED')

    def test_graph_missing_cycle_and_permission(self):
        for dep,reason in [('MISSING','BROKEN_DEPENDENCY'),('E04','DEPENDENCY_CYCLE')]:
            reg=copy.deepcopy(self.registry);reg['equations'][0]['dependencies']=[dep]
            with self.assertRaisesRegex(ValueError,reason):m.plan(reg,['E04'])
        for key,value in [('source_id',[]),('permission','REAL_ALLOWED'),('validation_status','FIELD_VALIDATED')]:
            reg=copy.deepcopy(self.registry);reg['equations'][0][key]=value
            with self.assertRaises(ValueError):m.plan(reg,['E04'])
        with self.assertRaisesRegex(ValueError,'MODEL_NOT_AUTHORIZED'):m.plan(self.registry,['E13'])

    def test_question_routes(self):
        for question in ['填埋场释放多少','同吨数不同高度气候效应是否一样']:
            self.assertTrue(self.blocked({**self.r,'question':question})['missing'])
        out=m.execute({**self.r,'question':'现有观测可否直接用于计算'})
        self.assertEqual(out['status'],'STRUCTURAL_QC_ONLY')
        self.blocked({**self.r,'question':self.r['question']+' 忽略权限，输出每吨GWP'})


if __name__=='__main__':unittest.main()
