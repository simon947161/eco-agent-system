import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from cczps_lite.environmental_question_runtime.program import PersistentResearchRuntime
from cczps_lite.environmental_question_runtime.evidence_links import (
    attach_reference, read_references, detach_reference, SOURCE_SHA, INDEX,
)


class MonthlyEvidenceLinkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name)/'research.sqlite3'
        self.runtime = PersistentResearchRuntime(self.db)
        self.cycle = self.runtime.start_cycle('2026-07')
        self.cid = self.cycle['cycle_id']

    def original(self):
        with closing(sqlite3.connect(self.db)) as db:
            return db.execute('SELECT record_json FROM research_cycles WHERE cycle_id=?',(self.cid,)).fetchone()[0]

    def test_reviewed_cycle_reopen_idempotence_and_no_receipt_mutation(self):
        self.runtime.compile_cycle(self.cid)
        reviewed = self.runtime.review_cycle(self.cid,decision='ACCEPT_CYCLE',reviewer='Test human',reason='Synthetic test acceptance, not scientific approval.')
        old = self.original()
        first=attach_reference(self.db,self.cid)
        self.assertEqual(first,attach_reference(self.db,self.cid))
        result=PersistentResearchRuntime(self.db).get_cycle(self.cid)
        self.assertEqual(result['receipt'],reviewed['receipt'])
        self.assertEqual(result['passport'],reviewed['passport'])
        self.assertEqual(result['human_review'],reviewed['human_review'])
        self.assertEqual(self.original(),old)
        self.assertEqual(len(result['evidence_references']),1)
        self.assertEqual(first[0]['source_sha256'],SOURCE_SHA)
        self.assertFalse(first[0]['original_monthly_receipt_amended'])

    def test_mismatch_and_missing_source_degrade_to_unknown(self):
        attach_reference(self.db,self.cid)
        for missing in [Path(self.temp.name)/'missing.json',Path(__file__)]:
            value=read_references(self.db,self.cid,missing)
            self.assertEqual(value[0]['reference_status'],'UNKNOWN_REFERENCE_REVALIDATION_REQUIRED')
        old=self.original()
        with patch('cczps_lite.environmental_question_runtime.evidence_links.SOURCE_SHA','0'*64):
            with self.assertRaises(ValueError):attach_reference(self.db,self.cid)
        self.assertEqual(self.original(),old)

    def test_tampered_link_conflict_no_silent_overwrite(self):
        attach_reference(self.db,self.cid)
        with closing(sqlite3.connect(self.db)) as db:
            db.execute("UPDATE research_evidence_references SET reference_json='{}'");db.commit()
        self.assertEqual(read_references(self.db,self.cid)[0]['reference_status'],'UNKNOWN_REFERENCE_REVALIDATION_REQUIRED')
        with self.assertRaises(ValueError):attach_reference(self.db,self.cid)

    def test_rollback_only_removes_link(self):
        old=self.original()
        ref=attach_reference(self.db,self.cid)[0]
        detach_reference(self.db,self.cid,ref['reference_id'])
        self.assertEqual(read_references(self.db,self.cid),[])
        self.assertEqual(self.original(),old)
        self.assertEqual(attach_reference(self.db,self.cid)[0]['reference_id'],ref['reference_id'])

    def test_requires_existing_monthly_cycle_and_invalid_source_never_writes(self):
        with self.assertRaises(ValueError):attach_reference(self.db,'missing')
        event=self.runtime.start_cycle('2026-07',trigger='MATERIAL_EVENT')
        with self.assertRaises(ValueError):attach_reference(self.db,event['cycle_id'])
        self.assertEqual(read_references(self.db,self.cid),[])


if __name__=='__main__':unittest.main()
