"""Read frozen output JSONs and compare displayed rounding; no model is run.

Requires the already-fetched public PR Git objects. No network and no original
data download. Multiplication by 1e6 is only kg-to-mg display formatting.
"""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / 'docs/tasks/climateos_explainable_science_web_001'
snapshot = json.loads((TASK / 'REMOTE_PR_SNAPSHOT.json').read_text(encoding='utf-8'))
heads = {p['number']: p['head_sha'] for p in snapshot['pull_requests']}
text = '\n'.join((ROOT / f'cczps_lite/dashboard/science/{name}').read_text(encoding='utf-8') for name in ['content.js','science.js'])
checks = []
cache = {}

def check(pr, filename, pointer, display, decimals=6, scale=1):
    if (pr, filename) not in cache:
        raw = subprocess.check_output(['git','show',f'{heads[pr]}:{filename}'],cwd=ROOT)
        cache[(pr,filename)] = (json.loads(raw),hashlib.sha256(raw).hexdigest())
    value, digest = cache[(pr,filename)]
    for part in pointer.split('/'):
        value = value[int(part)] if isinstance(value,list) else value[part]
    if value is None:
        assert display == 'null'
        assert '保留空值' in text and '未知部分不能按零排放处理' in text
    else:
        formatted = f'{value * scale:.{decimals}f}'
        assert formatted == display, (filename,pointer,formatted,display)
        assert display in text, (filename,display)
    checks.append({'pr':pr,'sha':heads[pr],'file':filename,'file_sha256':digest,'json_pointer':'/'+pointer,'archived_value':value,'display':display,'unit_scale_for_display':scale,'pass':True})

p = 'docs/tasks/climateos_physics_validation_001/'
check(138,p+'p1.json','rows/0/mass_concentration_kg_per_m3','1.333853',scale=1_000_000)
check(138,p+'p1.json','rows/4/mass_concentration_kg_per_m3','1.053129',scale=1_000_000)
check(138,p+'p1.json','rows/6/mass_concentration_kg_per_m3','1.039964673',decimals=9,scale=1_000_000)
for case,display in [('falling','0.037632'),('steady','0.024000'),('rising','0.010368')]:
    check(138,p+'p2.json',f'runs/{case}/vented_kg',display)
check(138,p+'p3.json','total_generated_CH4_Gg','1.183144192',decimals=9)
check(138,p+'p3.json','total_emitted_CH4_Gg','0.638897864',decimals=9)
check(138,p+'p3.json','final_DDOC_Gg_C','0.975284')
for case,display in [('C0','0.638897864'),('C1_temperature_only','0.662229328'),('C1_moisture_only','0.670311180')]:
    check(138,p+'p4.json',f'{case}/total_emitted_CH4_Gg',display,decimals=9)
check(138,p+'p4.json','neutral_max_abs_error_Gg','0',decimals=0)
for case,display in [('A','0'),('B','469.353312'),('C','469.353312'),('D','null')]:
    check(163,'docs/tasks/climateos_awt_001/evidence/results.json',f'{case}/calculation/estimated_net_abatement_t_CO2e',display,decimals=0 if case=='A' else 6)
result = {'scope':'Read-only transcription and display-rounding audit; no research recomputation','passed':len(checks),'failed':0,'checks':checks}
(TASK/'evidence/archived-value-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'archived_value_checks':len(checks),'passed':len(checks),'models_run':0}))
