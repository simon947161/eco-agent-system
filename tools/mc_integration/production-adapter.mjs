import { mkdir, open, readFile, readdir, rename, unlink, writeFile } from "node:fs/promises";
import path from "node:path";

export const DEFAULT_ADAPTER_CONFIG = Object.freeze({
  enabled: false,
  repository: "simon947161/eco-agent-system",
  issue: 126,
  allowedModels: ["codex-auto-review"],
  timeoutMs: 180_000,
  maxAttempts: 1,
  maxPromptBytes: 32_768,
  maxResultBytes: 65_536,
});

export class AdapterError extends Error {
  constructor(code, message = code) {
    super(message);
    this.name = "AdapterError";
    this.code = code;
  }
}

export function redact(value) {
  return String(value ?? "")
    .replace(/(authorization|token|password|secret|api[_-]?key)\s*[:=]\s*[^\s,;]+/gi, "$1=[REDACTED]")
    .replace(/gh[pousr]_[A-Za-z0-9_]{20,}/g, "[REDACTED_GITHUB_TOKEN]")
    .replace(/sk-[A-Za-z0-9_-]{20,}/g, "[REDACTED_API_KEY]");
}

function byteLength(value) {
  return Buffer.byteLength(typeof value === "string" ? value : JSON.stringify(value), "utf8");
}

async function atomicJson(file, value) {
  const temp = `${file}.${process.pid}.tmp`;
  const previous = `${file}.previous`;
  await writeFile(temp, `${JSON.stringify(value, null, 2)}\n`, "utf8");
  try { await rename(file, previous); } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  await rename(temp, file);
  await unlink(previous).catch((error) => {
    if (error.code !== "ENOENT") throw error;
  });
}

async function readJson(file) {
  return JSON.parse(await readFile(file, "utf8"));
}

function validateRequest(request, config) {
  if (!config.enabled) throw new AdapterError("ADAPTER_DISABLED");
  if (request.repository !== config.repository || Number(request.issue) !== config.issue) {
    throw new AdapterError("POLICY_DENIED", "repository or issue is outside the allowlist");
  }
  if (!config.allowedModels.includes(request.model)) throw new AdapterError("MODEL_UNSUPPORTED");
  if (!/^[A-Za-z0-9._-]{1,100}$/.test(request.jobId || "")) throw new AdapterError("INVALID_JOB_ID");
  if (!request.prompt || byteLength(request.prompt) > config.maxPromptBytes) throw new AdapterError("INVALID_PROMPT");
}

function withTimeout(promise, timeoutMs) {
  let timer;
  return Promise.race([
    promise,
    new Promise((_, reject) => { timer = setTimeout(() => reject(new AdapterError("EXECUTOR_TIMEOUT")), timeoutMs); }),
  ]).finally(() => clearTimeout(timer));
}

export function createProductionAdapter({ stateDir, executor, issueWriter, config = {}, now = () => new Date().toISOString() }) {
  if (!stateDir || typeof executor !== "function" || typeof issueWriter !== "function") {
    throw new TypeError("stateDir, executor and issueWriter are required");
  }
  const effective = { ...DEFAULT_ADAPTER_CONFIG, ...config };
  const jobsDir = path.join(stateDir, "jobs");
  const cancelDir = path.join(stateDir, "cancel");
  const jobFile = (jobId) => path.join(jobsDir, `${jobId}.json`);
  const cancelFile = (jobId) => path.join(cancelDir, `${jobId}.cancel`);

  async function initialize() {
    await mkdir(jobsDir, { recursive: true });
    await mkdir(cancelDir, { recursive: true });
  }

  async function isCancelled(jobId) {
    try { await readFile(cancelFile(jobId)); return true; } catch (error) {
      if (error.code === "ENOENT") return false;
      throw error;
    }
  }

  async function cancel(jobId) {
    await initialize();
    await writeFile(cancelFile(jobId), "cancelled\n", { flag: "wx" }).catch((error) => {
      if (error.code !== "EEXIST") throw error;
    });
    return { job_id: jobId, cancellation_requested: true };
  }

  async function submit(request) {
    validateRequest(request, effective);
    await initialize();
    const file = jobFile(request.jobId);
    let lock;
    try { lock = await open(file, "wx"); } catch (error) {
      if (error.code === "EEXIST") return { ...(await readJson(file)), duplicate: true };
      throw error;
    }
    const base = {
      schema: "kitty-codex-adapter-receipt/v1",
      job_id: request.jobId,
      repository: request.repository,
      issue: Number(request.issue),
      model: request.model,
      status: "RUNNING",
      attempts: 0,
      started_at: now(),
      finished_at: null,
      result: null,
      failure_reason: null,
      writeback: "NOT_ATTEMPTED",
    };
    await lock.writeFile(`${JSON.stringify(base, null, 2)}\n`, "utf8");
    await lock.close();
    let receipt = base;
    try {
      if (await isCancelled(request.jobId)) throw new AdapterError("CANCELLED");
      let execution;
      for (let attempt = 1; attempt <= effective.maxAttempts; attempt += 1) {
        receipt.attempts = attempt;
        await atomicJson(file, receipt);
        try {
          execution = await withTimeout(Promise.resolve(executor({ ...request, timeoutMs: effective.timeoutMs })), effective.timeoutMs);
          break;
        } catch (error) {
          if (attempt === effective.maxAttempts) throw error;
        }
      }
      if (await isCancelled(request.jobId)) throw new AdapterError("CANCELLED");
      if (!execution || execution.exitCode !== 0) throw new AdapterError("CODEX_UNAVAILABLE", redact(execution?.error || execution?.stderr || "Codex CLI unavailable"));
      if (!execution.result || execution.result.result !== "PASS") throw new AdapterError("INVALID_RESULT", "Codex returned no valid PASS result");
      if (byteLength(execution.result) > effective.maxResultBytes) throw new AdapterError("RESULT_TOO_LARGE");
      receipt = { ...receipt, status: "SUCCESS", result: execution.result, finished_at: now() };
      await atomicJson(file, receipt);
      try {
        const writeback = await issueWriter(receipt);
        receipt.writeback = "POSTED";
        receipt.comment_url = writeback?.commentUrl || null;
      } catch (error) {
        receipt.status = "FAILED";
        receipt.writeback = "FAILED";
        receipt.failure_reason = `GITHUB_WRITEBACK_FAILED: ${redact(error.message)}`;
      }
    } catch (error) {
      const code = error instanceof AdapterError ? error.code : "ADAPTER_FAILURE";
      receipt = { ...receipt, status: code === "CANCELLED" ? "CANCELLED" : "FAILED", failure_reason: `${code}: ${redact(error.message)}`, finished_at: now() };
    }
    await atomicJson(file, receipt);
    return receipt;
  }

  async function recover() {
    await initialize();
    const recovered = [];
    for (const name of await readdir(jobsDir)) {
      if (!name.endsWith(".json")) continue;
      const file = path.join(jobsDir, name);
      const receipt = await readJson(file);
      if (receipt.status !== "RUNNING") continue;
      const next = { ...receipt, status: "FAILED", failure_reason: "RECOVERY_REQUIRED: interrupted before terminal receipt", finished_at: now() };
      await atomicJson(file, next);
      recovered.push(next.job_id);
    }
    return recovered;
  }

  return { config: effective, initialize, submit, cancel, recover };
}
