"""Export one pinned, verified local HRS revision; never export SQLite or paths."""
import argparse
import hashlib
import json
import sqlite3
import sys
from contextlib import closing
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cczps_lite.environmental_question_runtime.streamflow import parse
from cczps_lite.environmental_question_runtime.program import _digest

PIN = '78e8188f3f445afa33ad466dd0554e653761ef617832b6df3a9eac6b1240ca1a'
BASELINE = '6ca8f9d913e99ba66d4743790b2e4f0df11cf571'


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')


def export(db_path, output):
    with closing(sqlite3.connect(Path(db_path).resolve().as_uri() + '?mode=ro', uri=True)) as db:
        record = db.execute('SELECT packet,raw FROM hrs_revisions WHERE sha=?', (PIN,)).fetchone()
    if record is None:
        raise ValueError('Pinned accepted revision missing')
    packet, raw = json.loads(record[0]), record[1]
    if hashlib.sha256(raw).hexdigest() != PIN:
        raise ValueError('Raw source digest mismatch')
    comments, rows = parse(raw)
    if packet['rows'] != rows or packet['source_header'] != comments:
        raise ValueError('Persisted rows differ from source parsing')
    evidence = {k: v for k, v in packet.items() if k not in ('receipt', 'passport', 'retrieved_at')}
    if _digest(evidence) != packet['receipt']['result_digest']:
        raise ValueError('Source evidence digest mismatch')
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    shards = []
    for year in sorted({row['date'][:4] for row in rows}):
        selected = [row for row in rows if row['date'].startswith(year)]
        content = encoded(selected)
        name = year + '.json'
        (output / name).write_bytes(content)
        shards.append({'file': name, 'start': selected[0]['date'], 'end': selected[-1]['date'],
                       'count': len(selected), 'sha256': hashlib.sha256(content).hexdigest()})
    metadata = {k: v for k, v in packet.items() if k != 'rows'}
    index = {'schema': 'climateos.hrs.sites.snapshot.v1', 'metadata': metadata,
             'source_code_baseline': BASELINE, 'transformer': 'tools/export_hrs_sites.py',
             'transformer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'transformation': 'validate raw/source equality and existing receipt; partition unchanged rows by calendar label year; canonical JSON UTF-8',
             'records': len(rows), 'shards': shards, 'read_only': True,
             'python_refresh_status': 'HTTP_403', 'automatic_updates': False,
             'scientific_review': 'PENDING',
             'data_package_sha256': hashlib.sha256(encoded(shards)).hexdigest()}
    content = encoded(index)
    (output / 'index.json').write_bytes(content)
    manifest = {'index_sha256': hashlib.sha256(content).hexdigest(),
                'data_package_sha256': index['data_package_sha256'], 'source_sha256': PIN,
                'source_code_baseline': BASELINE, 'records': len(rows)}
    (output / 'manifest.json').write_bytes(encoded(manifest))
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', type=Path, required=True)
    parser.add_argument('--output', type=Path, default=Path('apps/regional-public-os/data'))
    args = parser.parse_args()
    print(json.dumps(export(args.db, args.output), indent=2))
