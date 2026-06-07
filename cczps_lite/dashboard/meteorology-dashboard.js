"use strict";

const METEOROLOGY_STATUS = {
  success: { label: "Retrieved", className: "success" },
  blocked_by_budget_guard: { label: "Blocked by Budget Guard", className: "blocked" },
  missing_data: { label: "Missing data", className: "missing" },
  retrieval_failed: { label: "Retrieval failed", className: "failed" },
  not_retrieved: { label: "Not retrieved", className: "not-retrieved" },
};

function meteorologyValue(value, unit = "") {
  if (value === null || value === undefined || value === "") {
    return '<span class="missing-value">Not available</span>';
  }
  return `${escapeHtml(value)}${unit ? ` <span class="metric-unit">${escapeHtml(unit)}</span>` : ""}`;
}

function meteorologyStatus(status, fromCache) {
  if (fromCache && status === "success") {
    return { label: "Cached observation", className: "cached" };
  }
  return METEOROLOGY_STATUS[status] || {
    label: status ? String(status).replaceAll("_", " ") : "Status unavailable",
    className: "unknown",
  };
}

function metric(label, value, unit = "") {
  return `
    <div class="meteorology-metric">
      <dt>${escapeHtml(label)}</dt>
      <dd>${meteorologyValue(value, unit)}</dd>
    </div>
  `;
}

async function renderMeteorologyEvidence() {
  const container = document.querySelector("#meteorology-evidence");
  try {
    const response = await fetch("../output/meteorology_evidence.json");
    if (!response.ok) throw new Error(`Unable to load meteorology evidence (${response.status})`);
    const output = await response.json();
    const records = Object.entries(output.scenarios || {});
    if (!records.length) {
      container.innerHTML = '<p class="meteorology-empty">No meteorology evidence records are available.</p>';
      return;
    }
    container.innerHTML = `
      <div class="meteorology-grid">${records.map(([scenario, record]) => {
          const reading = record.meteorology_reading || {};
          const statusValue = record.retrieval_status || reading.retrieval_status || "";
          const status = meteorologyStatus(statusValue, record.from_cache === true);
          const cacheLabel = record.from_cache === true
            ? "Cached reading"
            : statusValue === "success" ? "Fresh reading" : "No cached reading";
          return `
            <article class="meteorology-card">
              <header class="meteorology-card-header">
                <div>
                  <span class="meteorology-scenario">${escapeHtml(scenario.replaceAll("_", " "))}</span>
                  <h3>${meteorologyValue(record.location_name || reading.location)}</h3>
                  <p>${meteorologyValue(record.source || reading.source)}</p>
                </div>
                <span class="meteorology-status ${status.className}">${escapeHtml(status.label)}</span>
              </header>
              <dl class="meteorology-context">
                <div><dt>Observation date</dt><dd>${meteorologyValue(record.observation_date || reading.observation_date)}</dd></div>
                <div><dt>Cache status</dt><dd>${escapeHtml(cacheLabel)}</dd></div>
                <div><dt>Budget Guard</dt><dd>${meteorologyValue(record.budget_guard_status || reading.budget_guard_status)}</dd></div>
                <div><dt>Confidence</dt><dd>${meteorologyValue(record.confidence || reading.confidence)}</dd></div>
              </dl>
              <dl class="meteorology-metrics">
                ${metric("Temperature", reading.temperature_c, "C")}
                ${metric("Rainfall", reading.rainfall_mm, "mm")}
                ${metric("Relative humidity", reading.humidity_percent, "%")}
                ${metric("Wind speed", reading.wind_speed_kmh, "km/h")}
                ${metric("Wind direction", reading.wind_direction_degrees, "degrees")}
                ${metric("Solar radiation", reading.solar_radiation_mj_m2, "MJ/m2")}
              </dl>
              ${record.budget_guard_summary || reading.budget_guard_summary ? `
                <p class="meteorology-guard-summary"><strong>Budget Guard note:</strong>
                  ${escapeHtml(record.budget_guard_summary || reading.budget_guard_summary)}
                </p>` : ""}
            </article>
          `;
        }).join("")}</div>`;
  } catch (error) {
    container.innerHTML = `<p class="meteorology-empty" role="alert">${escapeHtml(error.message)}</p>`;
  }
}

renderMeteorologyEvidence();
