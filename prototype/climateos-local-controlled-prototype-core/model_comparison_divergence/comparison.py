"""Fixture-only comparison and divergence layer for Task1420-1459."""
STATES = {'AGREEMENT','EVENT_SPECIFIC_DIVERGENCE','SYSTEMATIC_BIAS_EVIDENCE_REQUIRED','INSUFFICIENT_EVIDENCE','SOURCE_DEGRADED','OOD_UNRESOLVED'}

def evaluate_fixture(case):
    blockers = []
    required = {'comparison_id','route_id','variable_id','run_time_utc','valid_time_utc',
                'eligible_sources','excluded_sources','comparison_state','event_context',
                'ood_status','systematic_bias_status','downstream_uncertainty',
                'human_review_status','audit'}
    missing = sorted(k for k in required if k not in case)
    if missing: blockers.append({'code':'missing_comparison_fields','fields':missing})
    if case.get('comparison_state') not in STATES: blockers.append({'code':'invalid_comparison_state'})
    unresolved = case.get('comparison_state') in {'EVENT_SPECIFIC_DIVERGENCE','SOURCE_DEGRADED','OOD_UNRESOLVED','INSUFFICIENT_EVIDENCE'}
    if unresolved and case.get('human_review_status') != 'REQUIRED':
        blockers.append({'code':'unresolved_comparison_requires_human_review'})
    if case.get('comparison_state') == 'EVENT_SPECIFIC_DIVERGENCE' and case.get('systematic_bias_status') not in {'INSUFFICIENT_WINDOWS','NOT_EVALUATED'}:
        blockers.append({'code':'single_event_cannot_establish_systematic_bias'})
    output = dict(case)
    output['eligible_sources'] = [dict(x) for x in case.get('eligible_sources',[])]
    output['excluded_sources'] = [dict(x) for x in case.get('excluded_sources',[])]
    output['combined_value'] = None
    output['model_rank'] = None
    output['audit'] = list(case.get('audit',[])) + [{'event':'fixture_comparison_recorded'}]
    return {'valid':not blockers,'blockers':blockers,'comparison':output}

def rank_models(*_args, **_kwargs): raise PermissionError('model ranking is prohibited')
def average_disagreement(*_args, **_kwargs): raise PermissionError('silent averaging is prohibited')
def make_public_forecast(*_args, **_kwargs): raise PermissionError('public forecast is prohibited')
