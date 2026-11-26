"""P1 unit, fault-injection, counterfactual and evidence replay checks."""
import copy
import csv
import gzip
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import ledger
from ledger import (ARMS, EDGES, HERE, TOL, audit_hour, conditions, dispatch, exergy,
                    heat_pump, line_loss, load_inputs, pump_work, read_json, validate_parameters)
from replay import ClockAudit, impacts, sha, write_outputs


class ThermalLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_inputs()
        cls.p, cls.routes = cls.cases["central"]
        cls.archive = read_json(HERE/"results/P1_ENERGY_EXERGY_CARBON_LEDGER.json")["cases"]

    def setUp(self):
        self.demand = (210.0, 35.0, 8.0)
        self.f, self.end, self.hp = dispatch("L", 100, 20.0, self.demand, self.p, self.routes)

    def audit(self):
        return audit_hour(self.f, 20.0, self.end, self.demand, self.hp, self.p, 1, "L")

    def test_device_and_combined_residuals(self):
        self.assertLess(max(map(abs, self.audit().values())), TOL)
        self.f["low_loss"] += 1
        with self.assertRaisesRegex(ValueError, "ENERGY_RESIDUAL:AC"):
            self.audit()

    def test_source_and_receiver_double_count(self):
        self.f["network_service"] += self.f["space"]
        with self.assertRaisesRegex(ValueError, "ENERGY_RESIDUAL:CB"):
            self.audit()

    def test_duplicate_edge_in_serialized_input(self):
        with tempfile.TemporaryDirectory() as t:
            path = Path(t)/"duplicate.json"
            path.write_text('{"compressor": 2, "compressor": 2}',encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "DUPLICATE_KEY"):
                read_json(path)

    def test_grid_generation_losses_not_a_second_import(self):
        electricity = self.f["compressor"]+self.f["low_pump"]+self.f["high_pump"]
        expected = electricity*self.p["grid_pe"]+self.f["fuel"]*self.p["fuel_pe"]
        self.assertAlmostEqual(expected, impacts(self.f, self.p, "L", 120)["primary_kWh"])
        self.f["upstream_generation_losses"] = 20
        with self.assertRaisesRegex(ValueError, "MISSING_OR_DUPLICATE_EDGE"):
            self.audit()

    def test_missing_edge_and_missing_meter_are_not_zero(self):
        self.f["compressor"] = None
        with self.assertRaisesRegex(ValueError, "MISSING_OR_NONFINITE"):
            self.audit()
        del self.f["compressor"]
        with self.assertRaisesRegex(ValueError, "MISSING_OR_DUPLICATE_EDGE"):
            self.audit()

    def test_bad_unit_tag_and_missing_input(self):
        original = read_json(HERE/"P1_SYNTHETIC_INPUTS.json")
        schema = read_json(HERE/"P1_SYNTHETIC_INPUTS.schema.json")
        for change, reason in (("wrong_unit","UNIT_OR_ORIGIN"),("real","UNIT_OR_ORIGIN"),
                               ("missing","MISSING_METER"),("duplicate","DUPLICATE_OR_INVALID_SCENARIO")):
            manifest = copy.deepcopy(original)
            meter = manifest["parameters"]["source_kw"]
            if change == "wrong_unit": meter["unit"] = "kWh"
            if change == "real": meter["tag"] = "OBSERVED"
            if change == "missing": del manifest["parameters"]["source_kw"]
            if change == "duplicate": manifest["scenarios"].append(manifest["scenarios"][0])
            with self.subTest(change=change), patch.object(ledger,"read_json",side_effect=[manifest,schema]):
                with self.assertRaisesRegex(ValueError, reason):
                    load_inputs()

    def test_half_hour_conversion_independent_of_hourly_convention(self):
        f, end, hp = dispatch("R0", 0, 0, self.demand, self.p, self.routes, dt=0.5)
        self.assertEqual(f["space"],105)
        self.assertEqual(f["gross"],75)
        f["gross"] = self.p["source_kw"]
        with self.assertRaisesRegex(ValueError, "POWER_ENERGY_MISMATCH"):
            audit_hour(f,0,end,self.demand,hp,self.p,0.5,"R0")

    def test_storage_bounds_nonfinite_and_continuity(self):
        for value in (-1,self.p["tank_kwh"]+1,float("nan")):
            self.end = value
            with self.assertRaises(ValueError):
                self.audit()
        clock = ClockAudit()
        with self.assertRaisesRegex(ValueError,"SOC_CONTINUITY"):
            clock.accept(0,5,0)

    def test_stock_created_without_charge(self):
        self.end += 2
        with self.assertRaisesRegex(ValueError,"ENERGY_RESIDUAL:tank"):
            self.audit()

    def test_duplicate_hour_and_unrestored_terminal_stock(self):
        clock = ClockAudit()
        clock.accept(0,0,2)
        with self.assertRaisesRegex(ValueError,"DUPLICATE_OR_MISSING_HOUR"):
            clock.accept(0,2,0)
        clock.next_hour = 8760
        with self.assertRaisesRegex(ValueError,"TERMINAL_STOCK_OR_CLOCK"):
            clock.close()

    def test_cop_above_carnot_and_compressor_meter(self):
        cop, limit, cold, hot = self.hp
        self.hp = (limit+0.1,limit,cold,hot)
        with self.assertRaisesRegex(ValueError,"COP_BOUND"): self.audit()
        self.hp = (cop,limit,cold,hot)
        self.f["compressor"] += 1
        with self.assertRaisesRegex(ValueError,"COP_METER"): self.audit()

    def test_nonpositive_lift_and_infeasible_service_temperature(self):
        with self.assertRaisesRegex(ValueError,"LIFT"):
            heat_pump(dict(self.p,source_C=100),10,False)
        with self.assertRaisesRegex(ValueError,"SERVICE_TEMPERATURE"):
            validate_parameters(dict(self.p, hot_C=61))
        with self.assertRaisesRegex(ValueError,"EFFICIENCY"):
            validate_parameters(dict(self.p, pump_eff=0))

    def test_negative_loss_is_rejected(self):
        self.f["tank_loss"] = -0.1
        with self.assertRaisesRegex(ValueError,"NEGATIVE_FLOW:tank_loss"): self.audit()

    def test_underdelivery_and_purpose_swapping(self):
        with self.assertRaisesRegex(ValueError,"UNMET_SERVICE"):
            dispatch("R0",0,0,(700,0,10),self.p,self.routes)
        self.f["dhw"] -= 1
        self.f["space"] += 1
        with self.assertRaisesRegex(ValueError,"HOURLY_SERVICE"): self.audit()

    def test_zero_demands_and_source_outage(self):
        p = dict(self.p,source_kw=0,tank_kwh=0)
        for demand in ((0,0,10),(100,0,10)):
            f,end,hp = dispatch("T",0,0,demand,p,self.routes)
            audit_hour(f,0,end,demand,hp,p,1,"T")
            self.assertEqual(f["intercept"],0)
            self.assertEqual(f["boiler_service"],demand[0])

    def test_pipe_pump_and_exergy_against_hand_calculation(self):
        self.assertAlmostEqual(line_loss(40,65,40,self.p,1),0.8424)
        self.assertAlmostEqual(pump_work(25*4.18,25,40,self.p),33000/(1000*0.65*1000))
        q = exergy(self.f,self.hp,self.p)
        self.assertGreater(q["hp_destroyed_ex"],0)
        self.assertGreater(self.f["compressor"],q["minimum_work"])
        self.assertLess(q["service_ex"],sum(self.demand[:2]))

    def test_r0_fuel_carbon_and_cost_independent_oracle(self):
        m = self.archive["central"]["arms"]["R0"]["annual_metrics"]
        fuel = m["service_kWh"]/0.9
        self.assertAlmostEqual(m["fuel_kWh_LHV"]/fuel,1,places=12)
        self.assertAlmostEqual(m["operation_kgCO2e"],0.2*fuel,places=6)
        annuity = (1-(1.05)**-20)/0.05
        expected = (60000/annuity + 1500 + fuel*0.08)/(m["service_kWh"]/1000)
        self.assertAlmostEqual(m["LCOH_AUD_per_MWh"],expected,places=8)

    def test_cold_source_and_long_route_counterexamples(self):
        a = self.archive
        self.assertLess(a["central"]["delta_intervention_minus_reference"]["T-R1"]["primary_kWh"],0)
        for case in ("cold_source","long_pipes"):
            d = a[case]["delta_intervention_minus_reference"]["T-R1"]
            self.assertGreater(d["primary_kWh"],0)
            self.assertGreater(d["partial_life_kgCO2e"],0)
        self.assertGreater(a["long_pipes"]["arms"]["T"]["annual_edges_kWh"]["high_loss"],
                           a["central"]["arms"]["T"]["annual_edges_kWh"]["high_loss"])

    def test_seasonal_curtailment_and_winter_backup(self):
        a = self.archive["seasonal_mismatch"]["arms"]["L"]["monthly_edges_kWh"]
        central = self.archive["central"]["arms"]["L"]["monthly_edges_kWh"]
        self.assertGreater(a["1"]["bypass"], central["1"]["bypass"])
        self.assertGreater(a["7"]["boiler_service"], central["7"]["boiler_service"])

    def test_shifted_demand_matches_service_and_changes_peaks(self):
        p, _ = self.cases["diverse_demand"]
        base = [conditions(h, self.p) for h in range(8760)]
        shifted = [conditions(h, p) for h in range(8760)]
        self.assertEqual(sum(v[1] for v in base), sum(v[1] for v in shifted))
        self.assertGreater(max(s+w for s,w,_ in base), max(s+w for s,w,_ in shifted))

    def test_lifecycle_and_zero_discount(self):
        p = dict(self.p,rate=0)
        m = impacts(self.f, p, "L", 120)
        self.assertAlmostEqual(m["partial_life_kgCO2e"],20*m["operation_kgCO2e"]+m["optional_embodied_kgCO2e"])
        self.assertAlmostEqual(m["PV_cost_AUD"],sum(m["capital_AUD"].values())+20*sum(m["annual_opex_AUD"].values()))

    def test_low_and_high_segment_swaps_compose(self):
        swapped_low = self.archive["swap_low"]["arms"]
        swapped_hot = self.archive["swap_hot"]["arms"]
        self.assertEqual(swapped_low["L"], swapped_hot["T"])
        self.assertEqual(swapped_low["T"], swapped_hot["L"])

    def test_cost_and_operating_carbon_sign_reversals(self):
        a = self.archive
        for case,metric in (("cost_stress","LCOH_AUD_per_MWh"),("high_grid","operation_kgCO2e")):
            self.assertLess(a["central"]["delta_intervention_minus_reference"]["T-R0"][metric],0)
            self.assertGreater(a[case]["delta_intervention_minus_reference"]["T-R0"][metric],0)

    def test_label_null_and_storage_bypass(self):
        a = self.archive["equal_length"]["arms"]
        self.assertEqual(a["L"],a["T"])
        f = self.archive["no_store"]["arms"]["T"]["annual_edges_kWh"]
        self.assertEqual(sum(f[k] for k in ("charge","discharge","tank_loss","terminal_dump")),0)

    def test_receptor_and_global_scope_do_not_promote(self):
        for a in self.archive.values():
            self.assertEqual(a["receptor_effect"],"UNKNOWN")
            self.assertEqual(a["global_cooling"],"NOT_TESTABLE")

    def test_hourly_receipt_ids_services_and_stock(self):
        clocks = {arm:ClockAudit() for arm in ARMS}
        with gzip.open(HERE/"results/P1_HOURLY_central.csv.gz","rt",encoding="utf-8",newline="") as stream:
            reader = csv.DictReader(stream)
            self.assertEqual(len(reader.fieldnames),len(set(reader.fieldnames)))
            for row in reader:
                arm,h = row["arm"],int(row["hour"])
                self.assertEqual((row["tag"],row["case"]),("SYNTHETIC","central"))
                clocks[arm].accept(h,float(row["start_kWh"]),float(row["end_kWh"]))
                req = conditions(h,self.p)
                for k,want in zip(("space","dhw"),req):
                    self.assertAlmostEqual(float(row[k]),want,places=8)
                self.assertLess(abs(float(row["res_system"])),TOL)
        for c in clocks.values(): c.close()

    def test_offline_replay_matches_committed_results(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            write_outputs(out)
            stored = HERE/"results"
            self.assertEqual(sha(out/"P1_ENERGY_EXERGY_CARBON_LEDGER.json"),
                             sha(stored/"P1_ENERGY_EXERGY_CARBON_LEDGER.json"))
            current = read_json(out/"P1_RUN_PASSPORT.json")
            prior = read_json(stored/"P1_RUN_PASSPORT.json")
            self.assertEqual(current["inputs_and_code_sha256"],prior["inputs_and_code_sha256"])
            self.assertEqual(current["decompressed_hourly_csv_sha256"],prior["decompressed_hourly_csv_sha256"])
            for name,expected in prior["outputs_sha256"].items():
                self.assertEqual(sha(stored/name),expected)
