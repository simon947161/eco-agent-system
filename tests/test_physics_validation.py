"""Independent arithmetic/analytic oracles for authorized synthetic core."""
import math
import unittest

from cczps_lite.integration import physics_validation as p


class GasTests(unittest.TestCase):
    def test_pr137_pinned_numbers(self):
        self.assertAlmostEqual(p.gas_properties(2e-6,101325,293.15)['mass_concentration_kg_per_m3']*1e6,1.3338534241131146,places=12)
        self.assertAlmostEqual(p.gas_properties(2e-6,80000,293.15)['mass_concentration_kg_per_m3']*1e6,1.0531287829168434,places=12)

    def test_pressure_temperature_scaling(self):
        base=p.gas_properties(.01,100000,300)['mass_concentration_kg_per_m3']
        self.assertEqual(p.gas_properties(.01,50000,300)['mass_concentration_kg_per_m3'],base/2)
        self.assertEqual(p.gas_properties(.01,100000,600)['mass_concentration_kg_per_m3'],base/2)

    def test_inverse_dry_wet_and_concentration(self):
        for e in [0,1000,2000]:
            for pressure in [80000,101325]:
                r=p.gas_properties(2e-6,pressure,293.15,e)
                self.assertAlmostEqual(p.dry_fraction_from_concentration(r['mass_concentration_kg_per_m3'],pressure,293.15,e),2e-6,places=18)
                self.assertAlmostEqual(p.dry_fraction_from_wet(r['x_wet_mol_per_mol'],pressure,e),2e-6,places=18)

    def test_water_partial_pressure_oracle(self):
        wet=p.gas_properties(.1,100000,300,2000)
        dry=p.gas_properties(.1,100000,300)
        self.assertAlmostEqual(wet['mass_concentration_kg_per_m3']/dry['mass_concentration_kg_per_m3'],.98)
        self.assertAlmostEqual(wet['x_wet_mol_per_mol'],.098)

    def test_mixing_ratio_invariant(self):
        self.assertEqual(p.gas_properties(2e-6,80000,280,1000)['mass_mixing_ratio_kg_per_kg_dry_air'],p.gas_properties(2e-6,101325,300)['mass_mixing_ratio_kg_per_kg_dry_air'])

    def test_reference_volume_preserves_dry_ch4_mass(self):
        r=p.reference_dry_volume(3,80000,293.15,2000)
        actual=3*p.gas_properties(2e-6,80000,293.15,2000)['mass_concentration_kg_per_m3']
        reference=r*p.gas_properties(2e-6,101325,273.15)['mass_concentration_kg_per_m3']
        self.assertAlmostEqual(actual,reference,places=18)

    def test_zero_limits(self):
        self.assertEqual(p.gas_properties(0,101325,300)['mass_concentration_kg_per_m3'],0)
        self.assertEqual(p.reference_dry_volume(0,101325,300),0)

    def test_invalid_gas_inputs(self):
        for args in [(2,100000,300,0),(-1,100000,300,0),(.1,0,300,0),(.1,100000,0,0),(.1,100000,300,100000),(.1,100000,300,-1),(.1,float('nan'),300,0),(True,100000,300,0)]:
            with self.subTest(args=args),self.assertRaises(ValueError):p.gas_properties(*args)


class StorageTests(unittest.TestCase):
    def test_closed_box_oracle(self):
        r=p.storage_run(conductance_kg_h_pa=0)
        self.assertAlmostEqual(r['final_kg'],r['initial_kg']+.024,places=12)
        self.assertEqual(r['vented_kg'],0)

    def test_steady_equilibrium_oracle(self):
        r=p.storage_run()
        self.assertAlmostEqual(r['final_kg'],r['initial_kg'],places=14)
        self.assertAlmostEqual(r['vented_kg'],.024,places=14)

    def test_independent_integral_conservation(self):
        for slope in [-100,0,100]:
            r=p.storage_run(slope_pa_h=slope)
            integrated=math.fsum(x['vent_kg_h']*r['dt_h'] for x in r['rows'])
            self.assertAlmostEqual(integrated,r['initial_kg']+r['input_kg']-r['final_kg'],places=12)
            self.assertLess(abs(r['residual_kg']),1e-12)
            self.assertGreaterEqual(r['minimum_stock_kg'],0)

    def test_ramp_analytic_and_step_convergence(self):
        errors=[]
        for dt in [.5,.25,.125]:
            r=p.storage_run(slope_pa_h=-100,dt_h=dt)
            a=r['pressure_per_mass_pa_kg']; lam=2e-6*a
            delta_eq=(a*.001+100)/lam
            delta=delta_eq+(500-delta_eq)*math.exp(-lam*24)
            exact=(101325-100*24+delta)/a
            errors.append(abs(r['final_kg']-exact))
        self.assertGreater(errors[0],errors[1]);self.assertGreater(errors[1],errors[2])
        self.assertLess(errors[-1],2e-6)

    def test_hypothesis_direction_is_scenario_specific(self):
        f,s,r=[p.storage_run(slope_pa_h=x) for x in [-100,0,100]]
        self.assertGreater(f['vented_kg'],s['vented_kg']);self.assertGreater(s['vented_kg'],r['vented_kg'])

    def test_stored_release_with_zero_generation(self):
        r=p.storage_run(generation_kg_h=0,slope_pa_h=-100)
        self.assertGreater(r['vented_kg'],0)
        self.assertAlmostEqual(r['initial_kg']-r['final_kg'],r['vented_kg'],places=12)

    def test_one_way_valve_control(self):
        r=p.storage_run(initial_overpressure_pa=-1000,generation_kg_h=0,slope_pa_h=0)
        self.assertEqual(r['vented_kg'],0)
        self.assertEqual(r['final_kg'],r['initial_kg'])

    def test_refuse_unstable_or_bad_domain(self):
        for kwargs in [dict(dt_h=24),dict(dt_h=.7),dict(generation_kg_h=-1),dict(conductance_kg_h_pa=-1),dict(volume_m3=0),dict(slope_pa_h=-100000),dict(dt_h=True)]:
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):p.storage_run(**kwargs)


class FODTests(unittest.TestCase):
    def test_half_life_hand_oracle(self):
        r=p.fod_run([10,0,0],k_per_year=math.log(2),initial_ddoc_gg_c=0)
        # End-year input = 10*.15*.5=.75 Gg C, first year no generation.
        self.assertEqual(r['rows'][0]['generated_CH4_Gg'],0)
        self.assertAlmostEqual(r['rows'][1]['decomposed_Gg_C'],.375)
        self.assertAlmostEqual(r['rows'][1]['generated_CH4_Gg'],.25)
        self.assertAlmostEqual(r['rows'][1]['emitted_CH4_Gg'],.135)
        self.assertAlmostEqual(r['rows'][2]['end_DDOC_Gg_C'],.1875)

    def test_independent_closed_form_cohorts(self):
        waste=[10,12,8,0];r=p.fod_run(waste)
        for y,row in enumerate(r['rows']):
            oracle=.5*math.exp(-.1*(y+1))+sum(w*.15*.5*math.exp(-.1*(y-j)) for j,w in enumerate(waste[:y+1]))
            self.assertAlmostEqual(row['end_DDOC_Gg_C'],oracle,places=14)
            self.assertAlmostEqual(sum(row['cohorts_end_Gg_C'].values()),oracle,places=14)

    def test_conservation_and_methane_partition(self):
        r=p.fod_run([10,12,8]+[0]*20)
        self.assertLess(abs(r['carbon_residual_Gg_C']),1e-12)
        for row in r['rows']:
            self.assertLess(abs(row['carbon_residual_Gg_C']),1e-12)
            self.assertLess(abs(row['methane_partition_residual_Gg']),1e-12)

    def test_zero_decay_oracle(self):
        r=p.fod_run([10,10],k_per_year=0)
        self.assertEqual(r['total_generated_CH4_Gg'],0)
        self.assertEqual(r['final_DDOC_Gg_C'],2)

    def test_recovery_and_oxidation_limits(self):
        for key in ['recovered_fraction','oxidation_fraction']:
            r=p.fod_run([0],**{key:1})
            self.assertEqual(r['total_emitted_CH4_Gg'],0)

    def test_units_kg_gg(self):
        self.assertEqual(2.5*p.GG_TO_KG,2500000)
        self.assertEqual(2500000/p.GG_TO_KG,2.5)

    def test_invalid_fod_inputs(self):
        for kwargs in [dict(k_per_year=-1),dict(doc=1.1),dict(recovered_fraction=-.1),dict(oxidation_fraction=2),dict(initial_ddoc_gg_c=-1),dict(rate_multipliers=[1]),dict(rate_multipliers=[1,float('inf')])]:
            with self.subTest(kwargs=kwargs),self.assertRaises(ValueError):p.fod_run([10,10],**kwargs)


class ResponseTests(unittest.TestCase):
    def test_temperature_neutral_exact_baseline(self):
        w=[10,12,8,0]
        self.assertEqual(p.fod_run(w),p.fod_run(w,rate_multipliers=[p.temperature_multiplier(293.15)]*4))

    def test_moisture_neutral_exact_baseline(self):
        w=[10,12,8,0]
        self.assertEqual(p.fod_run(w),p.fod_run(w,rate_multipliers=[p.moisture_multiplier(.5)]*4))

    def test_zero_activation_energy_control(self):
        self.assertEqual(p.temperature_multiplier(310,activation_j_mol=0),1)

    def test_response_mathematical_oracles(self):
        # 1/T-1/Tref=-R*ln(2)/Ea makes normalized Arrhenius exactly 2.
        t=1/(1/293.15-p.R*math.log(2)/30000)
        self.assertAlmostEqual(p.temperature_multiplier(t),2,places=13)
        self.assertEqual(p.moisture_multiplier(.25),.5)
        self.assertEqual(p.moisture_multiplier(.75),1.5)

    def test_annual_cumulative_not_just_endpoint(self):
        base=p.fod_run([0]*5,initial_ddoc_gg_c=1)
        hot=p.fod_run([0]*5,initial_ddoc_gg_c=1,rate_multipliers=[2]*5)
        self.assertGreater(hot['total_generated_CH4_Gg'],base['total_generated_CH4_Gg'])
        self.assertAlmostEqual(hot['total_generated_CH4_Gg'],(1-math.exp(-1))*.5*16/12)

    def test_zero_and_bounded_moisture(self):
        self.assertEqual(p.moisture_multiplier(0),0)
        self.assertEqual(p.moisture_multiplier(1),2)
        self.assertEqual(p.fod_run([0]*3,rate_multipliers=[0]*3)['total_generated_CH4_Gg'],0)

    def test_response_invalid_domain(self):
        for call in [lambda:p.temperature_multiplier(0),lambda:p.temperature_multiplier(400),lambda:p.moisture_multiplier(1.1),lambda:p.moisture_multiplier(.5,1),lambda:p.moisture_multiplier(float('nan'))]:
            with self.assertRaises(ValueError):call()
