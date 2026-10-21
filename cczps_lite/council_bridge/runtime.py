"""Isolated SQLite nodes and a local operator workflow. No network egress.

Authority is scoped by a Principal supplied by the trusted local host, not by
reviewer labels. This rehearsal is not a multi-user identity implementation.
"""
from __future__ import annotations

import copy
import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from .contracts import LABEL, VERSION, BridgeError, canonical_json, digest, identifier, instant, require, utcnow, validate_config, validate_request
from .fixtures import evidence_fixture
from .providers import MockProvider, AlternateMockProvider, MatrixOneAdapter

ALL_PERMISSIONS = frozenset({"read", "compute", "review", "publish", "exchange", "observe"})


@dataclass(frozen=True)
class Principal:
    council_id: str
    permissions: frozenset[str]


class CouncilBridge:
    def __init__(self, root, configs, clock=utcnow, providers=None):
        self.root = Path(root).resolve()
        self.clock = clock
        validated = [validate_config(copy.deepcopy(c)) for c in configs]
        require(len({c["council_id"] for c in validated}) == len(validated), "duplicate Council")
        self.configs = {c["council_id"]: c for c in validated}
        self.providers = providers or {p.provider_id: p for p in (MockProvider(), AlternateMockProvider(), MatrixOneAdapter())}
        self.root.mkdir(parents=True, exist_ok=True)
        for cid in self.configs:
            folder = self.root / identifier(cid)
            require(not folder.is_symlink(), "symlink node refused")
            folder.mkdir(exist_ok=True)
            db = folder / "bridge.sqlite3"
            require(not db.is_symlink(), "symlink database refused")
            with self._connect(cid) as con:
                con.executescript("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK(id=1), body TEXT NOT NULL); CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, body TEXT NOT NULL, digest TEXT NOT NULL);")
                if con.execute("SELECT 1 FROM state").fetchone() is None:
                    evidence = evidence_fixture(self.configs[cid])
                    initial = {"schema_id": VERSION, "council_id": cid, "classification": LABEL,
                               "evidence": evidence, "evidence_history": copy.deepcopy(evidence), "jobs": {}, "assessments": [], "outcomes": [], "releases": {}, "imports": {}}
                    con.execute("INSERT INTO state VALUES(1,?)", (canonical_json(initial),))

    @contextmanager
    def _connect(self, cid):
        connection = sqlite3.connect(self.root / identifier(cid) / "bridge.sqlite3", timeout=3)
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _scope(self, principal, permission):
        require(isinstance(principal, Principal) and principal.council_id in self.configs, "unknown Council principal")
        require(permission in principal.permissions, "permission denied")
        return principal.council_id

    def _mutate(self, principal, permission, event_type, operation):
        cid = self._scope(principal, permission)
        with self._connect(cid) as con:
            con.execute("BEGIN IMMEDIATE")
            state = json.loads(con.execute("SELECT body FROM state WHERE id=1").fetchone()[0])
            rows = con.execute("SELECT body,digest FROM events ORDER BY seq").fetchall()
            predecessor = "GENESIS"
            for seq, (body, checksum) in enumerate(rows, 1):
                event = json.loads(body)
                require(event["sequence"] == seq and event["predecessor"] == predecessor and digest(event) == checksum, "audit inconsistency; mutation refused")
                predecessor = checksum
            if rows:
                require(json.loads(rows[-1][0])["state_digest"] == digest(state), "state inconsistency; mutation refused")
            result = operation(state)
            last = con.execute("SELECT seq,digest FROM events ORDER BY seq DESC LIMIT 1").fetchone()
            event = {"sequence": last[0] + 1 if last else 1, "predecessor": last[1] if last else "GENESIS",
                     "type": event_type, "at": self.clock(), "council_id": cid, "state_digest": digest(state)}
            con.execute("UPDATE state SET body=? WHERE id=1", (canonical_json(state),))
            con.execute("INSERT INTO events VALUES(?,?,?)", (event["sequence"], canonical_json(event), digest(event)))
            return copy.deepcopy(result)

    def snapshot(self, principal):
        cid = self._scope(principal, "read")
        with self._connect(cid) as con:
            state = json.loads(con.execute("SELECT body FROM state WHERE id=1").fetchone()[0])
            rows = con.execute("SELECT body,digest FROM events ORDER BY seq").fetchall()
        predecessor = "GENESIS"
        events = []
        valid = True
        for sequence, (body, checksum) in enumerate(rows, 1):
            event = json.loads(body)
            valid &= event["sequence"] == sequence and event["predecessor"] == predecessor and digest(event) == checksum
            predecessor = checksum
            events.append({**event, "digest": checksum})
        if events:
            valid &= events[-1]["state_digest"] == digest(state)
        state["events"] = events
        state["audit_consistent"] = bool(valid)
        state["config"] = self.configs[cid]
        state["providers"] = [p.capabilities() for p in self.providers.values()]
        now = instant(self.clock())
        for item in state["evidence"]:
            item["freshness"] = "EXPIRED" if instant(item["valid_until"]) <= now else "WITHIN_FIXTURE_WINDOW"
        for answer in state["assessments"]:
            answer["display_state"] = self._answer_state(answer, state, now)
        return state

    def _answer_state(self, answer, state, now):
        if instant(answer["valid_until"]) <= now:
            return "EXPIRED"
        by_id = {e["evidence_id"]: e for e in state["evidence"]}
        if any(by_id[e]["status"] != "ACTIVE" for e in answer["supporting_evidence"]):
            return "WITHDRAWN_EVIDENCE_REVIEW_REQUIRED"
        return answer["human_review"]["status"]

    @staticmethod
    def _input(state):
        return digest([{k: v for k, v in e.items() if k not in {"private_notes", "freshness"}} for e in state["evidence"]])

    def prepare_request(self, principal):
        cid = self._scope(principal, "compute")
        state = self.snapshot(Principal(cid, frozenset({"read"})))
        n = len(state["jobs"]) + 1
        request = {"request_id": cid + "-run-" + str(n), "council_id": cid, "question_id": cid + "-resource-question",
                   "spatial_ids": [e["spatial_id"] for e in state["evidence"]], "variable": "fixture_resource_index", "unit": "1",
                   "period_start": max(e["observed_at"] for e in state["evidence"]), "period_end": min(e["valid_until"] for e in state["evidence"]),
                   "input_digest": self._input(state), "data_classification": "SYNTHETIC_ONLY", "licence": "MIT_REPOSITORY_FIXTURE",
                   "model_version": "fixed-fixture-v1", "budget_aud": 0, "idempotency_key": cid + "-key-" + str(n),
                   "output_requirement": "SYNTHETIC_DIAGNOSTIC_ONLY"}
        return {**request, "approval_digest": digest(request)}

    def submit(self, principal, request, provider_id="mock-local"):
        cid = self._scope(principal, "compute")
        require(provider_id in self.providers, "unknown provider")
        def operation(state):
            validate_request(request, self.configs[cid], self._input(state))
            for old in state["jobs"].values():
                if old["request"]["idempotency_key"] == request["idempotency_key"]:
                    require(old["request"] == request and old["provider_id"] == provider_id, "idempotency collision")
                    return old
            require(request["request_id"] not in state["jobs"], "request identity collision")
            now = instant(self.clock())
            require(all(e["status"] == "ACTIVE" and instant(e["valid_until"]) > now for e in state["evidence"]), "expired or withdrawn evidence")
            status = self.providers[provider_id].submit(request)
            require(status["status"] == "QUEUED", "unexpected provider admission")
            job = {"request": copy.deepcopy(request), "provider_id": provider_id, "status": "QUEUED", "attempts": 1,
                   "receipt": None, "result": None}
            state["jobs"][request["request_id"]] = job
            return job
        return self._mutate(principal, "compute", "COMPUTE_APPROVED_EXACT_SCOPE", operation)

    def progress(self, principal, request_id, action="poll", mode="success"):
        identifier(request_id)
        def operation(state):
            require(request_id in state["jobs"], "job not found in this Council")
            job = state["jobs"][request_id]
            if action == "retry":
                require(job["status"] in {"FAILED", "TIMED_OUT"} and job["attempts"] < 3, "retry not admitted")
                job.update(status="QUEUED", attempts=job["attempts"] + 1)
                return job
            if action == "cancel":
                require(job["status"] == "QUEUED", "only queued jobs can be cancelled")
                job.update(self.providers[job["provider_id"]].cancel(job["request"]))
                return job
            require(action == "poll", "unknown job action")
            if job["status"] == "COMPLETED_QUARANTINED":
                return job
            require(job["status"] == "QUEUED", "job not queued")
            response = self.providers[job["provider_id"]].status(job["request"], mode)
            if response["status"] in {"FAILED", "TIMED_OUT"}:
                job.update(response)
                return job
            result = response["result"]
            expected = job["request"]
            for field in ("request_id", "input_digest", "model_version", "variable", "unit", "period_start", "period_end", "spatial_ids"):
                require(result.get(field) == expected[field], "provider result mismatch: " + field)
            require(result.get("classification") == "SYNTHETIC_ONLY" and result.get("network_used") is False and result.get("cost_aud") == 0, "result boundary violation")
            job.update(response)
            job["receipt"] = {"schema_id": "climateos.council_bridge.run_receipt.v0.1", "request_digest": digest(expected),
                              "provider_id": job["provider_id"], "result_digest": digest(result), "attempts": job["attempts"],
                              "at": self.clock(), "cost_aud": 0, "network_used": False, "classification": LABEL}
            return job
        return self._mutate(principal, "compute", "COMPUTE_" + action.upper(), operation)

    def assess(self, principal, request_id):
        def operation(state):
            require(request_id in state["jobs"], "job not found")
            job = state["jobs"][request_id]
            require(job["status"] == "COMPLETED_QUARANTINED", "quarantined completed result required")
            require(job["request"]["input_digest"] == self._input(state), "inputs changed; request a new run")
            now = self.clock()
            require(all(e["status"] == "ACTIVE" and instant(e["valid_until"]) > instant(now) for e in state["evidence"]), "stale evidence")
            require(not any(a["run_request_id"] == request_id for a in state["assessments"]), "assessment already exists")
            aid = state["council_id"] + "-answer-" + str(len(state["assessments"]) + 1)
            answer = {"schema_id": "climateos.time_bounded_environmental_answer.v0.1", "answer_id": aid,
                      "question": "How should evidence collection be coordinated across places and shared resources?",
                      "decision_use": "Rehearse Council-level evidence planning", "place": self.configs[state["council_id"]]["name"],
                      "spatial_boundary": "Synthetic object relations; administrative geometry not admitted",
                      "assessment_period": job["request"]["period_start"] + "/" + job["request"]["period_end"],
                      "evidence_cutoff": min(e["observed_at"] for e in state["evidence"]), "issued_at": now,
                      "valid_until": min(e["valid_until"] for e in state["evidence"]), "conclusion_level": "L0", "evidence_maturity": "S0",
                      "answer": "Rehearsal only: two fictional resource records can be traced across a Council workspace. No real Council environmental condition has been assessed.",
                      "confidence": "No environmental confidence: synthetic records and computation only",
                      "supporting_evidence": [e["evidence_id"] for e in state["evidence"]],
                      "conflicting_evidence": ["Fictional farm and service indices differ; no calibrated comparison"],
                      "missing_critical_evidence": ["Admitted Council geometry", "Representative observations", "Independent regional model", "Qualified review"],
                      "local_translation_path": ["Regional grid: unconnected", "Shared water-system hypothesis: synthetic", "Farm and service area: separate spatial scopes", "Human review"],
                      "alternative_explanations": ["Fixture values cannot test a physical mechanism"],
                      "consequence_if_true": "A traceable evidence request can be prepared", "consequence_if_false": "Revise the rehearsal in a new assessment",
                      "intervention_window": "A0 evidence collection and review preparation only", "permitted_actions": ["EVIDENCE_REQUEST", "RECORD_PRESERVATION"],
                      "prohibited_actions": ["PUBLIC_WARNING", "INFRASTRUCTURE_CONTROL", "STATUTORY_DECISION", "A1_OR_HIGHER"],
                      "update_triggers": ["Admitted new evidence", "source revision", "expiry"], "demotion_triggers": ["withdrawn evidence", "identity mismatch"],
                      "stop_conditions": ["Attempted real-world inference", "scope expansion"],
                      "human_review": {"status": "PENDING_HUMAN_REVIEW", "scientific_signoff": False},
                      "official_confirmation": {"status": "NONE"}, "retrospective_validation": {"status": "AWAITING_SYNTHETIC_OUTCOME"},
                      "run_request_id": request_id, "classification": LABEL,
                      "evidence_passport": {"schema_id": "climateos.environmental_evidence_passport.v0.1", "passport_id": aid + "-passport",
                          "subject": "Synthetic Council workflow", "source_identity": {"input_digest": job["request"]["input_digest"]},
                          "method": {"run_receipt_digest": digest(job["receipt"]), "method": "Fixed fixture; no local environmental inference"},
                          "derived_claim": {"answer_id": aid, "conclusion_level": "L0"}, "limitations": [LABEL],
                          "review": {"status": "PENDING_HUMAN_REVIEW"}, "retrospective_validation": {"status": "PENDING"}}}
            state["assessments"].append(answer)
            return answer
        return self._mutate(principal, "compute", "ASSESSMENT_DRAFTED", operation)

    def review(self, principal, answer_id, decision):
        require(decision in {"ACCEPT_DEMO", "REJECT_DEMO"}, "demo-only review")
        def operation(state):
            answers = [a for a in state["assessments"] if a["answer_id"] == answer_id]
            require(len(answers) == 1, "answer not found")
            answer = answers[0]
            require(self._answer_state(answer, state, instant(self.clock())) == "PENDING_HUMAN_REVIEW", "review not admitted")
            answer["human_review"] = {"status": decision, "at": self.clock(), "authority": "LOCAL_OPERATOR_CAPABILITY_NOT_PROFESSIONAL_IDENTITY", "scientific_signoff": False}
            answer["evidence_passport"]["review"] = copy.deepcopy(answer["human_review"])
            return answer
        return self._mutate(principal, "review", "HUMAN_DEMO_REVIEW", operation)

    def observe(self, principal, answer_id):
        def operation(state):
            answer = next((a for a in state["assessments"] if a["answer_id"] == answer_id), None)
            require(answer is not None and answer["human_review"]["status"] == "ACCEPT_DEMO", "accepted demo required")
            record = {"answer_id": answer_id, "at": self.clock(), "classification": "SYNTHETIC_ONLY", "action": "EVIDENCE_REQUEST_REHEARSAL", "outcome": "Fixture workflow completed; no field action or prediction skill claimed"}
            state["outcomes"].append(record)
            return record
        return self._mutate(principal, "observe", "SYNTHETIC_OUTCOME_RECORDED", operation)

    @staticmethod
    def _public_items(state):
        # Only exact repository fixture projections qualify. No free text is exported.
        items = []
        for e in state["evidence"]:
            if e["classification"] != "SYNTHETIC_ONLY" or e["share_class"] != "SYNTHETIC_APPROVED_FOR_REVIEW" or e["licence"] != "MIT_REPOSITORY_FIXTURE":
                continue
            items.append({k: e[k] for k in ("evidence_id", "revision", "classification", "observed_at", "valid_until", "status")})
        return items

    def preview(self, principal):
        self._scope(principal, "publish")
        state = self.snapshot(Principal(principal.council_id, frozenset({"read"})))
        items = self._public_items(state)
        require(bool(items), "no publishable synthetic metadata")
        body = {"schema_id": VERSION + ".exchange", "source_council": principal.council_id, "classification": "SYNTHETIC_ONLY", "licence": "MIT_REPOSITORY_FIXTURE", "items": items}
        return {"body": body, "digest": digest(body), "excluded": "Values, geometry, free text, notes, observations, job inputs and database omitted"}

    def approve_release(self, principal, preview_digest):
        def operation(state):
            body = {"schema_id": VERSION + ".exchange", "source_council": principal.council_id, "classification": "SYNTHETIC_ONLY", "licence": "MIT_REPOSITORY_FIXTURE", "items": self._public_items(state)}
            require(bool(body["items"]) and digest(body) == preview_digest, "preview changed")
            require(all(e["status"] == "ACTIVE" and instant(e["valid_until"]) > instant(self.clock()) for e in body["items"]), "stale release")
            state["releases"].setdefault(preview_digest, {"body": body, "approved_at": self.clock(), "status": "APPROVED_LOCAL_EXPORT"})
            return state["releases"][preview_digest]
        return self._mutate(principal, "publish", "EXACT_EXPORT_APPROVED", operation)

    def export(self, principal, release_digest):
        state = self.snapshot(Principal(self._scope(principal, "publish"), frozenset({"read"})))
        require(release_digest in state["releases"], "release not approved")
        release = state["releases"][release_digest]
        current = {e["evidence_id"]: e for e in state["evidence"]}
        require(release["status"] == "APPROVED_LOCAL_EXPORT" and all(current[e["evidence_id"]]["status"] == "ACTIVE" and instant(e["valid_until"]) > instant(self.clock()) for e in release["body"]["items"]), "release withdrawn or expired")
        return copy.deepcopy(release["body"])

    def import_release(self, principal, source_principal, release_digest):
        # Trusted local broker verifies source approval. No arbitrary JSON import.
        destination = self._scope(principal, "exchange")
        source = self._scope(source_principal, "publish")
        require(source != destination, "cross-Council exchange required")
        body = self.export(source_principal, release_digest)
        require(digest(body) == release_digest, "exchange integrity mismatch")
        def operation(state):
            state["imports"].setdefault(release_digest, {"body": body, "status": "METADATA_ONLY_NOT_LOCAL_EVIDENCE", "at": self.clock()})
            return state["imports"][release_digest]
        return self._mutate(principal, "exchange", "APPROVED_METADATA_IMPORTED", operation)

    def withdraw(self, principal, evidence_id):
        def operation(state):
            e = next((e for e in state["evidence"] if e["evidence_id"] == evidence_id), None)
            require(e is not None, "evidence not found")
            e["status"] = "WITHDRAWN"
            e["revision"] += 1
            state["evidence_history"].append(copy.deepcopy(e))
            for release in state["releases"].values():
                if any(i["evidence_id"] == evidence_id for i in release["body"]["items"]):
                    release["status"] = "WITHDRAWN"
            return e
        return self._mutate(principal, "publish", "EVIDENCE_WITHDRAWN_NEW_REVISION", operation)

    def sync_imports(self, principal):
        def operation(state):
            for release_digest, item in state["imports"].items():
                cid = item["body"]["source_council"]
                source = self.snapshot(Principal(cid, frozenset({"read"})))
                release = source["releases"].get(release_digest)
                if not release or release["status"] != "APPROVED_LOCAL_EXPORT":
                    item["status"] = "WITHDRAWN_AT_SOURCE"
                elif any(instant(e["valid_until"]) <= instant(self.clock()) for e in item["body"]["items"]):
                    item["status"] = "EXPIRED"
                else:
                    item["status"] = "METADATA_ONLY_NOT_LOCAL_EVIDENCE"
            return state["imports"]
        return self._mutate(principal, "exchange", "IMPORT_STATUS_RECONCILED", operation)
