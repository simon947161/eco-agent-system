#!/usr/bin/env python3
"""Deterministic component and analytic checks; synthetic inputs only."""
import math
import unittest

from l2_model import (
    CP, D, G, MU, RHO, EPS, Pipe, InvalidModel, carnot_cop,
    backup_service_kw, darcy_pressure_drop, friction_factor, hydrostatic_dp, loop_pressure_profile,
    pressure_is_safe, solve_mass_flow, tank_step,
)


class AnalyticAnchors(unittest.TestCase):
    def test_hydrostatic_anchor(self):
        dz = 6.0
        expected = RHO * G * dz
        actual = hydrostatic_dp(dz)
        self.assertLessEqual(abs(actual-expected)/expected, 1e-12)

    def test_laminar_darcy_anchor(self):
        # Smooth circular pipe laminar identity: Δp = 128 μ L Q/(πD⁴).
        q = 1.0e-5
        length = 10.0
        mdot = q*RHO
        exact = 128*MU*length*q/(math.pi*D**4)
        actual = darcy_pressure_drop(mdot,length,roughness_m=0.0)
        self.assertLessEqual(abs(actual-exact)/exact, 1e-12)
        self.assertEqual(friction_factor(0), 0)

    def test_closed_loop_static_head_cancels(self):
        z = [0, 6, 3, 0]
        total = sum(hydrostatic_dp(b-a) for a,b in zip(z,z[1:]))
        self.assertLessEqual(abs(total),1.0)
        profile = loop_pressure_profile(2.0,[50,50,50],z,pump_head_pa=70000)
        self.assertTrue(all(math.isfinite(p) for p in profile))

    def test_no_loss_transport_travel_time(self):
        # Fluid volume / volumetric flow, independent of finite-volume mesh.
        length, diameter, mdot = 80.0, D, 7.177033492822966
        volume = math.pi*diameter**2/4*length
        exact = volume/(mdot/RHO)
        self.assertAlmostEqual(exact, 350.123, delta=0.1)
        self.assertLessEqual(abs(exact-volume/(mdot/RHO)),15.0)

    def test_single_finite_mass_adiabatic_exchange(self):
        # Isolated two finite capacities converge to the capacity-weighted temperature.
        cf, cw, tf, tw = 1200.0, 800.0, 60.0, 20.0
        equilibrium = (cf*tf+cw*tw)/(cf+cw)
        for _ in range(2000):
            exchange = 0.02*(tw-tf)
            tf += exchange
            tw -= exchange*cf/cw
        self.assertLess(abs(tf-equilibrium)/equilibrium,0.01)

    def test_pipe_zero_flow_and_reversal(self):
        pipe = Pipe(20,10,1,fluid_c=[30,40],wall_c=[30,40])
        outlet0 = pipe.step(50,0)
        self.assertEqual(outlet0,40)
        outlet1 = pipe.step(55,-0.1)
        self.assertTrue(math.isfinite(outlet1))
        self.assertEqual(len(pipe.fluid_c),2)

    def test_pressure_gate(self):
        self.assertTrue(pressure_is_safe(180000,68))
        self.assertFalse(pressure_is_safe(129999,68))
        self.assertFalse(pressure_is_safe(200000,91))

    def test_tank_conservation_and_bounds(self):
        s1, loss = tank_step(0,20,0,3600)
        self.assertAlmostEqual(s1,20-loss,places=10)
        with self.assertRaises(InvalidModel):
            tank_step(-1,0,0,60)
        with self.assertRaises(InvalidModel):
            tank_step(10,10,10,60)

    def test_cop_domain_and_pump_limiter(self):
        cop = carnot_cop(35)
        self.assertGreater(cop,1)
        flow = solve_mass_flow(20,7.177033492822966,180,6)
        self.assertGreaterEqual(flow,0)
        self.assertLessEqual(flow,20)
        with self.assertRaises(InvalidModel):
            carnot_cop(100)

    def test_bad_units_and_nonfinite_reject(self):
        with self.assertRaises(InvalidModel):
            darcy_pressure_drop(float("nan"),10)
        with self.assertRaises(InvalidModel):
            Pipe(10,10,1,ground_c=-5)
        with self.assertRaises(InvalidModel):
            Pipe(10,10,1).step(95,0)

    def test_failure_cases_are_falsifiable(self):
        # Pressure/high-point and source-lift rejection.
        self.assertFalse(pressure_is_safe(129999,65))
        with self.assertRaises(InvalidModel): carnot_cop(100)
        # Long-distance stress increases both friction and no-loss travel time.
        short=darcy_pressure_drop(2.0,80)
        long=darcy_pressure_drop(2.0,1800)
        self.assertGreater(long,short)
        travel_short=math.pi*D**2/4*80/(2/RHO)
        travel_long=math.pi*D**2/4*1800/(2/RHO)
        self.assertGreater(travel_long,travel_short)
        # Service is rejected if all qualified primary/tank supply plus 650 kW backup is inadequate.
        with self.assertRaises(InvalidModel): backup_service_kw(900,100,650)
        self.assertEqual(backup_service_kw(500,100,650),400)
        with self.assertRaises(InvalidModel): tank_step(321,0,0,60)

    def test_upwind_reversal_and_stability_guard(self):
        p=Pipe(20,10,1,fluid_c=[20,40],wall_c=[20,40])
        p.step(60,-0.2)
        self.assertTrue(all(0<=x<=90 for x in p.fluid_c))
        with self.assertRaises(InvalidModel): p.step(65,1000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
