"""Freeze/verify exogenous hours. This command does not dispatch a network."""
import argparse
import csv
import gzip
import hashlib
import io
from pathlib import Path

from ledger import HERE, START, conditions, load_inputs
from datetime import timedelta

FIXTURE = HERE / "controls" / "paired_hours.csv.gz"
COLUMNS = ("origin", "hour", "utc", "gross_kw", "air_C", "space_kw", "dhw_kw",
           "mismatch_space_kw", "mismatch_dhw_kw", "diverse_space_kw", "diverse_dhw_kw",
           "july_source_available", "july_maintenance_source_available")


def encoded():
    cases = load_inputs()
    raw = io.StringIO(newline="")
    out = csv.writer(raw, lineterminator="\n")
    out.writerow(COLUMNS)
    for h in range(8760):
        stamp = START + timedelta(hours=h)
        space, dhw, air = conditions(h, cases["central"][0])
        mismatch = conditions(h, cases["seasonal_mismatch"][0])
        diverse = conditions(h, cases["diverse_demand"][0])
        # Whole-month and contiguous seven-day source-access failures. A still produces.
        out.writerow(["SYNTHETIC", h, stamp.isoformat(), cases["central"][0]["source_kw"],
                      air, space, dhw, *mismatch[:2], *diverse[:2], int(stamp.month != 7),
                      int(not (stamp.month == 7 and stamp.day <= 7))])
    return raw.getvalue().encode("utf-8")


def verify():
    actual = gzip.decompress(FIXTURE.read_bytes())
    if actual != encoded():
        raise ValueError("FROZEN_HOURLY_INPUT_DRIFT")
    return hashlib.sha256(actual).hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true", help="create an absent fixture once")
    args = parser.parse_args()
    if args.freeze:
        FIXTURE.parent.mkdir(exist_ok=True)
        with FIXTURE.open("xb") as raw:
            with gzip.GzipFile(filename="", mode="wb", mtime=0, fileobj=raw) as stream:
                stream.write(encoded())
    print(verify())
