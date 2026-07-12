(function () {
  function text(value) {
    return value === undefined || value === null ? "" : String(value);
  }

  function shown(value) {
    return value === undefined || value === null || value === "" ? "Not provided" : text(value);
  }

  function localDateTime(value) {
    if (!value) { return "Not provided"; }
    var parsed = new Date(value);
    return isNaN(parsed.getTime()) ? text(value) : parsed.toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" });
  }

  function splitList(value) {
    return text(value).split(",").map(function (item) {
      return item.trim();
    }).filter(Boolean);
  }

  function el(tag, className, content) {
    var node = document.createElement(tag);
    if (className) {
      node.className = className;
    }
    if (content !== undefined) {
      node.textContent = text(content);
    }
    return node;
  }

  async function api(path, options) {
    var response = await fetch(path, options);
    var payload = await response.json().catch(function () {
      return {};
    });
    if (!response.ok) {
      throw new Error(payload.detail || "Local prototype request failed");
    }
    return payload;
  }

  function field(label, value) {
    var row = el("div");
    row.appendChild(el("dt", "", label));
    row.appendChild(el("dd", "", shown(value)));
    return row;
  }

  function card(record) {
    var article = el("article", "record-card");
    var header = el("header");
    header.appendChild(el("h3", "", record.id));
    var label = el("span", "label", record.status || record.event_type || record.decision_status);
    if (text(label.textContent).toLowerCase().indexOf("blocked") >= 0 || text(label.textContent).toLowerCase().indexOf("gate") >= 0) {
      label.classList.add("block");
    }
    header.appendChild(label);
    article.appendChild(header);
    var list = el("dl", "field-list");
    [
      ["Title", record.title],
      ["Type", record.record_type],
      ["Readiness", record.readiness_label],
      ["Risk", (record.risk_flags || []).join(", ")],
      ["Boundary", record.boundary_label],
      ["Declared actor", record.actor_label || record.reviewer_label],
      ["Created (local time)", localDateTime(record.created_at || record.timestamp)]
    ].forEach(function (item) {
      if (item[1]) {
        list.appendChild(field(item[0], item[1]));
      }
    });
    article.appendChild(list);
    var responsibility = el("p", "responsibility-note", "Candidate only. A declared human remains responsible for review and use.");
    article.appendChild(responsibility);
    return article;
  }

  function readable(containerId, payload) {
    var container = document.getElementById(containerId);
    container.replaceChildren();
    var heading = el("h3", "", "Readable summary");
    container.appendChild(heading);
    var preview = el("pre", "readable-preview", JSON.stringify(payload, null, 2));
    container.appendChild(preview);
  }

  async function loadCandidates() {
    var list = document.getElementById("candidate-list");
    list.replaceChildren();
    var records = await api("/api/candidates");
    records.forEach(function (record) {
      list.appendChild(card(record));
    });
  }

  async function loadAudit() {
    var list = document.getElementById("audit-list");
    list.replaceChildren();
    var records = await api("/api/audit-events");
    records.forEach(function (record) {
      list.appendChild(card(record));
    });
  }

  function bindNavigation() {
    var buttons = Array.prototype.slice.call(document.querySelectorAll(".side-nav button"));
    var screens = Array.prototype.slice.call(document.querySelectorAll(".screen"));
    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        var target = button.getAttribute("data-target");
        buttons.forEach(function (item) {
          item.classList.toggle("active", item === button);
        });
        screens.forEach(function (screen) {
          screen.classList.toggle("active-screen", screen.id === target);
        });
        if (target === "audit") {
          loadAudit().catch(window.alert);
        }
      });
    });
    document.querySelectorAll("[data-go-to]").forEach(function (control) {
      control.addEventListener("click", function () {
        var target = document.querySelector('.side-nav button[data-target="' + control.getAttribute("data-go-to") + '"]');
        if (target) { target.click(); target.focus(); }
      });
    });
  }

  function bindForms() {
    document.getElementById("create-form").addEventListener("submit", async function (event) {
      event.preventDefault();
      var form = new FormData(event.target);
      var payload = {
        record_type: form.get("record_type"),
        title: form.get("title"),
        summary: form.get("summary") || "",
        risk_flags: splitList(form.get("risk_flags"))
      };
      var created = await api("/api/candidates", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      document.getElementById("create-result").textContent = "Created " + created.id;
      event.target.reset();
      await loadCandidates();
    });

    document.getElementById("review-form").addEventListener("submit", async function (event) {
      event.preventDefault();
      var form = new FormData(event.target);
      var recordId = form.get("record_id");
      var payload = {
        new_status: form.get("new_status"),
        reviewer_label: form.get("reviewer_label"),
        reason: form.get("reason")
      };
      var updated = await api("/api/candidates/" + encodeURIComponent(recordId) + "/review-transition", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      document.getElementById("review-result").textContent = "Recorded manual transition for " + updated.id;
      await loadCandidates();
    });

    document.getElementById("founder-form").addEventListener("submit", async function (event) {
      event.preventDefault();
      var form = new FormData(event.target);
      var payload = {
        gate_trigger: form.get("gate_trigger"),
        affected_record_ids: splitList(form.get("affected_record_ids")),
        decision_date: form.get("decision_date"),
        decision_status: form.get("decision_status"),
        founder_instruction_text: form.get("founder_instruction_text")
      };
      var created = await api("/api/founder-gates", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      document.getElementById("founder-result").textContent = "Recorded Founder Gate " + created.id;
    });

    document.getElementById("archive-form").addEventListener("submit", async function (event) {
      event.preventDefault();
      var form = new FormData(event.target);
      var payload = {
        case_id: form.get("case_id"),
        reviewer_label: form.get("reviewer_label"),
        reason: form.get("reason")
      };
      var exported = await api("/api/archive/export", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      document.getElementById("archive-result").textContent = "Created local archive: " + exported.bundle_dir;
    });
  }

  function bindModelBridge() {
    var box = document.getElementById("model-json");
    document.getElementById("prompt-bundle-button").addEventListener("click", async function () {
      var bundle = await api("/api/model/prompt-bundle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: "[]"
      });
      box.value = JSON.stringify(bundle, null, 2);
      readable("model-readable", bundle);
    });
    document.getElementById("mock-response-button").addEventListener("click", async function () {
      var response = await api("/api/model/mock-response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: "[]"
      });
      box.value = JSON.stringify(response, null, 2);
      readable("model-readable", response);
    });
    document.getElementById("import-response-button").addEventListener("click", async function () {
      var imported = await api("/api/model/import-response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: box.value
      });
      document.getElementById("model-result").textContent = "Imported " + imported.length + " suggestion(s). Human decision still required.";
    });
  }

  function bindAlphaReview() {
    var box = document.getElementById("alpha-json");
    [
      ["alpha-capabilities-button", "/api/alpha/capabilities"],
      ["alpha-domains-button", "/api/alpha/domains"],
      ["alpha-scenarios-button", "/api/alpha/synthetic-scenarios"],
      ["alpha-evidence-button", "/api/alpha/evidence-contracts"],
      ["alpha-audit-button", "/api/alpha/audit-events"]
    ].forEach(function (binding) {
      document.getElementById(binding[0]).addEventListener("click", async function () {
        var payload = await api(binding[1]);
        box.value = JSON.stringify(payload, null, 2);
        readable("alpha-readable", payload);
      });
    });

    document.getElementById("alpha-create-form").addEventListener("submit", async function (event) {
      event.preventDefault();
      var form = new FormData(event.target);
      var payload = {
        title: form.get("title"),
        domain: form.get("domain"),
        object_type: "synthetic_observation_candidate",
        summary: form.get("summary"),
        source_refs: ["LOCAL-USE-TRIAL-FIXTURE"],
        provenance: "Generated locally for a synthetic Founder-controlled use trial; no external or live source.",
        assumptions: ["Demonstration only", "No real-world inference"],
        uncertainty: form.get("uncertainty"),
        permissions: "synthetic/public-safe fixture",
        human_review_required: true
      };
      var created = await api("/api/alpha/evidence-contracts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      document.getElementById("alpha-create-result").textContent = "Created " + created.id + ". Candidate only; no truth or approval claim.";
      document.querySelector("#alpha-review-form [name=record_id]").value = created.id;
      box.value = JSON.stringify(created, null, 2);
      readable("alpha-readable", created);
    });

    document.getElementById("alpha-review-form").addEventListener("submit", async function (event) {
      event.preventDefault();
      var form = new FormData(event.target);
      var recordId = form.get("record_id");
      var payload = {
        action: form.get("action"),
        reviewer_label: form.get("reviewer_label"),
        reason: form.get("reason")
      };
      if (payload.action === "correct") {
        payload.correction_summary = form.get("correction_summary");
      }
      var reviewed = await api("/api/alpha/evidence-contracts/" + encodeURIComponent(recordId) + "/review-actions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      document.getElementById("alpha-review-result").textContent = "Recorded " + payload.action + " by a declared local label. Human responsibility remains; no conclusion was issued.";
      box.value = JSON.stringify(reviewed, null, 2);
      readable("alpha-readable", reviewed);
    });
  }

  bindNavigation();
  bindForms();
  bindModelBridge();
  bindAlphaReview();
  loadCandidates().catch(window.alert);
}());
