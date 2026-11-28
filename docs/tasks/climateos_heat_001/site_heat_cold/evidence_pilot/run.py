"""Run admitted datasets and compare outputs with reviewed receipts. No network."""
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FISH = '10.5281/zenodo.6563580'


def verified(script, receipt, *args):
    command = [sys.executable, str(ROOT / script), *args]
    output = subprocess.check_output(command)
    if output != (ROOT / receipt).read_bytes():
        raise ValueError(f'Replay differs from {receipt}')
    return hashlib.sha256(output).hexdigest()


def run(candidate=None):
    if candidate is not None:
        discovery = json.loads(candidate.read_bytes())
        if discovery.get('status') != 'CANDIDATE_ONLY':
            return {'status': 'NO_CANDIDATE'}
        record = discovery.get('selected') or {}
        if record.get('doi') != FISH:
            return {'status': 'REQUIRES_SOURCE_REVIEW', 'doi': record.get('doi')}
    with tempfile.TemporaryDirectory() as folder:
        clean = Path(folder) / 'clean.csv'
        fish_hash = verified('fish/replay.py', 'fish/receipt.json', str(clean))
        if clean.read_bytes() != (ROOT / 'fish/cleaned.csv').read_bytes():
            raise ValueError('Cleaned meter table differs')
    result = {'status': 'REPLAY_VERIFIED', 'fish_receipt_sha256': fish_hash,
              'site_investment_decision': 'DATA_NOT_READY'}
    if candidate is None:
        result['hardwick_receipt_sha256'] = verified('hardwick/hardwick.py', 'hardwick/hardwick_result.json')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate-receipt', type=Path)
    print(json.dumps(run(parser.parse_args().candidate_receipt), indent=2))
