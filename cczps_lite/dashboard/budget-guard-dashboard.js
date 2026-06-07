"use strict";

async function renderBudgetGuard() {
  const container = document.querySelector("#budget-guard-reading");
  try {
    const response = await fetch("../output/comparison_matrix.csv");
    if (!response.ok) throw new Error(`Unable to load budget guard data (${response.status})`);
    const records = parseCsv(await response.text());
    container.innerHTML = `
      <div class="table-shell">
        <table>
          <thead><tr>
            <th>Scenario</th><th>Budget status</th><th>Daily call limit</th>
            <th>Estimated calls</th><th>Agent run limit</th>
            <th>Manual confirmation</th><th>Stop if exceeded</th>
          </tr></thead>
          <tbody>
            ${records.map((row) => `<tr>
              <td><strong>${escapeHtml(row.scenario_name)}</strong></td>
              <td>${badge(row.budget_status)}</td>
              <td>${escapeHtml(row.daily_call_limit)}</td>
              <td>${escapeHtml(row.estimated_calls)}</td>
              <td>${escapeHtml(row.agent_run_limit)}</td>
              <td>${escapeHtml(row.requires_manual_confirmation)}</td>
              <td>${escapeHtml(row.stop_if_budget_exceeded)}</td>
            </tr>`).join("")}
          </tbody>
        </table>
      </div>
    `;
  } catch (error) {
    container.textContent = error.message;
  }
}

renderBudgetGuard();
