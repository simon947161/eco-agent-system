window.climateOsMockData = {
  caseSummary: {
    "Case ID": "CASE-MOCK-001",
    "Case label": "Xiong'an-Baiyangdian Evidence Passport skeleton case",
    "Sprint": "Task421-480",
    "Status": "Static mock review case",
    "Public use": "Not authorized",
    "Operational status": "Not operational"
  },
  workflow: [
    ["Source", "Candidate source metadata only"],
    ["Signal", "Candidate signal grouping only"],
    ["Claim", "Provisional claim candidate only"],
    ["Knowledge Object", "Candidate grouping only"],
    ["Evidence", "Evidence candidate only"],
    ["Human Review", "Required control, not automated"],
    ["Founder Gate", "Required before future escalation"],
    ["Archive", "Static closure trail only"]
  ],
  sources: [
    {
      id: "S001",
      title: "Official source candidate placeholder",
      publisher: "Public institution placeholder",
      language: "Chinese / English review needed",
      retrieval: "Needs source verification",
      caution: "Candidate only"
    },
    {
      id: "S003",
      title: "Planning or governance source candidate",
      publisher: "Regional context placeholder",
      language: "Translation review needed",
      retrieval: "Needs human review",
      caution: "Do not externalize without review"
    },
    {
      id: "S007-S008",
      title: "Event discovery source candidates",
      publisher: "News or tertiary source placeholder",
      language: "Scope review needed",
      retrieval: "Candidate only",
      caution: "Do not infer local resilience outcome"
    }
  ],
  signals: [
    {
      id: "SIG-001",
      label: "Water and regional planning signal candidate",
      sources: "S001, S002, S003",
      linkedClaims: "CC-001, CC-002, CC-003",
      status: "Needs review"
    },
    {
      id: "SIG-003",
      label: "Restoration or water condition signal candidate",
      sources: "S004-S006",
      linkedClaims: "CC-004",
      status: "Stop before conclusion"
    },
    {
      id: "SIG-005",
      label: "MVP requirements insight signal",
      sources: "S001-S011",
      linkedClaims: "CC-006",
      status: "Requirements insight only"
    }
  ],
  claims: [
    {
      id: "CC-001",
      statement: "Planning context candidate claim",
      linkedSources: "S001, S009",
      linkedKO: "KO-004",
      review: "Needs source verification",
      warning: "No claim validation"
    },
    {
      id: "CC-004",
      statement: "Water / restoration candidate claim",
      linkedSources: "S004-S006",
      linkedKO: "KO-003",
      review: "Blocked before conclusion",
      warning: "Do not draw water or restoration conclusion"
    },
    {
      id: "CC-006",
      statement: "MVP requirements candidate insight",
      linkedSources: "S001-S011",
      linkedKO: "KO-005",
      review: "Architecture consideration only",
      warning: "No runtime or implementation authorization"
    }
  ],
  knowledgeObjects: [
    {
      id: "KO-001",
      type: "Context candidate",
      sources: "S001, S002, S003",
      claims: "CC-001, CC-002, CC-003",
      evidence: "EC-001, EC-002, EC-003",
      status: "Needs human review"
    },
    {
      id: "KO-003",
      type: "Risk-sensitive candidate",
      sources: "S004-S006",
      claims: "CC-004",
      evidence: "EC-004",
      status: "Stop before conclusion"
    },
    {
      id: "KO-005",
      type: "Requirements insight candidate",
      sources: "S001-S011",
      claims: "CC-006",
      evidence: "EC-007",
      status: "Ready for architecture consideration"
    }
  ],
  evidence: [
    {
      id: "EC-001",
      source: "S001",
      claim: "CC-001",
      ko: "KO-001",
      readiness: "Needs source verification",
      risk: "RF-001",
      note: "Candidate evidence only"
    },
    {
      id: "EC-004",
      source: "S004-S006",
      claim: "CC-004",
      ko: "KO-003",
      readiness: "Needs source verification",
      risk: "RF-001, RF-006",
      note: "Do not draw water / restoration conclusion"
    },
    {
      id: "EC-007",
      source: "S001-S011",
      claim: "CC-006",
      ko: "KO-005",
      readiness: "Ready for architecture consideration",
      risk: "RF-001, RF-002, RF-006",
      note: "Requirements insight only"
    }
  ],
  readiness: [
    ["S001", "SIG-001, SIG-004", "CC-001", "KO-001, KO-004", "EC-001", "Needs source verification", "RF-001", "HR-001", "FG-001", "Do not use as final evidence"],
    ["S003", "SIG-001", "CC-003", "KO-001", "EC-003", "Needs human review", "RF-002", "HR-002", "FG-002", "Do not publish or externalize"],
    ["S004-S006", "SIG-003", "CC-004", "KO-003", "EC-004", "Needs source verification", "RF-001, RF-006", "HR-001, HR-004", "FG-003", "Do not draw water / restoration conclusion"],
    ["S001-S011", "SIG-005", "CC-006", "KO-005", "EC-007", "Ready for architecture consideration", "RF-001, RF-002, RF-006", "HR-001, HR-002", "FG-001", "Requirements insight only"]
  ],
  risks: [
    {
      id: "RF-001",
      risk: "Source verification risk",
      trigger: "Official or candidate citation path not directly verified",
      handling: "Human source review before future use",
      stop: "Block final evidence status"
    },
    {
      id: "RF-004",
      risk: "Compliance / ESG overclaim risk",
      trigger: "Wording implying compliance, ESG performance, assurance, or certification",
      handling: "Remove wording or escalate to Founder Gate",
      stop: "Block conclusion"
    },
    {
      id: "RF-008",
      risk: "Runtime creep risk",
      trigger: "Drift toward runtime, API, database, MCP, automation, or implementation",
      handling: "Reframe as question or defer",
      stop: "Block future-work execution"
    }
  ],
  humanReviews: [
    {
      id: "HR-001",
      need: "Source identity and retrieval review",
      linked: "S001, S002, S004-S006, EC-001, EC-002, EC-004",
      action: "Confirm source identity, date, URL, and publication context before future use",
      status: "Open for future review"
    },
    {
      id: "HR-002",
      need: "Language and translation review",
      linked: "S003, CC-003, KO-001",
      action: "Review source language and paraphrase boundaries",
      status: "Open for future review"
    },
    {
      id: "HR-005",
      need: "Source conflict / scope review",
      linked: "S007-S011, EC-005, EC-006",
      action: "Confirm scope and prevent overclaim",
      status: "Open for future review"
    }
  ],
  founderGates: [
    {
      id: "FG-002",
      need: "Public / partner use",
      trigger: "Any external reader, partner, public communication, or public case framing",
      required: "Founder review and approval of external-use boundary",
      status: "Not opened"
    },
    {
      id: "FG-003",
      need: "Conclusion-risk escalation",
      trigger: "Compliance, assurance, certification, ESG, carbon, standards, framework, scoring, water restoration success, or resilience conclusion",
      required: "Block unless a separate Founder-authorized future scope permits a reviewed path",
      status: "Not opened"
    },
    {
      id: "FG-004",
      need: "Operational Evidence Passport",
      trigger: "Runtime, API, database, MCP, n8n, QCloud, automation, implementation, or operational Evidence Passport proposal",
      required: "Separate future authorization",
      status: "Not opened"
    }
  ],
  archive: {
    "Documentation package": "docs/tasks/task421_480_climateos_web_mvp_skeleton/",
    "Static skeleton": "prototype/climateos-web-mvp-skeleton/",
    "Closure packet": "TASK471_480_WEB_SKELETON_CLOSURE_PACKET.md",
    "Task481": "Not started",
    "Deployment": "Not created",
    "Boundary": "Founder review required before future backend/data/model-adapter sprint"
  }
};
