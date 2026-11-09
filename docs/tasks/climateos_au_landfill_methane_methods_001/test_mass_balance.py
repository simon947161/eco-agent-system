import math
import unittest
from mass_balance import (evaluate, fixture, flow_mass, flux_chamber, operation_hour,
                          generation_from_decomposed_carbon, validate_graph, p)


class LedgerTests(unittest.TestCase):
    def test_three_independent_hand_answers(self):
        for name, air, reacted, co2 in [('uncaptured', 95, 0, 0),
                                      ('capture_flare', 32.7, 62.3, 171.325),
                                      ('oxidation_leaks', 31.08, 58.92, 162.03)]:
            with self.subTest(name=name):
                out = evaluate(fixture(name))
                self.assertAlmostEqual(out['emitted_kg_CH4'], air)
                self.assertAlmostEqual(out['consumed_kg_CH4'], reacted)
                self.assertAlmostEqual(out['co2_from_CH4_reaction_kg'], co2)
                self.assertAlmostEqual(out['carbon_out_plus_stock_kg_C'], 82.5)
                self.assertTrue(all(abs(x) < 1e-10 for x in out['residuals'].values()))

    def test_carbon_conversion_not_whole_carbon_to_ch4(self):
        self.assertEqual(generation_from_decomposed_carbon(12, .5), 8)
        self.assertEqual(generation_from_decomposed_carbon(12000, .5), 8000)
        self.assertNotEqual(generation_from_decomposed_carbon(12, .5), 16)

    def test_interface_double_count_rejected(self):
        for key in ['collected', 'destroyed', 'oxidized', 'surface', 'pipe_leak']:
            with self.subTest(key=key):
                req = fixture('oxidation_leaks'); req['flows'][key]['value'] += 1
                with self.assertRaises(ValueError): evaluate(req)

    def test_missing_nonfinite_negative(self):
        for bad in [None, -1, math.nan, math.inf, True, 'UNKNOWN']:
            with self.subTest(value=bad):
                req = fixture('uncaptured'); req['flows']['generated']['value'] = bad
                with self.assertRaises(ValueError): evaluate(req)
        req = fixture('uncaptured'); del req['flows']['lateral_out']
        with self.assertRaises(ValueError): evaluate(req)

    def test_time_and_units(self):
        for key, value in [('unit', 'kg_CH4/hour'), ('interval', 'SYNTHETIC_YEAR_001')]:
            req = fixture('uncaptured'); req['flows']['generated'][key] = value
            with self.assertRaises(ValueError): evaluate(req)

    def test_no_real_or_legal_route_and_unknown_provenance(self):
        for key, value in [('mode', 'OBSERVED'), ('version', 'NGER_2025_26'),
                           ('gas', 'CO2'), ('phase', 'gas_only'), ('source_id', ''),
                           ('licence', 'UNKNOWN'), ('calibration', 'UNKNOWN'),
                           ('uncertainty', 'UNKNOWN')]:
            with self.subTest(key=key):
                req = fixture('uncaptured'); req[key] = value
                with self.assertRaises(ValueError): evaluate(req)

    def test_methane_reaction_requires_carbon_not_equal_gas_mass(self):
        out = evaluate(fixture('capture_flare'))
        self.assertNotEqual(out['co2_from_CH4_reaction_kg'], out['consumed_kg_CH4'])
        self.assertAlmostEqual(out['co2_from_CH4_reaction_kg'] * 12 / 44,
                               out['consumed_kg_CH4'] * 12 / 16)

    def test_uncollected_and_collected_are_not_both_oxidized(self):
        out = evaluate(fixture('oxidation_leaks'))
        # Incorrect applying OX to all 95 leaving storage would consume 19, not 6.
        self.assertEqual(fixture('oxidation_leaks')['flows']['oxidized']['value'], 6)
        self.assertNotEqual(out['emitted_kg_CH4'], (100 - 60) * .8 + 60 * .02)

    def test_gas_state_conversion_and_reference_temperature(self):
        args = dict(volume=100, unit='m3_wet_actual', x_dry=.5,
                    pressure_pa=101325, temperature_k=293.15, vapour_pa=2000)
        out = flow_mass(**args)
        hand = 100 * .5 * 99325 * .016043 / (8.31446261815324 * 293.15)
        self.assertAlmostEqual(out['kg_CH4'], hand)
        v0 = p.reference_dry_volume(100, 101325, 293.15, 2000)
        self.assertAlmostEqual(out['m3_dry_15C_101325Pa'] / v0, 288.15 / 273.15)
        for key, bad in [('unit', 'Nm3'), ('x_dry', None), ('vapour_pa', None),
                         ('gas', 'N2O'), ('phase', 'dissolved'), ('calibration', '')]:
            with self.subTest(key=key):
                with self.assertRaises(ValueError): flow_mass(**{**args, key: bad})
        wet_x = .5 * (101325-2000)/101325
        self.assertAlmostEqual(p.dry_fraction_from_wet(wet_x,101325,2000), .5)
        self.assertNotEqual(flow_mass(**{**args, 'x_dry': wet_x})['kg_CH4'], out['kg_CH4'])

    def test_chamber_units_and_hour_gate(self):
        self.assertAlmostEqual(flux_chamber(volume_m3=.1,area_m2=.2,slope_mg_m3_s=2),1)
        with self.assertRaises(ValueError): flux_chamber(volume_m3=.1,area_m2=0,slope_mg_m3_s=2)
        with self.assertRaises(ValueError): flux_chamber(volume_m3=.1,area_m2=.2,slope_mg_m3_s=None)
        self.assertEqual(operation_hour([True]*60,'h1','h1'),1)
        self.assertEqual(operation_hour([True]*59+[False],'h1','h1'),0)
        for minutes in [[True]*59, [True]*59+[None]]:
            with self.assertRaises(ValueError): operation_hour(minutes,'h1','h1')
        with self.assertRaises(ValueError): operation_hour([True]*60,'h1','h2')

    def test_graph_break_and_duplicate(self):
        self.assertTrue(validate_graph(['G','body','air'],[['G','body'],['body','air']]))
        with self.assertRaises(ValueError): validate_graph(['G'],[['G','missing']])
        with self.assertRaises(ValueError): validate_graph(['G','G'],[])


if __name__ == '__main__': unittest.main(verbosity=2)
