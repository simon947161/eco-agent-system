"use strict";

async function renderPlanningHypotheses() {
  const container = document.querySelector("#planning-hypotheses");
  try {
    const response = await fetch("../output/planning_hypotheses.json");
    if (!response.ok) throw new Error(`Unable to load planning hypotheses (${response.status})`);
    const output = await response.json();
    const hypotheses = Object.values(output.hypotheses || {});
    if (!hypotheses.length) {
      container.innerHTML = '<p class="meteorology-empty">No planning hypotheses are available.</p>';
      return;
    }
    container.innerHTML = `<div class="hypothesis-grid">${hypotheses.map((item) => `
      <article class="hypothesis-card">
        <header class="meteorology-card-header">
          <div>
            <span class="meteorology-scenario">${escapeHtml(item.hypothesis_id)}</span>
            <h3>${escapeHtml(item.scenario)}</h3>
          </div>
          <span class="meteorology-status ${item.hypothesis_status === "evidence_supported" ? "success" : "missing"}">
            ${escapeHtml(item.hypothesis_status.replaceAll("_", " "))}
          </span>
        </header>
        <dl class="hypothesis-fields">
          <div><dt>Problem statement</dt><dd>${escapeHtml(item.problem_statement)}</dd></div>
          <div><dt>Planning assumption</dt><dd>${escapeHtml(item.planning_assumption)}</dd></div>
          <div><dt>Intervention logic</dt><dd>${escapeHtml(item.intervention_logic)}</dd></div>
          <div><dt>Expected effect</dt><dd>${escapeHtml(item.expected_effect)}</dd></div>
          <div><dt>Validation indicators</dt><dd>${escapeHtml((item.validation_indicators || []).join("; "))}</dd></div>
          <div><dt>Failure conditions</dt><dd>${escapeHtml((item.failure_conditions || []).join("; "))}</dd></div>
          <div><dt>Human review required</dt><dd>${escapeHtml(item.human_review_required)}</dd></div>
        </dl>
        <p class="meteorology-guard-summary">${escapeHtml(item.hypothesis_summary)}</p>
      </article>
    `).join("")}</div>`;
  } catch (error) {
    container.innerHTML = `<p class="meteorology-empty" role="alert">${escapeHtml(error.message)}</p>`;
  }
}

renderPlanningHypotheses();
