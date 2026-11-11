"""Public export schema gate; never reads or locates private assets."""
from pathlib import Path
import json,re
TASK=Path(__file__).resolve().parents[1]
ALLOW={'README.md','PUBLIC_FOUNDER_REPORT_ZH.md','NEXT_SESSION.md','QA_AND_PRIVACY.md','COMPARABILITY_MATRIX.md','PUBLIC_CASE_PROTOCOL.json','EXECUTION_STATUS.json','evidence/public_controls.json','evidence/test-summary.json','evidence/local-candidate-attestation.json','evidence/public-boundary-checks.json','scripts/public_controls.py','scripts/privacy_gate.py','scripts/public_boundary_checks.py'}

ATTESTATION_KEYS={'schema_version','evidence_level','method_identity','case_count','native_unique_cases','boundary_cases','repetitions_per_case','call_attempts','core_entries','non_null_core_returns','native_exact_replay','boundary_replay_excluding_tracebacks','native_status_messages_are_assertion_tests','harness_failed_launches_excluded','paired_prediction_accuracy_comparisons','winner','private_payload','originals_unchanged_in_inspected_set','network_and_external_write_guards_checked','boundary_outcomes','scientific_admission'}

def check_attestation(a):
    assert set(a)==ATTESTATION_KEYS,'UNAPPROVED_EXPORT_FIELD'
    assert a['schema_version']==1 and a['harness_failed_launches_excluded']==4
    for key in ('case_count','native_unique_cases','boundary_cases','repetitions_per_case','call_attempts','core_entries','non_null_core_returns','harness_failed_launches_excluded','paired_prediction_accuracy_comparisons'):
        assert type(a[key]) is int,'INVALID_COUNT_TYPE'
    for key in ('native_exact_replay','boundary_replay_excluding_tracebacks','originals_unchanged_in_inspected_set','network_and_external_write_guards_checked'):
        assert a[key] is True,'INVALID_ATTESTATION_FLAG'
    assert a['evidence_level']=='LOCAL_ATTESTATION_NOT_PUBLIC_REPRODUCTION'
    assert a['method_identity']=='VERSIONED_CANDIDATE_EXECUTED_JUMP_IDENTITY_UNCONFIRMED'
    assert a['private_payload'] is None and a['winner']=='UNKNOWN'
    assert a['paired_prediction_accuracy_comparisons']==0 and a['scientific_admission']=='PENDING'
    assert a['case_count']==a['native_unique_cases']+a['boundary_cases']==10
    assert (a['native_unique_cases'],a['boundary_cases'],a['repetitions_per_case'])==(7,3,2)
    assert a['call_attempts']==a['case_count']*a['repetitions_per_case']==20
    assert 0<=a['non_null_core_returns']<=a['core_entries']<=a['call_attempts']
    assert a['core_entries']==18 and a['non_null_core_returns']==16
    assert a['native_status_messages_are_assertion_tests'] is False
    assert a['boundary_outcomes']==[
      {'category':'missing_required_input','result':'TYPE_ERROR_BEFORE_CORE'},
      {'category':'empty_history','result':'DIVISION_BY_ZERO_IN_CORE'},
      {'category':'nonfinite_coordinate','result':'RETURNED_WITH_NONFINITE_VALUE'}]
    check_text(json.dumps(a))
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
    assert status['scientific_admission']=='PENDING' and status['legacy_code_executed'] is True
    assert status['comparison']=='PARTIAL' and status['private_evidence_publicly_reproducible'] is False
    assert status['paired_legacy_experiments_completed']==0
    check_attestation(json.loads((TASK/'evidence/local-candidate-attestation.json').read_text(encoding='utf-8')))
    return {'status':'PASS_PUBLIC_EXPORT_GATES','checked_files':files,'private_source_or_algorithm_exported':False,
            'scope':'checks newly authored public allowlist and labels; does not independently audit private files'}
if __name__=='__main__':print(json.dumps(gate(),ensure_ascii=False))
