"""Fixture-only coupling input eligibility gate for Task1490-1499."""
STATES={'COUPLING_INPUT_CANDIDATE','CANDIDATE_WITH_LIMITATIONS','REQUIRES_FURTHER_EVIDENCE','BLOCKED'}
REQUIRED_SCOPE={'source_id','source_version','variables','region','forecast_horizons','licence_status','evidence_snapshot_id','review_date','expiry_date','responsible_human'}
REQUIRED_EVIDENCE={'model_admission','source_registry','common_weather_data','orchestration','comparison_divergence','failure_fallback','regional_fitness','licence_commercial_rights'}

def evaluate_fixture(case):
    blockers=[]
    missing_scope=sorted(k for k in REQUIRED_SCOPE if not case.get(k))
    if missing_scope: blockers.append({'code':'missing_scope','fields':missing_scope})
    evidence=case.get('evidence',{})
    missing_evidence=sorted(k for k in REQUIRED_EVIDENCE if k not in evidence)
    if missing_evidence: blockers.append({'code':'missing_evidence','fields':missing_evidence})
    state=case.get('requested_state')
    if state not in STATES: blockers.append({'code':'invalid_state'})
    favourable=state in {'COUPLING_INPUT_CANDIDATE','CANDIDATE_WITH_LIMITATIONS'}
    if favourable and (missing_scope or missing_evidence or case.get('licence_status') in {'unknown','blocked'}):
        blockers.append({'code':'favourable_state_blocked'})
    if state=='COUPLING_INPUT_CANDIDATE' and case.get('limitations'):
        blockers.append({'code':'unlimited_candidate_cannot_hide_limitations'})
    result=dict(case)
    result['connection_authorized']=False
    result['task1500_authorized']=False
    return {'valid':not blockers,'blockers':blockers,'record':result}

def connect_source(*_args,**_kwargs): raise PermissionError('source connection is prohibited')
def calculate_coupling(*_args,**_kwargs): raise PermissionError('coupling calculation is prohibited')
def start_task1500(*_args,**_kwargs): raise PermissionError('Task1500 requires separate authorization')
