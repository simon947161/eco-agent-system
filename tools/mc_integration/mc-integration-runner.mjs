#!/usr/bin/env node

import { spawn } from "node:child_process";
import { createHash, randomBytes } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath, pathToFileURL } from "node:url";

export const POLICY = Object.freeze({
  actor: "KITTY",
  allowedRepository: "simon947161/eco-agent-system",
  allowedIssue: 126,
  sandbox: "read-only",
  prohibited: ["push", "merge", "deploy", "secret-read", "council-access", "public-listener"],
});

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}
function stamp() {
  return new Date().toISOString().replace(/[:.]/g, "-");
}

export function newJobId(now = Date.now(), entropy = randomBytes(3).toString("hex")) {
  return `MC126-${now}-${entropy}`;
}

export function assertAllowed({ repository, issue }) {
  if (repository !== POLICY.allowedRepository || Number(issue) !== POLICY.allowedIssue) {
    throw new Error(`POLICY_DENIED: only ${POLICY.allowedRepository}#${POLICY.allowedIssue} is allowed`);
  }
}

export function buildPrompt({ repository, issue, issueTitle, expectedHead, readmeSha256, readmeFirstLine }) {
  return [
    `You are Codex executing the bounded verification task ${repository}#${issue}, requested by KITTY.`,
    `Issue title: ${issueTitle}`,
    "KITTY's host adapter already performed the authorized read-only precheck and supplies its evidence below.",
    `Repository identity: ${repository}`,
    `Observed local HEAD: ${expectedHead}`,
    `README.md SHA-256: ${readmeSha256}`,
    `README.md first line: ${JSON.stringify(readmeFirstLine)}`,
    "This is a read-only probe. Do not edit files, do not create commits, do not push, merge, deploy, access secrets, access Council systems, or start a listener.",
    "Do not invoke tools or a shell. Validate only the supplied evidence and return JSON matching the supplied schema.",
    `Set result to PASS, observed_repo to ${JSON.stringify(repository)}, observed_head to the supplied HEAD, and read_file to README.md only when the HEAD is a 40-character lowercase hex value, the README hash is a 64-character lowercase hex value, and the first line is non-empty.`,
  ].join("\n");
}

export function buildIssueComment(receipt) {
  const status = receipt.status === "SUCCESS" ? "PASS" : "FAIL";
  const result = receipt.result || {};
  return [
    `### MC-INTEGRATION-001 minimal E2E — ${status}`,
    "",
    `- KITTY invocation job: \`${receipt.job_id}\``,
    `- Executor: \`Codex CLI ${receipt.codex_version || "UNKNOWN"}\``,
    `- Model: \`${receipt.model || "UNKNOWN"}\``,
    `- Safety mode: \`${receipt.sandbox}\`, ephemeral session; no push, merge, deployment, secret read, public listener, or Council access`,
    `- Repository/Issue: \`${receipt.repository}#${receipt.issue}\``,
    `- Baseline HEAD: \`${receipt.expected_head}\``,
    `- Codex observed HEAD: \`${result.observed_head || "NOT_RETURNED"}\``,
    `- Checked file: \`${result.read_file || "NOT_RETURNED"}\``,
    `- Input mode: \`${receipt.input_mode || "UNKNOWN"}\``,
    `- Exit code: \`${receipt.exit_code}\``,
    `- Prompt SHA-256: \`${receipt.prompt_sha256}\``,
    `- Result SHA-256: \`${receipt.result_sha256 || "NONE"}\``,
    `- Failure reason: ${receipt.failure_reason ? `\`${receipt.failure_reason}\`` : "none"}`,
    "",
    receipt.status === "SUCCESS"
      ? "Verified: KITTY invoked Codex without Simon relaying the prompt; Codex returned a durable, machine-readable result; this comment was generated automatically from that receipt."
      : "Blocked: the adapter preserved the failure reason and generated this comment automatically from the failed receipt.",
    "",
    "Local-only evidence remains on the authorized host; no local path is presented as remotely accessible evidence.",
  ].join("\n");
}

function run(command, args, { cwd, input = null, env = process.env, timeoutMs = 180000 } = {}) {
  return new Promise((resolve) => {
    const child = spawn(command, args, { cwd, env, windowsHide: true, stdio: ["pipe", "pipe", "pipe"] });
    let stdout = "";
    let stderr = "";
    let timedOut = false;
    const timer = setTimeout(() => {
      timedOut = true;
      child.kill();
    }, timeoutMs);
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", (error) => {
      clearTimeout(timer);
      resolve({ exitCode: -1, stdout, stderr, error: error.message, timedOut });
    });
    child.on("close", (code) => {
      clearTimeout(timer);
      resolve({ exitCode: timedOut ? -1 : code, stdout, stderr, error: timedOut ? "TIMEOUT" : null, timedOut });
    });
    if (input !== null) child.stdin.end(input);
    else child.stdin.end();
  });
}

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    if (key === "--writeback") out.writeback = true;
    else out[key.slice(2)] = argv[++i];
  }
  return out;
}

export function codexFailure(run, parseFailure = null) {
  if (run.error) return run.error;
  const unsupported = String(run.stderr || "").match(/message":"([^"]*model is not supported[^"]*)"/i);
  if (unsupported) return `MODEL_UNSUPPORTED: ${unsupported[1]}`;
  const errorLine = String(run.stderr || "").split(/\r?\n/).find((line) => /\bERROR\b|invalid_request_error/i.test(line));
  if (errorLine) return `CODEX_ERROR: ${errorLine.slice(0, 500)}`;
  return parseFailure || `CODEX_EXIT_${run.exitCode}`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const repository = args.repository || POLICY.allowedRepository;
  const issue = Number(args.issue || POLICY.allowedIssue);
  const workspace = path.resolve(args.workspace || process.cwd());
  const evidenceRoot = path.resolve(args["evidence-dir"] || path.join(workspace, ".mc-integration-evidence"));
  const codexBin = args.codex || process.env.CODEX_BIN || "codex";
  const ghBin = args.gh || process.env.GH_BIN || "gh";
  const model = args.model || "codex-auto-review";
  assertAllowed({ repository, issue });

  const jobId = args["job-id"] || newJobId();
  const jobDir = path.join(evidenceRoot, jobId);
  await mkdir(evidenceRoot, { recursive: true });
  await mkdir(jobDir, { recursive: false });
  const receiptPath = path.join(jobDir, "receipt.json");
  const resultPath = path.join(jobDir, "codex-result.json");
  const stdoutPath = path.join(jobDir, "codex-events.jsonl");
  const stderrPath = path.join(jobDir, "codex-stderr.log");
  const commentPath = path.join(jobDir, "issue-comment.md");

  const versionRun = await run(codexBin, ["--version"], { cwd: workspace, timeoutMs: 10000 });
  const codexVersion = versionRun.exitCode === 0 ? versionRun.stdout.trim().replace(/^codex-cli\s+/, "") : null;
  const issueRun = await run(ghBin, ["api", `repos/${repository}/issues/${issue}`], { cwd: workspace, timeoutMs: 30000 });
  const headRun = await run("git", ["rev-parse", "HEAD"], { cwd: workspace, timeoutMs: 10000 });
  if (issueRun.exitCode !== 0) throw new Error(`ISSUE_READ_FAILED: ${issueRun.stderr.trim() || issueRun.error || issueRun.exitCode}`);
  if (headRun.exitCode !== 0) throw new Error(`HEAD_READ_FAILED: ${headRun.stderr.trim() || headRun.error || headRun.exitCode}`);
  const issueRecord = JSON.parse(issueRun.stdout);
  const expectedHead = headRun.stdout.trim();
  const readmeText = await readFile(path.join(workspace, "README.md"), "utf8");
  const readmeSha256 = sha256(readmeText);
  const readmeFirstLine = readmeText.split(/\r?\n/, 1)[0].trim();
  const prompt = buildPrompt({ repository, issue, issueTitle: issueRecord.title, expectedHead, readmeSha256, readmeFirstLine });

  const startedAt = new Date().toISOString();
  const codexRun = await run(codexBin, [
    "exec", "--ephemeral", "--model", model, "--sandbox", POLICY.sandbox, "--color", "never", "--json",
    "--output-schema", path.join(path.dirname(fileURLToPath(import.meta.url)), "probe.schema.json"),
    "--output-last-message", resultPath, "--cd", workspace, "-",
  ], { cwd: workspace, input: prompt, timeoutMs: Number(args.timeout || 180000) });
  await writeFile(stdoutPath, codexRun.stdout, "utf8");
  await writeFile(stderrPath, codexRun.stderr, "utf8");

  let result = null;
  let parseFailure = null;
  try { result = JSON.parse(await readFile(resultPath, "utf8")); }
  catch (error) { parseFailure = `RESULT_PARSE_FAILED: ${error.message}`; }
  const success = codexRun.exitCode === 0 && result?.result === "PASS" && result?.observed_repo === repository && result?.observed_head === expectedHead && result?.read_file === "README.md";
  const failureReason = success ? null : (result?.reason || codexFailure(codexRun, parseFailure));
  const resultText = result ? JSON.stringify(result) : "";
  const receipt = {
    schema: "mc-integration-receipt/v1",
    job_id: jobId,
    actor: POLICY.actor,
    repository,
    issue,
    issue_url: issueRecord.html_url,
    issue_title: issueRecord.title,
    workspace,
    expected_head: expectedHead,
    input_mode: "KITTY_HOST_READ_ONLY_PRECHECK",
    input_evidence: { readme_sha256: readmeSha256, readme_first_line: readmeFirstLine },
    sandbox: POLICY.sandbox,
    ephemeral: true,
    codex_version: codexVersion,
    model,
    started_at: startedAt,
    finished_at: new Date().toISOString(),
    status: success ? "SUCCESS" : "FAILED",
    exit_code: codexRun.exitCode,
    prompt_sha256: sha256(prompt),
    result_sha256: resultText ? sha256(resultText) : null,
    result,
    failure_reason: failureReason,
    prohibited_actions_observed: [],
    local_evidence: { receipt: receiptPath, result: resultPath, events: stdoutPath, stderr: stderrPath, comment: commentPath },
    github_writeback: { requested: Boolean(args.writeback), status: "NOT_ATTEMPTED", comment_url: null, failure_reason: null },
  };
  const comment = buildIssueComment(receipt);
  await writeFile(commentPath, comment + "\n", "utf8");

  if (args.writeback) {
    const post = await run(ghBin, ["api", `repos/${repository}/issues/${issue}/comments`, "-f", `body=${comment}`], { cwd: workspace, timeoutMs: 30000 });
    if (post.exitCode === 0) {
      const posted = JSON.parse(post.stdout);
      receipt.github_writeback = { requested: true, status: "POSTED", comment_url: posted.html_url, failure_reason: null };
    } else {
      receipt.github_writeback = { requested: true, status: "FAILED", comment_url: null, failure_reason: post.stderr.trim() || post.error || `GH_EXIT_${post.exitCode}` };
    }
  }
  await writeFile(receiptPath, JSON.stringify(receipt, null, 2) + "\n", "utf8");
  process.stdout.write(JSON.stringify({ job_id: jobId, status: receipt.status, receipt: receiptPath, github_writeback: receipt.github_writeback }) + "\n");
  process.exitCode = success && (!args.writeback || receipt.github_writeback.status === "POSTED") ? 0 : 1;
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().catch((error) => {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  });
}
