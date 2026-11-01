"""Read-only HRS evidence association; never rewrite or re-review a cycle.

The separate link table is NOT part of a previously issued monthly Receipt.
"""
import hashlib
import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
INDEX = REPO / 'apps/regional-public-os/data/index.json'
INDEX_SHA = 'bd4728ea129330d5e1abd35dce9b223df87c6801c18ad52e7d9db0eb7e0d45ca'
SOURCE_SHA = '78e8188f3f445afa33ad466dd0554e653761ef617832b6df3a9eac6b1240ca1a'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def accepted_reference(index_path=INDEX):
    raw = Path(index_path).read_bytes()
    if digest(raw) != INDEX_SHA:
        raise ValueError('Accepted HRS index mismatch')
    index = json.loads(raw)
    metadata = index['metadata']
    if metadata['source_sha256'] != SOURCE_SHA:
        raise ValueError('Accepted HRS source mismatch')
    # Ensure the referenced package is actually available and still accepted.
    for shard in index['shards']:
        file = Path(shard['file'])
        if file.name != shard['file']:
            raise ValueError('Invalid shard path')
        if digest((Path(index_path).parent / file).read_bytes()) != shard['sha256']:
            raise ValueError('Referenced HRS shard mismatch')
    return {
        'source_id': metadata['source_id'], 'source_sha256': SOURCE_SHA,
        'index_sha256': INDEX_SHA, 'data_package_sha256': index['data_package_sha256'],
        'source_url': metadata['source_url'], 'source_version': metadata['source_version'],
        'coverage_start': metadata['coverage_start'], 'coverage_end': metadata['coverage_end'],
        'station': metadata['station'], 'unit': metadata['unit'], 'time_basis': metadata['time_basis'],
        'licence': metadata['licence'], 'attribution': metadata['attribution'],
        'receipt': metadata['receipt'], 'passport': metadata['passport'],
        'reference_path': 'apps/regional-public-os/data/index.json',
        'private_site': 'https://climateos-snowy-monaro.minshu.chatgpt.site',
        'temporal_status': 'HISTORICAL_STALE_FOR_CURRENT_USE',
        'human_scientific_review': 'PENDING',
        'association_meaning': 'POSTHOC_READ_ONLY_REFERENCE_NOT_PART_OF_ORIGINAL_MONTHLY_REVIEW',
        'original_monthly_receipt_amended': False,
        'current_conditions_supported': False,
    }


def attach_reference(db_path, cycle_id, index_path=INDEX):
    reference = accepted_reference(index_path)
    with closing(sqlite3.connect(Path(db_path).resolve().as_uri()+'?mode=rw', uri=True)) as db:
        db.execute('BEGIN IMMEDIATE')
        row = db.execute('SELECT record_json FROM research_cycles WHERE cycle_id=?', (cycle_id,)).fetchone()
        if row is None:
            raise ValueError('Existing cycle required; no cycle will be created')
        cycle = json.loads(row[0])
        if cycle['program_id'] != 'COOMA-WATER-FIRE-WASTEWATER-WATCH' or cycle['trigger'] != 'MONTHLY':
            raise ValueError('An existing monthly Cooma program cycle is required')
        reference.update(cycle_id=cycle_id, year_month=cycle['year_month'], original_cycle_sha256=digest(row[0].encode('utf-8')))
        reference['reference_id'] = 'HRS-CYCLE-LINK-' + digest((cycle_id+SOURCE_SHA+INDEX_SHA).encode())[:16].upper()
        canonical = json.dumps(reference, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        db.execute('CREATE TABLE IF NOT EXISTS research_evidence_references (cycle_id TEXT NOT NULL, source_id TEXT NOT NULL, reference_json TEXT NOT NULL, reference_digest TEXT NOT NULL, linked_at TEXT NOT NULL, PRIMARY KEY(cycle_id,source_id))')
        old = db.execute('SELECT reference_json,reference_digest FROM research_evidence_references WHERE cycle_id=? AND source_id=?', (cycle_id, reference['source_id'])).fetchone()
        if old and (old[0] != canonical or old[1] != digest(canonical.encode('utf-8'))):
            raise ValueError('Conflicting evidence link; no overwrite allowed')
        db.execute('INSERT OR IGNORE INTO research_evidence_references VALUES (?,?,?,?,?)', (cycle_id,reference['source_id'],canonical,digest(canonical.encode('utf-8')),datetime.now(timezone.utc).isoformat()))
        db.commit()
    return read_references(db_path, cycle_id, index_path)


def read_references(db_path, cycle_id, index_path=INDEX):
    with closing(sqlite3.connect(Path(db_path).resolve().as_uri()+'?mode=ro',uri=True)) as db:
        if not db.execute("SELECT 1 FROM sqlite_master WHERE name='research_evidence_references'").fetchone():
            return []
        cycle = db.execute('SELECT record_json FROM research_cycles WHERE cycle_id=?', (cycle_id,)).fetchone()
        links = db.execute('SELECT reference_json,reference_digest,linked_at FROM research_evidence_references WHERE cycle_id=? ORDER BY source_id', (cycle_id,)).fetchall()
    results = []
    for raw, expected, linked_at in links:
        # No mutable or corrupt reference is allowed to present as verified.
        try:
            if digest(raw.encode('utf-8')) != expected:
                raise ValueError('Link digest mismatch')
            ref = json.loads(raw)
            if cycle is None or digest(cycle[0].encode('utf-8')) != ref['original_cycle_sha256']:
                raise ValueError('Referenced cycle revision changed')
            verified = accepted_reference(index_path)
            if any(ref[key] != value for key,value in verified.items()):
                raise ValueError('Reference no longer matches accepted source')
            results.append(dict(ref, linked_at=linked_at, reference_status='VERIFIED_REFERENCE_ONLY'))
        except (OSError, ValueError, KeyError, TypeError):
            results.append({'cycle_id':cycle_id,'reference_status':'UNKNOWN_REFERENCE_REVALIDATION_REQUIRED',
                            'current_conditions_supported':False,'original_monthly_receipt_amended':False})
    return results


def detach_reference(db_path, cycle_id, reference_id):
    """Narrow rollback of the sidecar link only; keep all original cycle records."""
    with closing(sqlite3.connect(Path(db_path).resolve().as_uri()+'?mode=rw',uri=True)) as db:
        rows = db.execute('SELECT source_id,reference_json FROM research_evidence_references WHERE cycle_id=?', (cycle_id,)).fetchall()
        for source_id, raw in rows:
            if json.loads(raw).get('reference_id') == reference_id:
                db.execute('DELETE FROM research_evidence_references WHERE cycle_id=? AND source_id=?', (cycle_id,source_id))
        db.commit()
