#!/usr/bin/env python3
"""Validate the audit artefacts, not application behaviour or official admission."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
APP=HERE.parents[2]
ROOT=APP.parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
data=json.loads((HERE/'closure-baseline.json').read_text())
registry=json.loads((APP/'COI_TASK_REGISTRY_V1_7.json').read_text())
tasks=data['tasks']
assert len(tasks)==80
assert [r['id'] for r in tasks]==[f'COI-{i:03d}' for i in range(1,81)]
original={r['id']:r for r in registry['tasks']}
allowed={'PUBLIC_SOURCE_RESEARCH','RUNTIME_INTEGRATION','FOUNDER_DECISION','AUTHORISED_PRIVATE_ACCESS','HUMAN_OR_HARDWARE_ACCEPTANCE'}
reference_checks=0
test_checks=0
for row in tasks:
    src=original[row['id']]
    assert row['exactOriginalRequirement']==src['title_and_scope']
    assert row['registryStatus']==src['status']
    assert row['recommendedStatus']=='KEEP_'+src['status']
    assert row['founderActionNeededNow'] is False
    assert row['officialAdmission']=='PENDING_NOT_GRANTED'
    assert set(row['gapTypes']) <= allowed
    for key in ['actualBoundedImplementation','remainingGap','independentlyExecutableNextAction','completionCriterion','whatDoesNotRequireFounderAction','staleOrOverbroadPlanAssessment','softwareCapabilityAssessment','publicEvidenceAssessment','humanAdmissionAssessment','subcriteria']:
        assert row[key], (row['id'],key)
    requirement=row['requirementReference']
    line=(ROOT/requirement['path']).read_text().splitlines()[requirement['line']-1]
    observed=line.split('**'+row['id']+'** ',1)[1].replace('**','').strip()
    assert observed==row['exactOriginalRequirement'].replace('**','').strip(),row['id']
    refs=[row['requirementReference'],row['registryReference'],*row['implementationEvidence']]
    for test in row['testEvidence']:
        refs += [test['testFile'],test['recordedResult']]
        assert test['runInThisAudit'] is False
        assert test['currentTestFileMatchesRecordedSHA256'] is True
        assert test['recordedStatus']=='PASS_TESTED_HERE'
        test_checks+=1
    for reference in refs:
        path=ROOT/reference['path']
        assert path.is_file(),reference
        assert sha(path)==reference['sha256'],reference
        lines=path.read_text().splitlines()
        assert 1<=reference['line']<=len(lines),reference
        if not reference['locator'].startswith('line '):
            assert reference['locator'] in lines[reference['line']-1],reference
        reference_checks+=1
with (HERE/'closure-baseline.csv').open(encoding='utf-8-sig',newline='') as f:
    csv_rows=list(csv.DictReader(f))
assert len(csv_rows)==80
for row,c in zip(tasks,csv_rows):
    assert row['id']==c['id']
    assert row['exactOriginalRequirement']==c['exactOriginalRequirement']
    assert row['remainingGap']==c['remainingGap']
assert Counter(r['registryStatus'] for r in tasks)=={'VERIFIED':49,'PARTIAL':28,'BLOCKED':3}
assert data['statusChangesApplied']==0 and data['newApplicationTestsExecuted'] is False
result={
    'format':'csoi-audit-artefact-validation-1',
    'status':'PASS_AUDIT_ARTEFACT_CHECKS_ONLY',
    'baselineCommit':data['baselineCommit'],
    'rows':80,
    'originalMasterPlanRequirementsMatched':80,
    'registryStatusesPreserved':80,
    'csvRowsMatched':80,
    'fileLineSHAReferenceChecks':reference_checks,
    'recordedTestSHAReferencesMatched':test_checks,
    'newApplicationTestsExecuted':False,
    'networkOrPrivateAccessPerformed':False,
    'statusPromotionsApplied':0,
    'runtimeRegistrySiteMutationsPerformed':False,
    'artefacts':{name:sha(HERE/name) for name in ['closure-baseline.json','closure-baseline.csv','evidence-index.json','REPORT_ZH.md','build_baseline.py']},
    'limitations':['Author audit; independent parent review still required for task closure decisions.','Recorded app tests are previous verified results, not tests run by this audit.','Complete engineering/source/legal/actual work acceptance is not asserted.']
}
(HERE/'audit-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
