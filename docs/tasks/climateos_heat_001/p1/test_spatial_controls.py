"""Local controls for C-to-B tank relocation and matched synthetic service."""
import unittest

from ledger import TOL, audit_hour, load_inputs, validate_parameters
from spatial_controls import check, control_site_status


class TankLocationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p, cls.routes = load_inputs()["central"]

    def test_charging_at_b_crosses_pipe_even_without_immediate_demand(self):
        at_c, _, _, _ = check("T",10,0,(0,0,8),self.p,self.routes,False)
        at_b, _, _, residual = check("T",10,0,(0,0,8),self.p,self.routes,True)
        self.assertGreater(at_c["charge"],0)
        self.assertEqual(at_c["send"],0)
        self.assertAlmostEqual(at_b["network_service"],at_b["charge"])
        self.assertGreater(at_b["send"],at_b["charge"])
        self.assertGreater(at_b["high_pump"],0)
        self.assertLessEqual(max(map(abs,residual.values())),TOL)

    def test_discharge_at_b_bypasses_pipe_during_source_outage(self):
        p=dict(self.p,hp_kw=0)
        c=check("L",80,100,(30,10,12),p,self.routes,False)[0]
        b=check("L",80,100,(30,10,12),p,self.routes,True)[0]
        self.assertEqual(b["send"],0)
        self.assertEqual(b["high_pump"],0)
        self.assertAlmostEqual(b["discharge"],40)
        self.assertGreater(c["discharge"],b["discharge"])
        self.assertGreater(c["high_pump"],0)
        self.assertEqual(c["space"]+c["dhw"],b["space"]+b["dhw"])

    def test_terminal_stock_is_accounted_for_both_tank_locations(self):
        for moved in (True,False):
            f,end,_,_=check("T",8759,100,(0,0,8),self.p,self.routes,moved)
            self.assertEqual(end,0)
            self.assertGreater(f["terminal_dump"],0)
            self.assertAlmostEqual(f["terminal_dump"]+f["tank_loss"],100)

    def test_inadequate_backup_rejects_both_locations(self):
        for moved in (True,False):
            with self.assertRaisesRegex(ValueError,"UNMET_SERVICE"):
                check("T",4360,0,(40,20,6),dict(self.p,hp_kw=0,backup_kw=1),self.routes,moved)

    def test_pump_electricity_cannot_be_removed(self):
        f,end,hp,_=check("L",0,0,(30,10,12),self.p,self.routes,False)
        self.assertGreater(f["low_pump"],0)
        f["low_pump"]=0
        with self.assertRaisesRegex(ValueError,"ENERGY_RESIDUAL"):
            audit_hour(f,0,end,(30,10,12),hp,self.p,1,"L")

    def test_unqualified_temperature_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"SERVICE_TEMPERATURE"):
            validate_parameters(dict(self.p,hot_C=60))

    def test_no_receipt_from_location_or_heat_injection(self):
        self.assertEqual(control_site_status(),"UNKNOWN")
        self.assertEqual(control_site_status(False,True),"UNKNOWN")
        self.assertEqual(control_site_status(True,True),"REJECT_SYNTHETIC_FLAG")
        self.assertEqual(control_site_status(None,False),"REJECT_SYNTHETIC_FLAG")


if __name__=="__main__":
    unittest.main()
