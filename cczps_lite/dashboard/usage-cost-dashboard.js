"use strict";

async function renderUsageCostGovernance() {
  const container = document.querySelector("#usage-cost-governance");
  try {
    const response = await fetch("../output/comparison_matrix.csv");
    if (!response.ok) throw new Error(`Unable to load governance data (${response.status})`);
    const records = parseCsv(await response.text());
    container.innerHTML = `
      <div class="table-shell">
        <table>
          <thead><tr>
            <th>Scenario</th><th>Mode</th><th>Resource owner</th>
            <th>Cost bearer</th><th>Service recipient</th>
            <th>External cost</th><th>Fee model</th><th>Fee estimate</th>
            <th>Budget warning</th><th>Approval required</th>
            <th>Agentic consumption risk</th>
          </tr></thead>
          <tbody>
            ${records.map((row) => `<tr>
              <td><strong>${escapeHtml(row.scenario_name)}</strong></td>
              <td>${escapeHtml(row.usage_mode)}</td>
              <td>${escapeHtml(row.external_resource_owner)}</td>
              <td>${escapeHtml(row.external_cost_bearer)}</td>
              <td>${escapeHtml(row.platform_service_recipient)}</td>
              <td>${badge(row.estimated_external_resource_cost)}</td>
              <td>${escapeHtml(row.platform_service_fee_model)}</td>
              <td>${badge(row.platform_service_fee_estimate)}</td>
              <td>${escapeHtml(row.budget_warning)}</td>
              <td>${escapeHtml(row.requires_user_approval)}</td>
              <td>${badge(row.agentic_consumption_risk)}</td>
            </tr>`).join("")}
          </tbody>
        </table>
      </div>
    `;
  } catch (error) {
    container.textContent = error.message;
  }
}

renderUsageCostGovernance();
