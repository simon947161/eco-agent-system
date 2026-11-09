"""Run from repository root. Offline; writes only this task's evidence directory."""
from pathlib import Path
import hashlib
import json
import platform
import sys
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from cczps_lite.integration.client_ai_evidence import execute

TASK = Path(__file__).resolve().parent
OUT = TASK / 'evidence'


def main():
    request = json.loads((TASK/'request.json').read_text(encoding='utf-8'))
    tracemalloc.start(); start=time.perf_counter()
    result=execute(request)
    elapsed=time.perf_counter()-start; _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    if result['status']!='LOCAL_VERIFIED_PUBLIC_DESCRIPTIVE_SLICE':
        raise SystemExit(json.dumps(result,ensure_ascii=False))
    OUT.mkdir(exist_ok=True)
    def write(name,obj):
        (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    write('audit.json',result)
    write('station.geojson',result['spatial_result'])
    (OUT/'CLIENT_REPORT_ZH.md').write_text(result['observation_result']['report_zh']+'\n空间结果：station.geojson；单站边界框可复算，无受体距离或地块边界推断。\n',encoding='utf-8')
    write('runtime.json',{'python':platform.python_version(),'platform':platform.system(),'elapsed_seconds':elapsed,
                        'peak_traced_python_bytes':peak,'measurement_scope':'one local execute call; excludes interpreter startup; not total RSS',
                        'added_dependencies':[],'hardware_cost':'UNKNOWN','external_requests':0})
    print(json.dumps({'status':result['status'],'elapsed_seconds':elapsed,'peak_traced_python_bytes':peak},ensure_ascii=False))


if __name__=='__main__':
    main()
