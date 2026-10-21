"""Authored fictional values; real names are context, never observations."""
from .contracts import validate_config


def council_fixture(council_id="snowy-monaro-demo", name="Snowy Monaro Regional Council — rehearsal"):
    prefix = council_id + "-"
    items = [
        ("admin", "ADMINISTRATIVE", "Council scope (not admitted geometry)", 48, 10),
        ("cooma", "SETTLEMENT", "Cooma context — synthetic node", 25, 34),
        ("jindabyne", "SETTLEMENT", "Jindabyne context — synthetic node", 72, 36),
        ("farm", "SITE", "Hypothetical farm — retained case", 17, 72),
        ("water", "CATCHMENT", "Fictional cross-place water system", 49, 55),
        ("gauge", "STATION", "Fictional gauge — not 410033", 52, 81),
        ("service", "SERVICE_AREA", "Fictional service area", 81, 73),
        ("grid", "CLIMATE_GRID", "Fictional regional grid", 85, 12),
        ("asset", "ASSET", "Fictional storage asset", 34, 88),
        ("ecology", "ECOSYSTEM", "Fictional ecological resource", 9, 48),
    ]
    config = {
        "council_id": council_id, "name": name,
        "deployment": "LOCAL_SYNTHETIC_REHEARSAL_NOT_COUNCIL_ENDORSED",
        "boundary": {"geometry": None, "version": "NOT_ADMITTED", "status": "METADATA_ONLY_NOT_ADMITTED",
                     "source_url": "https://portal.spatial.nsw.gov.au/server/rest/services/NSW_Administrative_Boundaries_Theme/MapServer/8",
                     "licence": "EXACT_LAYER_TERMS_PENDING_REVIEW"},
        "objects": [{"id": prefix + key, "kind": kind, "name": label, "x": x, "y": y, "classification": "SYNTHETIC_ONLY"} for key, kind, label, x, y in items],
        "relations": [{"from": prefix + a, "to": prefix + b, "type": kind} for a, b, kind in [
            ("admin", "cooma", "CONTAINS"), ("admin", "jindabyne", "CONTAINS"),
            ("cooma", "water", "DEPENDS_ON"), ("farm", "water", "DEPENDS_ON"),
            ("jindabyne", "water", "DEPENDS_ON"), ("water", "service", "OVERLAPS"),
            ("gauge", "water", "UPSTREAM_OF"), ("grid", "admin", "OVERLAPS")]],
        "external_dependencies": [{"id": "external-upstream-context", "status": "UNVERIFIED_NOT_EVIDENCE", "relation": "UPSTREAM_CONTEXT_REFERENCE_ONLY"}],
        "legacy_references": [
            {"path": "cczps_lite/site_reading/cooma.py", "use": "Historical site-reading contract; not Council-wide current state"},
            {"path": "cczps_lite/qgis_local_spatial_foundation/contract.py", "use": "QGIS navigation contract; Cooma extent is not Council geometry"},
            {"path": "https://github.com/simon947161/eco-agent-system/pull/125", "use": "Unmerged farm research lineage; not imported or overwritten"}],
    }
    return validate_config(config)


def evidence_fixture(config):
    cid = config["council_id"]
    return [{"evidence_id": cid + "-e" + str(i), "revision": 1, "classification": "SYNTHETIC_ONLY",
             "source": "REPOSITORY_AUTHORED_FIXTURE", "method": "FIXED_EXAMPLE_NOT_MEASUREMENT",
             "spatial_id": cid + "-" + scope, "unit": "1", "value": value,
             "observed_at": "2026-10-01T00:00:00Z", "retrieved_at": "2026-10-01T00:00:00Z",
             "valid_until": "2026-11-01T00:00:00Z", "licence": "MIT_REPOSITORY_FIXTURE",
             "share_class": "SYNTHETIC_APPROVED_FOR_REVIEW", "quality": "FICTIONAL",
             "representativeness": "THIS_SYNTHETIC_OBJECT_ONLY", "derived_from": [],
             "status": "ACTIVE", "private_notes": "LOCAL ONLY: never exported"}
            for i, scope, value in [(1, "farm", 2), (2, "service", 3)]]
