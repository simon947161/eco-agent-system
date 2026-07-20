from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from cczps_lite.environmental_question_runtime.continuity import (
    BACKUP_SCHEMA,
    PRIVACY_LABEL,
    ContinuityBoundaryError,
    LocalPrivateContinuity,
    canonical_json,
)
from cczps_lite.environmental_question_runtime.program import PROGRAM_ID, PersistentResearchRuntime


class LocalPrivateContinuityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.db_path = self.root / "synthetic.sqlite3"
        self.backup_root = self.root / "runtime_data" / "local_private_continuity"
        self.programs = PersistentResearchRuntime(self.db_path)
        self.cycle = self.programs.start_cycle("2026-01", PROGRAM_ID, "MONTHLY")
        self.continuity = LocalPrivateContinuity(self.programs, self.backup_root, max_bytes=128 * 1024)

    def tearDown(self) -> None:
        self.continuity.close()
        self.programs.close()
        self.temp.cleanup()

    def _envelope(self):
        return self.continuity.build_envelope(
            program_id=PROGRAM_ID,
            cycle_ids=[self.cycle["cycle_id"]],
            exported_at="2026-07-20T00:00:00Z",
        )

    def test_preview_is_deterministic_and_does_not_write(self) -> None:
        first = self.continuity.preview_backup(
            program_id=PROGRAM_ID,
            cycle_ids=[self.cycle["cycle_id"]],
            exported_at="2026-07-20T00:00:00Z",
        )
        second = self.continuity.preview_backup(
            program_id=PROGRAM_ID,
            cycle_ids=[self.cycle["cycle_id"]],
            exported_at="2026-07-20T00:00:00Z",
        )
        self.assertEqual(first["manifest"]["content_digest"], second["manifest"]["content_digest"])
        self.assertEqual(first["operation"], "PREVIEW_ONLY")
        self.assertFalse(first["would_write"])
        self.assertFalse(first["sqlite_changed"])
        self.assertFalse(self.backup_root.exists())
        self.assertEqual(first["manifest"]["schema_id"], BACKUP_SCHEMA)
        self.assertEqual(first["manifest"]["privacy_label"], PRIVACY_LABEL)
        self.assertEqual(first["manifest"]["scientific_status"], "NOT_AN_ENVIRONMENTAL_CONCLUSION")

    def test_new_file_export_verifies_and_refuses_overwrite(self) -> None:
        before = self.db_path.read_bytes()
        result = self.continuity.export_new_file(
            "synthetic-backup.json",
            program_id=PROGRAM_ID,
            cycle_ids=[self.cycle["cycle_id"]],
            exported_at="2026-07-20T00:00:00Z",
        )
        destination = self.backup_root / "synthetic-backup.json"
        self.assertTrue(destination.is_file())
        self.assertEqual(result["operation"], "NEW_FILE_EXPORT_COMPLETE")
        self.assertFalse(result["overwrite"])
        self.assertFalse(result["sqlite_changed"])
        self.assertEqual(before, self.db_path.read_bytes())
        with self.assertRaisesRegex(ContinuityBoundaryError, "overwrite refused"):
            self.continuity.export_new_file(
                "synthetic-backup.json",
                program_id=PROGRAM_ID,
                cycle_ids=[self.cycle["cycle_id"]],
                exported_at="2026-07-20T00:00:00Z",
            )

    def test_restore_preview_reports_differences_without_mutation(self) -> None:
        self.continuity.export_new_file(
            "before-change.json",
            program_id=PROGRAM_ID,
            cycle_ids=[self.cycle["cycle_id"]],
            exported_at="2026-07-20T00:00:00Z",
        )
        self.programs.add_observation(
            self.cycle["cycle_id"],
            category="WATER",
            observed_on="2026-01-15",
            note="Synthetic public-safe observation for continuity testing only.",
            location_scope="Synthetic test location",
            public_safe_confirmation=True,
        )
        before_preview = self.db_path.read_bytes()
        result = self.continuity.restore_difference_preview("before-change.json")
        self.assertEqual(result["operation"], "RESTORE_DIFFERENCE_PREVIEW_ONLY")
        self.assertFalse(result["sqlite_changed"])
        self.assertFalse(result["automatic_import_available"])
        self.assertEqual(result["cycles_changed"], [self.cycle["cycle_id"]])
        self.assertEqual(before_preview, self.db_path.read_bytes())

    def test_digest_tampering_and_count_tampering_are_rejected(self) -> None:
        envelope = self._envelope()
        envelope["content"]["program"]["title"] = "tampered"
        with self.assertRaisesRegex(ContinuityBoundaryError, "digest mismatch"):
            self.continuity.validate_envelope(canonical_json(envelope))

        envelope = self._envelope()
        envelope["manifest"]["record_counts"]["cycles"] = 99
        with self.assertRaisesRegex(ContinuityBoundaryError, "record counts"):
            self.continuity.validate_envelope(canonical_json(envelope))

    def test_malformed_and_oversized_payloads_are_rejected_before_restore(self) -> None:
        self.backup_root.mkdir(parents=True)
        (self.backup_root / "bad.json").write_bytes(b"not-json")
        with self.assertRaisesRegex(ContinuityBoundaryError, "valid UTF-8 JSON"):
            self.continuity.restore_difference_preview("bad.json")

        oversized = self.backup_root / "large.json"
        oversized.write_bytes(b"x" * (self.continuity.max_bytes + 1))
        with self.assertRaisesRegex(ContinuityBoundaryError, "size"):
            self.continuity.restore_difference_preview("large.json")

    def test_path_absolute_nested_extension_and_unknown_identity_are_rejected(self) -> None:
        invalid_names = ["../escape.json", "folder/file.json", "/absolute.json", "C:\\escape.json", "backup.txt"]
        for name in invalid_names:
            with self.subTest(name=name):
                with self.assertRaises(ContinuityBoundaryError):
                    self.continuity.export_new_file(
                        name,
                        program_id=PROGRAM_ID,
                        cycle_ids=[self.cycle["cycle_id"]],
                        exported_at="2026-07-20T00:00:00Z",
                    )
        with self.assertRaisesRegex(ContinuityBoundaryError, "unknown identity"):
            self.continuity.preview_backup(program_id=PROGRAM_ID, cycle_ids=["UNKNOWN-CYCLE"])

    @unittest.skipUnless(hasattr(os, "symlink"), "symlink support unavailable")
    def test_symlink_root_is_rejected_when_platform_allows_it(self) -> None:
        real_root = self.root / "real"
        real_root.mkdir()
        link_root = self.root / "linked"
        try:
            os.symlink(real_root, link_root, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlink creation is not permitted on this platform")
        guarded = LocalPrivateContinuity(self.programs, link_root)
        with self.assertRaisesRegex(ContinuityBoundaryError, "symlink"):
            guarded.export_new_file(
                "blocked.json",
                program_id=PROGRAM_ID,
                cycle_ids=[self.cycle["cycle_id"]],
                exported_at="2026-07-20T00:00:00Z",
            )

    def test_envelope_fields_are_closed(self) -> None:
        envelope = self._envelope()
        envelope["unexpected"] = True
        with self.assertRaisesRegex(ContinuityBoundaryError, "envelope fields"):
            self.continuity.validate_envelope(canonical_json(envelope))

        envelope = self._envelope()
        envelope["manifest"]["unexpected"] = True
        with self.assertRaisesRegex(ContinuityBoundaryError, "manifest fields"):
            self.continuity.validate_envelope(canonical_json(envelope))


if __name__ == "__main__":
    unittest.main()
