"""Task1340-1379 synthetic Common Weather Data Contract validator."""
from datetime import datetime, timedelta, timezone

SECTIONS = {'source', 'forecast_time', 'spatial', 'vertical', 'fields', 'quality', 'provenance'}
QUALITY_FLAGS = {'VALID', 'MISSING', 'STALE', 'INVALID', 'TRANSFORMED', 'OUT_OF_DOMAIN'}

def _utc(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('timezone required')
    return parsed.astimezone(timezone.utc)

def validate_record(record):
    blockers = []
    missing = sorted(k for k in SECTIONS if k not in record)
    if missing:
        return {'valid': False, 'blockers': [{'code': 'missing_sections', 'fields': missing}]}
    timing = record['forecast_time']
    required_time = {'run_time_utc','valid_time_utc','lead_hours','member_type','member_id'}
    absent = sorted(k for k in required_time if k not in timing or timing[k] in (None, ''))
    if absent:
        blockers.append({'code': 'missing_forecast_time', 'fields': absent})
    else:
        expected = _utc(timing['run_time_utc']) + timedelta(hours=timing['lead_hours'])
        if _utc(timing['valid_time_utc']) != expected:
            blockers.append({'code': 'valid_time_lead_mismatch'})
        if timing['member_type'] == 'ENSEMBLE' and not timing['member_id']:
            blockers.append({'code': 'ensemble_member_id_required'})
    if record['spatial'].get('effective_resolution_status') in (None, ''):
        blockers.append({'code': 'effective_resolution_status_required'})
    for field in record['fields']:
        if field.get('quality_flag') not in QUALITY_FLAGS:
            blockers.append({'code': 'invalid_quality_flag'})
    provenance = record['provenance']
    for key in ('evidence_snapshot_id','retrieval_or_fixture_id','transformations','checksum','responsible_human'):
        if key not in provenance or provenance[key] in (None, ''):
            blockers.append({'code': 'missing_provenance', 'field': key})
    return {'valid': not blockers, 'blockers': blockers}

def ingest_live_data(*_args, **_kwargs):
    raise PermissionError('Task1340-1379 does not authorize live data')

def orchestrate_sources(*_args, **_kwargs):
    raise PermissionError('Task1380 orchestrator is not authorized')
