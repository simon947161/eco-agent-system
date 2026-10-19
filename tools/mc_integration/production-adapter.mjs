import { mkdir, open, readFile, readdir, rename, unlink, writeFile } from "node:fs/promises";
import path from "node:path";

const DEFAULT_MODELS = Object.freeze(["codex-auto-review"]);
export const DEFAULT_ADAPTER_CONFIG = Object.freeze({
  enabled: false,
  repository: "simon947161/eco-agent-system",
  issue: 126,
  allowedModels: DEFAULT_MODELS,
  timeoutMs: 180_000,
  terminationGraceMs: 1_000,
  duplicateWaitMs: 1_000,
  maxAttempts: 1,
  maxPromptBytes: 32_768,
  maxResultBytes: 65_536,
  maxFailureBytes: 4_096,
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

export function boundText(value, maxBytes) {
  const text = redact(value);
  if (byteLength(text) <= maxBytes) return text;
  const suffix = "...[TRUNCATED]";
  if (maxBytes <= byteLength(suffix)) return suffix.slice(0, Math.max(0, maxBytes));
  const budget = Math.max(0, maxBytes - byteLength(suffix));
  let output = "";
  let used = 0;
  for (const character of text) {
    const size = byteLength(character);
    if (used + size > budget) break;
    output += character;
    used += size;
  }
  return `${output}${suffix}`;
}

function sanitizeResult(value) {
  if (typeof value === "string") return redact(value);
  if (Array.isArray(value)) return value.map(sanitizeResult);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [
      key,
      /(authorization|credential|token|password|secret|api[_-]?key|private[_-]?key)/i.test(key) ? "[REDACTED]" : sanitizeResult(item),
    ]));
  }
  return value;
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

async function sleep(ms) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForReceipt(file, waitMs) {
  const deadline = Date.now() + waitMs;
  let lastError;
  do {
    try { return await readJson(file); } catch (error) {
      lastError = error;
      if (error.code !== "ENOENT" && !(error instanceof SyntaxError)) throw error;
    }
    await sleep(5);
  } while (Date.now() < deadline);
  throw new AdapterError("IDEMPOTENCY_PENDING", `claimed job has no readable receipt: ${lastError?.message || "unknown"}`);
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

function abortError(signal) {
  return signal.reason instanceof AdapterError ? signal.reason : new AdapterError("CANCELLED");
}

async function executeBounded(executor, payload, { timeoutMs, terminationGraceMs, controller }) {
  const execution = Promise.resolve().then(() => executor({ ...payload, timeoutMs, signal: controller.signal }));
  let onAbort;
  const aborted = new Promise((_, reject) => {
    onAbort = () => reject(abortError(controller.signal));
    controller.signal.addEventListener("abort", onAbort, { once: true });
  });
  const timer = setTimeout(() => controller.abort(new AdapterError("EXECUTOR_TIMEOUT")), timeoutMs);
  try {
    return await Promise.race([execution, aborted]);
  } catch (error) {
    if (!controller.signal.aborted) throw error;
    const terminated = await Promise.race([
      execution.then(() => true, () => true),
      sleep(terminationGraceMs).then(() => false),
    ]);
    if (!terminated) throw new AdapterError("EXECUTOR_TERMINATION_UNCONFIRMED", "executor did not terminate after abort; retries disabled");
    throw abortError(controller.signal);
  } finally {
    clearTimeout(timer);
    controller.signal.removeEventListener("abort", onAbort);
  }
}

export function createProductionAdapter({ stateDir, executor, issueWriter, config = {}, now = () => new Date().toISOString() }) {
  if (!stateDir || typeof executor !== "function" || typeof issueWriter !== "function") {
    throw new TypeError("stateDir, executor and issueWriter are required");
  }
  const effective = Object.freeze({
    ...DEFAULT_ADAPTER_CONFIG,
    ...config,
    allowedModels: Object.freeze([...(config.allowedModels ?? DEFAULT_ADAPTER_CONFIG.allowedModels)]),
  });
  const jobsDir = path.join(stateDir, "jobs");
  const locksDir = path.join(stateDir, "locks");
  const cancelDir = path.join(stateDir, "cancel");
  const activeControllers = new Map();
  const jobFile = (jobId) => path.join(jobsDir, `${jobId}.json`);
  const lockFile = (jobId) => path.join(locksDir, `${jobId}.lock`);
  const cancelFile = (jobId) => path.join(cancelDir, `${jobId}.cancel`);
  const failure = (code, message) => boundText(`${code}: ${message}`, effective.maxFailureBytes);

  async function initialize() {
    await mkdir(jobsDir, { recursive: true });
    await mkdir(locksDir, { recursive: true });
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
    activeControllers.get(jobId)?.abort(new AdapterError("CANCELLED"));
    return { job_id: jobId, cancellation_requested: true };
  }

  async function submit(request) {
    validateRequest(request, effective);
    await initialize();
    const file = jobFile(request.jobId);
    try { return { ...(await readJson(file)), duplicate: true }; } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    let lock;
    try {
      lock = await open(lockFile(request.jobId), "wx");
      await lock.writeFile(`${request.jobId}\n`, "utf8");
      await lock.close();
    } catch (error) {
      await lock?.close().catch(() => {});
      if (error.code === "EEXIST") return { ...(await waitForReceipt(file, effective.duplicateWaitMs)), duplicate: true };
      throw error;
    }
    try { return { ...(await readJson(file)), duplicate: true }; } catch (error) {
      if (error.code !== "ENOENT") throw error;
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
    await atomicJson(file, base);
    let receipt = base;
    try {
      if (await isCancelled(request.jobId)) throw new AdapterError("CANCELLED");
      let execution;
      for (let attempt = 1; attempt <= effective.maxAttempts; attempt += 1) {
        if (await isCancelled(request.jobId)) throw new AdapterError("CANCELLED");
        receipt.attempts = attempt;
        await atomicJson(file, receipt);
        const controller = new AbortController();
        activeControllers.set(request.jobId, controller);
        try {
          execution = await executeBounded(executor, request, { timeoutMs: effective.timeoutMs, terminationGraceMs: effective.terminationGraceMs, controller });
          break;
        } catch (error) {
          if (["CANCELLED", "EXECUTOR_TERMINATION_UNCONFIRMED"].includes(error.code) || attempt === effective.maxAttempts) throw error;
        } finally {
          if (activeControllers.get(request.jobId) === controller) activeControllers.delete(request.jobId);
        }
      }
      if (await isCancelled(request.jobId)) throw new AdapterError("CANCELLED");
      if (!execution || execution.exitCode !== 0) throw new AdapterError("CODEX_UNAVAILABLE", execution?.error || execution?.stderr || "Codex CLI unavailable");
      if (!execution.result || execution.result.result !== "PASS") throw new AdapterError("INVALID_RESULT", "Codex returned no valid PASS result");
      const sanitized = sanitizeResult(execution.result);
      if (byteLength(sanitized) > effective.maxResultBytes) throw new AdapterError("RESULT_TOO_LARGE");
      receipt = { ...receipt, status: "SUCCESS", result: sanitized, finished_at: now() };
      await atomicJson(file, receipt);
      try {
        const writeback = await issueWriter(receipt);
        receipt.writeback = "POSTED";
        receipt.comment_url = writeback?.commentUrl || null;
      } catch (error) {
        receipt.status = "FAILED";
        receipt.writeback = "FAILED";
        receipt.failure_reason = failure("GITHUB_WRITEBACK_FAILED", error.message);
      }
    } catch (error) {
      const code = error instanceof AdapterError ? error.code : "ADAPTER_FAILURE";
      receipt = { ...receipt, status: code === "CANCELLED" ? "CANCELLED" : "FAILED", failure_reason: failure(code, error.message), finished_at: now() };
    }
    await atomicJson(file, receipt);
    return receipt;
  }

  async function recover() {
    await initialize();
    const outcome = { recovered: [], corrupt: [] };
    for (const name of await readdir(jobsDir)) {
      if (!name.endsWith(".json")) continue;
      const file = path.join(jobsDir, name);
      try {
        const receipt = await readJson(file);
        if (receipt.status !== "RUNNING") continue;
        const next = { ...receipt, status: "FAILED", failure_reason: failure("RECOVERY_REQUIRED", "interrupted before terminal receipt"), finished_at: now() };
        await atomicJson(file, next);
        outcome.recovered.push(next.job_id);
      } catch (error) {
        const jobId = name.slice(0, -5);
        const suffix = now().replace(/[^0-9A-Za-z.-]/g, "-");
        const preserved = `${file}.corrupt-${suffix}`;
        try {
          await rename(file, preserved);
          await atomicJson(file, {
            schema: "kitty-codex-adapter-receipt/v1",
            job_id: jobId,
            status: "FAILED",
            result: null,
            failure_reason: failure("CORRUPT_RECEIPT", error.message),
            corrupt_evidence: path.basename(preserved),
            finished_at: now(),
            writeback: "NOT_ATTEMPTED",
          });
          outcome.corrupt.push(jobId);
        } catch (preserveError) {
          outcome.corrupt.push(`${jobId}:PRESERVE_FAILED:${boundText(preserveError.message, 256)}`);
        }
      }
    }
    for (const name of await readdir(locksDir)) {
      if (!name.endsWith(".lock")) continue;
      const jobId = name.slice(0, -5);
      const file = jobFile(jobId);
      try { await readFile(file); } catch (error) {
        if (error.code !== "ENOENT") continue;
        await atomicJson(file, {
          schema: "kitty-codex-adapter-receipt/v1",
          job_id: jobId,
          status: "FAILED",
          result: null,
          failure_reason: failure("RECOVERY_REQUIRED", "job was claimed before receipt initialization"),
          finished_at: now(),
          writeback: "NOT_ATTEMPTED",
        });
        outcome.recovered.push(jobId);
      }
    }
    return outcome;
  }

  return { config: effective, initialize, submit, cancel, recover };
}
