import copy
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

from cczps_lite.integration.cooma_official_source_metadata import (
    ACCESS_DATE,
    ALLOWED_DOMAINS,
    BASE_MAIN_SHA,
    CoomaSourceMetadataError,
    RETAINED_FIELDS,
    SOURCE_TIERS,
    build_cooma_source_metadata_preview,
    load_cooma_source_metadata,
    validate_cooma_source_metadata,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "cczps_lite" / "input" / "cooma_official_source_metadata_pilot.json"
SCHEMA = ROOT / "cczps_lite" / "contracts" / "cooma_official_source_metadata.schema.json"
MODULE = ROOT / "cczps_lite" / "integration" / "cooma_official_source_metadata.py"
PREVIEW = ROOT / "cczps_lite" / "output" / "cooma_official_source_metadata_preview.json"


class CoomaOfficialSourceMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.pack = load_cooma_source_metadata(FIXTURE)

    def test_schema_is_closed_and_restricts_zero_download_boundaries(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertFalse(schema["additionalProperties"])
        boundaries = schema["properties"]["boundaries"]["properties"]
        self.assertFalse(boundaries["dataset_downloaded"]["const"])
        self.assertFalse(boundaries["pdf_or_document_downloaded"]["const"])
        self.assertEqual(boundaries["cost_aud"]["const"], 0)

    def test_pilot_descends_from_current_main_and_records_real_metadata_access_truthfully(self) -> None:
        self.assertEqual(self.pack["pilot"]["base_main_sha"], BASE_MAIN_SHA)
        self.assertEqual(self.pack["pilot"]["accessed_on"], ACCESS_DATE)
        self.assertTrue(self.pack["boundaries"]["network_used"])
        self.assertTrue(self.pack["boundaries"]["public_pages_accessed"])
        self.assertTrue(self.pack["boundaries"]["real_page_metadata_retained"])

    def test_complete_source_tier_registry_and_ten_bounded_records(self) -> None:
        self.assertEqual(set(self.pack["source_tiers"]), SOURCE_TIERS)
        self.assertEqual(len(self.pack["records"]), 10)
        self.assertEqual(len({record["source_id"] for record in self.pack["records"]}), 10)

    def test_every_url_is_clean_https_on_an_approved_official_domain(self) -> None:
        for record in self.pack["records"]:
            parsed = urlparse(record["canonical_url"])
            normalized = parsed.netloc.removeprefix("www.")
            self.assertEqual(parsed.scheme, "https")
            self.assertEqual(record["domain"], normalized)
            self.assertIn(normalized, ALLOWED_DOMAINS)
            self.assertFalse(parsed.query)
            self.assertFalse(parsed.fragment)

        changed = copy.deepcopy(self.pack)
        changed["records"][0]["canonical_url"] = "https://example.invalid/cooma"
        changed["records"][0]["domain"] = "example.invalid"
        with self.assertRaises(CoomaSourceMetadataError):
            validate_cooma_source_metadata(changed)

    def test_only_fixed_metadata_fields_are_retained(self) -> None:
        for record in self.pack["records"]:
            self.assertEqual(set(record["retained_metadata_fields"]), RETAINED_FIELDS)
            self.assertEqual(record["licence_state"], "NOT_ASSESSED_REFERENCE_ONLY")
            self.assertEqual(record["reuse_permission"], "NOT_CLAIMED")

        changed = copy.deepcopy(self.pack)
        changed["records"][0]["retained_metadata_fields"].append("PAGE_BODY")
        with self.assertRaises(CoomaSourceMetadataError):
            validate_cooma_source_metadata(changed)

    def test_raw_content_files_datasets_and_reuse_claims_are_blocked(self) -> None:
        for field in ("raw_content_retained", "file_downloaded", "dataset_downloaded"):
            changed = copy.deepcopy(self.pack)
            changed["records"][0][field] = True
            with self.subTest(field=field):
                with self.assertRaises(CoomaSourceMetadataError):
                    validate_cooma_source_metadata(changed)

        changed = copy.deepcopy(self.pack)
        changed["records"][0]["reuse_permission"] = "OPEN_REUSE"
        with self.assertRaises(CoomaSourceMetadataError):
            validate_cooma_source_metadata(changed)

    def test_official_news_is_quarantined_as_discovery_only(self) -> None:
        news = [record for record in self.pack["records"] if record["source_kind"] == "OFFICIAL_NEWS_ITEM"]
        self.assertEqual(len(news), 1)
        self.assertEqual(news[0]["admission_state"], "DISCOVERY_ONLY_QUARANTINED")

        changed = copy.deepcopy(self.pack)
        changed["records"][-1]["admission_state"] = "METADATA_ADMITTED_REFERENCE_ONLY"
        with self.assertRaises(CoomaSourceMetadataError):
            validate_cooma_source_metadata(changed)

    def test_official_websites_are_not_treated_as_complete_databases(self) -> None:
        governance = self.pack["governance"]
        self.assertEqual(governance["website_completeness_status"], "NOT_ASSUMED_COMPLETE")
        self.assertEqual(governance["conflict_policy"], "RECORD_WITHOUT_RESOLUTION")
        changed = copy.deepcopy(self.pack)
        changed["governance"]["website_completeness_status"] = "ASSUMED_COMPLETE"
        with self.assertRaises(CoomaSourceMetadataError):
            validate_cooma_source_metadata(changed)

    def test_csiro_specific_and_internal_council_sources_remain_deferred(self) -> None:
        states = {item["candidate_class"]: item["state"] for item in self.pack["deferred_candidates"]}
        self.assertEqual(states["CSIRO_COOMA_SPECIFIC_SOURCE"], "NOT_IDENTIFIED_IN_BOUNDED_OFFICIAL_SEARCH")
        self.assertEqual(states["INTERNAL_COUNCIL_DATABASE"], "OUT_OF_SCOPE_NOT_ACCESSED")

    def test_private_operational_and_all_conclusion_boundaries_remain_closed(self) -> None:
        boundaries = self.pack["boundaries"]
        for field in (
            "private_worksite_data_included", "customer_or_person_data_included",
            "local_conclusion_formed", "external_contact_made", "monitoring_active", "model_executed",
        ):
            self.assertFalse(boundaries[field])
        self.assertTrue(all(value == "NONE" for key, value in self.pack["governance"].items() if key.endswith("conclusion")))

    def test_preview_is_deterministic_and_promotes_no_evidence(self) -> None:
        preview = build_cooma_source_metadata_preview(self.pack)
        self.assertEqual(preview, json.loads(PREVIEW.read_text(encoding="utf-8")))
        self.assertEqual(preview["metadata_admitted_reference_only"], 9)
        self.assertEqual(preview["news_discovery_quarantined"], 1)
        self.assertEqual(preview["raw_documents_downloaded"], 0)
        self.assertEqual(preview["datasets_downloaded"], 0)
        self.assertEqual(preview["evidence_relations_promoted"], 0)

    def test_loader_and_module_have_no_runtime_network_or_download_path(self) -> None:
        with self.assertRaises(CoomaSourceMetadataError):
            load_cooma_source_metadata("https://example.invalid/metadata.json")
        with self.assertRaises(CoomaSourceMetadataError):
            load_cooma_source_metadata(SCHEMA)
        source = MODULE.read_text(encoding="utf-8")
        for prohibited in ("import requests", "import httpx", "urlopen(", "import socket", "import subprocess"):
            self.assertNotIn(prohibited, source)


if __name__ == "__main__":
    unittest.main()
