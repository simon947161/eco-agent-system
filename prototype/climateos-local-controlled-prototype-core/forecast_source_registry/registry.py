"""Task1300-1339 structural source registry. No network or execution."""
import json
from pathlib import Path

STATES = [
    'VERIFIED_CANDIDATE', 'CONNECTED_FOR_RESEARCH',
    'CONNECTED_WITH_LIMITATIONS', 'DEFERRED_UNVERIFIED',
    'DEFERRED_ACCESS_OR_LICENCE', 'CUSTOMER_REQUESTED_EXPERIMENT',
    'NOT_SUITABLE_FOR_DECLARED_USE', 'RETIRED_OR_UNAVAILABLE',
]

REQUIRED = {
    'source_id', 'provider', 'product', 'source_class', 'version_status',
    'variables', 'grid', 'vertical_levels', 'update_cycle', 'latency',
    'archive', 'licence', 'commercial_rights', 'interface',
    'access_status', 'cost_status', 'service_level', 'maturity',
    'limitations', 'decision_owner', 'evidence_date', 'review_trigger',
    'source_state',
}

def validate_source(record):
    missing = sorted(k for k in REQUIRED if k not in record or record[k] in (None, ''))
    blockers = []
    if missing:
        blockers.append({'code': 'missing_required_metadata', 'fields': missing})
    if record.get('source_state') not in STATES:
        blockers.append({'code': 'invalid_source_state'})
    if record.get('source_state') == 'CUSTOMER_REQUESTED_EXPERIMENT':
        controls = record.get('experiment_controls', {})
        required = {'separate_approval', 'explicit_opt_in', 'risk_disclosure',
                    'bounded_trial', 'audit', 'stop_condition', 'exit_path'}
        absent = sorted(k for k in required if not controls.get(k))
        if absent:
            blockers.append({'code': 'customer_experiment_controls_missing',
                             'fields': absent})
    return {'valid': not blockers, 'blockers': blockers}

def load_registry(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    return [validate_source(item) for item in data['sources']]

def connect_source(*_args, **_kwargs):
    raise PermissionError('Task1300-1339 does not authorize source connection')

def activate_customer_experiment(*_args, **_kwargs):
    raise PermissionError('customer experiments require separate approval')
