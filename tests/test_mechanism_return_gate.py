import copy
import json
import unittest
from pathlib import Path

from cczps_lite.integration.mechanism_return_gate import (
    BASE_MAIN_SHA,
    COMPONENT_NAMES,
    EXPERIMENT_FIELDS,
    HYPOTHESIS_FIELDS,
    REFERENCE_REGISTRY,
    MechanismReturnGateError,
    build_mechanism_return_gate_preview,
    load_mechanism_return_gate,
    validate_mechanism_return_gate,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "cczps_lite" / "input" / "mechanism_return_gate_no_run.json"
SCHEMA = ROOT / "cczps_lite" / "contracts" / "mechanism_return_gate.schema.json"
MODULE = ROOT / "cczps_lite" / "integration" / "mechanism_return_gate.py"
PREVIEW = ROOT / "cczps_lite" / "output" / "mechanism_return_gate_preview.json"


class MechanismReturnGateTests(unittest.TestCase):
    def setUp(self):
        self.pack = load_mechanism_return_gate(FIXTURE)

    def test_locked_main_and_no_run_mode(self):
        self.assertEqual(self.pack["gate"]["base_main_sha"], BASE_MAIN_SHA)
        self.assertEqual(self.pack["gate"]["mode"], "NO_RUN_REFERENCE_REVALIDATION")

    def test_schema_is_closed_and_has_fixed_no_run_decision(self):
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["decision"]["properties"]["state"]["const"], "REFERENCE_REVIEW_INCOMPLETE")
        self.assertFalse(schema["properties"]["decision"]["properties"]["model_run_authorized"]["const"])
        self.assertFalse(schema["$defs"]["boundaries"]["properties"]["model_executed"]["const"])

    def test_five_reference_identities_remain_reference_only(self):
        self.assertEqual(len(self.pack["references"]), 5)
        self.assertEqual({x["reference_id"] for x in self.pack["references"]}, set(REFERENCE_REGISTRY))
        for ref in self.pack["references"]:
            self.assertEqual(ref["runtime_state"], "NOT_ADMITTED_NOT_EXECUTED")
            self.assertEqual(ref["climateos_use"], "REFERENCE_ONLY")

    def test_reference_kind_licence_or_artifact_promotion_fails(self):
        for field, value in (("kind", "MODEL_REPOSITORY"), ("licence_state", "PAPER_REFERENCE_ONLY"), ("artifact_state", "PUBLIC_AUTONOMOUS_CODEBASE")):
            changed = copy.deepcopy(self.pack)
            changed["references"][1][field] = value
            with self.subTest(field=field), self.assertRaises(MechanismReturnGateError):
                validate_mechanism_return_gate(changed)

    def test_runtime_dependency_promotion_fails(self):
        changed = copy.deepcopy(self.pack)
        changed["references"][0]["runtime_state"] = "ADMITTED"
        with self.assertRaises(MechanismReturnGateError):
            validate_mechanism_return_gate(changed)

    def test_wrf_components_are_separated(self):
        self.assertEqual({x["name"] for x in self.pack["model_components"]}, COMPONENT_NAMES)
        changed = copy.deepcopy(self.pack)
        changed["model_components"][1]["name"] = "WRF_CORE"
        with self.assertRaises(MechanismReturnGateError):
            validate_mechanism_return_gate(changed)

    def test_component_execution_admission_fails(self):
        changed = copy.deepcopy(self.pack)
        changed["model_components"][0]["admission_state"] = "READY_TO_RUN"
        with self.assertRaises(MechanismReturnGateError):
            validate_mechanism_return_gate(changed)

    def test_hypothesis_contract_requires_falsification_and_expert(self):
        self.assertEqual(set(self.pack["hypothesis_contract"]["required_fields"]), HYPOTHESIS_FIELDS)
        changed = copy.deepcopy(self.pack)
        changed["hypothesis_contract"]["required_fields"].remove("falsification_criteria")
        with self.assertRaises(MechanismReturnGateError):
            validate_mechanism_return_gate(changed)
        changed = copy.deepcopy(self.pack)
        changed["hypothesis_contract"]["expert_owner_required"] = False
        with self.assertRaises(MechanismReturnGateError):
            validate_mechanism_return_gate(changed)

    def test_experiment_contract_has_reproducibility_and_stop_fields(self):
        self.assertEqual(set(self.pack["experiment_contract"]["required_fields"]), EXPERIMENT_FIELDS)
        for required in ("configuration_hash", "stop_conditions", "compute_ceiling", "failure_log"):
            self.assertIn(required, EXPERIMENT_FIELDS)

    def test_run_permission_change_fails(self):
        changed = copy.deepcopy(self.pack)
        changed["experiment_contract"]["run_permission"] = "AUTHORIZED"
        with self.assertRaises(MechanismReturnGateError):
            validate_mechanism_return_gate(changed)

    def test_readiness_promotion_fails(self):
        changed = copy.deepcopy(self.pack)
        changed["readiness"]["overall"] = "READY_FOR_TINY_SYNTHETIC_DESIGN_GATE"
        with self.assertRaises(MechanismReturnGateError):
            validate_mechanism_return_gate(changed)

    def test_no_run_trials_allow_registration_and_reject_execution(self):
        outcomes = {x["request"]: x["actual"] for x in self.pack["trials"]}
        self.assertEqual(outcomes["REGISTER_NO_RUN_CONTRACT"], "ALLOW_STATIC_REGISTRATION")
        self.assertEqual(outcomes["START_WRF_CHEM_EXPERIMENT"], "REJECT_EXECUTION")
        changed = copy.deepcopy(self.pack)
        changed["trials"][1]["actual"] = "ALLOW_STATIC_REGISTRATION"
        with self.assertRaises(MechanismReturnGateError):
            validate_mechanism_return_gate(changed)

    def test_model_tiny_synthetic_and_task1711_authority_stay_false(self):
        for field in ("model_run_authorized", "tiny_synthetic_execution_authorized", "task1711_authorized"):
            changed = copy.deepcopy(self.pack)
            changed["decision"][field] = True
            with self.subTest(field=field), self.assertRaises(MechanismReturnGateError):
                validate_mechanism_return_gate(changed)

    def test_all_runtime_data_cost_and_conclusion_boundaries_hold(self):
        changed = copy.deepcopy(self.pack)
        for field in ("repository_cloned", "dataset_downloaded", "model_installed", "model_executed", "cloud_used", "api_key_used", "workos_data_used", "scientific_conclusion_formed", "local_conclusion_formed"):
            candidate = copy.deepcopy(changed)
            candidate["boundaries"][field] = True
            with self.subTest(field=field), self.assertRaises(MechanismReturnGateError):
                validate_mechanism_return_gate(candidate)
        candidate = copy.deepcopy(changed)
        candidate["boundaries"]["cost_aud"] = 1
        with self.assertRaises(MechanismReturnGateError):
            validate_mechanism_return_gate(candidate)

    def test_preview_is_deterministic(self):
        self.assertEqual(build_mechanism_return_gate_preview(self.pack), json.loads(PREVIEW.read_text(encoding="utf-8")))

    def test_loader_and_module_have_no_network_install_or_execution_path(self):
        with self.assertRaises(MechanismReturnGateError):
            load_mechanism_return_gate("https://example.invalid/gate.json")
        source = MODULE.read_text(encoding="utf-8")
        for prohibited in ("import requests", "import httpx", "urlopen(", "import socket", "import subprocess", "os.system("):
            self.assertNotIn(prohibited, source)


if __name__ == "__main__":
    unittest.main()
