const $ = (id) => document.getElementById(id);
let session = null;

async function request(path, body) {
  const response = await fetch(path, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body),
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail || payload.error || "Request refused");
  session = payload;
  render();
}

function reveal(id) { $(id).classList.remove("hidden"); }
function hide(id) { $(id).classList.add("hidden"); }
function safe(value) { return String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function list(items) { return `<ul>${items.map(item => `<li>${safe(item)}</li>`).join("")}</ul>`; }

function setStage(name) {
  const order = ["question","hypothesis","approval","run","receipt","review"];
  const position = order.indexOf(name);
  document.querySelectorAll("#stageRail li").forEach((node, index) => {
    node.classList.toggle("active", index === position);
    node.classList.toggle("done", index < position);
  });
}

function render() {
  if (!session) return;
  $("status").textContent = `Session ${session.session_id} · ${session.state}`;
  reveal("hypothesisPanel");
  if (session.object_graph) {
    const h = session.object_graph.hypothesis;
    $("hypothesisView").innerHTML = `<h3>${safe(h.hypothesis_statement)}</h3><dl><dt>Hypothesis ID</dt><dd>${safe(h.hypothesis_id)}</dd><dt>Expected direction</dt><dd>${safe(h.expected_direction)}</dd><dt>Evidence threshold</dt><dd>${safe(h.evidence_threshold)}</dd></dl><h4>Alternatives</h4>${list(h.alternative_explanations)}<h4>Falsification</h4>${list(h.falsification_criteria)}<h4>Limitations</h4>${list(h.limitations)}`;
    reveal("approvalPanel"); setStage("approval");
    $("hypothesisEdit").value = h.hypothesis_statement;
    $("hypothesisEdit").disabled = session.state !== "HYPOTHESIS_PROPOSED";
    $("reviseButton").disabled = session.state !== "HYPOTHESIS_PROPOSED";
    $("proposeButton").disabled = true;
    for (const id of ["approveButton","rejectButton","stopButton"]) $(id).disabled = session.state !== "HYPOTHESIS_PROPOSED";
    const c = session.object_graph.resource_ceiling;
    $("runLimits").innerHTML = `<div><strong>${c.logical_cpu_workers}</strong><span>CPU worker</span></div><div><strong>${c.wall_time_seconds}s</strong><span>wall ceiling</span></div><div><strong>${c.incremental_memory_mib} MiB</strong><span>memory target</span></div><div><strong>AUD ${c.cost_aud}</strong><span>cost</span></div>`;
  } else { $("proposeButton").disabled = false; setStage("hypothesis"); }
  if (session.state === "APPROVED_TO_RUN") { reveal("runPanel"); $("runButton").disabled = false; setStage("run"); }
  if (session.receipt) {
    reveal("resultPanel"); reveal("reviewPanel"); setStage("review");
    const r = session.receipt, p = session.passport;
    for (const id of ["acceptButton","insufficientButton","rejectDemoButton"]) $(id).disabled = !["RUN_COMPLETED_QUARANTINED", "RUN_FAILED_QUARANTINED"].includes(session.state);
    $("receiptView").innerHTML = `<h3>${safe(r.receipt_state)}</h3><dl><dt>Session</dt><dd>${safe(session.session_id)}</dd><dt>Receipt</dt><dd>${safe(r.receipt_id)}</dd><dt>Termination</dt><dd>${safe(r.termination)}</dd><dt>Wall time</dt><dd>${safe(r.resources_observed.wall_time_seconds)} s</dd><dt>Output bytes</dt><dd>${safe(r.resources_observed.output_bytes)}</dd><dt>Network</dt><dd>${r.resources_observed.network_used ? "used" : "not used"}</dd><dt>Audit chain</dt><dd>${session.audit_chain_valid ? "valid" : "invalid"}</dd></dl>`;
    $("passportView").innerHTML = `<h3>${safe(p.state)}</h3><dl><dt>Passport</dt><dd>${safe(p.passport_id)}</dd><dt>Evidence boundary</dt><dd>${safe(p.quarantine_state)}</dd><dt>Diagnostic</dt><dd>${safe(p.diagnostics.response_index_delta)}</dd></dl>${list(p.limitations)}`;
  }
  if (session.human_review) {
    reveal("finalState");
    $("finalState").innerHTML = `<strong>${safe(session.state)}</strong><p>${safe(session.human_review.reason)}</p><p>Environmental release: blocked</p>`;
  }
  if (["REJECTED_BEFORE_RUN", "STOPPED_BEFORE_RUN", "REVIEWED_DEMO_ACCEPTED", "REVIEWED_EVIDENCE_INSUFFICIENT", "REVIEWED_DEMO_REJECTED"].includes(session.state)) reveal("recoveryPanel");
}

function nextRevision(hypothesis) {
  const revised = JSON.parse(JSON.stringify(hypothesis));
  const match = /-R(\d+)$/.exec(revised.revision_id);
  const number = match ? Number(match[1]) + 1 : 2;
  revised.revision_id = `${revised.hypothesis_id}-R${number}`;
  revised.hypothesis_statement = $("hypothesisEdit").value;
  return revised;
}

async function restart() {
  const previous = session;
  try {
    const response = await fetch("/api/sessions", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({question:previous.question, session_label:`revision-of-${previous.session_id}`})});
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || payload.error || "Restart refused");
    session = payload;
    for (const id of ["approvalPanel","runPanel","resultPanel","reviewPanel","recoveryPanel","finalState"]) hide(id);
    $("hypothesisView").innerHTML = ""; $("hypothesisEdit").value = "";
    $("receiptView").innerHTML = ""; $("passportView").innerHTML = "";
    render();
  } catch (error) { $("status").textContent = error.message; }
}

async function act(path, body) {
  try { await request(path, body); } catch (error) { $("status").textContent = error.message; }
}

$("createButton").onclick = () => act("/api/sessions", {question: $("question").value, session_label: "founder-web-demo"});
$("proposeButton").onclick = () => act(`/api/sessions/${session.session_id}/propose`, {});
$("reviseButton").onclick = () => act(`/api/sessions/${session.session_id}/revise`, {hypothesis:nextRevision(session.object_graph.hypothesis), reviewer_label:$("reviewer").value, reason:$("revisionReason").value});
$("approveButton").onclick = () => act(`/api/sessions/${session.session_id}/decision`, {decision:"APPROVE", reviewer_label:$("reviewer").value, reason:$("approvalReason").value});
$("rejectButton").onclick = () => act(`/api/sessions/${session.session_id}/decision`, {decision:"REJECT", reviewer_label:$("reviewer").value, reason:"The human reviewer rejects this plan and requires a revised session before any run."});
$("stopButton").onclick = () => act(`/api/sessions/${session.session_id}/decision`, {decision:"STOP", reviewer_label:$("reviewer").value, reason:"Human chose to stop before local execution."});
$("runButton").onclick = () => act(`/api/sessions/${session.session_id}/run`, {});
$("acceptButton").onclick = () => act(`/api/sessions/${session.session_id}/review`, {decision:"ACCEPT_RUNTIME_DEMO", reviewer_label:$("reviewer").value, reason:$("reviewReason").value});
$("insufficientButton").onclick = () => act(`/api/sessions/${session.session_id}/review`, {decision:"EVIDENCE_INSUFFICIENT", reviewer_label:$("reviewer").value, reason:$("reviewReason").value});
$("rejectDemoButton").onclick = () => act(`/api/sessions/${session.session_id}/review`, {decision:"REJECT_RUNTIME_DEMO", reviewer_label:$("reviewer").value, reason:$("reviewReason").value});
$("restartButton").onclick = restart;
