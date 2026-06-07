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
            <th>Estimated cost</th><th>Budget warning</th>
            <th>Approval required</th><th>Agentic risk</th>
          </tr></thead>
          <tbody>
            ${records.map((row) => `<tr>
              <td><strong>${escapeHtml(row.scenario_name)}</strong></td>
              <td>${escapeHtml(row.usage_mode)}</td>
              <td>${escapeHtml(row.external_resource_owner)}</td>
              <td>${badge(row.estimated_cost_level)}</td>
              <td>${escapeHtml(row.budget_warning)}</td>
              <td>${escapeHtml(row.requires_user_approval)}</td>
              <td>${badge(row.agentic_risk_level)}</td>
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
