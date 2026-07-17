import copy
import json
import unittest
from pathlib import Path

from cczps_lite.integration.cooma_public_evidence_claims import (
    BASE_MAIN_SHA,
    CLAIM_TYPE_TO_GEOGRAPHY,
    CLAIM_TYPE_TO_SOURCE,
    CLAIM_TYPES,
    SOURCE_REGISTRY,
    CoomaClaimError,
    build_cooma_claim_preview,
    load_cooma_claim_pack,
    validate_cooma_claim_pack,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "cczps_lite" / "input" / "cooma_public_evidence_claims_pilot.json"
SCHEMA = ROOT / "cczps_lite" / "contracts" / "cooma_public_evidence_claims.schema.json"
MODULE = ROOT / "cczps_lite" / "integration" / "cooma_public_evidence_claims.py"
PREVIEW = ROOT / "cczps_lite" / "output" / "cooma_public_evidence_claims_preview.json"


class CoomaPublicEvidenceClaimTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pack = load_cooma_claim_pack(FIXTURE)

    def test_schema_is_closed_and_caps_sources_and_claims(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["selected_sources"]["maxItems"], 3)
        self.assertEqual(schema["properties"]["claims"]["maxItems"], 5)
        self.assertEqual(schema["$defs"]["claim"]["properties"]["verbatim_excerpt"]["type"], "null")
        source_rules = {
            rule["if"]["properties"]["source_id"]["const"]: {
                field: spec["const"]
                for field, spec in rule["then"]["properties"].items()
            }
            for rule in schema["$defs"]["selectedSource"]["allOf"]
        }
        self.assertEqual(source_rules, SOURCE_REGISTRY)
        claim_rules = {
            rule["if"]["properties"]["claim_type"]["const"]: rule["then"]["properties"]
            for rule in schema["$defs"]["claim"]["allOf"]
        }
        self.assertEqual(
            {claim_type: fields["source_id"]["const"] for claim_type, fields in claim_rules.items()},
            CLAIM_TYPE_TO_SOURCE,
        )
        self.assertEqual(
            {claim_type: fields["geographic_relevance"]["const"] for claim_type, fields in claim_rules.items()},
            CLAIM_TYPE_TO_GEOGRAPHY,
        )

    def test_pilot_descends_from_locked_main_and_uses_exact_authorized_mode(self) -> None:
        self.assertEqual(self.pack["pilot"]["base_main_sha"], BASE_MAIN_SHA)
        self.assertEqual(self.pack["pilot"]["mode"], "ZERO_DOWNLOAD_OFFICIAL_HTML_STRUCTURED_CLAIMS")

    def test_exact_three_registered_sources_and_five_claims(self) -> None:
        self.assertEqual(len(self.pack["selected_sources"]), 3)
        self.assertEqual({item["source_id"] for item in self.pack["selected_sources"]}, set(SOURCE_REGISTRY))
        self.assertEqual(len(self.pack["claims"]), 5)
        self.assertEqual({item["claim_type"] for item in self.pack["claims"]}, CLAIM_TYPES)

    def test_source_registry_binding_rejects_url_or_publisher_drift(self) -> None:
        for field, value in (("canonical_url", "https://example.invalid/cooma"), ("publisher", "Unknown publisher")):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.pack)
                changed["selected_sources"][0][field] = value
                with self.assertRaises(CoomaClaimError):
                    validate_cooma_claim_pack(changed)

    def test_claims_are_paraphrase_only_without_raw_content_or_reuse_claim(self) -> None:
        for claim in self.pack["claims"]:
            self.assertEqual(claim["claim_form"], "CONTROLLED_PARAPHRASE")
            self.assertIsNone(claim["verbatim_excerpt"])
            self.assertEqual(claim["licence_state"], "NOT_ASSESSED_REFERENCE_ONLY")
            self.assertFalse(claim["evidence_relation_eligible"])

        changed = copy.deepcopy(self.pack)
        changed["claims"][0]["verbatim_excerpt"] = "copied source text"
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

    def test_invalid_or_unselected_source_claim_is_rejected(self) -> None:
        changed = copy.deepcopy(self.pack)
        changed["claims"][0]["claim_id"] = "CLAIM-1"
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

    def test_claim_type_source_and_geography_mappings_are_fixed(self) -> None:
        for claim in self.pack["claims"]:
            self.assertEqual(claim["source_id"], CLAIM_TYPE_TO_SOURCE[claim["claim_type"]])
            self.assertEqual(claim["geographic_relevance"], CLAIM_TYPE_TO_GEOGRAPHY[claim["claim_type"]])

        changed = copy.deepcopy(self.pack)
        changed["claims"][0]["source_id"] = "COOMA-SRC-007"
        changed["selected_sources"][0]["claim_count"] -= 1
        changed["selected_sources"][1]["claim_count"] += 1
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

        changed = copy.deepcopy(self.pack)
        changed["claims"][0]["geographic_relevance"] = "MURRUMBIDGEE_VALLEY"
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

        changed = copy.deepcopy(self.pack)
        changed["claims"][0]["source_id"] = "COOMA-SRC-010"
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

    def test_source_claim_counts_must_match(self) -> None:
        changed = copy.deepcopy(self.pack)
        changed["selected_sources"][0]["claim_count"] = 3
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

    def test_more_than_five_claims_or_three_sources_is_rejected(self) -> None:
        changed = copy.deepcopy(self.pack)
        extra = copy.deepcopy(changed["claims"][0])
        extra["claim_id"] = "COOMA-CLAIM-006"
        changed["claims"].append(extra)
        changed["selected_sources"][0]["claim_count"] += 1
        changed["boundaries"]["structured_claim_count"] += 1
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

        changed = copy.deepcopy(self.pack)
        changed["selected_sources"].append(copy.deepcopy(changed["selected_sources"][0]))
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

    def test_relation_trials_reject_promotion_and_gate_bypass(self) -> None:
        for relation in self.pack["relation_trials"]:
            self.assertFalse(relation["evidence_relation_promoted"])
            self.assertFalse(relation["mechanism_candidate_activated"])

        changed = copy.deepcopy(self.pack)
        changed["relation_trials"][0]["evidence_relation_promoted"] = True
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

        changed = copy.deepcopy(self.pack)
        changed["relation_trials"][0]["gate_checks"]["licence"] = "PASS"
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

        changed = copy.deepcopy(self.pack)
        changed["relation_trials"][0]["gate_checks"]["licence"] = "UNKNOWN"
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

    def test_task1701_candidates_remain_synthetic_and_inactive(self) -> None:
        transition = self.pack["transition_review"]
        self.assertFalse(transition["task1701_execution_justified"])
        self.assertEqual(transition["candidate_state"], "SYNTHETIC_HYPOTHESES_ONLY_NOT_ACTIVATED")
        changed = copy.deepcopy(self.pack)
        changed["transition_review"]["task1701_execution_justified"] = True
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

    def test_all_download_private_execution_and_conclusion_boundaries_remain_false(self) -> None:
        boundaries = self.pack["boundaries"]
        true_fields = {"network_used", "public_html_accessed", "human_review_required"}
        count_fields = {"selected_source_count", "structured_claim_count", "cost_aud"}
        for field, value in boundaries.items():
            if field not in true_fields | count_fields:
                self.assertIs(value, False, field)
        changed = copy.deepcopy(self.pack)
        changed["boundaries"]["real_observations_acquired"] = True
        with self.assertRaises(CoomaClaimError):
            validate_cooma_claim_pack(changed)

    def test_preview_is_deterministic_and_promotes_no_relation(self) -> None:
        preview = build_cooma_claim_preview(self.pack)
        self.assertEqual(preview, json.loads(PREVIEW.read_text(encoding="utf-8")))
        self.assertEqual(preview["evidence_relations_promoted"], 0)
        self.assertEqual(preview["task1701_execution"], "NOT_AUTHORIZED_NOT_JUSTIFIED_BY_THIS_PILOT")

    def test_loader_and_module_have_no_runtime_network_download_or_execution_path(self) -> None:
        with self.assertRaises(CoomaClaimError):
            load_cooma_claim_pack("https://example.invalid/claims.json")
        with self.assertRaises(CoomaClaimError):
            load_cooma_claim_pack(SCHEMA)
        source = MODULE.read_text(encoding="utf-8")
        for prohibited in ("import requests", "import httpx", "urlopen(", "import socket", "import subprocess"):
            self.assertNotIn(prohibited, source)


if __name__ == "__main__":
    unittest.main()
