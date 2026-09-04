import argparse
from pathlib import Path
from cczps_lite.site_reading.cooma import run
if __name__=="__main__":
 p=argparse.ArgumentParser(); p.add_argument("--output-root",type=Path,default=Path("cczps_lite/output/cooma_site_reading_v0_1")); p.add_argument("--request",type=Path,default=Path("cczps_lite/input/cooma_site_reading_request_r1.json")); p.add_argument("--issued-at"); a=p.parse_args()
 for n,path in run(a.output_root,request_path=a.request,issued_at=a.issued_at).items(): print(f"{n}: {path}")
