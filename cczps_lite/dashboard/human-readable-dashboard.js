(function () {
  "use strict";

  const DATA_PATHS = {
    comparison: "../output/scenario_comparison.json",
    traceability: "../output/evidence_traceability.json",
    hypotheses: "../output/planning_hypotheses.json",
    governance: "../output/governance_decision_records.json",
    approval: "../output/planning_approval_support_report.json",
    spatial: "../output/spatial_transect_scenario_pack.json",
  };

  const STATUS_EXPLANATIONS = {
    not_ready_for_approval: "Not ready for approval. Professional review is required.",
    requires_further_review: "Further review is required before this can support a decision.",
    concept_level: "Early-stage idea. Worth reviewing, but not proven.",
    insufficient_evidence: "The system does not yet have enough evidence.",
    awaiting_professional_review: "A qualified professional has not reviewed this yet.",
    requires_validation: "The idea needs more local evidence and professional testing.",
    not_reviewed: "No completed expert review is recorded.",
    planning_only_not_acquired: "Spatial data needs are documented, but GIS and DEM data have not been acquired or analysed.",
    supporting_evidence_only: "This record supports review, but it does not establish a conclusion.",
    human_review_required: "Human review is required.",
  };

  const SCENARIO_CONTEXT = {
    batlow: { location: "Batlow, New South Wales, Australia", type: "Climate and landscape resilience demonstration", issue: "Dry-season water, heat, fire, and continuity pressures" },
    kunlun: { location: "Kunlun dryland context", type: "Dryland eco-water demonstration", issue: "Water limitation, ecological stress, and incomplete spatial context" },
    iraq: { location: "Iraq agricultural recovery context", type: "Agricultural recovery demonstration", issue: "Water scarcity, heat exposure, soil condition, and ecological buffers" },
    baiyangdian_xiongan: { location: "Baiyangdian-Xiong'an watershed", type: "Watershed continuity demonstration", issue: "Headwaters, wetland water balance, urban demand, and ecological connectivity" },
  };

  const escapeHtml = (value) => String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");
  const explain = (status, fallback = "Status is recorded for human review.") => STATUS_EXPLANATIONS[status] || fallback;
  const sentenceList = (items) => { const clean = (items || []).filter(Boolean); if (!clean.length) return "No additional items are recorded."; if (clean.length === 1) return clean[0]; return `${clean.slice(0, -1).join(", ")}, and ${clean.at(-1)}`; };
  const byScenario = (records, key = "scenario_id") => Object.fromEntries((records || []).map((record) => [record[key], record]));
  const scenarioIdFromName = (name) => String(name || "").toLowerCase().replaceAll("-", "_").replaceAll("'", "").replaceAll(" ", "_");
  const card = (scenario, label, body, details = "") => `<article class="human-card"><span class="human-card-label">${escapeHtml(label)}</span><h3>${escapeHtml(scenario)}</h3><p>${escapeHtml(body)}</p>${details ? `<div class="human-card-detail">${details}</div>` : ""}</article>`;
  const fallback = (message) => `<p class="human-fallback">${escapeHtml(message)} The rest of the dashboard remains available.</p>`;

  async function readJson(path) { const response = await fetch(path); if (!response.ok) throw new Error(`HTTP ${response.status}`); return response.json(); }
  async function loadData() { const entries = Object.entries(DATA_PATHS); const results = await Promise.allSettled(entries.map(([, path]) => readJson(path))); return Object.fromEntries(entries.map(([key], index) => [key, results[index].status === "fulfilled" ? results[index].value : null])); }

  function renderScenarios(data) {
    const target = document.querySelector("#human-scenario-cards"); const records = data.comparison?.records || [];
    if (!records.length) { target.innerHTML = fallback("Scenario comparison data is unavailable."); return; }
    target.innerHTML = records.map((record) => { const context = SCENARIO_CONTEXT[record.scenario_id] || {}; const body = `${record.scenario_name} is a ${context.type || "planning-support demonstration"}. The key issue is ${context.issue || "documented environmental uncertainty"}.`; const details = `<dl class="plain-status-list"><div><dt>Location or context</dt><dd>${escapeHtml(context.location || "Local context not recorded")}</dd></div><div><dt>Evidence</dt><dd>${escapeHtml(record.evidence_strength)} coverage with ${escapeHtml(record.uncertainty_level)} uncertainty</dd></div><div><dt>Review</dt><dd>${escapeHtml(explain(record.internal_governance_status))}</dd></div><div><dt>Approval support</dt><dd>${escapeHtml(explain(record.approval_support_status))}</dd></div><div><dt>Human review</dt><dd>${escapeHtml(record.human_review_required ? STATUS_EXPLANATIONS.human_review_required : "No additional human review flag is recorded.")}</dd></div></dl>`; return card(record.scenario_name, "Scenario overview", body, details); }).join("");
  }

  function renderEvidence(data) {
    const target = document.querySelector("#human-evidence-summary"); const records = data.comparison?.records || []; const traces = data.traceability?.records || [];
    if (!records.length) { target.innerHTML = fallback("Evidence summary data is unavailable."); return; }
    target.innerHTML = records.map((record) => { const localTraces = traces.filter((trace) => trace.scenario_id === record.scenario_id); const pending = localTraces.filter((trace) => ["insufficient_evidence", "awaiting_professional_review", "not_reviewed"].includes(trace.evidence_strength) || ["awaiting_professional_review", "not_reviewed"].includes(trace.review_status)); const body = record.evidence_strength === "medium" ? "The system has some supporting evidence, but it has not yet been checked and completed by qualified professionals." : "The system has limited supporting evidence and important gaps remain before the scenario can support a decision."; const details = `<p><strong>Traceability:</strong> ${localTraces.length || record.trace_record_count} local records connect displayed statements to source artifacts.</p><p><strong>Still incomplete:</strong> ${pending.length ? `${pending.length} traced records need more evidence or professional review.` : "Professional review remains required by the scenario record."}</p>`; return card(record.scenario_name, "Evidence summary", body, details); }).join("");
  }

  function renderHypotheses(data) {
    const target = document.querySelector("#human-hypothesis-summary"); const hypotheses = Object.values(data.hypotheses?.hypotheses || {});
    if (!hypotheses.length) { target.innerHTML = fallback("Planning hypothesis data is unavailable."); return; }
    target.innerHTML = hypotheses.map((item) => { const details = `<dl class="plain-status-list"><div><dt>Observed issue</dt><dd>${escapeHtml(item.problem_statement)}</dd></div><div><dt>Planning assumption</dt><dd>${escapeHtml(item.planning_assumption)}</dd></div><div><dt>Expected effect</dt><dd>${escapeHtml(item.expected_effect)}</dd></div><div><dt>What needs testing</dt><dd>${escapeHtml(sentenceList(item.validation_indicators))}</dd></div><div><dt>Failure conditions</dt><dd>${escapeHtml(sentenceList(item.failure_conditions))}</dd></div></dl>`; return card(item.scenario, explain(item.hypothesis_status), "The system has recorded a concept-level planning hypothesis. It is a testable idea for further review, not a proven finding.", details); }).join("");
  }

  function renderGovernance(data) {
    const target = document.querySelector("#human-governance-summary"); const records = data.governance?.records || [];
    if (!records.length) { target.innerHTML = fallback("Governance review data is unavailable."); return; }
    target.innerHTML = records.map((record) => { const body = `The current internal status is: ${explain(record.internal_decision_status)} This is not an approval decision.`; const details = `<p><strong>What remains unresolved:</strong> ${escapeHtml(sentenceList(record.unresolved_evidence_gaps))}</p><p><strong>Professional boundary:</strong> ${escapeHtml(explain(record.external_approval_status))}</p>`; return card(record.scenario_name, "Internal review status", body, details); }).join("");
  }

  function renderComparison(data) {
    const target = document.querySelector("#human-comparison-summary"); const summary = data.comparison?.cross_scenario_summary;
    if (!summary) { target.innerHTML = fallback("Cross-scenario comparison data is unavailable."); return; }
    const medium = summary.evidence_coverage_groups?.medium || []; const low = summary.evidence_coverage_groups?.low || [];
    target.innerHTML = `<div class="comparison-callout"><h3>Current evidence coverage</h3><p>${escapeHtml(sentenceList(medium))} currently have more documented local evidence coverage than ${escapeHtml(sentenceList(low))}. This describes the records available, not scenario quality.</p></div><div class="comparison-points"><p><strong>Higher uncertainty:</strong> ${escapeHtml(sentenceList(summary.high_uncertainty_scenarios))}.</p><p><strong>GIS / DEM validation needed:</strong> ${escapeHtml(sentenceList(summary.requires_spatial_validation))}.</p><p><strong>Expert review needed:</strong> ${escapeHtml(sentenceList(summary.requires_expert_review))}.</p><p><strong>Boundary:</strong> ${escapeHtml(summary.summary_boundary)}</p></div>`;
  }

  function readableAction(action) { const mappings = { "confirm required spatial datasets and licensing": "Confirm which terrain, hydrology, land-surface, and boundary datasets can be used.", "complete relevant professional validation categories": "Ask qualified planners and relevant technical specialists to complete the professional review fields.", "record expert findings with evidence references": "Record expert findings and link each finding to its supporting evidence.", "resolve material uncertainty before any approval process": "Resolve important evidence gaps before beginning any approval process." }; return mappings[action] || action; }

  function renderActions(data) {
    const target = document.querySelector("#human-next-actions"); const scenarios = data.approval?.scenarios || []; const spatial = byScenario(data.spatial?.scenarios || []);
    if (!scenarios.length) { target.innerHTML = fallback("Next-review action data is unavailable."); return; }
    target.innerHTML = scenarios.map((scenario) => { const scenarioId = scenarioIdFromName(scenario.scenario); const spatialRecord = spatial[scenarioId]; const actions = (scenario.recommended_next_steps || []).map(readableAction); if (spatialRecord?.validation_status === "configured_with_missing_data") actions.unshift("Complete missing configured spatial reference information before GIS or DEM validation."); const details = `<ol class="review-action-list">${actions.map((action) => `<li>${escapeHtml(action)}</li>`).join("")}</ol><p class="review-boundary">Review support only. These are not implementation instructions. A qualified human decides what work is appropriate.</p>`; return card(scenario.scenario, "Suggested review sequence", "The existing records identify these likely review steps.", details); }).join("");
  }

  loadData().then((data) => { renderScenarios(data); renderEvidence(data); renderHypotheses(data); renderGovernance(data); renderComparison(data); renderActions(data); }).catch(() => { document.querySelectorAll("[id^='human-']").forEach((target) => { target.innerHTML = fallback("Plain-language data could not be loaded."); }); });
}());
