# Carbon Scenario Conceptual Data Model

## Scenario

**Purpose:** identifies a bounded possible future or reference state.

**Example fields:** scenario ID, type, name, boundary, horizon, owner, status,
version, evidence status.

**Relationships:** contains assumptions, inputs, outcomes, and review notes.

## Scenario Assumption

**Purpose:** records a premise used inside a scenario.

**Example fields:** assumption ID, scenario ID, statement, source, owner,
confidence note, uncertainty, review status.

**Relationships:** may reference accounting, budget, energy, or evidence
records.

## Carbon Budget

**Purpose:** provides target, allocation, or period context for scenarios.

**Example fields:** budget ID, period, boundary, target reference, version,
status, limitations.

**Relationships:** supports target or budget-alignment scenarios.

## Emission Record

**Purpose:** references accounting records used as scenario inputs.

**Example fields:** emission record ID, inventory ID, boundary, period,
amount reference, uncertainty, review status.

**Relationships:** informs baseline or comparison records without being
recalculated in Task56.

## Energy Record

**Purpose:** references electricity or fuel information relevant to a scenario.

**Example fields:** energy record ID, type, quantity reference, source,
classification status, period, evidence status.

**Relationships:** may support green electricity adoption or facility
transition scenarios.

## Scenario Outcome

**Purpose:** describes a conceptual result or comparison note.

**Example fields:** outcome ID, scenario ID, description, source assumptions,
uncertainty, limitations, review status.

**Relationships:** derives from scenario assumptions and inputs. No outcome is
calculated in Task56.

## Review Note

**Purpose:** records reviewer observations, questions, or required follow-up.

**Example fields:** note ID, scenario ID, author, date, category, text, owner,
resolution status.

**Relationships:** belongs to a Scenario or Scenario Outcome.

Every future entity should preserve identifiers, source references, boundary,
period or horizon, version, uncertainty, and review status.
