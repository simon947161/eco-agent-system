// Production-candidate evidence routing for MC-INTEGRATION-001.
// Kept in the isolated staging branch until a separately approved deployment.

const SUCCESS = new Set(["SUCCESS", "FOUND_AND_READ", "ACCESS_CONFIRMED"]);
const BLOCKED = new Set([
  "AUTH_REQUIRED",
  "NOT_FOUND",
  "NOT_READABLE",
  "NOT_ALLOWLISTED",
  "UNVERIFIED_CONTENT",
  "404",
  "RATE_LIMIT",
  "NETWORK_ERROR",
  "ACCESS_BLOCKED",
]);

export function resolveAuthorizedRepoBinding({
  requestBinding = null,
  configuredBinding = null,
  isAllowlisted = () => false,
} = {}) {
  const candidates = [
    { value: requestBinding, source: "REQUEST" },
    { value: configuredBinding, source: "CONFIG" },
  ];
  for (const candidate of candidates) {
    const repo = String(candidate.value || "").trim();
    if (!repo) continue;
    if (!/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(repo)) {
      return { repo: null, source: candidate.source, reason: "INVALID_REPOSITORY_BINDING" };
    }
    if (!isAllowlisted(repo)) {
      return { repo: null, source: candidate.source, reason: "REPOSITORY_BINDING_NOT_ALLOWLISTED" };
    }
    return { repo, source: candidate.source, reason: "AUTHORIZED_REPOSITORY_BINDING" };
  }
  return { repo: null, source: "NONE", reason: "MISSING_AUTHORIZED_REPOSITORY_BINDING" };
}

export function hasGitHubEvidenceIntent(message) {
  const text = String(message || "");
  return /github\.com\/[^\s]+\/(?:issues|blob)\/|\/api\/github\/evidence|issue\s*#?\d+|comment\s*\d+|commit\s+[0-9a-f]{7,40}|[0-9a-f]{40}|github[^\n]{0,80}(?:issue|comment|commit|file|repo|仓库|文件|证据)/i.test(text);
}

export function classifyGitHubAccess({
  message,
  githubReads = [],
  readerAvailable = true,
  targetCount = 0,
  missingTargetReason = "NO_CANONICAL_TARGET_PARSED",
} = {}) {
  const intent = hasGitHubEvidenceIntent(message);
  if (!intent) {
    return { intent: false, status: null, reason: "NO_GITHUB_EVIDENCE_INTENT" };
  }

  const reads = Array.isArray(githubReads) ? githubReads : [];
  const statusOf = (read) => String(read?.status || read?.type || "").toUpperCase();
  const confirmed = reads.find((read) => read?.ok === true || SUCCESS.has(statusOf(read)));
  if (confirmed) {
    return { intent: true, status: "ACCESS_CONFIRMED", reason: "CANONICAL_READER_RETURNED_CONTENT" };
  }

  const blocked = reads.find((read) => read?.ok === false || BLOCKED.has(statusOf(read)));
  if (blocked) {
    return {
      intent: true,
      status: "ACCESS_BLOCKED",
      reason: statusOf(blocked) || "CANONICAL_READER_FAILED",
    };
  }

  return {
    intent: true,
    status: "TOOL_UNAVAILABLE",
    reason: !readerAvailable
      ? "CANONICAL_READER_UNAVAILABLE"
      : targetCount > 0
      ? "CANONICAL_READER_RETURNED_NO_RESULT"
      : missingTargetReason,
  };
}

export function decideEvidenceRoute({
  message,
  needsResearch = false,
  githubReads = [],
  readerAvailable = true,
  targetCount = 0,
  missingTargetReason = "NO_CANONICAL_TARGET_PARSED",
  publicSearchResults = [],
} = {}) {
  const access = classifyGitHubAccess({ message, githubReads, readerAvailable, targetCount, missingTargetReason });

  // Public search is neither an access probe nor evidence for repository bytes.
  // It must not run as a fallback for GitHub evidence intent, and its results must
  // never change the canonical reader's access classification.
  const allowPublicResearch = Boolean(needsResearch) && !access.intent;
  return {
    ...access,
    allowPublicResearch,
    ignoredPublicSearchResultCount: access.intent && Array.isArray(publicSearchResults)
      ? publicSearchResults.length
      : 0,
  };
}

export function safeRouteTelemetry(decision, {
  bindingSource = "NONE",
  issueTargetCount = 0,
  fileTargetCount = 0,
  githubReads = [],
} = {}) {
  return {
    intent: Boolean(decision?.intent),
    status: decision?.status || null,
    reason: decision?.reason || null,
    bindingSource,
    issueTargetCount,
    fileTargetCount,
    readStatuses: (Array.isArray(githubReads) ? githubReads : [])
      .slice(0, 8)
      .map((read) => String(read?.status || read?.type || (read?.ok ? "SUCCESS" : "UNKNOWN")).slice(0, 48)),
    publicResearchAllowed: Boolean(decision?.allowPublicResearch),
  };
}

export function formatAccessDecisionForPrompt(decision) {
  if (!decision?.intent || decision.status === "ACCESS_CONFIRMED") return "";
  return [
    "## GitHub 证据路由结果（不是网页搜索结果）",
    `status: ${decision.status}`,
    `reason: ${decision.reason}`,
    "规则：公开网页搜索不能证明 GitHub issue 或文件可访问或不可访问。没有 canonical reader 原文时，不得声称已读取，也不得用搜索零命中补足。",
  ].join("\n");
}

