"""Independently verify LSPS context positions against the pinned original PDF.

No builder is imported. Text, geometry, and RGB evidence are recomputed from
original bytes. These checks do not establish legal admission or full semantic
correctness; separately reviewed semantic assertions have their own evidence.
Original text/images stay in memory and are never written to repository output.
"""
from __future__ import annotations

import argparse
import collections
import copy
import csv
import datetime
import hashlib
import io
import json
import math
import re
import tempfile
import unicodedata
from pathlib import Path

import fitz
import pypdf

APP = Path(__file__).resolve().parents[1]
SOURCE_ID = "csoi:smrc-lsps-2020:20261030"
SOURCE_SHA = "sha256:9bf75ec6fb98f1d03bad47f5b9cda44e6ffadce3bf452eb5a343b394322f8f47"
PAGE_COUNT = 118
PARSER = "pymupdf-1.26.6-nfkc-unicode-whitespace-v1"
RENDERER = "pymupdf-1.26.6-rgb-100dpi-fresh-document-clip-v2"


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def norm(value):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip()


def digest(raw):
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def text_digest(value):
    return digest(norm(value).encode("utf-8"))


def canonical_digest(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode("utf-8"))


def equivalent_json(left, right):
    """Compare transfer values, allowing JSON's 735.0 -> 735 number spelling.

    JavaScript serializes integral numbers without '.0'. That does not alter a
    coordinate. Booleans, keys, list ordering and all actual values stay strict.
    Original evidence hashes and their exact coordinate values are still checked.
    """
    if isinstance(left, (int, float)) and not isinstance(left, bool):
        return (isinstance(right, (int, float)) and not isinstance(right, bool)
                and math.isfinite(left) and math.isfinite(right) and left == right)
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(equivalent_json(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(equivalent_json(x, y) for x, y in zip(left, right))
    return left == right


class Original:
    """Read-only original source with bounded, independently recomputed caches."""

    def __init__(self, path):
        self.path = Path(path)
        raw = self.path.read_bytes()
        require(digest(raw) == SOURCE_SHA, "ORIGINAL_SOURCE_BYTES_MISMATCH")
        require(fitz.VersionBind == "1.26.6", "PYMUPDF_VERSION_REQUIRES_REVIEW")
        self.byte_count = len(raw)
        self.original_bytes = raw
        self.doc = fitz.open(stream=raw, filetype="pdf")
        require(len(self.doc) == PAGE_COUNT, "ORIGINAL_PAGE_COUNT_MISMATCH")
        self.text_cache = {}
        self.raster_cache = {}
        self.words_cache = {}
        self.blocks_cache = {}
        self.layout_digest_cache = None

    def layout_digests(self):
        if self.layout_digest_cache is None:
            require(pypdf.__version__ == "6.10.0", "RUNTIME_PAGE_PARSER_VERSION_REQUIRES_REVIEW")
            reader = pypdf.PdfReader(io.BytesIO(self.original_bytes))
            self.layout_digest_cache = {
                pn: digest(" ".join((page.extract_text(extraction_mode="layout") or "").split()).encode())
                for pn, page in enumerate(reader.pages, 1)}
        return self.layout_digest_cache

    def words(self, page_number):
        if page_number not in self.words_cache:
            self.words_cache[page_number] = self.doc[page_number - 1].get_text("words")
        return self.words_cache[page_number]

    def blocks(self, page_number):
        if page_number not in self.blocks_cache:
            self.blocks_cache[page_number] = self.doc[page_number - 1].get_text("dict")["blocks"]
        return self.blocks_cache[page_number]

    def rect(self, page_number, bbox):
        require(isinstance(page_number, int) and not isinstance(page_number, bool)
                and 1 <= page_number <= PAGE_COUNT, "ANCHOR_PAGE_OUT_OF_BOUNDS")
        require(isinstance(bbox, list) and len(bbox) == 4 and all(
            isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
            for v in bbox), "ANCHOR_BBOX_INVALID")
        r = fitz.Rect(bbox)
        page = self.doc[page_number - 1]
        require(0 <= r.x0 < r.x1 <= page.rect.width + 0.0001 and
                0 <= r.y0 < r.y1 <= page.rect.height + 0.0001,
                "ANCHOR_BBOX_OUT_OF_BOUNDS")
        return r

    def text(self, page_number, bbox):
        r = self.rect(page_number, bbox)
        key = (page_number, tuple(bbox))
        if key not in self.text_cache:
            self.text_cache[key] = norm(self.doc[page_number - 1].get_text("text", clip=r))
        return self.text_cache[key]

    def raster(self, page_number, bbox):
        r = self.rect(page_number, bbox)
        key = (page_number, tuple(bbox))
        if key not in self.raster_cache:
            # MuPDF's reused document font state changed one caption's pixels
            # after other pages had been processed. A fresh document for EACH
            # crop makes the contract independent of extraction/render order.
            # It is opened from the already byte-verified immutable original.
            with fitz.open(stream=self.original_bytes, filetype="pdf") as render_doc:
                pix = render_doc[page_number - 1].get_pixmap(
                    matrix=fitz.Matrix(100 / 72, 100 / 72), clip=r,
                    colorspace=fitz.csRGB, alpha=False)
            self.raster_cache[key] = {
                "width": pix.width, "height": pix.height,
                "cropHash": digest(f"RGB|{pix.width}x{pix.height}|".encode() + pix.samples),
                "renderer": RENDERER,
            }
        return self.raster_cache[key]

    def census(self):
        pages = []
        block_rows = []
        image_rows = []
        for pn, page in enumerate(self.doc, 1):
            words = self.words(pn)
            blocks = self.blocks(pn)
            nonempty = 0
            empty = 0
            image_count = 0
            for i, block in enumerate(blocks):
                box = [round(v, 5) for v in block["bbox"]]
                if block["type"] == 0:
                    native_text = norm(" ".join(
                        span["text"] for line in block.get("lines", [])
                        for span in line["spans"]))
                    if not native_text:
                        empty += 1
                        continue
                    nonempty += 1
                    block_rows.append({
                        "blockId": f"pdf{pn:03d}-native-block{i:03d}",
                        "pdfPage": pn, "bbox": box,
                        "normalizedTextHash": text_digest(native_text),
                        "normalizedCharacterCount": len(native_text),
                        "semanticDisposition": "PENDING_DECLARED_INVENTORY_COMPARISON",
                    })
                elif block["type"] == 1:
                    image_count += 1
                    image_rows.append({
                        "imageBlockId": f"pdf{pn:03d}-native-image{i:03d}",
                        "pdfPage": pn, "bbox": box,
                        "embeddedBytesHash": digest(block["image"]),
                        "pixelWidth": block["width"], "pixelHeight": block["height"],
                        "meaning": "UNKNOWN_PENDING_VISUAL_REVIEW",
                    })
            pages.append({
                "pdfPage": pn, "pageWidthPt": page.rect.width,
                "pageHeightPt": page.rect.height,
                "normalizedPageTextHash": text_digest(page.get_text("text")),
                "nonemptyNativeTextBlocks": nonempty,
                "emptyNativeTextBlocks": empty,
                "nativeWordCount": len(words), "nativeImageBlockCount": image_count,
                "imageFreeDoesNotMeanVisualFree": True,
            })
        return {
            "format": "csoi-lsps-independent-source-census-1",
            "sourceId": SOURCE_ID, "sourceRevision": SOURCE_SHA,
            "sourceBytes": self.byte_count, "sourcePages": PAGE_COUNT,
            "parser": PARSER, "originalBytesCommitted": False,
            "counts": {
                "pages": len(pages), "nonemptyNativeTextBlocks": len(block_rows),
                "nativeWords": sum(p["nativeWordCount"] for p in pages),
                "nativeImageBlocks": len(image_rows),
            },
            "denominatorMeaning": "Native extraction positions, not a count of semantic paragraphs or obligations.",
            "semanticCompleteness": "NOT_ESTABLISHED_BY_GEOMETRY_OR_HASHES",
            "pages": pages, "nativeTextBlocks": block_rows, "nativeImageBlocks": image_rows,
        }


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def write_csv(path, rows):
    require(bool(rows), "EMPTY_CSV_EVIDENCE")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def verify_original_anchor(source, anchor, label, *, require_text=True, require_raster=False):
    """Validate declared geometry and independently regenerate each evidence hash."""
    pn = anchor["pdfPage"]
    box = anchor["bbox"]
    original_text = source.text(pn, box)
    if require_text or "sourceTextHash" in anchor:
        require(anchor.get("sourceTextHash") == text_digest(original_text),
                f"ORIGINAL_CLIP_TEXT_MISMATCH:{label}")
    if require_raster or "cropHash" in anchor or "rasterDigest" in anchor:
        raster = source.raster(pn, box)
        require(anchor.get("renderer") == RENDERER,
                f"RASTER_RENDERER_MISMATCH:{label}")
        require(anchor.get("cropHash", anchor.get("rasterDigest")) == raster["cropHash"],
                f"ORIGINAL_CLIP_RASTER_MISMATCH:{label}")
        if "width" in anchor:
            require(anchor["width"] == raster["width"], f"RASTER_WIDTH_MISMATCH:{label}")
        if "height" in anchor:
            require(anchor["height"] == raster["height"], f"RASTER_HEIGHT_MISMATCH:{label}")
    return original_text


def unit_id(unit):
    return unit.get("unitId", unit.get("id"))


def verify_runtime_bundle(bundle, narrative_units, maps, core):
    """Ensure page aggregation loses no reviewed units or qualifiers."""
    require(bundle["sourceId"] == SOURCE_ID and bundle["sourceRevision"] == SOURCE_SHA,
            "CONTEXT_BUNDLE_SOURCE_VERSION_MISMATCH")
    require(bundle["sourcePageCount"] == PAGE_COUNT, "CONTEXT_BUNDLE_PAGE_COUNT")
    require(bundle["format"] == "csoi-lsps-context-review-1", "CONTEXT_BUNDLE_FORMAT")
    core_ids = {r["id"] for r in core["records"]}
    map_priorities = {**dict.fromkeys([26, 27, 28, 108], 3),
                      **dict.fromkeys([48, 109], 10),
                      **dict.fromkeys([57, 60, 61, 65, 66, 69, 72, 75, 88,
                                       106, 107, 110, 111, 112, 113, 114, 115, 116], 12)}
    seen_units = {}
    seen_maps = {}
    records = bundle["records"]
    require(len({r["id"] for r in records}) == len(records), "DUPLICATE_CONTEXT_RECORD_ID")
    for record in records:
        require(record.get("parentId") == "csoi:knowledge:lsps2020:document",
                "CONTEXT_PARENT_DOCUMENT_CHANGED")
        facts = record["facts"]
        for key, expected in [("sourceRevision", SOURCE_SHA), ("currentLaw", "UNKNOWN"),
                              ("currentLegalApplicability", "UNKNOWN"), ("actualExecution", "UNKNOWN"),
                              ("officialAdmission", "PENDING"), ("humanReview", "PENDING")]:
            require(facts.get(key) == expected, "CONTEXT_RECORD_AUTHORITY_BOUNDARY:" + key)
        relations = record.get("relations", [])
        require(all(rel.get("type") == "SOURCE_READING_CONTEXT" and rel.get("targetId") in core_ids
                    for rel in relations), "CONTEXT_RELATION_TARGET_OR_SEMANTICS_INVALID")
        if record["category"] == "LSPS_NARRATIVE":
            require(bool(facts.get("units")), "EMPTY_NARRATIVE_RECORD")
            for unit in facts["units"]:
                uid = unit_id(unit)
                require(uid and uid not in seen_units, "DUPLICATE_OR_MISSING_RUNTIME_UNIT_ID")
                seen_units[uid] = unit
        elif record["category"] == "LSPS_MAP":
            entry = facts["map"]
            mid = entry["id"]
            require(mid not in seen_maps, "DUPLICATE_RUNTIME_MAP_ID")
            seen_maps[mid] = entry
            expected_priority = map_priorities.get(entry["pdfPage"])
            priority_targets = {rel["targetId"] for rel in relations if ":priority:" in rel["targetId"]}
            expected_targets = ({"csoi:knowledge:lsps2020:priority:" + str(expected_priority)}
                                if expected_priority else set())
            require(priority_targets == expected_targets, "MAP_READING_PRIORITY_WRONG_SOURCE_SECTION:" + mid)
        else:
            raise ValueError("UNEXPECTED_CONTEXT_CATEGORY:" + record["category"])
    expected_units = {unit_id(u): u for u in narrative_units}
    expected_maps = {m["id"]: m for m in maps}
    require(set(seen_units) == set(expected_units), "RUNTIME_NARRATIVE_UNIT_CENSUS_MISMATCH")
    require(set(seen_maps) == set(expected_maps), "RUNTIME_MAP_CENSUS_MISMATCH")
    for uid, unit in expected_units.items():
        require(equivalent_json(seen_units[uid], unit),
                "RUNTIME_AUTHORED_UNIT_LOSS_OR_ALTERATION:" + uid)
    for mid, entry in expected_maps.items():
        require(equivalent_json(seen_maps[mid], entry),
                "RUNTIME_MAP_LOSS_OR_ALTERATION:" + mid)
    return {"status": "PASS_EXACT_REVIEWED_UNIT_AND_MAP_TRANSFER",
            "records": len(records), "narrativeUnits": len(seen_units), "maps": len(seen_maps),
            "aggregationDoesNotChangeSemanticDenominator": True}


def verify_runtime_source_metadata(source, bundle, narrative, maps, core):
    """Verify page-level metadata and reading links against actual source positions."""
    digests = source.layout_digests()
    parser = "pypdf-6.10.0-layout-whitespace-1"
    starts = [23, 25, 26, 29, 33, 35, 38, 41, 43, 47, 51, 53]
    for priority, pn in enumerate(starts, 1):
        text = norm(source.doc[pn - 1].get_text("text"))
        require(re.search(r"Planning Priority\s+" + str(priority) + r"\b", text, re.I),
                "ORIGINAL_PRIORITY_SECTION_START_MISSING:" + str(priority))
    core_ids = {r["id"] for r in core["records"]}
    ids = core_ids | {r["id"] for r in bundle["records"]}
    relation_rows = []
    for record in bundle["records"]:
        anchor = record["anchor"]
        pn = anchor["pdfPage"]
        require(anchor["parserVersion"] == parser and anchor["normalizedPageDigest"] == digests.get(pn),
                "RUNTIME_RECORD_ORIGINAL_PAGE_ANCHOR_MISMATCH:" + record["id"])
        relations = record.get("relations", [])
        targets = [r["targetId"] for r in relations]
        require(len(targets) == len(set(targets)), "DUPLICATE_SOURCE_READING_CONTEXT")
        if record["category"] == "LSPS_NARRATIVE":
            require(all(u["pdfPage"] == pn for u in record["facts"]["units"]),
                    "RUNTIME_PAGE_AGGREGATION_MISLOCATED:" + record["id"])
            action_targets = {aid for item in narrative["inventory"] if item["pdfPage"] == pn
                              for aid in item.get("existingActionIds", [])}
            priority = max((i for i, start in enumerate(starts, 1) if start <= pn), default=0) if pn <= 89 else 0
            expected = action_targets | ({"csoi:knowledge:lsps2020:priority:" + str(priority)} if priority else set())
            require(set(targets) == expected, "NARRATIVE_READING_CONTEXT_NOT_MATCHING_SOURCE_PAGE:" + record["id"])
        else:
            require(record["facts"]["map"]["pdfPage"] == pn, "RUNTIME_MAP_RECORD_PAGE_MISMATCH:" + record["id"])
        for relation in relations:
            relation_rows.append({"fromId": record["id"], "pdfPage": pn,
                                  "type": relation["type"], "targetId": relation["targetId"],
                                  "status": "PASS_SOURCE_READING_CONTEXT_ONLY",
                                  "officialRelationship": "NOT_ADMITTED"})
    pages = bundle["pages"]
    require(len(pages) == PAGE_COUNT and {p["pdfPage"] for p in pages} == set(range(1, 119)),
            "RUNTIME_PAGE_CENSUS_MISSING_OR_DUPLICATE")
    for page in pages:
        pn = page["pdfPage"]
        require(page["pageDigest"] == digests[pn], "RUNTIME_PAGE_INDEX_ORIGINAL_HASH_MISMATCH:" + str(pn))
        expected_units = {unit_id(u) for u in narrative["units"] if any(a["pdfPage"] == pn for a in u["evidenceAnchors"])}
        require(set(page["unitIds"]) == expected_units, "RUNTIME_PAGE_UNIT_INDEX_MISSING_OR_EXTRA:" + str(pn))
        require(set(page["mapIds"]) == {m["id"] for m in maps["maps"] if m["pdfPage"] == pn},
                "RUNTIME_PAGE_MAP_INDEX_MISSING_OR_EXTRA:" + str(pn))
        require(set(page["recordIds"]) <= ids, "RUNTIME_PAGE_INDEX_UNKNOWN_RECORD:" + str(pn))
    expected_counts = {"pages": PAGE_COUNT, "narrativePageRecords": sum(r["category"] == "LSPS_NARRATIVE" for r in bundle["records"]),
                       "semanticUnits": len(narrative["units"]), "mapOccurrences": len(maps["maps"]),
                       "implementationActionsRetained": 83, "conflictingObservationsRetained": 18}
    require(all(bundle["counts"].get(k) == v for k, v in expected_counts.items()), "RUNTIME_DECLARED_COUNT_MISMATCH")
    return {"status": "PASS_ORIGINAL_PAGE_ANCHORS_AND_READING_CONTEXT_LINKS", "pages": PAGE_COUNT,
            "relations": len(relation_rows), "relationRows": relation_rows,
            "basis": "Same-page original action inventory plus explicitly located priority chapters; reading links are not admitted official relationships."}


def verify_retained_actions(bundle, baseline):
    require(bundle["sourceId"] == SOURCE_ID and bundle["sourceRevision"] == SOURCE_SHA,
            "CORE_SOURCE_BINDING_MISMATCH")
    for key, expected in [("sourcePageCount", PAGE_COUNT), ("rights", "UNKNOWN"),
                          ("currentVersion", "UNKNOWN"), ("officialAdmission", "PENDING"),
                          ("originalBytesCommitted", False)]:
        require(bundle.get(key) == expected, "CORE_SOURCE_AUTHORITY_BOUNDARY:" + key)
    if "allRecordHashes" in baseline:
        require({r["id"]: canonical_digest(r) for r in bundle["records"]} == baseline["allRecordHashes"],
                "EXISTING_CORE_RECORD_REMOVED_OR_CHANGED")
    actions = [r for r in bundle["records"] if r["category"] == "ACTION"]
    require(len(actions) == 101, "EXISTING_ACTION_COUNT_CHANGED")
    ids = {r["id"] for r in actions}
    require(ids == set(baseline["recordHashes"]), "EXISTING_ACTION_REMOVED_OR_REPLACED")
    for record in actions:
        require(canonical_digest(record) == baseline["recordHashes"][record["id"]],
                "EXISTING_ACTION_RECORD_CHANGED:" + record["id"])
    kinds = collections.Counter(r["facts"]["sourceSection"] for r in actions)
    require(kinds == {"IMPLEMENTATION_TABLE": 83, "CORE_NARRATIVE_CONFLICT": 5,
                      "LOCAL_ACTION_CONFLICT": 13}, "EXISTING_ACTION_SECTION_COUNTS_CHANGED")
    return {"status": "PASS_UNCHANGED_EXISTING_ACTION_RECORDS", "implementationActions": 83,
            "coreNarrativeConflicts": 5, "localActionConflicts": 13,
            "sourceSemanticValidation": "SEPARATE_EXISTING_ORIGINAL_SOURCE_VERIFIER"}


def word_coverage(source, anchors_by_page):
    """Census every original word centre; independent of authored unit counts.

    This checks that no extractable source position silently disappears. It does
    not turn extraction fragments into semantic units or prove a summary's truth.
    """
    result = []
    for pn, page in enumerate(source.doc, 1):
        rectangles = [(aid, fitz.Rect(box)) for aid, box in anchors_by_page.get(pn, [])]
        words = source.words(pn)
        missing = []
        for index, word in enumerate(words):
            point = fitz.Point((word[0] + word[2]) / 2, (word[1] + word[3]) / 2)
            if not any(rect.contains(point) for _, rect in rectangles):
                missing.append({"wordIndex": index,
                                "bbox": [round(v, 5) for v in word[:4]],
                                "textHash": text_digest(word[4])})
        result.append({"pdfPage": pn, "originalWords": len(words),
                       "coveredWords": len(words) - len(missing),
                       "uncoveredWords": len(missing), "uncoveredPositions": missing,
                       "status": "PASS_POSITIONS_COVERED" if not missing else "GAP"})
    return result


def verify_narrative(source, review, core, *, allow_draft=False):
    document = review["document"]
    require(document["sourceId"] == SOURCE_ID and document["sourceRevision"] == SOURCE_SHA,
            "NARRATIVE_SOURCE_VERSION_MISMATCH")
    require(document["totalPages"] == PAGE_COUNT, "NARRATIVE_TOTAL_PAGES_MISMATCH")
    require(document["renderer"] == RENDERER, "NARRATIVE_RENDERER_MISMATCH")
    for key, expected in [("currentLaw", "UNKNOWN"), ("actualExecution", "UNKNOWN"),
                          ("officialAdmission", "PENDING")]:
        require(document.get(key) == expected, "NARRATIVE_AUTHORITY_BOUNDARY:" + key)
    pages = review["pages"]
    require(len(pages) == PAGE_COUNT and {p["pdfPage"] for p in pages} == set(range(1, 119)),
            "NARRATIVE_PAGE_INVENTORY_MISSING_OR_DUPLICATE")
    inventory = review["inventory"]
    units = review["units"]
    inventory_by_id = {i["inventoryId"]: i for i in inventory}
    units_by_id = {unit_id(u): u for u in units}
    image_by_id = {i["id"]: i for i in review["images"]}
    require(len(inventory_by_id) == len(inventory), "DUPLICATE_INVENTORY_ID")
    require(len(units_by_id) == len(units), "DUPLICATE_SEMANTIC_UNIT_ID")
    core_by_id = {r["id"]: r for r in core["records"]}
    positions = collections.defaultdict(list)
    inventory_rows = []
    action_link_gaps = []
    for item in inventory:
        iid = item["inventoryId"]
        anchors = item["evidenceAnchors"]
        require(bool(anchors), "INVENTORY_WITHOUT_SOURCE_ANCHOR:" + iid)
        require(all(a.get("renderer") == RENDERER for a in anchors),
                "NARRATIVE_ANCHOR_REQUIRES_FRESH_DOCUMENT_RENDERER:" + iid)
        extracted = [verify_original_anchor(source, a, iid, require_raster=True) for a in anchors]
        require(item["sourceTextHash"] == text_digest(" ".join(extracted)),
                "INVENTORY_AGGREGATE_TEXT_MISMATCH:" + iid)
        require(item["cropHash"] == anchors[0]["cropHash"], "INVENTORY_PRIMARY_RASTER_MISMATCH:" + iid)
        require(item["pdfPage"] == anchors[0]["pdfPage"] and item["bbox"] == anchors[0]["bbox"],
                "INVENTORY_PRIMARY_POSITION_MISMATCH:" + iid)
        disposition = item["disposition"]
        require(bool(item.get("reason")), "INVENTORY_CLASSIFICATION_WITHOUT_REASON:" + iid)
        if not allow_draft:
            require("PENDING" not in disposition, "UNRESOLVED_INVENTORY_CLASSIFICATION:" + iid)
        for anchor in anchors:
            positions[anchor["pdfPage"]].append((iid, anchor["bbox"]))
        uid = item.get("reviewUnitId")
        if uid:
            require(uid in units_by_id and iid in units_by_id[uid]["inventoryIds"],
                    "INVENTORY_SEMANTIC_UNIT_LINK_MISMATCH:" + iid)
        if disposition == "AUTHORED_SUBSTANTIVE":
            require(bool(uid), "SUBSTANTIVE_INVENTORY_WITHOUT_REVIEW_UNIT:" + iid)
        linked = item.get("existingActionIds", [])
        require(all(aid in core_by_id and core_by_id[aid]["category"] == "ACTION" for aid in linked),
                "UNKNOWN_EXISTING_ACTION_LINK:" + iid)
        if disposition == "EXISTING_NUMBERED_ACTION":
            require(bool(linked), "EXISTING_ACTION_DISPOSITION_WITHOUT_ACTION:" + iid)
            old_anchors = [e["anchor"] for aid in linked
                           for e in core_by_id[aid]["facts"]["evidenceAnchors"]]
            for a in anchors:
                r = fitz.Rect(a["bbox"])
                matches = [fitz.Rect(old["bbox"]) for old in old_anchors
                           if old["pdfPage"] == a["pdfPage"]]
                require(any((r & m).get_area() > 0 for m in matches),
                        "EXISTING_ACTION_LINK_MISLOCATED:" + iid)
                words = [w for w in source.words(a["pdfPage"])
                         if r.contains(fitz.Point((w[0]+w[2])/2, (w[1]+w[3])/2))]
                uncovered = [w for w in words if not any(
                    m.contains(fitz.Point((w[0]+w[2])/2, (w[1]+w[3])/2)) for m in matches)]
                # The retained narrative anchors begin at action codes, excluding
                # 134 printed bullet glyphs and nine nested-list 'o' marks in this
                # exact original. These marks have no independent action meaning.
                substantive = [w for w in uncovered if w[4] != "\uf0b7" and not (
                    iid == "p050-b15-u01" and w[4] == "o")]
                require(not substantive, "SUBSTANTIVE_TEXT_MISCLASSIFIED_AS_EXISTING_ACTION:" + iid)
                if uncovered:
                    action_link_gaps.append({"inventoryId": iid, "pdfPage": a["pdfPage"],
                                             "originalWords": len(words),
                                             "wordsOutsideLinkedOldAnchors": len(uncovered),
                                             "nonSubstantiveListMarkers": len(uncovered)-len(substantive),
                                             "substantiveWordsOutsideLinkedOldAnchors": len(substantive)})
        inventory_rows.append({"inventoryId": iid, "pdfPage": item["pdfPage"],
                               "disposition": disposition, "reviewUnitId": uid,
                               "existingActionIds": ";".join(linked),
                               "sourceTextHash": item["sourceTextHash"],
                               "status": "PASS_ORIGINAL_TEXT_AND_RASTER_POSITION"})
    consumed = collections.Counter()
    unit_rows = []
    for unit in units:
        uid = unit_id(unit)
        require(bool(unit.get("summary")) and bool(unit.get("unitKind")),
                "SEMANTIC_UNIT_WITHOUT_AUTHORED_DESCRIPTION:" + uid)
        anchors = unit["evidenceAnchors"]
        require(bool(anchors), "SEMANTIC_UNIT_WITHOUT_EVIDENCE:" + uid)
        extracted = [verify_original_anchor(source, a, uid, require_raster=True) for a in anchors]
        require(unit["sourceTextHash"] == text_digest(" ".join(extracted)),
                "MERGED_UNIT_ORIGINAL_TEXT_MISMATCH:" + uid)
        require(unit["cropHash"] == anchors[0]["cropHash"], "UNIT_PRIMARY_RASTER_MISMATCH:" + uid)
        expected_anchors = []
        for iid in unit["inventoryIds"]:
            require(iid in inventory_by_id and inventory_by_id[iid].get("reviewUnitId") == uid,
                    "SEMANTIC_UNIT_INVENTORY_LINK_MISMATCH:" + uid)
            consumed[iid] += 1
            expected_anchors.extend(inventory_by_id[iid]["evidenceAnchors"])
        if unit["unitKind"] == "NON_SPATIAL_VISUAL":
            # A qualitative vision icon can have an empty numeric-observation
            # dictionary; its authored summary still carries the reviewed meaning.
            require(isinstance(unit.get("visualObservations"), dict),
                    "VISUAL_UNIT_WITHOUT_EXPLICIT_OBSERVATION_FIELD:" + uid)
            for image_id in unit.get("imageInventoryIds", []):
                require(image_id in image_by_id and image_by_id[image_id].get("reviewUnitId") == uid,
                        "VISUAL_UNIT_IMAGE_INVENTORY_LINK_MISMATCH:" + uid)
                image_item = image_by_id[image_id]
                image_box = fitz.Rect(image_item["bbox"])
                require(any(a["pdfPage"] == image_item["pdfPage"] and
                            (fitz.Rect(a["bbox"]) & image_box).get_area() / image_box.get_area() > 0.99
                            for a in anchors), "VISUAL_UNIT_IMAGE_MISLOCATION:" + uid)
        else:
            require(anchors == expected_anchors, "SEMANTIC_UNIT_MERGE_ORDER_OR_ANCHORS_CHANGED:" + uid)
        for field in ["conditions", "qualifiers"]:
            require(isinstance(unit.get(field), list), "MISSING_EXPLICIT_CONDITION_QUALIFIER_FIELD:" + uid)
            for condition in unit[field]:
                require(bool(condition.get("text")), "EMPTY_AUTHORED_CONDITION:" + uid)
                evidence = condition.get("sourceEvidence")
                require(bool(evidence) and all(a in anchors for a in evidence),
                        "CONDITION_EVIDENCE_OUTSIDE_OWNING_UNIT:" + uid)
        unit_rows.append({"unitId": uid, "pdfPage": unit["pdfPage"], "unitKind": unit["unitKind"],
                          "inventoryFragments": len(unit["inventoryIds"]),
                          "sourceAnchors": len(anchors), "conditions": len(unit["conditions"]),
                          "qualifiers": len(unit["qualifiers"]),
                          "status": "PASS_ORIGINAL_POSITION_AND_EXPLICIT_EVIDENCE_LINKS",
                          "semanticAdmission": "NOT_ESTABLISHED_BY_HASHES"})
    require(all(v == 1 for v in consumed.values()), "INVENTORY_FRAGMENT_DUPLICATED_AS_SEMANTIC_UNITS")
    for page in pages:
        pn = page["pdfPage"]
        require(set(page["inventoryIds"]) == {i["inventoryId"] for i in inventory if i["pdfPage"] == pn},
                "PAGE_INVENTORY_INDEX_MISMATCH:" + str(pn))
        require(set(page["unitIds"]) == {unit_id(u) for u in units
                                          if any(a["pdfPage"] == pn for a in u["evidenceAnchors"])},
                "PAGE_SEMANTIC_UNIT_INDEX_MISMATCH:" + str(pn))
    coverage = word_coverage(source, positions)
    require(all(p["uncoveredWords"] == 0 for p in coverage), "ORIGINAL_WORD_POSITIONS_DROPPED")
    image_rows = []
    seen_images = set()
    for item in review["images"]:
        iid = item["id"]
        match = re.fullmatch(r"p(\d{3})-image-b(\d+)", iid)
        require(match and iid not in seen_images, "INVALID_OR_DUPLICATE_IMAGE_INVENTORY_ID")
        seen_images.add(iid)
        pn, block_no = map(int, match.groups())
        require(item["pdfPage"] == pn, "IMAGE_INVENTORY_PAGE_MISMATCH")
        original = source.blocks(pn)[block_no]
        require(original["type"] == 1 and digest(original["image"]) == item["sourceImageHash"],
                "ORIGINAL_EMBEDDED_IMAGE_MISMATCH:" + iid)
        require(item["renderer"] == RENDERER, "IMAGE_ANCHOR_REQUIRES_FRESH_DOCUMENT_RENDERER:" + iid)
        verify_original_anchor(source, item, iid, require_text=False, require_raster=True)
        if not allow_draft:
            require("PENDING" not in item["disposition"], "IMAGE_DISPOSITION_PENDING:" + iid)
        if item["disposition"] == "SUBSTANTIVE_NON_SPATIAL_FIGURE":
            uid = item.get("reviewUnitId")
            require(uid in units_by_id and iid in units_by_id[uid].get("imageInventoryIds", []),
                    "SUBSTANTIVE_IMAGE_WITHOUT_REVIEWED_UNIT:" + iid)
        image_rows.append({"imageId": iid, "pdfPage": pn, "disposition": item["disposition"],
                           "status": "PASS_ORIGINAL_EMBEDDED_IMAGE_AND_CROP"})
    expected_images = {f"p{pn:03d}-image-b{i:02d}" for pn, page in enumerate(source.doc, 1)
                       for i, block in enumerate(source.blocks(pn)) if block["type"] == 1}
    require(seen_images == expected_images, "ORIGINAL_EMBEDDED_IMAGE_INVENTORY_MISSING_OR_EXTRA")
    actual_counts = {"pages": PAGE_COUNT, "inventoryUnits": len(inventory),
                     "authorReviewUnits": len(units), "sourceImages": len(image_rows)}
    for key, value in actual_counts.items():
        require(review["counts"].get(key) == value, "AUTHOR_DECLARED_COUNT_MISMATCH:" + key)
    return {"status": "PASS_ORIGINAL_POSITIONS_WITH_DRAFT_GAPS" if allow_draft else "PASS_ORIGINAL_POSITIONS_AND_CLASSIFIED_INVENTORY",
            "counts": actual_counts, "inventoryDispositions": dict(collections.Counter(i["disposition"] for i in inventory)),
            "imageDispositions": dict(collections.Counter(i["disposition"] for i in review["images"])),
            "pages": coverage, "inventory": inventory_rows, "units": unit_rows, "images": image_rows,
            "existingActionAnchorOverlapWarnings": action_link_gaps,
            "wholeSemanticCompleteness": "REQUIRES_SEPARATE_SEMANTIC_AND_VISUAL_REVIEW"}


def verify_maps(source, review, visual_review):
    require(review["sourceRevision"] == SOURCE_SHA and review["sourcePageCount"] == PAGE_COUNT,
            "MAP_REVIEW_SOURCE_VERSION_MISMATCH")
    require("sha256:" + visual_review["source"]["sha256"] == SOURCE_SHA,
            "INDEPENDENT_VISUAL_REVIEW_SOURCE_MISMATCH")
    maps = review["maps"]
    expected = {r["pdfPage"] for r in visual_review["records"] if r["type"] == "MAP"}
    require(len({m["id"] for m in maps}) == len(maps), "DUPLICATE_MAP_ID")
    require(len(maps) == len(expected) and {m["pdfPage"] for m in maps} == expected,
            "INDEPENDENT_VISUAL_MAP_CENSUS_MISMATCH")
    rows = []
    for item in maps:
        mid = item["id"]
        verify_original_anchor(source, item, mid, require_text=False, require_raster=True)
        legend = item["legendAnchor"]
        require(legend["pdfPage"] == item["pdfPage"], "MAP_LEGEND_DIFFERENT_PAGE:" + mid)
        verify_original_anchor(source, legend, mid + ":legend", require_text=False, require_raster=True)
        require(bool(item.get("summary")) and isinstance(item.get("legend"), list),
                "MAP_WITHOUT_AUTHORED_SUMMARY_OR_LEGEND:" + mid)
        for key, expected_value in [("spatialApplicability", "UNKNOWN"),
                                    ("legalStatus", "HISTORICAL_RESEARCH_NOT_CURRENT_LAW"),
                                    ("actualExecution", "UNKNOWN"), ("geometryExtracted", False)]:
            require(item.get(key) == expected_value, "MAP_AUTHORITY_OR_GEOMETRY_PROMOTION:" + mid + ":" + key)
        rows.append({"mapId": mid, "pdfPage": item["pdfPage"],
                     "mapRasterDigest": item["rasterDigest"], "legendRasterDigest": legend["rasterDigest"],
                     "legendEntries": len(item["legend"]),
                     "status": "PASS_ORIGINAL_MAP_AND_LEGEND_POSITION_PIXELS",
                     "legendMeaning": "SEPARATE_INDEPENDENT_VISUAL_SEMANTIC_REVIEW"})
    return {"status": "PASS_ORIGINAL_MAP_POSITIONS_AND_INDEPENDENT_MAP_CENSUS",
            "mapOccurrences": len(maps), "records": rows,
            "mapSemanticCompleteness": "NOT_ESTABLISHED_BY_PIXELS_ALONE"}


def flattened_authored_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(flattened_authored_text(v) for v in value)
    if isinstance(value, dict):
        # Evidence identifiers/digests must never accidentally satisfy a meaning check.
        return " ".join(flattened_authored_text(v) for k, v in value.items()
                        if k in {"summary", "text", "condition", "qualifier", "meaning", "label"})
    return ""


def verify_semantic_assertions(source, narrative_units, maps, assertions):
    """Replay narrowly reviewed semantic guards against fresh original evidence.

    An assertion is an explicit reviewer decision, not an automatic assertion
    that the entirety of a record has been interpreted correctly.
    """
    require(assertions.get("sourceRevision") == SOURCE_SHA, "SEMANTIC_GUARDS_SOURCE_VERSION_MISMATCH")
    require(bool(assertions.get("assertions")), "MISSING_INDEPENDENT_SEMANTIC_GUARDS")
    units = {unit_id(u): u for u in narrative_units}
    map_units = {u["id"]: u for u in maps}
    checked = []
    for check in assertions.get("assertions", []):
        aid = check["assertionId"]
        text = verify_original_anchor(source, check["sourceAnchor"], aid,
                                      require_text="originalPattern" in check,
                                      require_raster="originalPattern" not in check)
        if "originalPattern" in check:
            require(re.search(check["originalPattern"], text, re.I),
                    "SEMANTIC_GUARD_ORIGINAL_BASIS_MISSING:" + aid)
        record = (map_units if check.get("collection") == "maps" else units).get(check["recordId"])
        require(record is not None, "SEMANTIC_GUARD_RECORD_MISSING:" + aid)
        for field, patterns in check.get("requiredPatterns", {}).items():
            value = flattened_authored_text(record.get(field))
            require(all(re.search(pattern, value, re.I) for pattern in patterns),
                    "REVIEWED_CONDITION_OR_LEGEND_MEANING_DROPPED:" + aid + ":" + field)
        for field, expected in check.get("reviewedFieldDigests", {}).items():
            require(canonical_digest(record.get(field)) == expected,
                    "REVIEWED_SEMANTIC_FIELD_CHANGED:" + aid + ":" + field)
        for field, expected_members in check.get("requiredListMembers", {}).items():
            require(isinstance(record.get(field), list) and all(
                member in record[field] for member in expected_members),
                "ORIGINAL_REVIEWED_LEGEND_ENTRY_CHANGED:" + aid + ":" + field)
        checked.append({"assertionId": aid, "recordId": check["recordId"],
                        "status": "PASS_BOUNDED_REVIEWED_GUARD_AND_SOURCE_ANCHOR",
                        "pdfPage": check["sourceAnchor"]["pdfPage"]})
    return checked


def verify_all(source, narrative, maps, visual, core, baseline, guards, bundle, *, allow_draft=False):
    retained = verify_retained_actions(core, baseline)
    narrative_result = verify_narrative(source, narrative, core, allow_draft=allow_draft)
    map_result = verify_maps(source, maps, visual)
    semantic_result = verify_semantic_assertions(source, narrative["units"], maps["maps"], guards)
    runtime = (verify_runtime_bundle(bundle, narrative["units"], maps["maps"], core) if bundle is not None
               else {"status": "PENDING_RUNTIME_BUNDLE_NOT_CHECKED"})
    metadata = (verify_runtime_source_metadata(source, bundle, narrative, maps, core) if bundle is not None
                else {"status": "PENDING_RUNTIME_METADATA_NOT_CHECKED"})
    require(allow_draft or bundle is not None, "FINAL_RUNTIME_BUNDLE_MISSING")
    return {"status": "PARTIAL_DRAFT_POSITION_CHECKS" if allow_draft else "PASS_BOUNDED_ORIGINAL_SOURCE_AND_TRANSFER_VERIFICATION",
            "sourceId": SOURCE_ID, "sourceRevision": SOURCE_SHA,
            "retainedCore": retained, "narrative": narrative_result,
            "maps": map_result, "selectedSemanticGuards": semantic_result,
            "runtimeTransfer": runtime, "runtimeSourceMetadata": metadata, "officialAdmission": "PENDING",
            "currentLegalApplicability": "UNKNOWN", "actualExecution": "UNKNOWN",
            "limits": ["Text and pixel hashes verify exact original source locations, not complete semantic truth.",
                       "The semantic guard list is intentionally selected; separate full narrative and map reviews are required.",
                       "Native extraction fragments, merged semantic units, actions and map occurrences have different denominators.",
                       "No original PDF, extracted original prose, rendered page or crop is written to repository output."]}


def negative_checks(source, narrative, maps, visual, core, baseline, guards, bundle, *, allow_draft=False):
    cases = []

    def test(name, mutate, expected_reason):
        n, m, c, b = copy.deepcopy(narrative), copy.deepcopy(maps), copy.deepcopy(core), copy.deepcopy(bundle)
        mutate(n, m, c, b)
        try:
            verify_all(source, n, m, visual, c, baseline, guards, b, allow_draft=allow_draft)
        except (ValueError, KeyError) as error:
            require(expected_reason in str(error), "NEGATIVE_FAILED_FOR_UNEXPECTED_REASON:" + name + ":" + str(error))
            cases.append({"case": name, "status": "REJECTED_EXPECTED", "reason": str(error),
                          "basis": "Mutation of checked source-linked inputs; original PDF remains unchanged."})
            return
        raise AssertionError("NEGATIVE_ACCEPTED:" + name)

    def inventory(n):
        return next(i for i in n["inventory"] if i["inventoryId"] == "p056-b09-u01")

    def unit(n):
        return next(u for u in n["units"] if unit_id(u) == "csoi:lsps2020:narrative:p056-b09-u01")

    test("wrong_source_version", lambda n, m, c, b: n["document"].update(sourceRevision="sha256:" + "0" * 64),
         "NARRATIVE_SOURCE_VERSION_MISMATCH")
    test("wrong_original_page", lambda n, m, c, b: inventory(n)["evidenceAnchors"][0].update(pdfPage=57),
         "ORIGINAL_CLIP_TEXT_MISMATCH")

    def shift_bbox(n, m, c, b):
        a = inventory(n)["evidenceAnchors"][0]
        a["bbox"] = [a["bbox"][0], a["bbox"][1] + 20, a["bbox"][2], a["bbox"][3]]
    test("wrong_original_bbox", shift_bbox, "ORIGINAL_CLIP_TEXT_MISMATCH")
    test("dropped_original_need_condition", lambda n, m, c, b: unit(n).update(conditions=[]),
         "REVIEWED_CONDITION_OR_LEGEND_MEANING_DROPPED")

    def wrong_legend(n, m, c, b):
        entry = next(x for x in m["maps"] if x["pdfPage"] == 114)
        row = next(x for x in entry["legend"] if x["label"].endswith("Option 5"))
        row["label"] = row["label"].replace("Option 5", "Option 4")
    test("wrong_original_legend_option_with_unchanged_pixels", wrong_legend,
         "ORIGINAL_REVIEWED_LEGEND_ENTRY_CHANGED")

    def wrong_colour(n, m, c, b):
        entry = next(x for x in m["maps"] if x["pdfPage"] == 114)
        next(x for x in entry["legend"] if x["label"].endswith("Option 5"))["symbol"] = "yellow dashed line"
    test("wrong_original_legend_colour_with_unchanged_pixels", wrong_colour,
         "ORIGINAL_REVIEWED_LEGEND_ENTRY_CHANGED")

    def wrong_legend_crop(n, m, c, b):
        entry = next(x for x in m["maps"] if x["pdfPage"] == 114)
        entry["legendAnchor"]["bbox"][0] += 20
    test("mislocated_original_legend_crop", wrong_legend_crop, "ORIGINAL_CLIP_RASTER_MISMATCH")

    def drop_position(n, m, c, b):
        iid = "p001-b00-u01"
        n["inventory"] = [i for i in n["inventory"] if i["inventoryId"] != iid]
        n["pages"][0]["inventoryIds"].remove(iid)
        n["counts"]["inventoryUnits"] -= 1
    test("dropped_original_position_despite_recounted_inventory", drop_position,
         "ORIGINAL_WORD_POSITIONS_DROPPED")

    def drop_action(n, m, c, b):
        c["records"] = [r for r in c["records"] if r["id"] != "csoi:knowledge:lsps2020:narrative-action:p27:3.2"]
    test("removed_existing_conflict", drop_action, "EXISTING_CORE_RECORD_REMOVED_OR_CHANGED")
    if bundle is not None:
        def drop_runtime_unit(n, m, c, b):
            record = next(r for r in b["records"] if r["category"] == "LSPS_NARRATIVE" and len(r["facts"]["units"]) > 1)
            record["facts"]["units"].pop()
        test("lost_unit_during_page_aggregation", drop_runtime_unit, "RUNTIME_NARRATIVE_UNIT_CENSUS_MISMATCH")
        def wrong_priority(n, m, c, b):
            record = next(r for r in b["records"] if r["category"] == "LSPS_MAP" and r["anchor"]["pdfPage"] == 48)
            next(rel for rel in record["relations"] if ":priority:" in rel["targetId"])["targetId"] = "csoi:knowledge:lsps2020:priority:9"
        test("wrong_map_source_reading_priority_despite_valid_target", wrong_priority,
             "MAP_READING_PRIORITY_WRONG_SOURCE_SECTION")
        def drop_action_context(n, m, c, b):
            record = next(r for r in b["records"] if r["category"] == "LSPS_NARRATIVE" and any(
                ":action:" in rel["targetId"] for rel in r.get("relations", [])))
            record["relations"].remove(next(rel for rel in record["relations"] if ":action:" in rel["targetId"]))
        test("missing_original_same_page_action_context", drop_action_context,
             "NARRATIVE_READING_CONTEXT_NOT_MATCHING_SOURCE_PAGE")
        test("wrong_original_page_index_digest", lambda n, m, c, b: b["pages"][7].update(pageDigest="sha256:" + "0" * 64),
             "RUNTIME_PAGE_INDEX_ORIGINAL_HASH_MISMATCH")

    with tempfile.TemporaryDirectory(prefix="csoi-lsps-context-negative-", dir="/tmp") as temp:
        missing = Path(temp) / "missing-original.pdf"
        try:
            Original(missing)
        except FileNotFoundError:
            cases.append({"case": "missing_original_pdf", "status": "REJECTED_EXPECTED",
                          "reason": "FileNotFoundError: original bytes required; no substitute or cached PASS."})
        else:
            raise AssertionError("MISSING_ORIGINAL_ACCEPTED")
        corrupt = Path(temp) / "corrupt-original.pdf"
        raw = bytearray(source.path.read_bytes())
        raw[512] ^= 1
        corrupt.write_bytes(raw)
        try:
            Original(corrupt)
        except ValueError as error:
            require(str(error) == "ORIGINAL_SOURCE_BYTES_MISMATCH", "CORRUPT_SOURCE_UNEXPECTED_FAILURE")
            cases.append({"case": "corrupt_original_pdf", "status": "REJECTED_EXPECTED", "reason": str(error)})
        else:
            raise AssertionError("CORRUPT_ORIGINAL_ACCEPTED")
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--out", type=Path,
                        default=APP / "qa/lsps-completion/independent-position")
    parser.add_argument("--census-only", action="store_true")
    parser.add_argument("--draft", action="store_true", help="Permit explicit unfinished classifications; never returns final PASS.")
    parser.add_argument("--without-runtime", action="store_true", help="Draft-only source check before runtime packaging exists.")
    defaults = {
        "narrative": "qa/lsps-completion/author/narrative-review.json",
        "maps": "qa/lsps-completion/maps/map-review.json",
        "visual": "qa/lsps-completion/independent-visual/initial-visual-review.json",
        "guards": "qa/lsps-completion/independent-position/semantic-guards.json",
        "conditions": "qa/lsps-completion/independent-narrative/condition-assertions.json",
        "core": "sources/lsps-public-knowledge.json",
        "baseline": "qa/lsps-completion/independent-position/existing-actions-baseline.json",
        "bundle": "sources/lsps-context-review.json",
    }
    for name, relative in defaults.items():
        parser.add_argument("--" + name, type=Path, default=APP / relative)
    args = parser.parse_args()
    require(not args.without_runtime or args.draft, "SKIPPING_RUNTIME_REQUIRES_EXPLICIT_DRAFT_MODE")
    source = Original(args.pdf)
    census = source.census()
    write_json(args.out / "original-source-census.json", census)
    write_csv(args.out / "original-page-census.csv", census["pages"])
    if args.census_only:
        print(json.dumps({"status": "PASS_ORIGINAL_CENSUS_ONLY", **census["counts"],
                          "semanticCompleteness": census["semanticCompleteness"]}))
        return
    input_bytes = {name: getattr(args, name).read_bytes() for name in defaults
                   if name != "bundle" or not args.without_runtime}
    loaded = {name: json.loads(raw) for name, raw in input_bytes.items()}
    require(loaded["conditions"].get("sourceRevision") == SOURCE_SHA,
            "INDEPENDENT_CONDITION_REVIEW_SOURCE_VERSION_MISMATCH")
    merged_guards = copy.deepcopy(loaded["guards"])
    guards_by_record = {(g.get("collection", "narrative"), g["recordId"]): g
                        for g in merged_guards["assertions"]}
    guards_by_record.update({(g.get("collection", "narrative"), g["recordId"]): g
                            for g in loaded["conditions"]["assertions"]})
    merged_guards["assertions"] = list(guards_by_record.values())
    data = (source, loaded["narrative"], loaded["maps"], loaded["visual"], loaded["core"],
            loaded["baseline"], merged_guards, loaded.get("bundle"))
    result = verify_all(*data, allow_draft=args.draft)
    negatives = negative_checks(*data, allow_draft=args.draft)
    require(all(getattr(args, name).read_bytes() == raw for name, raw in input_bytes.items()),
            "INPUT_FILES_CHANGED_DURING_VERIFICATION_RERUN_REQUIRED")
    result.update(at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  negativeCases=negatives, originalCensus=census["counts"],
                  checkedInputDigests={name: digest(raw) for name, raw in input_bytes.items()},
                  verifierDigest=digest(Path(__file__).read_bytes()))
    write_json(args.out / "verification.json", result)
    write_json(args.out / "negative-cases.json", negatives)
    write_csv(args.out / "inventory-position-matrix.csv", result["narrative"]["inventory"])
    write_csv(args.out / "semantic-unit-position-matrix.csv", result["narrative"]["units"])
    write_csv(args.out / "map-position-matrix.csv", result["maps"]["records"])
    if "relationRows" in result["runtimeSourceMetadata"]:
        write_csv(args.out / "source-reading-context-matrix.csv", result["runtimeSourceMetadata"]["relationRows"])
    write_csv(args.out / "page-coverage-matrix.csv", [
        {k: value for k, value in row.items() if k != "uncoveredPositions"}
        for row in result["narrative"]["pages"]])
    print(json.dumps({"status": result["status"], **result["narrative"]["counts"],
                      "maps": result["maps"]["mapOccurrences"], "negativeCases": len(negatives),
                      "runtimeTransfer": result["runtimeTransfer"]["status"],
                      "officialAdmission": "PENDING"}))


if __name__ == "__main__":
    main()
