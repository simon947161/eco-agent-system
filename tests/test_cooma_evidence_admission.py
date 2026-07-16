import copy
import json
import unittest
from pathlib import Path

from cczps_lite.integration.cooma_evidence_admission import (
    CoomaAdmissionError,
    REQUIRED_INTERFACE_BLOCKS,
    REQUIRED_TRANSLATION_CHECKS,
    build_cooma_admission_preview,
    load_fictional_cooma_pack,
    validate_cooma_admission_pack,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "cczps_lite" / "input" / "cooma_evidence_admission_fictional_examples.json"
SCHEMA = ROOT / "cczps_lite" / "contracts" / "cooma_regional_evidence_admission.schema.json"
PREVIEW = ROOT / "cczps_lite" / "output" / "cooma_evidence_admission_preview.json"


class CoomaEvidenceAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pack = load_fictional_cooma_pack(FIXTURE)

    def test_schema_is_closed_draft_2020_12_contract(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["research_anchor"]["properties"]["place_name"]["const"], "Cooma")

    def test_static_pack_validates_with_named_anchor_but_no_local_conclusion(self) -> None:
        validate_cooma_admission_pack(self.pack)
        anchor = self.pack["research_anchor"]
        self.assertEqual(anchor["place_name"], "Cooma")
        self.assertEqual(anchor["local_conclusion_state"], "NONE")
        self.assertEqual(anchor["exact_worksite"], "NOT_PROVIDED_NOT_REQUIRED")

    def test_all_external_and_conclusion_boundaries_remain_false_and_zero_cost(self) -> None:
        boundaries = self.pack["boundaries"]
        for field, value in boundaries.items():
            if field not in {"cost_aud", "human_review_required"}:
                self.assertIs(value, False)
        self.assertEqual(boundaries["cost_aud"], 0)
        self.assertIs(boundaries["human_review_required"], True)

        changed = copy.deepcopy(self.pack)
        changed["boundaries"]["source_accessed"] = True
        with self.assertRaises(CoomaAdmissionError):
            validate_cooma_admission_pack(changed)

    def test_nonfictional_or_source_backed_candidate_is_blocked(self) -> None:
        for field, value in (
            ("fictional", False),
            ("external_locator", "https://example.invalid/source"),
            ("content_retained", True),
            ("observed_time", "2026-01-01"),
            ("source_identity_state", "VERIFIED"),
        ):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.pack)
                changed["candidate_records"][0][field] = value
                with self.assertRaises(CoomaAdmissionError):
                    validate_cooma_admission_pack(changed)

    def test_unverified_candidate_cannot_claim_visibility_or_reuse_permission(self) -> None:
        for field, value in (("licence_state", "OPEN_REUSE_CONFIRMED"), ("visibility_state", "PUBLIC")):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.pack)
                changed["candidate_records"][0][field] = value
                with self.assertRaises(CoomaAdmissionError):
                    validate_cooma_admission_pack(changed)

    def test_scale_hierarchy_blocks_mixing_and_automatic_translation(self) -> None:
        changed = copy.deepcopy(self.pack)
        changed["scale_objects"][2]["rank"] = 4
        with self.assertRaises(CoomaAdmissionError):
            validate_cooma_admission_pack(changed)

        changed = copy.deepcopy(self.pack)
        changed["scale_objects"][2]["automatic_translation_allowed"] = True
        with self.assertRaises(CoomaAdmissionError):
            validate_cooma_admission_pack(changed)

    def test_every_translation_retains_full_manual_gate_and_blocked_output(self) -> None:
        for rule in self.pack["translation_rules"]:
            self.assertEqual(set(rule["required_checks"]), REQUIRED_TRANSLATION_CHECKS)
            self.assertFalse(rule["automatic_translation"])
            self.assertEqual(rule["output_state"], "BLOCKED_PENDING_EVIDENCE_AND_HUMAN_REVIEW")

        changed = copy.deepcopy(self.pack)
        changed["translation_rules"][0]["required_checks"].remove("STATIONARITY")
        with self.assertRaises(CoomaAdmissionError):
            validate_cooma_admission_pack(changed)

    def test_uncertainty_and_nonstationarity_cannot_be_assessed_without_evidence(self) -> None:
        changed = copy.deepcopy(self.pack)
        changed["candidate_records"][0]["uncertainty"]["stationarity"] = "ASSUMED_STABLE"
        with self.assertRaises(CoomaAdmissionError):
            validate_cooma_admission_pack(changed)

    def test_review_roles_are_placeholders_without_authority(self) -> None:
        self.assertTrue(all(role["appointment_state"] == "UNASSIGNED" for role in self.pack["review_roles"]))
        changed = copy.deepcopy(self.pack)
        changed["review_roles"][0]["decision_authority"] = "APPROVE_EVIDENCE"
        with self.assertRaises(CoomaAdmissionError):
            validate_cooma_admission_pack(changed)

    def test_workos_interface_blocks_private_compliance_legal_and_operational_fields(self) -> None:
        interface = self.pack["climateos_workos_interface"]
        self.assertTrue(REQUIRED_INTERFACE_BLOCKS <= set(interface["blocked_fields"]))
        self.assertEqual(interface["writeback_state"], "BLOCKED_PENDING_SEPARATE_AUTHORIZATION")

        changed = copy.deepcopy(self.pack)
        changed["climateos_workos_interface"]["blocked_fields"].remove("PROPERTY_OR_WORKSITE_ADDRESS")
        with self.assertRaises(CoomaAdmissionError):
            validate_cooma_admission_pack(changed)

    def test_preview_is_deterministic_and_admits_nothing(self) -> None:
        preview = build_cooma_admission_preview(self.pack)
        self.assertEqual(preview, json.loads(PREVIEW.read_text(encoding="utf-8")))
        self.assertEqual(preview["scale_count"], 6)
        self.assertEqual(preview["candidate_record_count"], 4)
        self.assertEqual(preview["admitted_evidence_count"], 0)
        self.assertEqual(preview["source_access_count"], 0)
        self.assertEqual(preview["local_environmental_conclusion"], "NONE")
        self.assertEqual(preview["compliance_decision"], "NONE")

    def test_loader_rejects_urls_and_paths_outside_repository_fixture_root(self) -> None:
        with self.assertRaises(CoomaAdmissionError):
            load_fictional_cooma_pack("https://example.invalid/cooma.json")
        with self.assertRaises(CoomaAdmissionError):
            load_fictional_cooma_pack(SCHEMA)


if __name__ == "__main__":
    unittest.main()
