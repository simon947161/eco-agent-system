"""Replay a bounded independently pixel-reviewed map snapshot against source nodes.

This does not certify GIS accuracy, current legal applicability, browser rendering,
or the non-map narrative. The frozen review snapshot must change only after a
new explicit original-image review, not to make this checker pass.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def verify(bundle, reviewed):
    maps = {m["id"]: m for m in reviewed["maps"]}
    nodes = [n for n in bundle["records"] if n.get("category") == "LSPS_MAP"]
    assert len(maps) == len(nodes) == 27, "MAP_OCCURRENCE_MISSING_OR_ADDED"
    assert len({n["id"] for n in nodes}) == 27, "DUPLICATE_MAP_NODE"
    seen = set()
    checks = []
    for node in nodes:
        facts = node["facts"]
        item = facts["map"]
        assert item["id"] in maps and item["id"] not in seen, "MAP_ID_UNREVIEWED_OR_DUPLICATE"
        assert item == maps[item["id"]], "PIXEL_REVIEWED_MAP_CONTENT_CHANGED"
        assert node["summary"] == item["summary"], "DISPLAY_SUMMARY_DIFFERS_FROM_REVIEWED_MAP"
        assert node["anchor"]["pdfPage"] == item["pdfPage"], "NODE_PAGE_DIFFERS"
        assert facts["sourceRevision"] == reviewed["sourceRevision"], "NODE_SOURCE_REVISION_DIFFERS"
        assert all(facts[k] == "UNKNOWN" for k in ["currentLaw", "currentLegalApplicability", "actualExecution"]), "UNSUPPORTED_CURRENT_OR_ACTUAL_ADMISSION"
        assert all(facts[k] == "PENDING" for k in ["officialAdmission", "humanReview"]), "UNSUPPORTED_REVIEW_ADMISSION"
        assert item["geometryExtracted"] is False, "UNSUPPORTED_GEOMETRY_CLAIM"
        assert item["spatialApplicability"] == "UNKNOWN", "UNSUPPORTED_SPATIAL_ADMISSION"
        assert item["coordinateReferenceSystem"] == "NOT_STATED", "UNSUPPORTED_CRS"
        seen.add(item["id"])
        checks.append({"nodeId": node["id"], "mapId": item["id"], "pdfPage": item["pdfPage"],
                       "reviewedMapCanonicalSha256": digest(item), "status": "PASS_REVIEWED_MAP_CONTENT_AND_BOUNDARIES"})
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    own = Path(__file__).resolve().parent
    app = own.parents[2]
    bundle_path = args.bundle or app / "sources/lsps-context-review.json"
    snapshot = own / "reviewed-map-author-snapshot.json"
    bundle = json.loads(bundle_path.read_text())
    reviewed = json.loads(snapshot.read_text())
    checked = verify(bundle, reviewed)
    negatives = []
    for name in ["missing-map", "changed-option-preserving-source-hashes", "invented-crs-preserving-source-hashes"]:
        bad = copy.deepcopy(bundle)
        maps = [n for n in bad["records"] if n.get("category") == "LSPS_MAP"]
        if name == "missing-map":
            bad["records"].remove(maps[-1])
        elif name == "changed-option-preserving-source-hashes":
            node = next(n for n in maps if n["facts"]["map"]["pdfPage"] == 114)
            entry = next(e for e in node["facts"]["map"]["legend"] if e["label"].endswith("Option 5"))
            entry["label"] = entry["label"].replace("Option 5", "Option 4")
        else:
            maps[0]["facts"]["map"]["coordinateReferenceSystem"] = "EPSG:4326"
        try:
            verify(bad, reviewed)
        except AssertionError as e:
            negatives.append({"case": name, "status": "REJECTED", "reason": str(e)})
        else:
            raise AssertionError("NEGATIVE_CASE_NOT_REJECTED:" + name)
    result = {"schema": "lsps-independent-map-node-readback-1",
              "sourceRevision": reviewed["sourceRevision"],
              "reviewedAuthorSnapshotSha256": hashlib.sha256(snapshot.read_bytes()).hexdigest(),
              "bundlePath": str(bundle_path.relative_to(app)) if bundle_path.is_relative_to(app) else str(bundle_path),
              "bundleSha256AtReadback": hashlib.sha256(bundle_path.read_bytes()).hexdigest(),
              "reviewedMapRecordsCanonicalSha256": digest([n for n in bundle["records"] if n.get("category") == "LSPS_MAP"]),
              "scope": "27 generated source-bundle LSPS_MAP nodes exactly retain the independently pixel-reviewed maps and unknown/pending admission boundaries. No browser or deployment claim.",
              "counts": {"mapNodesChecked": len(checked), "negativeCasesRejected": len(negatives)},
              "checks": checked, "negativeCases": negatives,
              "limitations": ["No parcel/GIS geometry verification", "No current-law or actual-delivery verification", "Non-map narrative excluded from this node readback", "Browser and publication acceptance belong to root task"]}
    destination = args.output or own / "map-node-readback.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "PASS_BOUNDED_MAP_NODE_READBACK", "counts": result["counts"], "mapRecordsDigest": result["reviewedMapRecordsCanonicalSha256"]}))


if __name__ == "__main__":
    main()
