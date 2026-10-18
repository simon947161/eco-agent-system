import assert from "node:assert/strict";
import test from "node:test";

import {
  POLICY,
  assertAllowed,
  buildIssueComment,
  buildPrompt,
  codexFailure,
  newJobId,
} from "../tools/mc_integration/mc-integration-runner.mjs";

test("policy permits only the registered Issue #126", () => {
  assert.doesNotThrow(() => assertAllowed({ repository: POLICY.allowedRepository, issue: 126 }));
  assert.throws(() => assertAllowed({ repository: POLICY.allowedRepository, issue: 124 }), /POLICY_DENIED/);
  assert.throws(() => assertAllowed({ repository: "example/other", issue: 126 }), /POLICY_DENIED/);
});
test("Codex model failures are preserved instead of masked by a missing result file", () => {
  const failure = codexFailure({ exitCode: 1, error: null, stderr: '{"error":{"message":"The model is not supported when using Codex with a ChatGPT account."}}' }, "RESULT_PARSE_FAILED");
  assert.match(failure, /^MODEL_UNSUPPORTED:/);
});

test("prompt fixes the read-only and Council boundaries", () => {
  const prompt = buildPrompt({ repository: POLICY.allowedRepository, issue: 126, issueTitle: "MC-INTEGRATION-001", expectedHead: "a".repeat(40), readmeSha256: "b".repeat(64), readmeFirstLine: "# Eco Agent System" });
  assert.match(prompt, /requested by KITTY/);
  assert.match(prompt, /read-only probe/);
  assert.match(prompt, /do not push, merge, deploy, access secrets, access Council systems/);
  assert.match(prompt, /Do not invoke tools or a shell/);
});

test("job IDs and comments expose evidence without claiming local paths are remote", () => {
  assert.match(newJobId(42, "abc123"), /^MC126-42-abc123$/);
  const comment = buildIssueComment({
    status: "SUCCESS", job_id: "MC126-42-abc123", codex_version: "0.142.5",
    sandbox: "read-only", repository: POLICY.allowedRepository, issue: 126,
    expected_head: "a".repeat(40), exit_code: 0, prompt_sha256: "b".repeat(64),
    result_sha256: "c".repeat(64), failure_reason: null,
    result: { observed_head: "a".repeat(40), read_file: "README.md" },
  });
  assert.match(comment, /KITTY invocation job/);
  assert.match(comment, /generated automatically/);
  assert.match(comment, /no local path is presented as remotely accessible evidence/);
  assert.doesNotMatch(comment, /C:\\/);
});
