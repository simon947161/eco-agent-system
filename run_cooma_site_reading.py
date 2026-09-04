"""CLI for verifying the committed fixture or producing a new immutable revision."""
import argparse,json
from pathlib import Path
from cczps_lite.site_reading.cooma import run,verify_fixture

def main():
 p=argparse.ArgumentParser(description="Verify EP-SKILL-001's committed fixture or run an explicitly supplied new revision. Immutable revision directories are never overwritten.")
 mode=p.add_mutually_exclusive_group(required=True)
 mode.add_argument("--verify-fixture",action="store_true",help="rebuild the committed R1 fixture in a temporary directory and compare it without changing tracked files")
 mode.add_argument("--request",type=Path,help="path to a new SiteReadingRequest with a unique revision_id")
 p.add_argument("--output-root",type=Path,default=Path("runtime_data/site_readings"),help="artifact root for a new revision (default: untracked runtime_data/site_readings)")
 p.add_argument("--issued-at",help="optional machine-readable issue time for a new revision; current UTC is used when omitted")
 a=p.parse_args()
 if a.verify_fixture:
  print(json.dumps(verify_fixture(),indent=2)); return
 for name,path in run(a.output_root,request_path=a.request,issued_at=a.issued_at).items(): print(f"{name}: {path}")
if __name__=="__main__": main()
