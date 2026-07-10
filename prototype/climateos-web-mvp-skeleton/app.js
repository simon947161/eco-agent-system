(function () {
  var data = window.climateOsMockData;

  function text(value) {
    return value === undefined || value === null ? "" : String(value);
  }

  function metric(label, value) {
    return '<article class="metric"><h3>' + text(label) + '</h3><p>' + text(value) + '</p></article>';
  }

  function fields(record, keys) {
    return '<dl class="field-list">' + keys.map(function (key) {
      return '<div><dt>' + text(key.label) + '</dt><dd>' + text(record[key.field]) + '</dd></div>';
    }).join("") + '</dl>';
  }

  function card(record, titleField, statusField, keys, statusClass) {
    var status = text(record[statusField]);
    var labelClass = statusClass || (status.toLowerCase().indexOf("stop") >= 0 || status.toLowerCase().indexOf("blocked") >= 0 ? "block" : "warn");
    return '<article class="record-card"><header><h3>' + text(record[titleField]) + '</h3><span class="label ' + labelClass + '">' + status + '</span></header>' + fields(record, keys) + '</article>';
  }

  function renderCaseSummary() {
    var html = Object.keys(data.caseSummary).map(function (key) {
      return metric(key, data.caseSummary[key]);
    }).join("");
    document.getElementById("case-summary").innerHTML = html;

    document.getElementById("workflow-rail").innerHTML = data.workflow.map(function (step) {
      return '<article class="workflow-step"><strong>' + text(step[0]) + '</strong><span>' + text(step[1]) + '</span></article>';
    }).join("");
  }

  function renderRecordLists() {
    document.getElementById("sources").innerHTML = data.sources.map(function (record) {
      return card(record, "id", "retrieval", [
        { label: "Title", field: "title" },
        { label: "Publisher", field: "publisher" },
        { label: "Language", field: "language" },
        { label: "Caution", field: "caution" }
      ]);
    }).join("");

    document.getElementById("signals").innerHTML = data.signals.map(function (record) {
      return card(record, "id", "status", [
        { label: "Label", field: "label" },
        { label: "Sources", field: "sources" },
        { label: "Claims", field: "linkedClaims" }
      ]);
    }).join("");

    document.getElementById("claims").innerHTML = data.claims.map(function (record) {
      return card(record, "id", "review", [
        { label: "Candidate", field: "statement" },
        { label: "Sources", field: "linkedSources" },
        { label: "KO", field: "linkedKO" },
        { label: "Warning", field: "warning" }
      ]);
    }).join("");

    document.getElementById("knowledge-objects-list").innerHTML = data.knowledgeObjects.map(function (record) {
      return card(record, "id", "status", [
        { label: "Type", field: "type" },
        { label: "Sources", field: "sources" },
        { label: "Claims", field: "claims" },
        { label: "Evidence", field: "evidence" }
      ]);
    }).join("");

    document.getElementById("evidence").innerHTML = data.evidence.map(function (record) {
      return card(record, "id", "readiness", [
        { label: "Source", field: "source" },
        { label: "Claim", field: "claim" },
        { label: "KO", field: "ko" },
        { label: "Risk", field: "risk" },
        { label: "Note", field: "note" }
      ]);
    }).join("");

    document.getElementById("risk-flags-list").innerHTML = data.risks.map(function (record) {
      return card(record, "id", "stop", [
        { label: "Risk", field: "risk" },
        { label: "Trigger", field: "trigger" },
        { label: "Handling", field: "handling" }
      ], "block");
    }).join("");

    document.getElementById("human-review-list").innerHTML = data.humanReviews.map(function (record) {
      return card(record, "id", "status", [
        { label: "Need", field: "need" },
        { label: "Linked", field: "linked" },
        { label: "Action", field: "action" }
      ]);
    }).join("");

    document.getElementById("founder-gate-list").innerHTML = data.founderGates.map(function (record) {
      return card(record, "id", "status", [
        { label: "Need", field: "need" },
        { label: "Trigger", field: "trigger" },
        { label: "Required", field: "required" }
      ], "block");
    }).join("");

    document.getElementById("archive-summary").innerHTML = Object.keys(data.archive).map(function (key) {
      return metric(key, data.archive[key]);
    }).join("");
  }

  function renderReadiness() {
    var headers = ["Source", "Signal", "Claim", "KO", "Evidence", "Readiness", "Risk", "Human Review", "Founder Gate", "Stop point"];
    var rows = data.readiness.map(function (row) {
      return "<tr>" + row.map(function (cell) {
        return "<td>" + text(cell) + "</td>";
      }).join("") + "</tr>";
    }).join("");
    document.getElementById("readiness-table").innerHTML = "<thead><tr>" + headers.map(function (header) {
      return "<th>" + header + "</th>";
    }).join("") + "</tr></thead><tbody>" + rows + "</tbody>";
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
      });
    });
  }

  renderCaseSummary();
  renderRecordLists();
  renderReadiness();
  bindNavigation();
}());
