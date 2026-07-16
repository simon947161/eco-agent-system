"""Tests for the bounded Task1661–1670 environmental coupling prototype."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from cczps_lite.integration.environmental_coupling import (
    CouplingContractError,
    build_internal_coupling_preview,
    load_static_coupling_graph,
    validate_coupling_graph,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "cczps_lite" / "input" / "australian_environmental_coupling_static_example.json"
SCHEMA = REPO_ROOT / "cczps_lite" / "contracts" / "environmental_coupling_relation.schema.json"
MODULE = REPO_ROOT / "cczps_lite" / "integration" / "environmental_coupling.py"
PREVIEW = REPO_ROOT / "cczps_lite" / "output" / "environmental_coupling_static_preview.json"


class EnvironmentalCouplingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = load_static_coupling_graph(FIXTURE)

    def test_schema_is_closed_draft_2020_12_contract(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(schema["properties"]["boundaries"]["properties"]["cost_aud"]["const"], 0)

    def test_static_australian_chain_validates_without_a_conclusion(self) -> None:
        validate_coupling_graph(self.graph)
        self.assertEqual(len(self.graph["states"]), 5)
        self.assertEqual(len(self.graph["relations"]), 4)
        self.assertTrue(all("PROHIBITED_CONCLUSION" in item["governance_states"] for item in self.graph["relations"]))

    def test_all_network_data_model_monitoring_action_and_conclusion_flags_are_blocked(self) -> None:
        fields = (
            "network_used", "real_data_accessed", "model_executed", "monitoring_active",
            "external_action", "scientific_conclusion_formed", "project_performance_conclusion_formed",
        )
        for field in fields:
            changed = copy.deepcopy(self.graph)
            changed["boundaries"][field] = True
            with self.subTest(field=field):
                with self.assertRaisesRegex(CouplingContractError, "must remain false"):
                    validate_coupling_graph(changed)

    def test_nonzero_cost_and_removed_human_review_are_blocked(self) -> None:
        changed = copy.deepcopy(self.graph)
        changed["boundaries"]["cost_aud"] = 1
        with self.assertRaisesRegex(CouplingContractError, "remain zero"):
            validate_coupling_graph(changed)
        changed = copy.deepcopy(self.graph)
        changed["boundaries"]["human_review_required"] = False
        with self.assertRaisesRegex(CouplingContractError, "remain true"):
            validate_coupling_graph(changed)

    def test_observed_association_and_model_inference_are_blocked(self) -> None:
        for relation_type, message in (
            ("observed_association", "separately authorized evidence gate"),
            ("model_inference", "Model inference"),
        ):
            changed = copy.deepcopy(self.graph)
            changed["relations"][0]["relationship_type"] = relation_type
            with self.subTest(relation_type=relation_type):
                with self.assertRaisesRegex(CouplingContractError, message):
                    validate_coupling_graph(changed)

    def test_causal_hypothesis_must_route_to_task1701_plus(self) -> None:
        changed = copy.deepcopy(self.graph)
        changed["relations"][1]["future_mechanism_test_id"] = None
        with self.assertRaisesRegex(CouplingContractError, "future_mechanism_test_id"):
            validate_coupling_graph(changed)
        changed = copy.deepcopy(self.graph)
        changed["relations"][1]["governance_states"].remove("ROUTE_TO_TASK1701_PLUS")
        with self.assertRaisesRegex(CouplingContractError, "route to Task1701"):
            validate_coupling_graph(changed)

    def test_lagged_signal_cannot_claim_an_estimated_window(self) -> None:
        changed = copy.deepcopy(self.graph)
        changed["relations"][0]["lead_lag_window"]["minimum"] = 1
        with self.assertRaisesRegex(CouplingContractError, "No lead-lag value"):
            validate_coupling_graph(changed)

    def test_unknown_state_source_and_missing_stationarity_warning_are_blocked(self) -> None:
        changed = copy.deepcopy(self.graph)
        changed["relations"][0]["target_state_id"] = "STATE-UNKNOWN"
        with self.assertRaisesRegex(CouplingContractError, "unknown states"):
            validate_coupling_graph(changed)
        changed = copy.deepcopy(self.graph)
        changed["states"][0]["evidence_source_ids"] = ["SYN-SRC-999"]
        with self.assertRaisesRegex(CouplingContractError, "unknown synthetic sources"):
            validate_coupling_graph(changed)
        changed = copy.deepcopy(self.graph)
        changed["relations"][0]["stationarity_warning"] = ""
        with self.assertRaisesRegex(CouplingContractError, "stationarity_warning"):
            validate_coupling_graph(changed)

    def test_cycles_are_blocked(self) -> None:
        changed = copy.deepcopy(self.graph)
        closing_relation = copy.deepcopy(changed["relations"][0])
        closing_relation["relation_id"] = "REL-999"
        closing_relation["source_state_id"] = "STATE-GOVERNANCE-001"
        closing_relation["target_state_id"] = "STATE-CLIMATE-001"
        changed["relations"].append(closing_relation)
        with self.assertRaisesRegex(CouplingContractError, "cycles are blocked"):
            validate_coupling_graph(changed)

    def test_safe_governance_states_cannot_be_dropped(self) -> None:
        for safe_state in ("SYNTHETIC_ONLY", "HYPOTHESIS_ONLY", "HUMAN_REVIEW_REQUIRED", "PROHIBITED_CONCLUSION"):
            changed = copy.deepcopy(self.graph)
            changed["relations"][0]["governance_states"].remove(safe_state)
            with self.subTest(safe_state=safe_state):
                with self.assertRaisesRegex(CouplingContractError, "retain all"):
                    validate_coupling_graph(changed)

    def test_internal_preview_is_deterministic_and_not_decision_ready(self) -> None:
        first = build_internal_coupling_preview(self.graph)
        second = build_internal_coupling_preview(self.graph)
        self.assertEqual(first, second)
        self.assertEqual(first, json.loads(PREVIEW.read_text(encoding="utf-8")))
        self.assertEqual(first["scientific_conclusion"], "NONE")
        self.assertEqual(first["governance_recommendation"], "NONE")
        self.assertEqual(first["decision_support_status"], "NOT_READY_FOR_DECISION")
        self.assertEqual(first["future_mechanism_test_ids"], [
            "TASK1701-CANDIDATE-001", "TASK1701-CANDIDATE-002", "TASK1701-CANDIDATE-003"
        ])

    def test_loader_and_module_have_no_external_runtime_path(self) -> None:
        with self.assertRaisesRegex(CouplingContractError, "cczps_lite/input"):
            load_static_coupling_graph(REPO_ROOT / "README.md")
        with self.assertRaisesRegex(CouplingContractError, "URL and network"):
            load_static_coupling_graph("https://example.invalid/graph.json")
        source = MODULE.read_text(encoding="utf-8")
        for prohibited_import in ("import requests", "import urllib", "import socket", "import subprocess"):
            self.assertNotIn(prohibited_import, source)


if __name__ == "__main__":
    unittest.main()
