(function () {
  "use strict";

  const target = document.querySelector("#location-meteorology-records");
  if (!target) return;

  const escapeHtml = (value) =>
    String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  fetch("../output/location_meteorology_evidence.json")
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((data) => {
      const records = data.records || [];
      target.innerHTML = records.length ? records.map((record) => `
        <article class="human-card intake-card">
          <span class="human-card-label">Governed meteorology evidence</span>
          <h3>${escapeHtml(record.location_name)}</h3>
          <dl class="plain-status-list">
            <div><dt>Intake scenario</dt><dd>${escapeHtml(record.scenario_id)}</dd></div>
            <div><dt>Date</dt><dd>${escapeHtml(record.observation_date)}</dd></div>
            <div><dt>Status</dt><dd>${escapeHtml(record.meteorology_status)}</dd></div>
            <div><dt>Source</dt><dd>${escapeHtml(record.source)}</dd></div>
            <div><dt>Cache</dt><dd>${record.from_cache ? "Cache hit" : "Not from cache"}</dd></div>
            <div><dt>Budget Guard</dt><dd>${escapeHtml(record.budget_guard_status)}</dd></div>
            <div><dt>Approval support</dt><dd>${escapeHtml(record.approval_support_status)}</dd></div>
            <div><dt>Human review</dt><dd>${record.human_review_required ? "Required" : "Not recorded"}</dd></div>
          </dl>
          <p class="review-boundary">${escapeHtml((record.limitations || []).join(". "))}.</p>
        </article>
      `).join("") : '<p class="human-fallback">No governed location meteorology records are available.</p>';
    })
    .catch((error) => {
      target.innerHTML = `<p class="human-fallback">Location meteorology output unavailable: ${escapeHtml(error.message)}.</p>`;
    });
}());
