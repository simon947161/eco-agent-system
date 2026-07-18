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
    const c = session.object_graph.resource_ceiling;
    $("runLimits").innerHTML = `<div><strong>${c.logical_cpu_workers}</strong><span>CPU worker</span></div><div><strong>${c.wall_time_seconds}s</strong><span>wall ceiling</span></div><div><strong>${c.incremental_memory_mib} MiB</strong><span>memory target</span></div><div><strong>AUD ${c.cost_aud}</strong><span>cost</span></div>`;
  } else { setStage("hypothesis"); }
  if (session.state === "APPROVED_TO_RUN") { reveal("runPanel"); setStage("run"); }
  if (session.receipt) {
    reveal("resultPanel"); reveal("reviewPanel"); setStage("review");
    const r = session.receipt, p = session.passport;
    $("receiptView").innerHTML = `<h3>${safe(r.receipt_state)}</h3><dl><dt>Receipt</dt><dd>${safe(r.receipt_id)}</dd><dt>Termination</dt><dd>${safe(r.termination)}</dd><dt>Wall time</dt><dd>${safe(r.resources_observed.wall_time_seconds)} s</dd><dt>Output bytes</dt><dd>${safe(r.resources_observed.output_bytes)}</dd><dt>Network</dt><dd>${r.resources_observed.network_used ? "used" : "not used"}</dd><dt>Audit chain</dt><dd>${session.audit_chain_valid ? "valid" : "invalid"}</dd></dl>`;
    $("passportView").innerHTML = `<h3>${safe(p.state)}</h3><p>${safe(p.quarantine_state)}</p><p><strong>Diagnostic:</strong> ${safe(p.diagnostics.response_index_delta)}</p>${list(p.limitations)}`;
  }
  if (session.human_review) {
    reveal("finalState");
    $("finalState").innerHTML = `<strong>${safe(session.state)}</strong><p>${safe(session.human_review.reason)}</p><p>Environmental release: blocked</p>`;
  }
}

async function act(path, body) {
  try { await request(path, body); } catch (error) { $("status").textContent = error.message; }
}

$("createButton").onclick = () => act("/api/sessions", {question: $("question").value, session_label: "founder-web-demo"});
$("proposeButton").onclick = () => act(`/api/sessions/${session.session_id}/propose`, {});
$("approveButton").onclick = () => act(`/api/sessions/${session.session_id}/decision`, {decision:"APPROVE", reviewer_label:$("reviewer").value, reason:$("approvalReason").value});
$("stopButton").onclick = () => act(`/api/sessions/${session.session_id}/decision`, {decision:"STOP", reviewer_label:$("reviewer").value, reason:"Human chose to stop before local execution."});
$("runButton").onclick = () => act(`/api/sessions/${session.session_id}/run`, {});
$("acceptButton").onclick = () => act(`/api/sessions/${session.session_id}/review`, {decision:"ACCEPT_RUNTIME_DEMO", reviewer_label:$("reviewer").value, reason:$("reviewReason").value});
$("insufficientButton").onclick = () => act(`/api/sessions/${session.session_id}/review`, {decision:"EVIDENCE_INSUFFICIENT", reviewer_label:$("reviewer").value, reason:$("reviewReason").value});
