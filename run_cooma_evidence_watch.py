"""CLI for EP-SKILL-002 offline Option B."""
import argparse,json
from pathlib import Path
from cczps_lite.evidence_watch.cooma import run,verify_fixture
def main():
 p=argparse.ArgumentParser(description="Run or verify the offline Cooma Evidence Watch; no network path exists")
 g=p.add_mutually_exclusive_group(required=True); g.add_argument("--verify-fixture",action="store_true"); g.add_argument("--request",type=Path)
 p.add_argument("--output-root",type=Path,default=Path("runtime_data/evidence_watch")); a=p.parse_args()
 if a.verify_fixture: print(json.dumps(verify_fixture(),indent=2)); return
 for key,path in run(a.output_root,request_path=a.request).items(): print(f"{key}: {path}")
if __name__=="__main__": main()
