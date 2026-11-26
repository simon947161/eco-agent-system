"""Reproduce both ledgers, compare archived outputs and run every P1 test offline."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from independent_meter_check import independent
from ledger import HERE
from paired_inputs import FIXTURE, verify
from replay import write_outputs
from spatial_controls import run as spatial_run


def digest(data):
    return hashlib.sha256(data).hexdigest()


def same(path, expected):
    actual, archive = path.read_bytes(), expected.read_bytes()
    # DEFLATE implementations can encode identical rows differently.
    if path.suffix == ".gz":
        actual, archive = gzip.decompress(actual), gzip.decompress(archive)
    if actual != archive:
        raise ValueError("REPLAY_DIFF: "+expected.name)
    return digest(actual)


def execute(out):
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        raise ValueError("use an empty output directory")
    hourly_hash = verify()
    raw = (HERE/"P1_SYNTHETIC_INPUTS.json").read_bytes()
    # The original compact encoding of the parameter manifest was frozen before any run.
    # The final manifest adds just the explicit presentation of the same hourly profile.
    original = b"".join(line for line in raw.splitlines(keepends=True) if not line.startswith(b'  "profile":'))
    if digest(original) != "7ab3301ab667340863d8e0494e9d027ca168f62380c7f98e6e9616777b4e2f94":
        raise ValueError("PARAMETER_FREEZE_DRIFT")
    if hourly_hash != "20211941069b2748b2e55404d366807c94c0115c6a8aa8ef9bc4fdfce02b8bde":
        raise ValueError("HOURLY_FREEZE_DRIFT")
    write_outputs(out/"results")
    spatial_run(out/"controls")
    checks = {}
    for name in ("results/P1_ENERGY_EXERGY_CARBON_LEDGER.json","results/P1_HOURLY_central.csv.gz",
                 "controls/P1_PAIRED_SPATIAL_CONTROLS.json"):
        checks[name] = same(out/name,HERE/name)
    passport = json.loads((HERE/"results/P1_RUN_PASSPORT.json").read_text("utf-8"))
    for name, hash_value in passport["inputs_and_code_sha256"].items():
        if digest((HERE/name).read_bytes()) != hash_value:
            raise ValueError("BASE_PASSPORT_INPUT: "+name)
    for name, hash_value in passport["outputs_sha256"].items():
        if digest((HERE/"results"/name).read_bytes()) != hash_value:
            raise ValueError("BASE_PASSPORT_OUTPUT: "+name)
    result=unittest.TextTestRunner(verbosity=1).run(
        unittest.defaultTestLoader.discover(str(HERE),pattern="test_*.py"))
    if not result.wasSuccessful() or result.skipped:
        raise ValueError("TESTS_FAILED_OR_SKIPPED")
    return {"tag":"SYNTHETIC","fixture_uncompressed_sha256":hourly_hash,
            "replayed_content_sha256":checks, "primary_arm_hours":passport["validated_arm_hours"],
            "supplement_arm_hours":12*4*8760, "unit_tests_passed":result.testsRun,
            "independent_csv_audit":independent(HERE), "independent_science_review":"PENDING",
            "receptor_response":"UNKNOWN","global_cooling":"NOT_TESTABLE"}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,help="empty directory to keep regenerated ledgers and receipt")
    args=p.parse_args()
    if args.out:
        details=execute(args.out)
        (args.out/"replay-receipt.json").write_bytes((json.dumps(details,indent=2)+"\n").encode())
    else:
        with tempfile.TemporaryDirectory(prefix="heat-p1-replay-") as tmp:
            details=execute(Path(tmp))
    print(json.dumps(details,indent=2))
