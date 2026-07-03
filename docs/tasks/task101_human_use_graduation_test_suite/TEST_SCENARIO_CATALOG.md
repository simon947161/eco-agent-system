# Test Scenario Catalog

## Purpose

This document describes the compact first-pass scenario set for Task101 Human Use Graduation.

Each scenario is a test design — a structured environmental judgment situation used to evaluate whether the frozen ClimateOS Foundation can support real environmental project judgment.

Scenarios are not validated environmental conclusions. They are designed to test the Foundation's judgment logic.

## Scenario Design Principles

Each scenario is designed to:

1. **Represent a real environmental judgment situation** — the kind that environmental planners, engineers, scientists, or community governance participants face
2. **Exercise all five Task100 graduation checks** — Reality, Evidence, Validation, Governance, Inheritance
3. **Be bounded** — each scenario has a clear scope, a specific environmental object, and a defined judgment question
4. **Be human-reviewable** — no specialized technical knowledge required beyond domain expertise

## Scenario Coverage Matrix

| ID | Scenario | Domain | Judgment Type | Reality | Evidence | Validation | Governance | Inheritance |
|----|----------|--------|--------------|---------|---------|-----------|-----------|------------|
| CarbonOS-01 | Carbon Claim / ESG Disclosure | CarbonOS | Disclosure readiness | ✓ | ✓ | ✓ | ✓ | ✓ |
| WaterOS-01 | Drainage / Stormwater Risk | WaterOS | Risk assessment | ✓ | ✓ | ✓ | ✓ | ✓ |
| EnergyOS-01 | Community Energy Project | EnergyOS | Project viability | ✓ | ✓ | ✓ | ✓ | ✓ |
| BuildingOS-01 | Building Module / Interface | BuildingOS | Interface compliance | ✓ | ✓ | ✓ | ✓ | ✓ |
| ClimateData-01 | NASA/BOM Observation | Climate Data | Observation interpretation | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## CarbonOS-01: Carbon Claim / ESG Disclosure

**Domain:** CarbonOS  
**Judgment Type:** Carbon claim readiness / ESG disclosure assessment  
**Complexity:** Medium  
**Environmental Object:** A specific carbon sequestration project on a defined land parcel

### Scenario Description

An organization has developed a carbon sequestration project on a parcel of rural land. The project claims 10,000 tCO2e sequestration per year based on vegetation growth measurements. The organization wants to prepare an ESG disclosure or carbon credit claim.

The task is to use the ClimateOS Foundation to assess whether the claim is sufficiently evidenced, validated, and governed for a responsible party to make a judgment.

### Judgment Question

```
Is the carbon sequestration claim sufficiently evidenced, validated,
and governed for a responsible party to issue or recommend
an ESG disclosure or carbon credit claim?
```

### Environmental Object

A defined rural land parcel with vegetation cover. The parcel has known soil type, climate zone, and prior land use history.

### Key Judgment Dimensions

**Reality Test:**
- Can the Foundation identify the specific environmental object (the land parcel, the vegetation type)?
- Is the sequestration activity described with enough specificity to be measurable?

**Evidence Test:**
- Can the Foundation trace the claim from raw measurement data to observation to inference to evidence to claim?
- Is the measurement methodology documented and distinguishable from the inference?

**Validation Test:**
- Does the Foundation assess the source reliability of the carbon measurements?
- Does it evaluate time validity (is the measurement period appropriate)?
- Does it evaluate spatial fit (does the measurement cover the claimed area)?
- Does it identify conflicting evidence (e.g., prior land use disturbance)?
- Does it assign a confidence level?

**Governance Test:**
- Is a responsible party identified for the judgment?
- Is the governance boundary defined — who can approve the claim vs. who can dispute it?
- Is human review required before the disclosure is issued?

**Inheritance Test:**
- Could WaterOS, EnergyOS, or BuildingOS apply the same evidence → validation → governance logic to their domain scenarios?
- Is the judgment pattern domain-agnostic?

### Bounded Scope

- This scenario tests the Foundation's carbon claim judgment logic.
- It does not validate the specific carbon sequestration measurement.
- It does not determine the market value of the carbon credits.
- The ESG disclosure standard (ISSB, TNFD, etc.) is treated as external context — the scenario tests whether the Foundation can work with such standards, not whether it mandates them.

### Pass Criterion

The scenario passes if a human reviewer can trace the judgment from:
1. Environmental object (land parcel) → 
2. Evidence chain (measurement → observation → inference → evidence → claim) →
3. Validation assessment (source, time, space, confidence) →
4. Governance boundary (responsible party, review requirement) →
5. Inheritance confirmation (pattern is domain-agnostic)

---

## WaterOS-01: Drainage / Stormwater Risk

**Domain:** WaterOS  
**Judgment Type:** Drainage and stormwater risk assessment  
**Complexity:** Medium  
**Environmental Object:** A catchment area or drainage system in a defined location

### Scenario Description

A local government is planning a residential development on a parcel of land adjacent to a creek. The planning authority requires a drainage and stormwater risk assessment. Historical records show the creek has flooded three times in the past 20 years. Current site survey data shows the land is low-lying.

The task is to use the ClimateOS Foundation to assess whether the stormwater risk judgment is sufficiently evidenced, validated, and governed.

### Judgment Question

```
Is the stormwater risk assessment sufficiently evidenced, validated,
and governed for a responsible party to make a planning
recommendation regarding the residential development?
```

### Environmental Object

A defined land parcel adjacent to a creek, within a specific catchment area, with known topography, soil type, and historical flood records.

### Key Judgment Dimensions

**Reality Test:**
- Can the Foundation identify the specific environmental object (the land parcel, the creek, the catchment)?
- Is the flood history treated as a real observation, not assumed or generalized?

**Evidence Test:**
- Can the Foundation trace the risk assessment from historical flood records to observation to inference to risk evidence?
- Is raw flood data distinguished from interpreted flood risk?

**Validation Test:**
- Does the Foundation assess the reliability of historical flood records?
- Does it evaluate time validity (are the records current enough)?
- Does it evaluate spatial fit (does the flood history apply to this specific parcel)?
- Does it identify conflicting evidence (e.g., recent drainage improvements)?
- Does it assign a confidence level to the risk estimate?

**Governance Test:**
- Is a responsible party identified (e.g., the planning authority, the drainage engineer)?
- Is the governance boundary defined — what approvals are required before development proceeds?
- Does the Foundation require human review before any recommendation is issued?

**Inheritance Test:**
- Could CarbonOS, EnergyOS, or BuildingOS apply the same evidence → validation → governance logic?
- Is the risk assessment pattern domain-agnostic?

### Bounded Scope

- This scenario tests the Foundation's stormwater risk judgment logic.
- It does not produce a technical drainage engineering report.
- It does not determine planning approval.
- It tests whether the Foundation can support the judgment process, not whether it replaces the drainage engineer.

### Pass Criterion

The scenario passes if a human reviewer can trace the judgment from:
1. Environmental object (land parcel + creek + catchment) →
2. Evidence chain (flood records → observation → risk evidence) →
3. Validation assessment (record reliability, time validity, spatial fit, confidence) →
4. Governance boundary (responsible party, review requirement) →
5. Inheritance confirmation (pattern is domain-agnostic)

---

## EnergyOS-01: Community Energy Project

**Domain:** EnergyOS  
**Judgment Type:** Community energy project viability judgment  
**Complexity:** Medium  
**Environmental Object:** A community energy installation at a defined location

### Scenario Description

A community energy cooperative is evaluating a solar + battery storage installation at a community hall in regional Australia. The cooperative needs to assess project viability including energy output estimate, grid connection feasibility, and community benefit distribution.

The task is to use the ClimateOS Foundation to assess whether the project viability judgment is sufficiently evidenced, validated, and governed.

### Judgment Question

```
Is the community energy project viability assessment sufficiently evidenced,
validated, and governed for a responsible party to recommend
or approve the project?
```

### Environmental Object

A defined community hall site with known solar irradiance, grid connection point, and surrounding community profile.

### Key Judgment Dimensions

**Reality Test:**
- Can the Foundation identify the specific environmental object (the site, the installation type)?
- Is the energy output estimate traceable to real solar irradiance data and site characteristics?

**Evidence Test:**
- Can the Foundation trace the viability judgment from solar irradiance data → observation → inference → evidence → recommendation?
- Is modeled output distinguished from measured output?

**Validation Test:**
- Does the Foundation assess the reliability of solar irradiance data sources?
- Does it evaluate time validity (is the data representative of expected conditions)?
- Does it evaluate spatial fit (does the irradiance data apply to this site)?
- Does it identify conflicting evidence (e.g., grid capacity constraints)?
- Does it assign a confidence level to the viability estimate?

**Governance Test:**
- Is a responsible party identified for the project approval (e.g., cooperative board, network operator)?
- Is the governance boundary defined — what approvals are required before construction?
- Does the Foundation require human review before any recommendation is issued?

**Inheritance Test:**
- Could CarbonOS, WaterOS, or BuildingOS apply the same evidence → validation → governance logic?
- Is the project viability judgment pattern domain-agnostic?

### Bounded Scope

- This scenario tests the Foundation's energy project viability judgment logic.
- It does not produce a technical energy modeling report.
- It does not determine financial viability.
- It tests whether the Foundation can support the judgment process, not whether it replaces energy engineers or financial analysts.

### Pass Criterion

The scenario passes if a human reviewer can trace the judgment from:
1. Environmental object (site + installation type) →
2. Evidence chain (solar data → observation → modeled output → viability evidence) →
3. Validation assessment (data source, time validity, spatial fit, confidence) →
4. Governance boundary (responsible party, approval requirements) →
5. Inheritance confirmation (pattern is domain-agnostic)

---

## BuildingOS-01: Building Module / Interface

**Domain:** BuildingOS  
**Judgment Type:** Building module interface compliance assessment  
**Complexity:** Medium  
**Environmental Object:** A building module or building system at a defined location

### Scenario Description

A building project has developed a modular construction system for affordable housing. The project team needs to assess whether the modular system interfaces correctly with a specific site context — including climate zone, surrounding built environment, and infrastructure connection points.

The task is to use the ClimateOS Foundation to assess whether the interface compliance judgment is sufficiently evidenced, validated, and governed.

### Judgment Question

```
Is the building module interface compliance assessment sufficiently evidenced,
validated, and governed for a responsible party to approve
or certify the modular system for this site context?
```

### Environmental Object

A defined building site with known climate zone, surrounding built environment, and infrastructure connection points.

### Key Judgment Dimensions

**Reality Test:**
- Can the Foundation identify the specific environmental object (the building module, the site context)?
- Is the interface requirement described with enough specificity to be assessed?

**Evidence Test:**
- Can the Foundation trace the compliance judgment from site data → observation → inference → evidence → compliance assessment?
- Is design specification distinguished from empirical performance data?

**Validation Test:**
- Does the Foundation assess the reliability of performance data sources?
- Does it evaluate time validity (are the performance claims current)?
- Does it evaluate spatial fit (does the module perform as specified in this climate zone)?
- Does it identify conflicting evidence (e.g., performance claims vs. field observations)?
- Does it assign a confidence level to the compliance assessment?

**Governance Test:**
- Is a responsible party identified for the certification (e.g., building surveyor, certifier)?
- Is the governance boundary defined — what standards apply, what review is required?
- Does the Foundation require human review before certification is issued?

**Inheritance Test:**
- Could CarbonOS, WaterOS, or EnergyOS apply the same evidence → validation → governance logic to their domain scenarios?
- Is the interface compliance pattern domain-agnostic?

### Bounded Scope

- This scenario tests the Foundation's building module interface judgment logic.
- It does not replace a building surveyor or certifier.
- It does not produce a technical building compliance report.
- It tests whether the Foundation can support the judgment process.

### Pass Criterion

The scenario passes if a human reviewer can trace the judgment from:
1. Environmental object (building module + site context) →
2. Evidence chain (site data → observation → compliance evidence) →
3. Validation assessment (data source, time validity, spatial fit, confidence) →
4. Governance boundary (responsible party, certification requirements) →
5. Inheritance confirmation (pattern is domain-agnostic)

---

## ClimateData-01: NASA / BOM Climate Observation Interpretation

**Domain:** Climate Data  
**Judgment Type:** Climate observation interpretation for environmental decision-making  
**Complexity:** Medium  
**Environmental Object:** A defined climate dataset or observation record from NASA or BOM

### Scenario Description

A regional council is reviewing climate observations from NASA and BOM datasets for a planning area. The council needs to interpret temperature trend data, rainfall pattern data, and extreme event frequency data to inform a regional climate adaptation plan.

The task is to use the ClimateOS Foundation to assess whether the interpretation of NASA/BOM climate observations is sufficiently evidenced, validated, and governed for a responsible party to use in a regional adaptation recommendation.

### Judgment Question

```
Is the interpretation of NASA/BOM climate observations sufficiently evidenced,
validated, and governed for a responsible party to use the interpretation
in a regional climate adaptation recommendation?
```

### Environmental Object

A defined geographic planning area with known climate zone, and associated NASA and/or BOM observation datasets.

### Key Judgment Dimensions

**Reality Test:**
- Can the Foundation identify the specific environmental object (the geographic planning area)?
- Is the climate observation data attributed to a specific source (NASA, BOM) and time period?

**Evidence Test:**
- Can the Foundation trace the interpretation from raw observation data → observation → inference → evidence → interpretation?
- Is the raw dataset distinguished from the interpreted trend?
- Is attribution to the correct data source maintained throughout?

**Validation Test:**
- Does the Foundation assess the reliability of the data source (NASA, BOM)?
- Does it evaluate time validity (is the observation period appropriate for the decision timeframe)?
- Does it evaluate spatial fit (does the dataset represent the planning area)?
- Does it identify conflicting evidence (e.g., BOM data vs. NASA data showing different trends)?
- Does it assign a confidence level to the interpretation?

**Governance Test:**
- Is a responsible party identified for the adaptation recommendation (e.g., council planner, climate scientist)?
- Is the governance boundary defined — what review is required before the adaptation plan is adopted?
- Does the Foundation require human review before any recommendation is issued?

**Inheritance Test:**
- Could CarbonOS, WaterOS, or EnergyOS apply the same evidence → validation → governance logic to their data interpretation scenarios?
- Is the climate data interpretation pattern domain-agnostic?

### Bounded Scope

- This scenario tests the Foundation's climate data interpretation judgment logic.
- It does not validate or invalidate NASA or BOM datasets.
- It does not produce a climate adaptation plan.
- It tests whether the Foundation can support the interpretation process, not whether it replaces climate scientists.

### Pass Criterion

The scenario passes if a human reviewer can trace the judgment from:
1. Environmental object (geographic planning area + data source) →
2. Evidence chain (raw observation → observation → trend inference → interpretation) →
3. Validation assessment (source reliability, time validity, spatial fit, cross-source comparison, confidence) →
4. Governance boundary (responsible party, adaptation plan review requirement) →
5. Inheritance confirmation (pattern is domain-agnostic)

---

## Scenario Status Summary

| ID | Scenario | Status | Pass/Fail |
|----|----------|--------|-----------|
| CarbonOS-01 | Carbon Claim / ESG Disclosure | Draft | Not yet evaluated |
| WaterOS-01 | Drainage / Stormwater Risk | Draft | Not yet evaluated |
| EnergyOS-01 | Community Energy Project | Draft | Not yet evaluated |
| BuildingOS-01 | Building Module / Interface | Draft | Not yet evaluated |
| ClimateData-01 | NASA / BOM Observation | Draft | Not yet evaluated |

All scenarios are test designs. Evaluation is conducted by human reviewers applying the Pass/Fail Decision Model.

## Related Documents

- `TASK101_HUMAN_USE_GRADUATION_TEST_SUITE.md` — test suite overview
- `TEST_INPUT_OUTPUT_TEMPLATE.md` — how to evaluate each scenario
- `PASS_FAIL_DECISION_MODEL.md` — how to determine pass/fail

## Status

Draft in progress.
