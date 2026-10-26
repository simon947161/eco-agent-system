"""Risk checks with explicitly synthetic CSV; real-data acceptance is separate."""
import json
from contextlib import closing
import sqlite3
import tempfile
import threading
import unittest
from datetime import date
from pathlib import Path
from urllib.request import urlopen

from cczps_lite.environmental_question_runtime.streamflow import import_series, read_series
from cczps_lite.environmental_question_runtime.server import create_server

FIXTURE = b'''#,"Murrumbidgee River at Mittagang Crossing (410033)"
#,"Daily streamflow (ML/day) reported at 9am local time"
#,"Dataset version: SYNTHETIC TEST ONLY"
Date,Flow (ML),Bureau QCode
2020-01-01,2,B
2020-01-03,5,G
2020-01-04,,E
'''


class HRSStreamflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / 'research.sqlite3'

    def test_restart_idempotence_gaps_quality_and_historical_status(self):
        first = import_series(self.db, FIXTURE)
        self.assertEqual(first, import_series(self.db, FIXTURE))
        result = read_series(self.db, '2020-01-01', '2020-01-04', date(2026,10,26))
        self.assertEqual(result['selected_absent_dates'], 1)
        self.assertEqual(result['null_values'], 1)
        self.assertEqual(result['rows'][1]['quality'], 'G')
        self.assertEqual(result['status'], 'HISTORICAL_STALE_FOR_CURRENT_USE')
        self.assertFalse(result['passport']['release_as_environmental_evidence'])
        self.assertEqual(read_series(self.db, '2020-01-03', '2020-01-03')['rows'][0]['value'], 5)

    def test_reject_wrong_station_units_quality_duplicates_and_nonfinite(self):
        for before, after in [(b'410033', b'999999'), (b'ML/day', b'm3/s'),
                              (b'2,B', b'NaN,B'), (b'2,B', b'-1,B'),
                              (b'2,B', b'2,Z'), (b'2020-01-03', b'2020-01-01')]:
            with self.subTest(after=after), self.assertRaises(ValueError):
                import_series(self.db, FIXTURE.replace(before, after))
        self.assertFalse(self.db.exists())

    def test_corrupted_persistence_is_quarantined(self):
        packet = import_series(self.db, FIXTURE)
        packet['rows'][0]['value'] = 999
        with closing(sqlite3.connect(self.db)) as db:
            db.execute('UPDATE hrs_revisions SET packet=?', (json.dumps(packet),))
            db.commit()
        with self.assertRaisesRegex(ValueError, 'digest mismatch'):
            read_series(self.db)

    def test_http_readback_is_bounded_and_no_import_is_explicit(self):
        server = create_server(self.db, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f'http://127.0.0.1:{server.server_address[1]}'
        try:
            with urlopen(base + '/api/streamflow') as response:
                self.assertEqual(json.load(response)['status'], 'NOT_IMPORTED')
            import_series(self.db, FIXTURE)
            with urlopen(base + '/api/streamflow?start=2020-01-03&end=2020-01-04') as response:
                self.assertEqual(len(json.load(response)['rows']), 2)
            from urllib.error import HTTPError
            with self.assertRaises(HTTPError) as error:
                urlopen(base + '/api/streamflow?start=1900-01-01&end=2026-01-01')
            self.assertEqual(error.exception.code, 400)
            error.exception.close()
        finally:
            server.shutdown(); server.server_close(); thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main()
