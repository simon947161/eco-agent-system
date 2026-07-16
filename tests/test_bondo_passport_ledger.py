"""Tests for the bounded machine-readable passport and manual ledger."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from cczps_lite.integration.bondo_passport_ledger import (
    PassportContractError, append_manual_event, load_static_passport,
    preview_internal_alert, validate_passport, verify_ledger,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE = REPO_ROOT / "cczps_lite" / "input" / "bondo_evidence_passport_static_example.json"


def fictional_event(classification: str = "NON_MATERIAL_CHANGE") -> dict:
    return {
        "event_id": "FIC-CHANGE-001",
        "observed_at": "2026-07-16T10:00:00Z",
        "event_origin": "FICTIONAL_MANUAL",
        "classification": classification,
        "summary": "Fictional repository-authored event for contract testing only.",
        "affected_claim_ids": ["C-001"],
        "affected_evidence_ids": ["E-NSW-001"],
        "re_review_required": classification not in {"NO_CHANGE", "NON_MATERIAL_CHANGE"},
        "source_access_performed": False,
        "real_data_acquired": False,
        "external_contact": False,
        "notification_sent": False,
        "scientific_conclusion_formed": False,
    }


class BondoPassportLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.passport = load_static_passport(FIXTURE)

    def test_static_passport_preserves_readable_and_controlled_states(self) -> None:
        claims = {item["claim_id"]: item for item in self.passport["claims"]}
        self.assertEqual(claims["C-001"]["readable_state"], "admitted")
        self.assertEqual(claims["C-001"]["controlled_states"], ["ADMITTED_IDENTITY"])
        self.assertIn("PROHIBITED_CONCLUSION", claims["C-010"]["controlled_states"])
        self.assertTrue(claims["C-010"]["human_review_required"])

    def test_raw_data_or_scientific_approval_is_blocked(self) -> None:
        changed = copy.deepcopy(self.passport)
        changed["passport"]["raw_data_included"] = True
        with self.assertRaisesRegex(PassportContractError, "Raw data"):
            validate_passport(changed)
        changed = copy.deepcopy(self.passport)
        changed["passport"]["human_scientific_approval"] = "APPROVED"
        with self.assertRaisesRegex(PassportContractError, "cannot record"):
            validate_passport(changed)

    def test_unknown_state_and_unresolved_reference_are_blocked(self) -> None:
        changed = copy.deepcopy(self.passport)
        changed["claims"][0]["controlled_states"] = ["TRUE"]
        with self.assertRaisesRegex(PassportContractError, "controlled_states"):
            validate_passport(changed)
        changed = copy.deepcopy(self.passport)
        changed["claims"][0]["supporting_evidence_ids"] = ["E-MISSING-001"]
        with self.assertRaisesRegex(PassportContractError, "unresolved references"):
            validate_passport(changed)

    def test_manual_events_form_and_verify_hash_chain(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "events.jsonl"
            first = append_manual_event(ledger, fictional_event())
            second_event = fictional_event("MATERIAL_METADATA_CHANGE")
            second_event["event_id"] = "FIC-CHANGE-002"
            second = append_manual_event(ledger, second_event)
            records = verify_ledger(ledger)
            self.assertEqual(len(records), 2)
            self.assertEqual(second["previous_hash"], first["record_hash"])

    def test_tampered_ledger_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "events.jsonl"
            append_manual_event(ledger, fictional_event())
            record = json.loads(ledger.read_text(encoding="utf-8"))
            record["event"]["summary"] = "tampered"
            ledger.write_text(json.dumps(record) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(PassportContractError, "record_hash"):
                verify_ledger(ledger)

    def test_network_contact_data_and_conclusion_flags_are_blocked(self) -> None:
        for field in ("source_access_performed", "real_data_acquired", "external_contact", "notification_sent", "scientific_conclusion_formed"):
            event = fictional_event()
            event[field] = True
            with self.subTest(field=field):
                with self.assertRaisesRegex(PassportContractError, "blocked"):
                    append_manual_event("events.jsonl", event)

    def test_alert_is_deterministic_preview_only(self) -> None:
        event = fictional_event("MATERIAL_SCIENTIFIC_CHANGE")
        preview = preview_internal_alert(event)
        self.assertTrue(preview["preview_only"])
        self.assertFalse(preview["dispatch_performed"])
        self.assertEqual(preview["severity"], "REVIEW_REQUIRED")

    def test_fixture_loader_blocks_paths_outside_repository_input(self) -> None:
        with self.assertRaisesRegex(PassportContractError, "cczps_lite/input"):
            load_static_passport(REPO_ROOT / "README.md")


if __name__ == "__main__":
    unittest.main()
