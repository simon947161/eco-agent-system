(function () {
  "use strict";

  const target = document.getElementById("governance-decision-support");
  if (!target) return;

  const escapeHtml = (value) =>
    String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  fetch("../output/governance_decision_records.json")
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((data) => {
      const cards = data.records.map((record) => `
        <article class="overview-card">
          <span class="eyebrow">${escapeHtml(record.scenario_name)}</span>
          <h3>${escapeHtml(record.internal_decision_status.replaceAll("_", " "))}</h3>
          <p>${escapeHtml(record.evidence_summary)}</p>
          <dl>
            <dt>External approval</dt>
            <dd>${escapeHtml(record.external_approval_status)}</dd>
            <dt>Trace records</dt>
            <dd>${record.evidence_trace_ids.length}</dd>
            <dt>Human review</dt>
            <dd>${record.human_review_required ? "Required" : "Not required"}</dd>
            <dt>Professional review</dt>
            <dd>${record.professional_review_required ? "Required" : "Not required"}</dd>
          </dl>
          <p><strong>Open gaps:</strong> ${escapeHtml(record.unresolved_evidence_gaps.join(" "))}</p>
        </article>
      `).join("");
      target.innerHTML = `<div class="overview-grid">${cards}</div>`;
    })
    .catch((error) => {
      target.textContent = `Governance decision support output unavailable: ${error.message}`;
    });
}());
