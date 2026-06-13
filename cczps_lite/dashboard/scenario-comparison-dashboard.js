(function () {
  "use strict";

  const target = document.getElementById("evidence-scenario-comparison");
  if (!target) return;

  const escapeHtml = (value) =>
    String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  fetch("../output/scenario_comparison.json")
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((data) => {
      const rows = data.records.map((record) => `
        <tr>
          <td><strong>${escapeHtml(record.scenario_name)}</strong><br><small>${escapeHtml(record.comparison_status)}</small></td>
          <td>${escapeHtml(record.evidence_strength)}</td>
          <td>${escapeHtml(record.uncertainty_level)}</td>
          <td>${escapeHtml(record.risk_level)}</td>
          <td>${escapeHtml(record.planning_hypothesis_status)}</td>
          <td>${escapeHtml(record.traceability_status)} (${record.trace_record_count})</td>
          <td>${escapeHtml(record.internal_governance_status)}</td>
          <td>${escapeHtml(record.expert_review_status)}</td>
          <td>${escapeHtml(record.approval_support_status)}</td>
          <td>${record.human_review_required ? "Required" : "Not required"}</td>
        </tr>
      `).join("");
      target.innerHTML = `
        <div class="table-shell">
          <table>
            <thead><tr><th>Scenario</th><th>Evidence</th><th>Uncertainty</th><th>Risk</th><th>Hypothesis</th><th>Traceability</th><th>Governance</th><th>Expert review</th><th>Approval support</th><th>Human review</th></tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
        <p>${escapeHtml(data.cross_scenario_summary.summary_boundary)}</p>
      `;
    })
    .catch((error) => {
      target.textContent = `Scenario comparison output unavailable: ${error.message}`;
    });
}());
