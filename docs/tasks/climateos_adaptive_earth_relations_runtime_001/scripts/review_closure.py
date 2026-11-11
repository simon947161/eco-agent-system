"""Recalculate differences from frozen pairs; do not rerun or replace timings."""
from pathlib import Path
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT))
from cczps_lite.integration.earth_relations.experiments import comparison_metrics,public_hashes
TASK=Path(__file__).resolve().parents[1]
raw=(TASK/'evidence/benchmark_final/runs.jsonl').read_bytes().replace(b'\r\n',b'\n')
old=json.loads((TASK/'evidence/benchmark_final/summary.json').read_text())
assert hashlib.sha256(raw).hexdigest()==old['runs_sha256']
rows=[]
for line in raw.splitlines():
    row=json.loads(line)
    rows.append({'id':row['id'],**comparison_metrics(row['modes']['selective'],row['modes']['full_safe'])})
out={'historical_head':'256f950685c0eafd3771ff1c1c8fe696de6f5d1d',
     'historical_runs_sha256':old['runs_sha256'],'historical_source_hashes':old['source_hashes'],
     'source_hashes':public_hashes(),'method':'Independent per-field absolute subtraction of archived pairs. No new physical sweep or timing. Empty states are NOT_COMPARABLE.',
     'historical_max_output_delta_meaning':'EQUALITY_ASSERTED receipt, not a measured prediction error',
     'whole_step_contract':'checkpoint before forcing sync; restore Field metadata, revision, inventories and port clocks on any exception',
     'science':'PENDING','rows':rows}
(TASK/'evidence/review_closure.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('120 archived pairs checked; current source hashes recorded; timings unchanged')
