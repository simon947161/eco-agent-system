"""Associate accepted source evidence with one existing MONTHLY cycle only."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cczps_lite.environmental_question_runtime.evidence_links import attach_reference, detach_reference

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--db',type=Path,required=True)
    p.add_argument('--cycle-id',required=True)
    p.add_argument('--remove-reference-id',help='Rollback this sidecar link only; no original record changes')
    args=p.parse_args()
    if args.remove_reference_id:
        detach_reference(args.db,args.cycle_id,args.remove_reference_id)
        print('Sidecar rollback complete; original cycle untouched')
    else:
        result=attach_reference(args.db,args.cycle_id)
        print(json.dumps([{k:r.get(k) for k in ('reference_id','cycle_id','year_month','source_sha256','reference_status','association_meaning')} for r in result],indent=2))
