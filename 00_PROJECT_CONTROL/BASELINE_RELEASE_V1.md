# Baseline Release V1

## Baseline Name

**ClimateOS Repository OS v1.0**

This is a repository-governance and architecture baseline. It is not a
ClimateOS scientific model, subsystem runtime, professional certification, or
operational product release.

## Release Date

2026-06-15

## Repository Scope

The baseline covers:

- repository control and architecture decisions;
- the ClimateOS master directory scaffold;
- the Codex batch queue and task lifecycle;
- the Agent Factory documentation standard and reusable templates;
- maturity and safety boundaries for future subsystem work.

It preserves the existing CCZPS-Lite runtime and does not change scientific,
GIS, validation, dashboard, API, or decision logic.

## Completed Tasks

- Task46 - ClimateOS Repository Control and Codex Batch Queue System
- Task47 - ClimateOS Master Directory Scaffold
- Task48 - Codex Batch Queue System
- Task49 - Agent Template Standard
- Task49.5 - Repository Baseline Release

Completion here means the documentation acceptance criteria and repository
tests passed for this baseline. It does not mean future subsystem agents are
implemented.

## Outstanding Tasks

- Task50 - CarbonOS Foundation
- Task51 - Green Power Accounting Agent
- Task52 - Carbon Budget Agent
- Task53 - ESG Disclosure Auditor Agent
- Task54 - Zero Carbon Park Agent
- Task55 - Demo Integration: Batlow + Datong + Shanghai
- Task56 - Independent Business Layer Planning

## Current Maturity Level

**Repository operating system: Documented Baseline**

The control, queue, and Agent Standard layers are documented and verified. The
master directory is a scaffold. Existing CCZPS-Lite modules remain the only
implemented runtime family described by this baseline.

CarbonOS, EnergyOS, WaterOS, LandOS, BiodiversityOS, ParkOS, ESGOS, GISOS,
ScenarioOS, ValidationOS, and GovernanceOS directories are not implemented
subsystems.

## Next Recommended Tasks

1. Review this baseline as the checkpoint for future work.
2. Start Task50 - CarbonOS Foundation as a documentation-first subsystem task.
3. Define CarbonOS evidence, ontology, validation, and governance boundaries
   before implementing any carbon agent.
4. Keep one primary task per Codex session.

## Verification Record

The baseline review confirmed:

- `MASTER_DIRECTORY_MAP.md` describes the current scaffold and legacy-folder
  compatibility;
- queue documents use a consistent task lifecycle;
- `AGENT_STANDARD.md` and templates preserve evidence, validation, governance,
  and limitation requirements;
- `REPOSITORY_MATURITY.md` separates scaffold, documentation, implementation,
  validation, and operation;
- no existing file was deleted;
- no runtime or test logic was modified.

Test command and result:

```text
python -m unittest discover
210 tests passed
```
