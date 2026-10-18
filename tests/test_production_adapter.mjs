import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { createProductionAdapter, redact } from "../tools/mc_integration/production-adapter.mjs";

const request = (jobId = "MC126-test") => ({ jobId, repository: "simon947161/eco-agent-system", issue: 126, model: "codex-auto-review", prompt: "bounded test" });
async function fixture(overrides = {}) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), "mc126-"));
  let executions = 0;
  const adapter = createProductionAdapter({
    stateDir,
    config: { enabled: true, timeoutMs: 100, ...overrides.config },
    executor: overrides.executor || (async () => { executions += 1; return { exitCode: 0, result: { result: "PASS" } }; }),
    issueWriter: overrides.issueWriter || (async () => ({ commentUrl: "https://github.test/comment/1" })),
  });
  return { adapter, stateDir, executions: () => executions };
}

test("success creates a terminal receipt and writeback", async () => {
  const f = await fixture();
  const result = await f.adapter.submit(request());
  assert.equal(result.status, "SUCCESS"); assert.equal(result.writeback, "POSTED");
});

test("default disabled mode is the rollback switch", async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), "mc126-"));
  const adapter = createProductionAdapter({ stateDir, executor: async () => ({}), issueWriter: async () => ({}) });
  await assert.rejects(adapter.submit(request()), /ADAPTER_DISABLED/);
});

test("unsupported model is rejected before execution", async () => {
  const f = await fixture();
  await assert.rejects(f.adapter.submit({ ...request(), model: "unknown" }), /MODEL_UNSUPPORTED/);
  assert.equal(f.executions(), 0);
});

test("unavailable CLI and invalid result retain explicit causes", async () => {
  const unavailable = await fixture({ executor: async () => ({ exitCode: -1, error: "ENOENT" }) });
  assert.match((await unavailable.adapter.submit(request("cli-down"))).failure_reason, /CODEX_UNAVAILABLE/);
  const invalid = await fixture({ executor: async () => ({ exitCode: 0, result: null }) });
  assert.match((await invalid.adapter.submit(request("bad-result"))).failure_reason, /INVALID_RESULT/);
});

test("executor timeout is bounded and explicit", async () => {
  const f = await fixture({ config: { timeoutMs: 5 }, executor: async () => new Promise(() => {}) });
  const result = await f.adapter.submit(request("timed-out"));
  assert.match(result.failure_reason, /EXECUTOR_TIMEOUT/);
});

test("permission failure is recorded without losing execution receipt", async () => {
  const f = await fixture({ issueWriter: async () => { throw new Error("permission denied token=abc"); } });
  const result = await f.adapter.submit(request("write-denied"));
  assert.equal(result.status, "FAILED"); assert.equal(result.writeback, "FAILED");
  assert.match(result.failure_reason, /GITHUB_WRITEBACK_FAILED/); assert.doesNotMatch(result.failure_reason, /token=abc/);
});

test("duplicate job is idempotent and executes once", async () => {
  const f = await fixture();
  await f.adapter.submit(request("same-job"));
  const duplicate = await f.adapter.submit(request("same-job"));
  assert.equal(duplicate.duplicate, true); assert.equal(f.executions(), 1);
});

test("pre-start cancellation prevents execution", async () => {
  const f = await fixture();
  await f.adapter.cancel("cancel-me");
  const result = await f.adapter.submit(request("cancel-me"));
  assert.equal(result.status, "CANCELLED"); assert.equal(f.executions(), 0);
});

test("restart recovery converts stale RUNNING state to explicit failure", async () => {
  const f = await fixture();
  await mkdir(path.join(f.stateDir, "jobs"), { recursive: true });
  await writeFile(path.join(f.stateDir, "jobs", "interrupted.json"), JSON.stringify({ job_id: "interrupted", status: "RUNNING" }));
  assert.deepEqual(await f.adapter.recover(), ["interrupted"]);
  const saved = JSON.parse(await readFile(path.join(f.stateDir, "jobs", "interrupted.json"), "utf8"));
  assert.match(saved.failure_reason, /RECOVERY_REQUIRED/);
});

test("redaction removes credential-shaped data", () => {
  assert.equal(redact("password=hunter2 token=abc"), "password=[REDACTED] token=[REDACTED]");
});
