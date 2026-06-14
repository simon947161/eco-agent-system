# CCZPS-Lite Minimal Core Model and Output Consolidation Plan

## Planning Status

This document defines a future-facing conceptual model and consolidation
direction. It does not refactor runtime code, create consolidated outputs,
change schemas, remove or rename files, restructure the repository, or change
the dashboard.

The core question is:

> What is the smallest useful model of CCZPS-Lite?

The proposed answer is five objects:

```text
Scenario
Evidence
Hypothesis
Review
Report
```

These objects should become the stable conceptual backbone of future
CCZPS-Lite and ClimateOS development while detailed runtime artifacts remain
available for audit, testing, and specialist use.

## 1. Why Consolidation Is Needed

CCZPS-Lite has become operationally rich but structurally complex. Location
intake, governed meteorology retrieval, scenario runtimes, time-series storage,
trend readings, configured spatial context, hypotheses, validation interfaces,
review records, traceability, governance, comparison, reporting, dashboards,
release material, usage governance, and Budget Guard each serve a legitimate
purpose. Together, however, they present too many concepts to a normal user at
once.

Uncontrolled growth creates several risks:

- too many output files for users to identify the right starting point;
- too many dashboard sections competing for attention;
- repeated status fields that can appear authoritative or contradictory;
- overlapping Markdown reports that explain similar boundaries differently;
- difficulty describing the system without requiring knowledge of its runtime
  architecture;
- difficulty reusing the kernel for FarmerOS, GardenOS, WaterOS, ClimateOS,
  Building Climate OS, and Dryland Restoration OS;
- increased regression-test, documentation, release, and maintenance burden;
- greater risk that an internal artifact is mistaken for a user-facing
  conclusion.

The goal is not to delete existing work. Detailed artifacts preserve
provenance, testability, and audit value. The goal is to create a clearer
external model so users can understand the system through a small set of
durable concepts.

## 2. Current System State

CCZPS-Lite v0.5+ is a local, deterministic, evidence-based environmental
planning-support kernel. It organises scenario data, evidence, planning
hypotheses, validation needs, traceability, internal governance status,
comparison outputs, and human-readable reports. It is not a professional
approval system, engineering design tool, GIS platform, simulation engine, or
autonomous decision-maker.

The current system is best understood as a layered evidence and review
workflow. Its detailed files are useful to maintainers and reviewers, but the
file layout should not define the public mental model. Future external
interfaces should describe what the user has, what is known, what is being
tested, what review remains, and what report to read.

## 3. Minimal Core Model

The five objects are conceptual objects, not new Task 44 schemas. Existing
files may contribute to more than one object, but each should have one primary
role in the external model.

### 3.1 Scenario

**Definition:** the place, project, case, or environmental context being
considered.

A Scenario may include:

- location;
- scenario ID;
- status;
- intent;
- geographic context;
- workflow stage.

It maps from current items such as location intake profiles, scenario packs,
demonstration cases, and pilot cases.

Scenario answers:

```text
What place or case are we considering, and where is it in the workflow?
```

### 3.2 Evidence

**Definition:** what the system knows, where that knowledge came from, and how
strong or uncertain it is.

Evidence may include:

- meteorology;
- time series;
- trends;
- spatial profiles and configured transects;
- a future manually governed GIS / DEM profile;
- data source and provenance;
- confidence;
- uncertainty;
- evidence strength.

It maps from current meteorology evidence, meteorology trends, time-series
records, spatial transects, GIS / DEM plans, and evidence traceability.

Evidence answers:

```text
What observations or supporting records exist, and what are their limits?
```

### 3.3 Hypothesis

**Definition:** a testable planning assumption that connects a documented
problem to a possible intervention logic.

A Hypothesis may include:

- problem statement;
- planning assumption;
- intervention logic;
- expected effect;
- validation indicators;
- failure conditions.

It maps primarily from the current planning hypotheses.

Hypothesis answers:

```text
What assumption is being tested, and what evidence could support or reject it?
```

A hypothesis is not a recommendation, finding, design, or approval decision.

### 3.4 Review

**Definition:** the human, professional, validation, governance, and
approval-boundary status associated with a scenario and its evidence.

Review may include:

- expert review;
- professional validation;
- internal governance decision support;
- approval-support status;
- human review required;
- professional review required;
- unresolved gaps and limitations.

It maps from expert review records, the professional validation interface,
internal governance decision records, and planning approval support reports.

Review answers:

```text
Who must review this, what remains unresolved, and what authority is absent?
```

An internal review status must never be presented as statutory approval or
professional certification.

### 3.5 Report

**Definition:** a human-readable or machine-readable presentation assembled
from the other four objects.

A Report may include:

- dashboard views;
- Markdown reports;
- JSON summaries;
- release documents;
- demonstration and operator guides.

It maps from the human-readable dashboard, scenario comparison report, release
package, generated summaries, and maintained documentation.

Report answers:

```text
What should a particular audience read or exchange?
```

A Report presents existing information. It does not create new authority,
evidence, recommendations, or conclusions.

## 4. Existing File Mapping

The following mapping is a planning guide. "Internal" means the artifact
should remain available for runtime, audit, testing, or specialist inspection.
"Expose" means it may be shown directly to users during the transition; future
consolidated packs should become the preferred entry points.

| Current File | Current Purpose | Minimal Core Object | Keep As Internal Artifact? | Expose To Users? | Suggested Future Role |
| --- | --- | --- | --- | --- | --- |
| `cczps_lite/output/location_intake_profiles.json` | Preliminary location intake records | Scenario | Yes | Limited | Scenario source for new, intake-only cases |
| `cczps_lite/output/location_meteorology_evidence.json` | Governed meteorology for intake locations | Evidence | Yes | Through a pack | Evidence source linked to an intake Scenario |
| `cczps_lite/output/meteorology_evidence.json` | Current scenario observation records | Evidence | Yes | Through a pack | Observation section of the Evidence Review Pack |
| `cczps_lite/output/meteorology_timeseries.json` | Stored meteorology observations over time | Evidence | Yes | Specialist only | Detailed evidence store and audit source |
| `cczps_lite/output/meteorology_trends.json` | Deterministic trend readings | Evidence | Yes | Through a pack | Bounded trend summary with uncertainty |
| `cczps_lite/output/spatial_transects.json` | Configured spatial relationship records | Evidence | Yes | Specialist only | Detailed configured spatial evidence |
| `cczps_lite/output/spatial_transect_scenario_pack.json` | Scenario-oriented spatial context | Evidence | Yes | Through a pack | Spatial context section with validation limits |
| `cczps_lite/output/planning_hypotheses.json` | Testable planning assumptions | Hypothesis | Yes | Yes, summarised | Canonical hypothesis source |
| `cczps_lite/output/gis_dem_access_plan.json` | Future GIS / DEM access and governance plan | Evidence | Yes | Specialist only | Evidence-gap and future acquisition plan |
| `cczps_lite/output/professional_validation_interface.json` | Professional validation template and status | Review | Yes | Through a pack | Professional review requirements and state |
| `cczps_lite/output/expert_review_records.json` | Human-authored expert review templates or records | Review | Yes | Through a pack | Expert review evidence and completion state |
| `cczps_lite/output/planning_approval_support_report.json` | Approval-boundary support summary | Review | Yes | Through a pack | Explicit authority boundary and unresolved needs |
| `cczps_lite/output/evidence_traceability.json` | Links outputs to supporting evidence | Evidence | Yes | Specialist only | Audit appendix and provenance index |
| `cczps_lite/output/governance_decision_records.json` | Internal governance decision support | Review | Yes | Through a pack | Internal status, required actions, and limitations |
| `cczps_lite/output/scenario_comparison.json` | Cross-scenario evidence and review comparison | Report | Yes | Yes, summarised | Optional portfolio or multi-scenario report |
| `cczps_lite/output/scenario_report.md` | Human-readable scenario report | Report | Yes | Transitional | Input to a consolidated Scenario Summary Pack |
| `cczps_lite/output/scenario_validation_pack.md` | Validation-oriented scenario summary | Review | Yes | Transitional | Review appendix or source material |
| `cczps_lite/output/governance_summary.md` | Governance summary | Report | Yes | Transitional | Input to a Governance Review Pack |
| `cczps_lite/output/runtime_capability_map.md` | Detailed capability and readiness map | Report | Yes | Maintainers and auditors | Technical appendix, not a normal-user start page |
| `cczps_lite/dashboard/index.html` and dashboard assets | Static presentation of local generated outputs | Report | Yes | Yes | Simplified five-question user interface |
| `docs/05_RELEASE/*` and release-package documents | Release scope, validation, limitations, and usage guidance | Report | Yes | Yes | Versioned release and audit package |
| `docs/06_ROADMAP/*` | Future direction and capability planning | Report | Yes | Selected documents | Maintainer roadmap, separate from current capability claims |

Markdown companions to JSON files should continue to support inspection and
accessibility during the transition. Future consolidation should avoid
silently changing their meaning or treating duplicate wording as a new source
of truth.

## 5. Proposed External Output Consolidation

Future work should reduce the default external surface to three main packages.
These packages should be deterministic views assembled from existing internal
artifacts. They should carry source references, generation metadata,
limitations, and explicit missing-data states.

Task 44 does not implement these files.

### 5.1 Scenario Summary Pack

**Audience:** normal users, project participants, demonstration users, and
first-time reviewers.

**Purpose:**

> Explain what the scenario is, what the system currently knows, what it cannot
> conclude, and what human review is required.

Potential future files:

```text
cczps_lite/output/consolidated/scenario_summary_pack.json
cczps_lite/output/consolidated/scenario_summary_pack.md
```

Suggested contents:

- Scenario identity, location, intent, and workflow stage;
- concise Evidence summary and major gaps;
- current Hypothesis summary;
- Review status and authority boundary;
- links to relevant technical or governance reports.

This should be the primary normal-user entry point.

### 5.2 Evidence Review Pack

**Audience:** planners, researchers, consultants, technical reviewers, and
professional validators.

**Purpose:**

> Combine meteorology, spatial context, trends, evidence traceability,
> uncertainty, and validation needs.

Potential future files:

```text
cczps_lite/output/consolidated/evidence_review_pack.json
cczps_lite/output/consolidated/evidence_review_pack.md
```

Suggested contents:

- observation sources and dates;
- meteorology and time-series summaries;
- bounded trend readings;
- configured spatial context;
- evidence strength, confidence, and uncertainty;
- traceability references;
- missing data and validation requirements.

It must distinguish observed, configured, derived, planned, missing, and
unreviewed information.

### 5.3 Governance Review Pack

**Audience:** project owners, internal governance teams, funders, councils, and
review coordinators.

**Purpose:**

> Combine internal governance status, expert review status, approval boundary,
> next actions, and limitations.

Potential future files:

```text
cczps_lite/output/consolidated/governance_review_pack.json
cczps_lite/output/consolidated/governance_review_pack.md
```

Suggested contents:

- internal governance status;
- human and professional review requirements;
- expert review completion state;
- approval-support boundary;
- unresolved risks and evidence gaps;
- review coordination actions;
- links to supporting evidence.

"Next actions" in this pack should mean review and evidence-completion actions,
not implementation recommendations.

## 6. Internal vs External Outputs

### Internal Artifacts

Internal artifacts support deterministic runtime behavior, audit, provenance,
testing, debugging, specialist review, and backward compatibility. They may
remain detailed and numerous. Internal names can reflect technical ownership,
provided their status and source relationships remain clear.

Examples include raw or detailed time series, traceability records, configured
transects, governance records, validation templates, cache records, and
machine-readable runtime outputs.

### External Demonstration Outputs

External outputs should be simple, readable, audience-specific, and limited in
number. They should explain the five core objects without requiring users to
understand the runtime chain or browse many JSON files.

The governing principle is:

> Keep detailed runtime outputs for audit and testing. Expose simplified
> consolidated packs for users.

Consolidation should be additive before it is subtractive. Existing artifacts
should not be removed until a later task establishes compatibility,
traceability, migration guidance, and sufficient test coverage.

## 7. Dashboard Simplification Direction

The current dashboard provides useful visibility across many runtime layers,
but the future default experience should focus on five questions:

```text
What is the scenario?
What evidence exists?
What hypothesis is being tested?
What review is required?
What report should be read?
```

The dashboard should:

- lead with a Scenario Summary Pack;
- progressively disclose Evidence, Hypothesis, and Review detail;
- direct technical users to an Evidence Review Pack;
- direct governance users to a Governance Review Pack;
- keep uncertainty, missing data, provenance, and authority boundaries visible;
- retain access to technical artifacts without making them the default view.

The dashboard should not become a raw JSON explorer. It should not duplicate
every internal status field, invent new analysis, trigger browser-side external
services, or imply that visual prominence changes evidentiary weight.

Task 44 makes no dashboard change.

## 8. Future Refactor Roadmap

Refactoring should be incremental, additive, and reversible.

### Task 45 - Scenario Summary Pack Builder

Define and build a deterministic Scenario Summary Pack from existing outputs,
with provenance and compatibility tests.

### Task 46 - Evidence Review Pack Builder

Consolidate meteorology, trends, spatial context, traceability, uncertainty,
and validation needs without changing source artifacts.

### Task 47 - Governance Review Pack Builder

Consolidate governance, professional validation, expert review, approval
boundary, limitations, and review-coordination actions.

### Task 48 - Dashboard Simplification

Reorganise the dashboard around the five core questions and three consolidated
packs while retaining access to technical detail.

### Task 49 - Minimal Core Schema Definitions

Define versioned schemas and relationships for Scenario, Evidence, Hypothesis,
Review, and Report after the pack builders reveal stable shared fields.

### Task 50 - v0.6 Minimal Core Release

Publish migration guidance, compatibility commitments, consolidated examples,
release validation, and a clear statement of retained internal artifacts.

No major file deletion, renaming, or repository restructuring should occur
until these stages demonstrate that the consolidated model preserves
traceability, tests, and user needs.

## 9. Relationship to Application Layers

The five-object model allows application products to share one kernel while
using domain-specific evidence and language.

| Core Object | FarmerOS | GardenOS | WaterOS | ClimateOS | Building Climate OS | Dryland Restoration OS |
| --- | --- | --- | --- | --- | --- | --- |
| Scenario | Farm or paddock | Garden or site | Watershed or water project | Town, region, or climate case | Building or precinct site | Restoration site or catchment |
| Evidence | Soil, weather, crop, water, sensor data | Soil, shade, water, vegetation data | Flow, rainfall, storage, quality, spatial data | Climate, land, water, vegetation, spatial data | Weather, envelope, energy, comfort, site data | Rainfall, soil, runoff, vegetation, erosion data |
| Hypothesis | Management or production assumption | Planting or microclimate assumption | Water-management assumption | Adaptation or resilience assumption | Passive-design or operation assumption | Restoration or runoff-harvesting assumption |
| Review | Farmer, agronomist, regulator, governance review | Gardener, designer, specialist review | Hydrologist, council, regulator, community review | Expert, professional, governance review | Architect, engineer, certifier, owner review | Ecologist, soil, water, landholder review |
| Report | Farm action or audit pack | Garden plan or care pack | Watershed evidence or review pack | Dashboard, evidence pack, governance pack | Site review or performance pack | Restoration evidence or monitoring pack |

The common mapping is:

```text
Scenario = farm / garden / watershed / town / building site
Evidence = sensor, climate, soil, water, vegetation, spatial data
Hypothesis = proposed intervention or management assumption
Review = human / expert / governance review
Report = dashboard, action pack, audit pack
```

Here, an "action pack" may organise human-approved actions; the kernel must not
autonomously generate authoritative recommendations. Domain products may add
specialist interfaces, but they should preserve the same evidence, review, and
authority boundaries.

## 10. Safety Boundaries

Consolidation changes presentation and conceptual organisation, not system
authority. CCZPS-Lite remains:

- local-first;
- deterministic;
- evidence-based;
- human-review-centered;
- not ready for statutory approval;
- not a professional certification system;
- not an engineering design tool;
- not a GIS platform or DEM-processing runtime;
- not a simulation engine;
- not an autonomous decision-maker.

Future consolidated packs must not hide missing evidence, flatten uncertainty,
convert internal governance status into external approval, or turn hypotheses
into recommendations. Source artifacts and traceability references should
remain accessible so every summary can be audited.

## Decision Summary

The smallest useful model of CCZPS-Lite is:

1. **Scenario** - the case being considered.
2. **Evidence** - what is known and how it is supported.
3. **Hypothesis** - the testable assumption.
4. **Review** - the human and authority boundary.
5. **Report** - the audience-specific presentation.

Detailed runtime outputs should remain internal artifacts. Future user-facing
work should converge on a Scenario Summary Pack, Evidence Review Pack, and
Governance Review Pack. This approach simplifies the external system without
discarding the auditability, governance, and test coverage already built.
