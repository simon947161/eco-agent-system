"""Manual fixed-source refresh. Raw bytes and database stay local."""
import argparse
import json
import sys
from pathlib import Path
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cczps_lite.environmental_question_runtime.streamflow import SOURCE, import_series

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', type=Path, default=Path('runtime_data/task2002_environmental_questions.sqlite3'))
    parser.add_argument('--snapshot', type=Path, help='Previously retrieved official CSV; never synthetic data')
    args = parser.parse_args()
    if args.snapshot:
        raw = args.snapshot.read_bytes()
    else:
        with urlopen(SOURCE, timeout=30) as response:
            if response.url != SOURCE:
                raise ValueError('Unexpected redirect')
            raw = response.read(8_000_001)
    if len(raw) > 8_000_000:
        raise ValueError('Source exceeds size limit')
    packet = import_series(args.db, raw)
    print(json.dumps({k: packet[k] for k in ('source_sha256', 'coverage_start', 'coverage_end', 'quality_counts', 'absent_dates', 'null_values', 'receipt', 'passport')}, indent=2))
