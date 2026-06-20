# AGENTS.md

## Purpose

This file is the repository operating constitution for AI coding agents working
in this ClimateOS / eco-agent-system repository.

Target readers include Codex, ChatGPT, Claude Code, future AI contributors, and
human maintainers reviewing AI-generated work.

This is not a Climate Agent product specification. Business agents, scientific
agents, and governance agents should be defined in separate documents using the
project control standards.

## Project Positioning

ClimateOS is an evolving Earth System Governance Runtime architecture.

Do not describe ClimateOS as:

- a dashboard
- a reporting platform
- a NASA data viewer
- a carbon accounting tool
- a completed system
- a finished product

ClimateOS connects:

```text
Observation
-> Relationship
-> Radar
-> Evidence
-> Validation
-> Governance
```

The current repository is establishing foundational layers. Most ClimateOS
documents are architecture, governance, and framework foundations, not
operational software.

## Core System Boundaries

### ClimateOS

ClimateOS is responsible for governance runtime architecture, observation
management, relationship analysis framework, evidence management, validation
framework, and governance coordination.

### EcoEngine

EcoEngine is a separate scientific computation engine. It may support threshold
detection, boundary detection, pattern discovery, and scientific modelling.

### Relationship

```text
ClimateOS
-> Call
-> EcoEngine
```

ClimateOS may use EcoEngine. ClimateOS does not replace EcoEngine. EcoEngine
does not replace ClimateOS.

## Supporting Components

CCZPS is the climate zone reasoning framework. It supports climate zone
interpretation, spatial reasoning, and context generation.

ESG++ is the governance translation layer. It helps translate environmental
reality into governance language and connects evidence with reporting and
decision-making.

EcoChain is the validated evidence chain. It supports evidence traceability,
validation history, and the Proof of Reality foundation.

## External Data Rules

NASA is not part of ClimateOS. NASA is an external observation resource
provider.

ClimateOS may consume external observation resources from NASA, Copernicus,
ECMWF, BOM, Open-Meteo, local sensors, community observation, and future
providers.

ClimateOS must remain provider-independent. Do not build a task as if any
single data provider is the system.

## Contribution Rules For AI Agents

1. Read the relevant local documentation before editing.
2. Preserve the existing architecture unless a task explicitly changes it.
3. Prefer small Markdown and Python files over large rewrites.
4. Keep outputs human-readable.
5. Clearly distinguish implemented, planned, and vision content.
6. Do not claim runtime, API, modelling, forecasting, or automation capability
   unless it exists in code and tests.
7. Do not add external integrations, downloads, authentication, databases, or
   network dependencies unless explicitly requested.
8. Do not modify runtime logic for documentation-only tasks.
9. Do not delete or rename existing files unless explicitly instructed.
10. Run existing tests when requested or when code changes occur.
11. Restore test-generated artifacts if they are unrelated to the task.
12. Stop after task completion when the user asks for batch-control behavior.

## Documentation Standards

Use plain Markdown. Write for future contributors, research collaborators,
project maintainers, AI agents, reviewers, and non-programmer project owners.

Every foundation task should state:

- purpose
- scope
- architecture position
- inputs or concepts
- outputs or documents
- limitations
- verification result

Avoid hype. Avoid professional, regulatory, scientific, financial, engineering,
or approval claims unless they are explicitly supported.

## Repository Starting Points

- [PRD](PRD.md)
- [Project Index](PROJECT_INDEX.md)
- [Repository Onboarding Guide](docs/onboarding/REPOSITORY_ONBOARDING_GUIDE.md)
- [Root README](README.md)
- [Project Control Layer](00_PROJECT_CONTROL/README.md)
- [Repository Governance](docs/governance/REPOSITORY_GOVERNANCE.md)
- [ClimateOS Core](01_CLIMATEOS_CORE/README.md)
- [Master Directory Map](MASTER_DIRECTORY_MAP.md)
- [Agent Standard](00_PROJECT_CONTROL/AGENT_STANDARD.md)
- [Task Index](00_PROJECT_CONTROL/TASK_INDEX.md)

## Common Templates

- [Conversation Radar Template](docs/radar/CLIMATEOS_CONVERSATION_RADAR_TEMPLATE.md)
- [Observation Diary Template](docs/observation/CLIMATEOS_OBSERVATION_DIARY_TEMPLATE.md)
- [Validation Report Template](docs/validation/CLIMATEOS_VALIDATION_REPORT_TEMPLATE.md)
- [Skills Roadmap](docs/skills/CLIMATEOS_SKILLS_ROADMAP.md)

## Safe Default

When uncertain, preserve the repository, document assumptions, keep the change
small, and make the boundary between present capability and future vision
obvious.
