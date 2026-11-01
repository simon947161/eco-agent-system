"""Build a public-safe policy packet for the existing ClimateOS Console.

Local original files are read-only. No PDF bodies, absolute paths or personnel
records enter the output. A missing copy does not block other research work.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONFIG = REPO / 'config/regional-public-os/smrc-policy-sources.json'


def configured_directories(repo=REPO):
    paths = []
    if os.environ.get('CLIMATEOS_PUBLIC_SOURCE_DIR'):
        paths.append(Path(os.environ['CLIMATEOS_PUBLIC_SOURCE_DIR']))
    private_config = repo / '.local/smrc-source-locations.json'
    if private_config.exists():
        value = json.loads(private_config.read_text(encoding='utf-8'))
        paths.extend(Path(item) for item in value.get('source_dirs', []))
    return paths


def file_digest(path):
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def build_packet(config, source_dirs=()):
    if config.get('data_class') != 'PUBLIC_REFERENCE_METADATA':
        raise ValueError('Only reviewed public-reference metadata is supported')
    rows = []
    seen = set()
    for document in config['documents']:
        name = document['filename']
        if Path(name).name != name or '/' in name or '\\' in name:
            raise ValueError('Document name must be a basename')
        if document['id'] in seen:
            raise ValueError('Duplicate source identity')
        seen.add(document['id'])
        expected = document.get('sha256')
        if expected is not None and (len(expected) != 64 or any(c not in '0123456789abcdef' for c in expected)):
            raise ValueError('Invalid SHA256')
        found = []
        inaccessible = False
        for root in source_dirs:
            candidate = Path(root) / name
            try:
                if candidate.is_file():
                    found.append(file_digest(candidate))
            except OSError:
                inaccessible = True
        if not found:
            state = 'LOCAL_COPY_INACCESSIBLE' if inaccessible else 'MISSING_LOCAL_COPY'
        elif expected is None:
            state = 'NEW_COPY_REQUIRES_ADMISSION'
        elif any(h != expected for h in found):
            state = 'QUARANTINED_VERSION_MISMATCH'
        else:
            state = 'MATCHED_RECORDED_VERSION'
        rows.append(dict(document, local_copy_state=state,
                         source_body_published=False, current_execution_authority=False))
    return {
        'schema_id': 'climateos.smrc_policy_console.v0.1',
        'mission_id': config['mission_id'], 'parent_issue': 128,
        'data_class': 'PUBLIC_REFERENCE_METADATA', 'sources': rows,
        'research_lines': config['research_lines'],
        'mapping_state': 'RESEARCH_CROSSWALK_NOT_STATUTORY_INTERPRETATION',
        'review_state': 'HUMAN_REVIEW_REQUIRED',
        'network_used': False, 'official_decision': None,
        'personnel_model': 'ROLE_BASED_CURRENT_NAMES_NOT_INFERRED_FROM_HISTORICAL_FILES'
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, default=CONFIG)
    parser.add_argument('--source-dir', action='append', type=Path, default=[])
    parser.add_argument('--out', type=Path, default=REPO / '.local/smrc-policy-console/packet.json')
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding='utf-8'))
    result = build_packet(config, [*configured_directories(), *args.source_dir])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'mission_id': result['mission_id'], 'source_states': {s['id']: s['local_copy_state'] for s in result['sources']}, 'network_used': False}))


if __name__ == '__main__':
    main()
