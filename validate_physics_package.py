"""Check actual output/package links and exact-byte source manifests offline."""
import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parent
TASK=ROOT/'docs/tasks/climateos_physics_validation_001'
CODE=['cczps_lite/integration/physics_validation.py','tests/test_physics_validation.py',
      'run_physics_validation.py','run_physics_tests.py','build_physics_report.py',
      'validate_physics_package.py','tools/physics_qa/report_qa.cjs',
      'tools/physics_qa/package.json','tools/physics_qa/package-lock.json']


class Report(HTMLParser):
    def __init__(self):super().__init__();self.sections=0;self.local=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='section':self.sections+=1
        for key in ['href','src']:
            value=a.get(key,'')
            if value and '://' not in value and not value.startswith('#'):
                self.local.append(unquote(value.split('#')[0]))
        if tag in ['script','img','link']:
            assert not a.get('src',a.get('href','')).startswith(('http:','https:')),'automatic network dependency'


def files():
    return [ROOT/x for x in CODE]+[p for p in TASK.rglob('*') if p.is_file() and p.name not in ['manifest.json','validation.json'] and not any(x in p.parts for x in ['qa','__pycache__'])]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-manifest',action='store_true');args=parser.parse_args()
    if args.write_manifest:
        manifest={'hash_algorithm':'SHA-256 exact bytes; new files protected by .gitattributes -text',
                  'base_HEAD':'37c4b093e511bd9b5014c276390ebde114d28eed',
                  'scope':'new physics code, task inputs, outputs, charts, test logs and QA; self manifest and validation excluded',
                  'files':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files())}}
        (TASK/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    manifest=json.loads((TASK/'manifest.json').read_text(encoding='utf-8'))
    for name,digest in manifest['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    report=Report();report.feed((TASK/'index.html').read_text(encoding='utf-8'))
    assert report.sections==12
    for target in report.local:assert (TASK/target).exists(),target
    for path in TASK.glob('*.json'):json.loads(path.read_text(encoding='utf-8'))
    bal=json.loads((TASK/'conservation.json').read_text(encoding='utf-8'))
    assert bal['P2_max_absolute_residual_kg']<1e-12
    assert bal['P2_minimum_stock_kg']>=0
    assert bal['P3_absolute_carbon_residual_Gg_C']<1e-12
    assert bal['P3_max_methane_partition_residual_Gg']<1e-12
    assert bal['P4_max_absolute_carbon_residual_Gg_C']<1e-12
    assert bal['P4_max_methane_partition_residual_Gg']<1e-12
    assert bal['P4_minimum_DDOC_Gg_C']>=0
    assert bal['P4_neutral_max_absolute_difference_Gg_CH4']==0
    for name in ['physics-tests.json','full-suite.json']:
        assert json.loads((TASK/name).read_text(encoding='utf-8'))['successful']
    qa=json.loads((TASK/'browser_qa.json').read_text(encoding='utf-8'));assert qa['status']=='PASS' and qa['render_combinations']==24
    assert not qa['automatic_network_requests'] and not qa['console_errors']
    result={'status':'PASS_RESTRICTED_SYNTHETIC_IMPLEMENTATION',
            'report_pages':12,'local_html_targets_checked':len(report.local),
            'source_and_artifact_hashes_checked':len(manifest['files']),
            'physical_parameter_calibration':'NOT_PERFORMED','independent_observational_validation':'NOT_PERFORMED',
            'D3':'DATA_NOT_READY','P1_A':'PENDING','ChatGPT_scientific_review':'REQUESTED_PENDING'}
    (TASK/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
