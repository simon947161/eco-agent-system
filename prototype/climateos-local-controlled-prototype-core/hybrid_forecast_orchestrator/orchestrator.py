"""Fixture-only Hybrid Forecast Orchestrator for Task1380-1419."""
AVAILABILITY = {'AVAILABLE', 'STALE', 'MISSING', 'INVALID', 'DEFERRED'}

def build_route(case):
    blockers = []
    required = {'route_id','run_time_utc','valid_time_utc','variable_id','sources',
                'reference_source_id','fallback_source_ids','disagreement_status',
                'human_review_status','audit'}
    missing = sorted(k for k in required if k not in case)
    if missing:
        blockers.append({'code': 'missing_route_fields', 'fields': missing})
    sources = case.get('sources', [])
    invalid = [s.get('source_id') for s in sources if s.get('availability') not in AVAILABILITY]
    if invalid:
        blockers.append({'code': 'invalid_availability', 'sources': invalid})
    degraded = [s['source_id'] for s in sources if s.get('availability') != 'AVAILABLE']
    if degraded and case.get('human_review_status') != 'REQUIRED':
        blockers.append({'code': 'degraded_source_requires_human_review'})
    if len([s for s in sources if s.get('availability') == 'AVAILABLE']) < 2:
        if case.get('disagreement_status') not in {'INSUFFICIENT_SOURCES','SOURCE_DEGRADED'}:
            blockers.append({'code': 'insufficient_sources_must_be_exposed'})
    output = dict(case)
    output['sources'] = [dict(s) for s in sources]
    output['audit'] = list(case.get('audit', [])) + [{'event': 'fixture_route_built'}]
    output['numeric_combination'] = None
    output['automatic_best_source'] = None
    return {'valid': not blockers, 'blockers': blockers, 'route': output}

def average_sources(*_args, **_kwargs):
    raise PermissionError('silent or automatic averaging is prohibited')

def select_best_source(*_args, **_kwargs):
    raise PermissionError('automatic best-model selection is prohibited')

def call_live_source(*_args, **_kwargs):
    raise PermissionError('live sources are not authorized')

def public_forecast(*_args, **_kwargs):
    raise PermissionError('public forecasting is not authorized')
