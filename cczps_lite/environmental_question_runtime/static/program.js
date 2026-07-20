const PROGRAM = "COOMA-WATER-FIRE-WASTEWATER-WATCH";
const REVIEWED_STATES = new Set([
  "CYCLE_REVIEWED_ACCEPTED_AS_RESEARCH_RECORD",
  "CYCLE_REVIEWED_QUESTIONED",
  "CYCLE_REVIEWED_REVISION_REQUIRED",
  "CYCLE_REVIEWED_REJECTED",
]);
let program = null;
let cycle = null;

const $ = id => document.getElementById(id);
const esc = value => String(value ?? "").replace(/[&<>"']/g, char => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
}[char]));

async function get(path) {
  const response = await fetch(path);
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || data.error);
  return data;
}

async function post(path, body) {
  const response = await fetch(path, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || data.error);
  return data;
}

function fail(error) {
  $("error").textContent = error.message;
  $("error").style.display = "block";
  setTimeout(() => $("error").style.display = "none", 7000);
}

function kv(items) {
  return `<div class="kv">${items.map(([key, value]) => `<b>${esc(key)}</b><span>${esc(value)}</span>`).join("")}</div>`;
}

function applyRefreshGate(state) {
  const inProgress = state === "REFRESH_IN_PROGRESS";
  const retry = state === "REFRESH_INTERRUPTED_RETRY_ALLOWED";
  const complete = state === "COMPLETE_ATOMIC_SET";
  $("refresh").disabled = inProgress || complete;
  $("compile").disabled = inProgress || retry;
  $("refreshStatus").textContent = inProgress
    ? "Refresh in progress. Compile is locked until all five source outcomes are committed."
    : retry
      ? "Refresh was interrupted. Retry the refresh before compiling."
      : complete
        ? "Refresh complete. The atomic source set is stored and Compile is available."
        : "No source refresh has been requested. Compile is available.";
}

function renderCycleIdentity() {
  $("cycleIdentity").innerHTML = kv([
    ["Cycle ID", cycle.cycle_id],
    ["Period", `${cycle.period_start} → ${cycle.period_end}`],
    ["Review due", cycle.review_due_on],
    ["Previous cycle", cycle.previous_cycle_id || "First baseline"],
    ["State", cycle.state],
    ["Source refresh", cycle.source_refresh_state || "LEGACY_NOT_RECORDED"],
  ]);
}

function nextActionText() {
  if (cycle.state === "COLLECTING_EVIDENCE") {
    if (cycle.source_refresh_state === "REFRESH_IN_PROGRESS") return "Next action: wait for the approved source refresh to finish. Compile remains locked.";
    if (cycle.source_refresh_state === "REFRESH_INTERRUPTED_RETRY_ALLOWED") return "Next action: retry the interrupted source refresh, or leave this cycle unchanged. Compile remains locked.";
    return "Next action: add an honest public-safe observation if available, optionally approve one source refresh, then compile the monthly comparison.";
  }
  if (cycle.state === "COMPILED_AWAITING_HUMAN_REVIEW") return "Next action: inspect the Difference, Receipt and Passport, then record one human review decision.";
  if (REVIEWED_STATES.has(cycle.state)) return "Cycle closed: this record is historical and read-only. Start a later monthly or material-event cycle when needed.";
  return "This cycle state is not editable. Inspect the stored record before taking another action.";
}

function renderObservations() {
  $("observations").innerHTML = cycle.observations.map(item => `<div class="card">${kv([
    ["Date", item.observed_on], ["Category", item.category], ["Place", item.location_scope],
    ["Observation", item.note], ["Evidence class", item.evidence_class],
  ])}</div>`).join("");
}

function renderSnapshots() {
  $("snapshots").innerHTML = cycle.source_snapshots.map(item => `<div class="card">${kv([
    ["Source", item.title], ["Publisher", item.publisher], ["State", item.change_state],
    ["Fetched", item.fetched_at], ["Raw retained", item.raw_content_retained],
    ["Error", item.error_detail || "None"],
  ])}</div>`).join("");
}

function renderCompiled() {
  if (!cycle.comparison || !cycle.hypothesis_version || !cycle.receipt || !cycle.passport) {
    $("compiled").innerHTML = "";
    return;
  }
  const comparison = cycle.comparison;
  const hypothesis = cycle.hypothesis_version;
  const receipt = cycle.receipt;
  const passport = cycle.passport;
  $("compiled").innerHTML = `<div class="card"><h3>Difference from previous cycle</h3>${kv([
    ["Comparison", comparison.comparison_state], ["New field observations", comparison.new_human_observation_count],
    ["Source snapshots", comparison.source_snapshot_count], ["Potential source changes", comparison.potential_source_change_count],
    ["Retrieval failures", comparison.retrieval_failure_count],
  ])}</div><div class="card"><h3>Hypothesis version ${esc(hypothesis.version)}</h3>${kv([
    ["State", hypothesis.state], ["Environmental conclusion", hypothesis.environmental_conclusion || "None"], ["Reason", hypothesis.reason],
  ])}</div><div class="card"><h3>Run Receipt</h3>${kv([
    ["Receipt ID", receipt.receipt_id], ["Termination", receipt.termination], ["Network used", receipt.network_used], ["Cost", `A$${receipt.cost_aud}`],
  ])}</div><div class="card"><h3>Evidence Passport</h3>${kv([
    ["Passport ID", passport.passport_id], ["State", passport.state], ["Supports", passport.supports], ["Does not support", passport.does_not_support.join("; ")],
  ])}</div>`;
}

function renderHumanDecision() {
  if (!cycle.human_review) {
    $("final").innerHTML = "";
    return;
  }
  $("final").innerHTML = `<div class="success"><b>${esc(cycle.state)}</b>${kv([
    ["Decision", cycle.human_review.decision], ["Reviewer", cycle.human_review.reviewer],
    ["Reviewed", cycle.human_review.reviewed_at], ["Reason", cycle.human_review.reason],
  ])}<br>This decision updates the research record, not the environment.</div>`;
}

function setWorkspacePermissions() {
  const collecting = cycle.state === "COLLECTING_EVIDENCE";
  const awaitingReview = cycle.state === "COMPILED_AWAITING_HUMAN_REVIEW";
  for (const id of ["category", "observedOn", "location", "note", "publicSafe", "addObservation", "networkApproval"]) $(id).disabled = !collecting;
  applyRefreshGate(cycle.source_refresh_state || "NOT_REQUESTED");
  if (!collecting) {
    $("refresh").disabled = true;
    $("compile").disabled = true;
  }
  $("reviewer").disabled = !awaitingReview;
  $("reviewReason").disabled = !awaitingReview;
  document.querySelectorAll("[data-decision]").forEach(button => button.disabled = !awaitingReview);
}

function renderCycleWorkspace() {
  renderCycleIdentity();
  $("cycleNextAction").textContent = nextActionText();
  renderObservations();
  renderSnapshots();
  renderCompiled();
  renderHumanDecision();
  setWorkspacePermissions();
  $("collect").hidden = false;
  $("review").hidden = !cycle.comparison;
}

async function openCycle(cycleId) {
  try {
    cycle = await get(`/api/cycles/${cycleId}`);
    renderCycleWorkspace();
    $("collect").scrollIntoView({behavior: "smooth"});
  } catch (error) {
    fail(error);
  }
}

function renderProgram() {
  $("question").textContent = program.question;
  $("programSummary").innerHTML = `<span class="step">Program</span><h2>Durable identity</h2>${kv([
    ["Program ID", program.program_id], ["State", program.state], ["Monthly due rule", program.cadence.monthly_due_rule],
    ["Annual report rule", program.cadence.annual_report_rule], ["Hypothesis version", program.current_hypothesis_version],
    ["Last reviewed cycle", program.last_reviewed_cycle_id || "None yet"], ["Conversation bridge", program.boundaries.conversation_bridge_state],
    ["Unattended scheduler", program.cadence.unattended_scheduler_installed],
  ])}<div>${program.modules.map(item => `<span class="tag">${esc(item.replaceAll("_", " "))}</span>`).join("")}</div>`;
  $("timeline").innerHTML = program.cycles.length
    ? program.cycles.slice().reverse().map(item => `<div class="card">${kv([
      ["Month", item.year_month], ["Period", `${item.period_start || "legacy"} → ${item.period_end || "legacy"}`],
      ["Review due", item.review_due_on || "legacy cycle"], ["Cycle", item.cycle_id], ["State", item.state], ["Trigger", item.trigger],
    ])}<button class="secondary" data-open-cycle="${esc(item.cycle_id)}">Open stored cycle</button></div>`).join("")
    : '<p class="muted">No monthly cycle yet.</p>';
  document.querySelectorAll("[data-open-cycle]").forEach(button => button.onclick = () => openCycle(button.dataset.openCycle));
}

async function load() {
  try {
    program = await get(`/api/programs/${PROGRAM}`);
    renderProgram();
    const today = new Date();
    $("month").value = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}`;
    $("observedOn").value = today.toISOString().slice(0, 10);
    $("reportYear").value = today.getFullYear();
  } catch (error) {
    fail(error);
  }
}

$("startCycle").onclick = async () => {
  try {
    cycle = await post(`/api/programs/${PROGRAM}/cycles`, {year_month: $("month").value, trigger: $("trigger").value});
    renderCycleWorkspace();
    $("collect").scrollIntoView({behavior: "smooth"});
    program = await get(`/api/programs/${PROGRAM}`);
    renderProgram();
  } catch (error) {
    fail(error);
  }
};

$("addObservation").onclick = async () => {
  try {
    await post(`/api/cycles/${cycle.cycle_id}/observations`, {
      category: $("category").value, observed_on: $("observedOn").value, note: $("note").value,
      location_scope: $("location").value, public_safe_confirmation: $("publicSafe").checked,
    });
    cycle = await get(`/api/cycles/${cycle.cycle_id}`);
    renderCycleWorkspace();
    $("note").value = "";
  } catch (error) {
    fail(error);
  }
};

$("refresh").onclick = async () => {
  try {
    applyRefreshGate("REFRESH_IN_PROGRESS");
    await post(`/api/cycles/${cycle.cycle_id}/refresh`, {human_approval: $("networkApproval").checked});
    cycle = await get(`/api/cycles/${cycle.cycle_id}`);
    renderCycleWorkspace();
  } catch (error) {
    fail(error);
    try {
      cycle = await get(`/api/cycles/${cycle.cycle_id}`);
      renderCycleWorkspace();
    } catch (_) {
      applyRefreshGate("REFRESH_IN_PROGRESS");
    }
  }
};

$("compile").onclick = async () => {
  try {
    cycle = await post(`/api/cycles/${cycle.cycle_id}/compile`, {});
    renderCycleWorkspace();
    $("review").scrollIntoView({behavior: "smooth"});
  } catch (error) {
    fail(error);
  }
};

document.querySelectorAll("[data-decision]").forEach(button => button.onclick = async () => {
  try {
    cycle = await post(`/api/cycles/${cycle.cycle_id}/review`, {
      decision: button.dataset.decision, reviewer: $("reviewer").value, reason: $("reviewReason").value,
    });
    renderCycleWorkspace();
    program = await get(`/api/programs/${PROGRAM}`);
    renderProgram();
  } catch (error) {
    fail(error);
  }
});

$("annualReport").onclick = async () => {
  try {
    const report = await post(`/api/programs/${PROGRAM}/annual-report`, {report_year: Number($("reportYear").value)});
    const summary = report.summary;
    $("annualOutput").innerHTML = `<div class="card"><h3>${esc(report.title)}</h3>${kv([
      ["Report ID", report.report_id], ["Cycles", summary.cycle_count], ["Months present", summary.months_present.join(", ")],
      ["Missing months", summary.missing_months.join(", ") || "None"], ["Field observations", summary.field_observation_count],
      ["Source snapshots", summary.official_source_snapshot_count], ["Potential source changes", summary.potential_source_change_count],
      ["Environmental conclusion", report.environmental_conclusion || "None"], ["Receipt", report.receipt.receipt_id], ["Passport", report.passport.passport_id],
    ])}</div>`;
  } catch (error) {
    fail(error);
  }
};

load();
