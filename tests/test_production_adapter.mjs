import assert from "node:assert/strict";
import { mkdtemp, mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { DEFAULT_ADAPTER_CONFIG, boundText, createProductionAdapter, redact } from "../tools/mc_integration/production-adapter.mjs";

const request = (jobId = "MC126-test") => ({ jobId, repository: "simon947161/eco-agent-system", issue: 126, model: "codex-auto-review", prompt: "bounded test" });

async function fixture(overrides = {}) {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), "mc126-"));
  let executions = 0;
  const implementation = overrides.executor || (async () => ({ exitCode: 0, result: { result: "PASS" } }));
  const adapter = createProductionAdapter({
    stateDir,
    config: { enabled: true, timeoutMs: 100, terminationGraceMs: 25, ...overrides.config },
    executor: async (input) => { executions += 1; return implementation(input); },
    issueWriter: overrides.issueWriter || (async () => ({ commentUrl: "https://github.test/comment/1" })),
    now: overrides.now,
  });
  return { adapter, stateDir, executions: () => executions };
}

test("success creates a terminal receipt and writeback", async () => {
  const f = await fixture();
  const result = await f.adapter.submit(request());
  assert.equal(result.status, "SUCCESS");
  assert.equal(result.writeback, "POSTED");
});

test("default disabled mode is the rollback switch", async () => {
  const stateDir = await mkdtemp(path.join(os.tmpdir(), "mc126-"));
  const adapter = createProductionAdapter({ stateDir, executor: async () => ({}), issueWriter: async () => ({}) });
  await assert.rejects(adapter.submit(request()), /ADAPTER_DISABLED/);
});

test("policy, job ID and prompt validation fail before execution", async () => {
  const f = await fixture({ config: { maxPromptBytes: 8 } });
  await assert.rejects(f.adapter.submit({ ...request(), repository: "other/repo" }), { code: "POLICY_DENIED" });
  await assert.rejects(f.adapter.submit({ ...request(), issue: 125 }), { code: "POLICY_DENIED" });
  await assert.rejects(f.adapter.submit({ ...request(), jobId: "bad/job" }), /INVALID_JOB_ID/);
  await assert.rejects(f.adapter.submit({ ...request(), prompt: "" }), /INVALID_PROMPT/);
  await assert.rejects(f.adapter.submit({ ...request(), prompt: "123456789" }), /INVALID_PROMPT/);
  assert.equal(f.executions(), 0);
});

test("model allowlists are copied and frozen", async () => {
  assert.equal(Object.isFrozen(DEFAULT_ADAPTER_CONFIG.allowedModels), true);
  assert.throws(() => DEFAULT_ADAPTER_CONFIG.allowedModels.push("attacker-model"), TypeError);
  const callerModels = ["codex-auto-review"];
  const f = await fixture({ config: { allowedModels: callerModels } });
  callerModels.push("attacker-model");
  assert.equal(Object.isFrozen(f.adapter.config.allowedModels), true);
  assert.throws(() => f.adapter.config.allowedModels.push("other"), TypeError);
  await assert.rejects(f.adapter.submit({ ...request(), model: "attacker-model" }), /MODEL_UNSUPPORTED/);
});

test("unavailable CLI, missing result and non-PASS result retain explicit causes", async () => {
  const unavailable = await fixture({ executor: async () => ({ exitCode: -1, error: "ENOENT" }) });
  assert.match((await unavailable.adapter.submit(request("cli-down"))).failure_reason, /CODEX_UNAVAILABLE/);
  const missing = await fixture({ executor: async () => ({ exitCode: 0, result: null }) });
  assert.match((await missing.adapter.submit(request("missing-result"))).failure_reason, /INVALID_RESULT/);
  const nonPass = await fixture({ executor: async () => ({ exitCode: 0, result: { result: "FAIL" } }) });
  assert.match((await nonPass.adapter.submit(request("non-pass"))).failure_reason, /INVALID_RESULT/);
});

test("oversize result fails before persistence or publication", async () => {
  let writes = 0;
  const f = await fixture({
    config: { maxResultBytes: 64 },
    executor: async () => ({ exitCode: 0, result: { result: "PASS", detail: "x".repeat(100) } }),
    issueWriter: async () => { writes += 1; return {}; },
  });
  const result = await f.adapter.submit(request("large-result"));
  assert.match(result.failure_reason, /RESULT_TOO_LARGE/);
  assert.equal(result.result, null);
  assert.equal(writes, 0);
});

test("timeout aborts cooperatively and retry starts only after termination", async () => {
  let active = 0;
  let maxActive = 0;
  const f = await fixture({
    config: { timeoutMs: 5, terminationGraceMs: 50, maxAttempts: 2 },
    executor: async ({ signal }) => {
      active += 1;
      maxActive = Math.max(maxActive, active);
      await new Promise((_, reject) => signal.addEventListener("abort", () => setTimeout(() => { active -= 1; reject(signal.reason); }, 2), { once: true }));
    },
  });
  const result = await f.adapter.submit(request("timed-out"));
  assert.match(result.failure_reason, /EXECUTOR_TIMEOUT/);
  assert.equal(f.executions(), 2);
  assert.equal(maxActive, 1);
});

test("unconfirmed termination fails closed and suppresses retry", async () => {
  const f = await fixture({
    config: { timeoutMs: 5, terminationGraceMs: 5, maxAttempts: 2 },
    executor: async () => new Promise(() => {}),
  });
  const result = await f.adapter.submit(request("unconfirmed-stop"));
  assert.match(result.failure_reason, /EXECUTOR_TERMINATION_UNCONFIRMED/);
  assert.equal(f.executions(), 1);
});

test("failure output is redacted and capped by UTF-8 bytes", async () => {
  const f = await fixture({ config: { maxFailureBytes: 128 }, executor: async () => ({ exitCode: -1, stderr: `token=abc ${"界".repeat(1000)}` }) });
  const result = await f.adapter.submit(request("bounded-failure"));
  assert.ok(Buffer.byteLength(result.failure_reason, "utf8") <= 128);
  assert.match(result.failure_reason, /\[REDACTED\]/);
  assert.doesNotMatch(result.failure_reason, /token=abc/);
  assert.match(result.failure_reason, /\[TRUNCATED\]$/);
});

test("permission failure is recorded without losing execution receipt", async () => {
  const f = await fixture({ issueWriter: async () => { throw new Error("permission denied token=abc"); } });
  const result = await f.adapter.submit(request("write-denied"));
  assert.equal(result.status, "FAILED");
  assert.equal(result.writeback, "FAILED");
  assert.match(result.failure_reason, /GITHUB_WRITEBACK_FAILED/);
  assert.doesNotMatch(result.failure_reason, /token=abc/);
});

test("success result is recursively sanitized before persistence and writeback", async () => {
  let published;
  const f = await fixture({
    executor: async () => ({ exitCode: 0, result: { result: "PASS", password: "hunter2", nested: { note: "token=abc", api_key: "value", credential: "hidden" } } }),
    issueWriter: async (receipt) => { published = structuredClone(receipt); return {}; },
  });
  const result = await f.adapter.submit(request("sanitized-success"));
  const serialized = JSON.stringify({ result, published });
  assert.doesNotMatch(serialized, /hunter2|token=abc|"value"|hidden/);
  assert.match(serialized, /\[REDACTED\]/);
});

test("concurrent duplicate submissions are deterministic and execute once", async () => {
  let release;
  let startedResolve;
  const started = new Promise((resolve) => { startedResolve = resolve; });
  const gate = new Promise((resolve) => { release = resolve; });
  const f = await fixture({ executor: async () => { startedResolve(); await gate; return { exitCode: 0, result: { result: "PASS" } }; } });
  const first = f.adapter.submit(request("same-job"));
  await started;
  const duplicates = await Promise.all(Array.from({ length: 12 }, () => f.adapter.submit(request("same-job"))));
  release();
  const original = await first;
  assert.equal(original.status, "SUCCESS");
  assert.equal(f.executions(), 1);
  assert.equal(duplicates.every((item) => item.duplicate === true && item.job_id === "same-job"), true);
});

test("pre-start cancellation prevents execution", async () => {
  const f = await fixture();
  await f.adapter.cancel("cancel-me");
  const result = await f.adapter.submit(request("cancel-me"));
  assert.equal(result.status, "CANCELLED");
  assert.equal(f.executions(), 0);
});

test("post-start cancellation aborts the executor cooperatively", async () => {
  let startedResolve;
  const started = new Promise((resolve) => { startedResolve = resolve; });
  const f = await fixture({ executor: async ({ signal }) => {
    startedResolve();
    await new Promise((_, reject) => signal.addEventListener("abort", () => reject(signal.reason), { once: true }));
  } });
  const pending = f.adapter.submit(request("cancel-running"));
  await started;
  await f.adapter.cancel("cancel-running");
  const result = await pending;
  assert.equal(result.status, "CANCELLED");
  assert.equal(f.executions(), 1);
});

test("recovery isolates corrupt evidence and continues valid jobs", async () => {
  const f = await fixture({ now: () => "2026-10-19T00:00:00.000Z" });
  const jobs = path.join(f.stateDir, "jobs");
  await mkdir(jobs, { recursive: true });
  await writeFile(path.join(jobs, "corrupt.json"), "");
  await writeFile(path.join(jobs, "interrupted.json"), JSON.stringify({ job_id: "interrupted", status: "RUNNING" }));
  const outcome = await f.adapter.recover();
  assert.deepEqual(outcome, { recovered: ["interrupted"], corrupt: ["corrupt"] });
  const recovered = JSON.parse(await readFile(path.join(jobs, "interrupted.json"), "utf8"));
  const placeholder = JSON.parse(await readFile(path.join(jobs, "corrupt.json"), "utf8"));
  const names = await readdir(jobs);
  assert.match(recovered.failure_reason, /RECOVERY_REQUIRED/);
  assert.match(placeholder.failure_reason, /CORRUPT_RECEIPT/);
  assert.ok(names.some((name) => name.startsWith("corrupt.json.corrupt-")));
});

test("recovery turns an orphan claim into a terminal failure receipt", async () => {
  const f = await fixture();
  const locks = path.join(f.stateDir, "locks");
  await mkdir(locks, { recursive: true });
  await writeFile(path.join(locks, "orphan.lock"), "orphan\n");
  const outcome = await f.adapter.recover();
  assert.deepEqual(outcome, { recovered: ["orphan"], corrupt: [] });
  const receipt = JSON.parse(await readFile(path.join(f.stateDir, "jobs", "orphan.json"), "utf8"));
  assert.match(receipt.failure_reason, /claimed before receipt initialization/);
});

test("redaction and byte bounding helpers are deterministic", () => {
  assert.equal(redact("password=hunter2 token=abc"), "password=[REDACTED] token=[REDACTED]");
  assert.ok(Buffer.byteLength(boundText("界".repeat(100), 31), "utf8") <= 31);
  assert.equal(Buffer.byteLength(boundText("longer", 5), "utf8"), 5);
});
