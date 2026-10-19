import assert from "node:assert/strict";
import test from "node:test";

import {
  classifyGitHubAccess,
  decideEvidenceRoute,
  hasGitHubEvidenceIntent,
} from "../tools/mc_integration/kitty-evidence-routing.mjs";

test("reproduces the shorthand Issue request without falling back to public search", () => {
  const message = "读取 GitHub Issue #126 最新复审任务 comment 6262500930，对固定提交 269e06960e5cf81cc5d75aac906343a8c8d82b3e 的七份文件复审";
  const decision = decideEvidenceRoute({ message, needsResearch: true, githubReads: [] });
  assert.equal(hasGitHubEvidenceIntent(message), true);
  assert.deepEqual(decision, {
    intent: true,
    status: "TOOL_UNAVAILABLE",
    reason: "NO_CANONICAL_TARGET_PARSED",
    allowPublicResearch: false,
    ignoredPublicSearchResultCount: 0,
  });
});

test("fresh pinned file read is ACCESS_CONFIRMED", () => {
  const decision = decideEvidenceRoute({
    message: "Read https://github.com/simon947161/eco-agent-system/blob/269e06960e5cf81cc5d75aac906343a8c8d82b3e/tools/mc_integration/production-adapter.mjs",
    needsResearch: true,
    githubReads: [{ status: "FOUND_AND_READ", ok: true, commit_sha: "269e06960e5cf81cc5d75aac906343a8c8d82b3e" }],
  });
  assert.equal(decision.status, "ACCESS_CONFIRMED");
  assert.equal(decision.allowPublicResearch, false);
});

test("existing-session canonical issue result is ACCESS_CONFIRMED", () => {
  const access = classifyGitHubAccess({
    message: "继续检查 simon947161/eco-agent-system Issue #126",
    githubReads: [{ type: "SUCCESS", ok: true, number: 126 }],
  });
  assert.equal(access.status, "ACCESS_CONFIRMED");
});

test("canonical reader failure is ACCESS_BLOCKED and remains explicit", () => {
  const decision = decideEvidenceRoute({
    message: "Read pinned repo/ref/path from GitHub",
    needsResearch: true,
    githubReads: [{ status: "NOT_ALLOWLISTED", ok: false }],
  });
  assert.equal(decision.status, "ACCESS_BLOCKED");
  assert.equal(decision.reason, "NOT_ALLOWLISTED");
  assert.equal(decision.allowPublicResearch, false);
});

test("missing canonical reader is TOOL_UNAVAILABLE", () => {
  const decision = decideEvidenceRoute({
    message: "Use /api/github/evidence to read commit 269e06960e5cf81cc5d75aac906343a8c8d82b3e",
    readerAvailable: false,
  });
  assert.equal(decision.status, "TOOL_UNAVAILABLE");
  assert.equal(decision.reason, "CANONICAL_READER_UNAVAILABLE");
});

test("public search results never prove or disprove GitHub access", () => {
  const decision = decideEvidenceRoute({
    message: "Read GitHub Issue #126",
    needsResearch: true,
    githubReads: [],
    publicSearchResults: ["zero relevant hits"],
  });
  assert.equal(decision.status, "TOOL_UNAVAILABLE");
  assert.equal(decision.allowPublicResearch, false);
  assert.equal(decision.ignoredPublicSearchResultCount, 1);
});

test("ordinary current-information questions may still use public research", () => {
  const decision = decideEvidenceRoute({
    message: "请核查 DeepSeek Harness 最新官方版本",
    needsResearch: true,
  });
  assert.equal(decision.intent, false);
  assert.equal(decision.allowPublicResearch, true);
});

