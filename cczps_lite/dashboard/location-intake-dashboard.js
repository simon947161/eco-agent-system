(function () {
  "use strict";

  const target = document.querySelector("#location-intake-profiles");
  const invalidTarget = document.querySelector("#location-intake-invalid");
  if (!target || !invalidTarget) return;

  const STATUS_TEXT = {
    intake_only: "This is only a preliminary location intake record.",
    awaiting_evidence_generation: "Evidence has not been generated yet.",
    not_generated: "This output has not been generated yet.",
    not_requested: "This workflow has not been requested yet.",
    not_ready_for_approval: "This location is not ready for approval. Professional review is required.",
  };

  const escapeHtml = (value) =>
    String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

  const explain = (status) => STATUS_TEXT[status] || String(status || "Not recorded");

  fetch("../output/location_intake_profiles.json")
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((data) => {
      const profiles = data.scenario_profiles || [];
      target.innerHTML = profiles.length ? profiles.map((profile) => `
        <article class="human-card intake-card">
          <span class="human-card-label">Preliminary location intake</span>
          <h3>${escapeHtml(profile.location_name)}</h3>
          <p>${escapeHtml(explain(profile.scenario_status))}</p>
          <dl class="plain-status-list">
            <div><dt>Country / region</dt><dd>${escapeHtml(profile.country || "Not supplied")} / ${escapeHtml(profile.region || "Not supplied")}</dd></div>
            <div><dt>Coordinates</dt><dd>${escapeHtml(profile.latitude)}, ${escapeHtml(profile.longitude)}</dd></div>
            <div><dt>Intake context</dt><dd>${escapeHtml(profile.intake_context)}</dd></div>
            <div><dt>Workflow</dt><dd>${escapeHtml(explain(profile.workflow_status))}</dd></div>
            <div><dt>Evidence</dt><dd>${escapeHtml(explain(profile.evidence_status))}</dd></div>
            <div><dt>Meteorology</dt><dd>${escapeHtml(explain(profile.meteorology_status))}</dd></div>
            <div><dt>GIS / DEM</dt><dd>${escapeHtml(explain(profile.gis_dem_status))}</dd></div>
            <div><dt>Approval support</dt><dd>${escapeHtml(explain(profile.approval_support_status))}</dd></div>
          </dl>
          <div class="human-card-detail">
            <strong>Review-support next steps</strong>
            <ol class="review-action-list">${(profile.recommended_next_steps || []).map((step) => `<li>${escapeHtml(step)}</li>`).join("")}</ol>
            <p class="review-boundary">${escapeHtml((profile.limitations || []).join(". "))}.</p>
          </div>
        </article>
      `).join("") : '<p class="human-fallback">No valid location intake profiles are available.</p>';

      const invalid = data.invalid_records || [];
      invalidTarget.innerHTML = invalid.length
        ? `<strong>${invalid.length} invalid intake record(s) were not promoted.</strong> ${invalid.map((record) => `${escapeHtml(record.location_name || `Input ${record.input_index}`)}: ${escapeHtml((record.validation_errors || []).join(", "))}`).join("; ")}`
        : "No invalid intake records were reported.";
    })
    .catch((error) => {
      target.innerHTML = `<p class="human-fallback">Location intake output unavailable: ${escapeHtml(error.message)}. Other dashboard sections remain available.</p>`;
      invalidTarget.textContent = "";
    });
}());
