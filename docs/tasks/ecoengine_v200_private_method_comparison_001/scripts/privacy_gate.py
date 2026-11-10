"""Public export schema gate; never reads or locates private assets."""
from pathlib import Path
import json,re
TASK=Path(__file__).resolve().parents[1]
ALLOW={'README.md','PUBLIC_FOUNDER_REPORT_ZH.md','NEXT_SESSION.md','QA_AND_PRIVACY.md','PUBLIC_CASE_PROTOCOL.json','EXECUTION_STATUS.json','evidence/public_controls.json','evidence/test-summary.json','scripts/public_controls.py','scripts/privacy_gate.py'}
def check_text(text):
    # Disallow local drive paths and secret-bearing forms in newly authored exports.
    patterns=(r'(?<![A-Za-z])[A-Za-z]:[\\/]',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{30,}')
    assert not any(re.search(p,text) for p in patterns),'SENSITIVE_EXPORT_PATTERN'

def gate():
    files=[]
    for rel in sorted(ALLOW):
        p=TASK/rel
        if p.exists():check_text(p.read_text(encoding='utf-8'));files.append(rel)
    result=json.loads((TASK/'evidence/public_controls.json').read_text(encoding='utf-8'))
    assert result['legacy_execution_count']==0
    assert result['scope']=='public new-model controls; NOT eight completed old-versus-new experiments'
    for row in result['rows']:
        assert row['legacy'] is None and row['paired_comparison']=='NOT_EXECUTED' and row['winner']=='UNKNOWN'
        assert row['id'] in {f'C{i:02d}' for i in range(1,9)}
    status=json.loads((TASK/'EXECUTION_STATUS.json').read_text(encoding='utf-8'))
    assert status['scientific_admission']=='PENDING' and status['legacy_code_executed'] is False
    assert status['comparison']=='PARTIAL' and status['private_evidence_publicly_reproducible'] is False
    return {'status':'PASS_PUBLIC_EXPORT_GATES','checked_files':files,'private_source_or_algorithm_exported':False,
            'scope':'checks newly authored public allowlist and labels; does not independently audit private files'}
if __name__=='__main__':print(json.dumps(gate(),ensure_ascii=False))
