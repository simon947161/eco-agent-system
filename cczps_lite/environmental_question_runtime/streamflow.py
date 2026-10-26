"""P02: fixed-source HRS import, immutable revisions and bounded readback.

No fetching on HTTP reads. Daily totals are not supply, water quality or causality.
"""
import csv
from contextlib import closing
import io
import json
import math
import sqlite3
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from .program import _digest, _stable_id

SOURCE = 'https://www.bom.gov.au/water/hrs/content/data/410033/410033_daily_ts.csv'
LICENCE = 'https://creativecommons.org/licenses/by/3.0/au/'
QUALITY = {'A': 'Best available', 'B': 'Good', 'C': 'Poor', 'E': 'Unreliable', 'G': 'Gap filled'}
METHOD = 'hrs-410033-daily-v1'


def parse(raw):
    text = raw.decode('utf-8-sig')
    required = ['Murrumbidgee River at Mittagang Crossing (410033)',
                'Daily streamflow (ML/day)', 'reported at 9am local time',
                'Dataset version:']
    if not all(value in text for value in required):
        raise ValueError('Unexpected station, units, timing or version')
    comments = [row for row in csv.reader(io.StringIO(text)) if row and row[0] == '#']
    reader = csv.DictReader(line for line in text.splitlines() if not line.startswith('#'))
    if reader.fieldnames != ['Date', 'Flow (ML)', 'Bureau QCode']:
        raise ValueError('Unexpected CSV schema')
    rows = []
    for row in reader:
        day = date.fromisoformat(row['Date'])
        if rows and day <= date.fromisoformat(rows[-1]['date']):
            raise ValueError('Duplicate or unordered date')
        quality = row['Bureau QCode'].strip()
        if quality not in QUALITY:
            raise ValueError('Unknown quality code')
        value = None if not row['Flow (ML)'].strip() else float(row['Flow (ML)'])
        if value is not None and (not math.isfinite(value) or value < 0):
            raise ValueError('Invalid flow')
        rows.append({'date': day.isoformat(), 'value': value, 'quality': quality})
    if not rows:
        raise ValueError('Empty series')
    return comments, rows


def import_series(db_path, raw):
    import hashlib
    comments, rows = parse(raw)
    sha = hashlib.sha256(raw).hexdigest()
    counts = {code: sum(r['quality'] == code for r in rows) for code in QUALITY}
    gaps = (date.fromisoformat(rows[-1]['date']) - date.fromisoformat(rows[0]['date'])).days + 1 - len(rows)
    packet = {
        'source_id': 'COOMA-FLOW-STATION-410033', 'source_url': SOURCE,
        'source_sha256': sha, 'source_header': comments,
        'source_version': next(row[1].split(':', 1)[1].strip() for row in comments if len(row) > 1 and row[1].startswith('Dataset version:')),
        'publisher': 'Australian Bureau of Meteorology', 'data_owner': 'WaterNSW',
        'attribution': '© WaterNSW; Australian Bureau of Meteorology Hydrologic Reference Stations. ClimateOS parsed daily records; no source values altered.',
        'licence': LICENCE, 'licence_evidence': 'https://www.bom.gov.au/water/hrs/copyright.shtml',
        'licence_verified_on': '2026-10-26', 'raw_publication': 'not committed; local raw snapshot retained',
        'station': {'id': '410033', 'name': 'Murrumbidgee River at Mittagang Crossing',
                    'longitude': 149.09, 'latitude': -36.17, 'catchment_km2': 1889.8,
                    'scope': 'gauge upstream catchment; not Council or town supply boundary'},
        'unit': 'ML per daily interval', 'source_column_unit': 'Flow (ML)',
        'source_description_unit': 'ML/day',
        'time_basis': 'source date labels; previous 24h reported at 09:00 local time; UTC offset unspecified, no invented UTC conversion',
        'method': METHOD, 'quality_definitions': QUALITY, 'quality_counts': counts,
        'coverage_start': rows[0]['date'], 'coverage_end': rows[-1]['date'],
        'absent_dates': gaps, 'null_values': sum(r['value'] is None for r in rows),
        'warnings': ['Header extraction date can predate records; retain source header and retrieval time separately.',
                     'HRS may contain model gap filling; G is not a measurement.',
                     'No supply sufficiency, causal, compliance or current-condition conclusion.'],
        'rows': rows,
    }
    receipt = {'receipt_id': _stable_id('HRS-RECEIPT', {'sha': sha, 'method': METHOD}),
               'input_digest': sha, 'result_digest': _digest(packet), 'method': METHOD,
               'termination': 'VALIDATED_SOURCE_RECORDS_AWAITING_HUMAN_REVIEW', 'cost_aud': 0}
    packet['receipt'] = receipt
    packet['passport'] = {'passport_id': _stable_id('HRS-PASSPORT', receipt),
                          'state': 'SOURCE_RECORDS_AWAITING_HUMAN_REVIEW',
                          'human_review_required': True, 'release_as_environmental_evidence': False,
                          'supports': 'dated source streamflow records with original quality flags',
                          'does_not_support': ['town supply adequacy', 'water quality', 'causality', 'current conditions']}
    packet['retrieved_at'] = datetime.now(timezone.utc).isoformat()
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(db_path)) as db:
        db.execute('CREATE TABLE IF NOT EXISTS hrs_revisions (sha TEXT PRIMARY KEY, packet TEXT NOT NULL, raw BLOB NOT NULL)')
        db.execute('INSERT OR IGNORE INTO hrs_revisions VALUES (?, ?, ?)', (sha, json.dumps(packet), raw))
        db.commit()
        stored = json.loads(db.execute('SELECT packet FROM hrs_revisions WHERE sha=?', (sha,)).fetchone()[0])
    return stored


def read_series(db_path, start=None, end=None, today=None):
    # Never create a database merely by viewing a page.
    if not Path(db_path).exists():
        return {'status': 'NOT_IMPORTED', 'rows': []}
    with closing(sqlite3.connect(db_path)) as db:
        if not db.execute("SELECT 1 FROM sqlite_master WHERE name='hrs_revisions'").fetchone():
            return {'status': 'NOT_IMPORTED', 'rows': []}
        result = db.execute('SELECT packet FROM hrs_revisions ORDER BY rowid DESC LIMIT 1').fetchone()
    if result is None:
        return {'status': 'NOT_IMPORTED', 'rows': []}
    packet = json.loads(result[0])
    evidence = {key: value for key, value in packet.items() if key not in ('receipt', 'passport', 'retrieved_at')}
    if _digest(evidence) != packet['receipt']['result_digest']:
        raise ValueError('Stored evidence digest mismatch; quarantine this revision')
    first, last = date.fromisoformat(packet['coverage_start']), date.fromisoformat(packet['coverage_end'])
    lower, upper = date.fromisoformat(start) if start else max(first, last - timedelta(days=365)), date.fromisoformat(end) if end else last
    if lower > upper or (upper-lower).days > 3660:
        raise ValueError('Select an ordered interval of at most ten years')
    packet['rows'] = [r for r in packet['rows'] if lower.isoformat() <= r['date'] <= upper.isoformat()]
    packet['selected_start'], packet['selected_end'] = lower.isoformat(), upper.isoformat()
    packet['selected_absent_dates'] = (upper-lower).days + 1 - len(packet['rows'])
    packet['age_days'] = ((today or date.today()) - last).days
    packet['status'] = 'HISTORICAL_STALE_FOR_CURRENT_USE' if packet['age_days'] > 90 else 'HISTORICAL_RECORDS'
    return packet
