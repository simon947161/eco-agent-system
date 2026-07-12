"""Fixture-only failure, fallback and human-review governance."""
STATES={'NORMAL','DEGRADED','FALLBACK_PROPOSED','HUMAN_ACK_REQUIRED','RECOVERY_PENDING','RECOVERED','STOP_REQUIRED'}

def validate_event(event):
    blockers=[]
    required={'event_id','route_id','detected_at','source_conditions','primary_source_id',
              'fallback_candidates','failure_state','reason','limitations','human_review',
              'expiry','recovery','audit'}
    missing=sorted(k for k in required if k not in event)
    if missing: blockers.append({'code':'missing_event_fields','fields':missing})
    if event.get('failure_state') not in STATES: blockers.append({'code':'invalid_failure_state'})
    if event.get('fallback_candidates') and event.get('failure_state') not in {'FALLBACK_PROPOSED','HUMAN_ACK_REQUIRED','DEGRADED'}:
        blockers.append({'code':'fallback_state_mismatch'})
    if event.get('failure_state')=='STOP_REQUIRED' and event.get('fallback_candidates'):
        blockers.append({'code':'stop_required_cannot_offer_fallback'})
    output=dict(event)
    output['fallback_active']=False
    output['primary_source_id']=event.get('primary_source_id')
    output['audit']=list(event.get('audit',[]))+[{'event':'failure_record_validated'}]
    return {'valid':not blockers,'blockers':blockers,'record':output}

def record_human_ack(event, decision):
    if not decision.get('reviewer') or not decision.get('reason') or not decision.get('reviewed_at'):
        raise ValueError('reviewer, reason and reviewed_at are required')
    if decision.get('action') not in {'ACKNOWLEDGE_LIMITED_RESEARCH_FALLBACK','STOP','REQUIRE_FURTHER_EVIDENCE'}:
        raise ValueError('invalid human action')
    result=dict(event)
    result['human_review']=dict(decision)
    result['audit']=list(event.get('audit',[]))+[{'event':'human_decision_recorded','reviewer':decision['reviewer']}]
    result['fallback_active']=decision['action']=='ACKNOWLEDGE_LIMITED_RESEARCH_FALLBACK'
    return result

def automatic_failover(*_args,**_kwargs): raise PermissionError('automatic failover is prohibited')
def public_warning(*_args,**_kwargs): raise PermissionError('public warnings are prohibited')
def accept_recovery_without_evidence(*_args,**_kwargs): raise PermissionError('recovery requires new evidence')
