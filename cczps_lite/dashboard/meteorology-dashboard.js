"use strict";

async function renderMeteorologyEvidence() {
  const container = document.querySelector("#meteorology-evidence");
  try {
    const response = await fetch("../output/meteorology_evidence.json");
    if (!response.ok) throw new Error(`Unable to load meteorology evidence (${response.status})`);
    const output = await response.json();
    const records = Object.values(output.scenarios || {});
    container.innerHTML = `
      <div class="table-shell"><table>
        <thead><tr><th>Location</th><th>Source</th><th>Status</th><th>Cache</th><th>Date</th><th>Temperature</th><th>Rainfall</th><th>Wind</th><th>Confidence</th><th>Budget guard</th></tr></thead>
        <tbody>${records.map((record) => {
          const reading = record.meteorology_reading || {};
          return `<tr><td><strong>${escapeHtml(record.location_name || reading.location || "")}</strong></td><td>${escapeHtml(record.source || reading.source || "")}</td><td>${escapeHtml(record.retrieval_status || reading.retrieval_status || "")}</td><td>${escapeHtml(String(record.from_cache || false))}</td><td>${escapeHtml(record.observation_date || reading.observation_date || "")}</td><td>${escapeHtml(reading.temperature_c ?? "")}</td><td>${escapeHtml(reading.rainfall_mm ?? "")}</td><td>${escapeHtml(reading.wind_speed_kmh ?? "")}</td><td>${escapeHtml(record.confidence || reading.confidence || "")}</td><td>${escapeHtml(record.budget_guard_status || "")}</td></tr>`;
        }).join("")}</tbody>
      </table></div>`;
  } catch (error) {
    container.textContent = error.message;
  }
}

renderMeteorologyEvidence();
