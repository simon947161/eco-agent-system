"use strict";

const DATA_PATHS = {
  matrix: "../output/comparison_matrix.csv",
  validation: "../../docs/CCZPS_LITE_SYSTEM_VALIDATION_REPORT.md",
  capability: "../output/runtime_capability_map.md",
};

const SCENARIOS = {
  batlow: {
    label: "Batlow",
    location: "Batlow, New South Wales, Australia",
    representativeId: "BATLOW_ENERGY_RESILIENCE",
    match: (row) => row.scenario_id.startsWith("BATLOW_"),
  },
  kunlun: {
    label: "Kunlun",
    location: "Kunlun dryland context",
    representativeId: "KUNLUN_ECO_WATER",
    match: (row) => row.scenario_id === "KUNLUN_ECO_WATER",
  },
  iraq: {
    label: "Iraq",
    location: "Iraq agricultural recovery context",
    representativeId: "IRAQ_AGRICULTURE_RECOVERY",
    match: (row) => row.scenario_id === "IRAQ_AGRICULTURE_RECOVERY",
  },
  baiyangdian: {
    label: "Baiyangdian-Xiong'an",
    location: "Baiyangdian-Xiong'an watershed",
    representativeId: "XIONGAN_BAIYANGDIAN_WETLAND",
    match: (row) => row.scenario_id.startsWith("XIONGAN_"),
  },
};

const RUNTIME_STAGES = [
  {
    name: "Evidence",
    fields: [
      ["Strength", "evidence_strength"],
      ["Source", "source_basis"],
      ["Human review", "human_review_required"],
    ],
  },
  {
    name: "Differential",
    fields: [
      ["Status", "differential_status"],
      ["Water gradient", "water_gradient"],
      ["Fire gradient", "fire_gradient"],
    ],
  },
  {
    name: "Forcing",
    fields: [
      ["Primary", "primary_forcing"],
      ["Priority", "forcing_priority"],
      ["Candidates", "forcing_candidates"],
    ],
  },
  {
    name: "Validation",
    fields: [
      ["Status", "validation_status"],
      ["Score", "validation_score"],
      ["Gaps", "validation_gaps"],
    ],
  },
  {
    name: "Feedback",
    fields: [
      ["Action", "review_action"],
      ["Owner", "review_owner"],
      ["Priority", "review_priority"],
    ],
  },
  {
    name: "Adaptive response",
    fields: [
      ["Mode", "response_mode"],
      ["Priority", "response_priority"],
      ["Options", "response_options"],
    ],
  },
  {
    name: "Prioritisation",
    fields: [
      ["First response", "prioritised_response"],
      ["Urgency", "urgency_level"],
      ["Expected benefit", "expected_benefit"],
    ],
  },
  {
    name: "System validation",
    fields: [
      ["Readiness", "recommendation_class"],
      ["Continuity", "watershed_continuity"],
      ["Boundary", "uncertainty_notes"],
    ],
  },
];

let rows = [];
let selectedKey = "batlow";

function parseCsv(text) {
  const records = [];
  let row = [];
  let value = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];
    const next = text[index + 1];

    if (character === '"' && quoted && next === '"') {
      value += '"';
      index += 1;
    } else if (character === '"') {
      quoted = !quoted;
    } else if (character === "," && !quoted) {
      row.push(value);
      value = "";
    } else if ((character === "\n" || character === "\r") && !quoted) {
      if (character === "\r" && next === "\n") index += 1;
      row.push(value);
      if (row.some((cell) => cell !== "")) records.push(row);
      row = [];
      value = "";
    } else {
      value += character;
    }
  }

  if (value || row.length) {
    row.push(value);
    records.push(row);
  }

  const [headers = [], ...dataRows] = records;
  return dataRows.map((cells) => Object.fromEntries(
    headers.map((header, index) => [header, cells[index] || ""]),
  ));
}

function representative(key) {
  const config = SCENARIOS[key];
  return rows.find((row) => row.scenario_id === config.representativeId) ||
    rows.find(config.match) || {};
}

function scenarioRows(key) {
  return rows.filter(SCENARIOS[key].match);
}

function safe(value, fallback = "Not available") {
  return String(value || fallback);
}

function escapeHtml(value) {
  return safe(value, "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function badgeClass(value) {
  const text = safe(value, "").toLowerCase();
  if (text.includes("insufficient") || text === "high") return "high insufficient";
  if (text.includes("technical") || text.includes("local") || text === "medium") return "medium technical";
  if (text.includes("validated") || text === "low") return "low validated";
  return "";
}

function badge(value) {
  return `<span class="badge ${badgeClass(value)}">${escapeHtml(value)}</span>`;
}

function scaleFor(key, row) {
  if (key === "baiyangdian") return "watershed system / three validation points";
  return safe(row.geographic_scale, key === "batlow" ? "regional town and agricultural continuity" : "regional context");
}

function renderOverview() {
  const container = document.querySelector("#overview-cards");
  container.innerHTML = Object.entries(SCENARIOS).map(([key, config], index) => {
    const row = representative(key);
    return `
      <article class="scenario-card" data-scenario="${key}" tabindex="0">
        <span class="card-number">0${index + 1}</span>
        <h3>${escapeHtml(config.label)}</h3>
        <p class="card-meta">${escapeHtml(config.location)}<br>${escapeHtml(scaleFor(key, row))}</p>
        ${badge(row.validation_status)}
        <p class="card-response">${escapeHtml(row.prioritised_response)}</p>
      </article>
    `;
  }).join("");

  container.querySelectorAll(".scenario-card").forEach((card) => {
    const selectCard = () => {
      selectedKey = card.dataset.scenario;
      document.querySelector("#scenario-select").value = selectedKey;
      renderSelectedScenario();
      document.querySelector("#scenario-detail").scrollIntoView({ behavior: "smooth" });
    };
    card.addEventListener("click", selectCard);
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectCard();
      }
    });
  });
}

function renderComparison() {
  document.querySelector("#comparison-body").innerHTML = Object.entries(SCENARIOS).map(([key, config]) => {
    const row = representative(key);
    return `
      <tr>
        <td class="scenario-cell"><strong>${escapeHtml(config.label)}</strong><span>${escapeHtml(scaleFor(key, row))}</span></td>
        <td>${badge(row.validation_status)}</td>
        <td>${badge(row.implementation_priority)}<br><small>${escapeHtml(row.prioritised_response)}</small></td>
        <td><strong>${escapeHtml(row.risk_index)}</strong><br><small>indicative index</small></td>
        <td>${escapeHtml(row.recommendation_class)}</td>
      </tr>
    `;
  }).join("");
}

function renderRuntime(row) {
  document.querySelector("#runtime-flow").innerHTML = RUNTIME_STAGES.map((stage, index) => `
    <article class="runtime-stage">
      <span class="stage-label">Stage ${String(index + 1).padStart(2, "0")}</span>
      <h3>${escapeHtml(stage.name)}</h3>
      <dl>
        ${stage.fields.map(([label, field]) => `
          <dt>${escapeHtml(label)}</dt>
          <dd>${escapeHtml(row[field])}</dd>
        `).join("")}
      </dl>
    </article>
  `).join("");
}

function detailCard(title, content, lead = false) {
  return `
    <article class="detail-card">
      <h4>${escapeHtml(title)}</h4>
      <p class="${lead ? "lead" : ""}">${escapeHtml(content)}</p>
    </article>
  `;
}

function renderWatershedPoints(key) {
  const container = document.querySelector("#watershed-points");
  if (key !== "baiyangdian") {
    container.hidden = true;
    container.innerHTML = "";
    return;
  }

  const points = scenarioRows(key);
  container.hidden = false;
  container.innerHTML = `
    <h3>Watershed validation points</h3>
    <div class="point-grid">
      ${points.map((point) => `
        <article class="point-card">
          <strong>${escapeHtml(point.watershed_stage || point.scenario_name)}</strong>
          <span>${escapeHtml(point.scenario_name)}</span>
          <span>${escapeHtml(point.validation_status)}</span>
          <span>${escapeHtml(point.prioritised_response)}</span>
        </article>
      `).join("")}
    </div>
  `;
}

function renderSelectedScenario() {
  const config = SCENARIOS[selectedKey];
  const row = representative(selectedKey);
  renderRuntime(row);

  document.querySelector("#detail-header").innerHTML = `
    <div>
      <h3>${escapeHtml(config.label)}</h3>
      <p>${escapeHtml(config.location)} · ${escapeHtml(scaleFor(selectedKey, row))}</p>
    </div>
    ${badge(row.validation_status)}
  `;

  document.querySelector("#detail-grid").innerHTML = [
    detailCard("Evidence summary", `${safe(row.evidence_strength)} evidence · ${safe(row.source_basis)}. ${safe(row.uncertainty_notes)}`),
    detailCard("Validation summary", row.validation_summary),
    detailCard("Review recommendation", `${safe(row.review_action)}. Owner: ${safe(row.review_owner)}. ${safe(row.review_summary)}`),
    detailCard("Adaptive responses", `${safe(row.response_mode)}: ${safe(row.response_options)}`),
    detailCard("Prioritised response", `${safe(row.prioritised_response)} · ${safe(row.implementation_priority)} priority · ${safe(row.urgency_level)} urgency`, true),
    detailCard("Readiness notes", `${safe(row.recommendation_class)}. ${safe(row.prioritisation_summary)}`),
  ].join("");

  renderWatershedPoints(selectedKey);
}

function inlineMarkdown(text) {
  return text
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}

function markdownTable(lines) {
  const cells = lines.map((line) => line.split("|").slice(1, -1).map((cell) => cell.trim()));
  const headers = cells[0] || [];
  const body = cells.slice(2);
  return `<div class="table-wrap"><table><thead><tr>${headers.map((cell) => `<th>${inlineMarkdown(cell)}</th>`).join("")}</tr></thead><tbody>${body.map((row) => `<tr>${row.map((cell) => `<td>${inlineMarkdown(cell)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}

function renderMarkdown(markdown) {
  const lines = escapeHtml(markdown).replaceAll("\r\n", "\n").split("\n");
  const output = [];
  let index = 0;
  let inCode = false;
  let code = [];
  let listType = "";

  const closeList = () => {
    if (listType) output.push(`</${listType}>`);
    listType = "";
  };

  while (index < lines.length) {
    const line = lines[index];

    if (line.startsWith("```")) {
      closeList();
      if (inCode) {
        output.push(`<pre><code>${code.join("\n")}</code></pre>`);
        code = [];
      }
      inCode = !inCode;
      index += 1;
      continue;
    }
    if (inCode) {
      code.push(line);
      index += 1;
      continue;
    }

    if (line.startsWith("|") && lines[index + 1]?.match(/^\|[\s:|-]+\|$/)) {
      closeList();
      const tableLines = [];
      while (lines[index]?.startsWith("|")) {
        tableLines.push(lines[index]);
        index += 1;
      }
      output.push(markdownTable(tableLines));
      continue;
    }

    const heading = line.match(/^(#{1,4})\s+(.+)$/);
    if (heading) {
      closeList();
      const level = heading[1].length;
      output.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`);
      index += 1;
      continue;
    }

    const unordered = line.match(/^[-*]\s+(.+)$/);
    const ordered = line.match(/^\d+\.\s+(.+)$/);
    if (unordered || ordered) {
      const desired = unordered ? "ul" : "ol";
      if (listType !== desired) {
        closeList();
        output.push(`<${desired}>`);
        listType = desired;
      }
      output.push(`<li>${inlineMarkdown((unordered || ordered)[1])}</li>`);
      index += 1;
      continue;
    }

    closeList();
    if (line.trim()) output.push(`<p>${inlineMarkdown(line)}</p>`);
    index += 1;
  }
  closeList();
  return output.join("\n");
}

async function fetchText(path) {
  const response = await fetch(path);
  if (!response.ok) throw new Error(`Unable to load ${path} (${response.status})`);
  return response.text();
}

async function initialise() {
  const loadMessage = document.querySelector("#load-message");
  try {
    const [csv, validationMarkdown, capabilityMarkdown] = await Promise.all([
      fetchText(DATA_PATHS.matrix),
      fetchText(DATA_PATHS.validation),
      fetchText(DATA_PATHS.capability),
    ]);
    rows = parseCsv(csv);
    renderOverview();
    renderComparison();
    renderSelectedScenario();
    document.querySelector("#validation-document").innerHTML = renderMarkdown(validationMarkdown);
    document.querySelector("#capability-document").innerHTML = renderMarkdown(capabilityMarkdown);
    loadMessage.hidden = true;
  } catch (error) {
    loadMessage.classList.add("error");
    loadMessage.textContent = `${error.message}. Serve the repository root with a local static server so the dashboard can read the generated CSV and Markdown files.`;
    document.querySelector("#validation-document").textContent = "Validation report unavailable.";
    document.querySelector("#capability-document").textContent = "Capability map unavailable.";
  }
}

document.querySelector("#scenario-select").addEventListener("change", (event) => {
  selectedKey = event.target.value;
  renderSelectedScenario();
});

initialise();
