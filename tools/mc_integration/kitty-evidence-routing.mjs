// Isolated reference implementation for MC-INTEGRATION-001.
//
// This module is intentionally not wired into the production KITTY service. It
// makes the evidence-routing rule deterministic so it can be reviewed and tested
// before a separately approved production change.

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

export function hasGitHubEvidenceIntent(message) {
  const text = String(message || "");
  return /github|issue\s*#?\d+|comment\s*\d+|commit\s+[0-9a-f]{7,40}|[0-9a-f]{40}|\/api\/github\/evidence|github\.com\/[^\s]+\/(?:issues|blob)\//i.test(text);
}

export function classifyGitHubAccess({
  message,
  githubReads = [],
  readerAvailable = true,
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
    reason: readerAvailable ? "NO_CANONICAL_TARGET_PARSED" : "CANONICAL_READER_UNAVAILABLE",
  };
}

export function decideEvidenceRoute({
  message,
  needsResearch = false,
  githubReads = [],
  readerAvailable = true,
  publicSearchResults = [],
} = {}) {
  const access = classifyGitHubAccess({ message, githubReads, readerAvailable });

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

