# Eco Agent System

**Open-source Environmental Decision Support Framework**

Eco Agent System is an early-stage open-source prototype for translating environmental observations into planning, resilience, maintenance, ESG interpretation, and climate-risk decision support.

It is also the current public implementation home of **ClimateOS**, a long-horizon human–AI operating-system direction for shared climate stewardship and governance. ClimateOS combines human life experience, local observation, values and action responsibility with AI long-term memory, scientific synthesis, multi-model reasoning, evidence organisation and system execution. Its identity and cumulative history must not be reduced to the newest runtime or demonstration. See the [Stewardship and Civilization Care vision](docs/00_VISION/CLIMATEOS_STEWARDSHIP_AND_CIVILIZATION_CARE.md) and the [Integrity, Long-Horizon, and Human–AI Covenant](docs/00_VISION/CLIMATEOS_INTEGRITY_LONG_HORIZON_AND_HUMAN_AI_COVENANT.md).

It explores how environmental data can become practical, human-reviewed action logic for communities, planners, land managers, researchers, and public-good projects.

## CCZPS-Lite v0.5

CCZPS-Lite v0.5 is the repository's deterministic, local-first environmental
intelligence and planning-support foundation. It connects evidence,
meteorology, spatial context, planning hypotheses, validation support,
traceability, internal governance support, and scenario comparison.

It is not a statutory approval tool, professional certification system,
engineering or construction decision system, regulatory determination, or
financial recommendation system. Human and professional review remain required.

Run the tests:

```bash
python -m unittest discover
```

## Meaningful Environmental Question Runtime (Task2002 prototype)

This supervised local prototype accepts a real environmental question in the
user's own words and structures it as an evidence plan. Real-place execution is
blocked: the Runtime does not fetch current data or manufacture a regional
conclusion. A separate, explicitly fictional Australian highland-town fixture
can rehearse the human approval, deterministic run, Run Receipt, quarantined
Evidence Passport, and human review workflow.

From the repository folder, start it with:

```bash
python run_environmental_question_runtime.py
```

Then open <http://127.0.0.1:8766>. The process must remain open while the page
is in use; press `Ctrl+C` to stop it. The older scalar control demonstration
continues to use port 8765 and is not the entry for this prototype.

The executable rehearsal is repository-authored tiny-synthetic data, runs with
no network access and no paid service, and is not environmental evidence. In
particular, it cannot support a Cooma condition, ENSO, bushfire, drinking-water,
wastewater, Bondo/Riverina wind-resource, or project-feasibility conclusion.

Generate the principal downstream outputs:

```bash
python cczps_lite/engine/evidence_traceability.py
python cczps_lite/engine/governance_decision_support.py
python cczps_lite/engine/scenario_comparison.py
```

Committed outputs are under `cczps_lite/output/`; the static dashboard is under
`cczps_lite/dashboard/`. See the
[v0.5 release package](docs/08_RELEASES/README.md) for release notes,
architecture, demonstration guidance, and the output inventory.

FarmerOS, GardenOS, and WaterOS remain future application-layer directions
that may reuse this foundation. ClimateOS is the longer-horizon umbrella system
to which this repository now contributes; its full intended capability is not
implemented in v0.5 or in any single current runtime.

```text
Climate · Water · Vegetation · Infrastructure · Maintenance · Resilience · Governance
```

---

## Why This Project Exists

Environmental data is growing rapidly.

However, local governments, planners, land managers, and communities often struggle to translate environmental information into practical decisions.

Eco Agent System explores a simple but important question:

> How can environmental observations become structured decisions, maintenance actions, and resilience evidence?

The project is not designed to replace expert judgement. It is designed to support human-reviewed reasoning by connecting environmental system logic with professional decision workflows.

---

## Core Idea

Environmental systems can be described in physical terms such as water, heat, vegetation, soil, infrastructure stress, and climate exposure.

Eco Agent System translates these observations into a structured decision layer called **Eco Decision DNA**.

Eco Decision DNA is a way to make environmental actions:

- computable
- comparable
- reviewable
- environmentally accountable
- useful for long-term maintenance and resilience planning

---

## System Architecture

```text
Environmental Inputs
Climate · Water · Heat · Vegetation · Soil · Infrastructure · Maintenance
        ↓
Eco Decision DNA
        ↓
Agent Framework
Planning Agent · Delivery Agent · Operations Agent · ESG Interpretation Agent · Resilience Review Agent
        ↓
Decision Support Outputs
Planning notes · Risk interpretation · Maintenance priorities · Resilience evidence · Governance reports
```

The system connects:

- **Eco Engine** — physical environment and modelling logic
- **Professional Agents** — planning, delivery, operations, and review logic
- **ESG-style Interpretation** — governance and reporting interface
- **Climate Resilience Layer** — risk reduction, maintenance, and adaptation support

---

## Key Themes

### Climate Resilience

The project supports climate adaptation, disaster-risk reduction, and long-term environmental maintenance.

It may help structure reasoning around:

- bushfire risk
- flood risk
- drought stress
- heat exposure
- vegetation health
- infrastructure vulnerability
- community resilience

### Climate Risk, Insurance and Resilience Finance Interface

A future direction is to explore how prediction, microclimate governance, and maintenance records can support evidence of climate-risk reduction.

```text
Climate and weather prediction
↓
Microclimate and environmental intervention
↓
Risk-score reduction
↓
Maintenance and monitoring records
↓
Evidence for insurers, local governments, communities, and resilience-finance partners
```

This project does **not** provide insurance, financial advice, actuarial certification, or investment products.

It aims to build an open decision-support and evidence-recording framework that may support better collaboration with climate-insurance and resilience-finance sectors.

### Eco Chain Contribution Logic

Eco Chain is treated here as a contribution-recording and environmental value interpretation concept.

It is not presented as a speculative token system or financial product.

In this project, Eco Chain means:

- recording environmental actions
- recording maintenance work
- linking actions with observed outcomes
- supporting public-good environmental contribution
- making long-term ecological value easier to review and explain

---

## Integration Vision

Eco Agent System should not exist as an isolated tool.

A long-term goal is to connect with existing and emerging software used in spatial planning, environmental modelling, engineering simulation, digital twins, and climate data analysis.

Future integration directions may include:

- GIS platforms
- CFD and fluid simulation tools such as ANSYS Fluent or equivalent systems
- hydrology and terrain models
- vegetation and heat-flow models
- remote sensing and open climate datasets
- smart city and digital twin platforms
- APIs or export formats for other modelling environments

The long-term vision is to create an interface layer between traditional simulation tools and agent-based decision-support systems.

In simple terms:

```text
Simulation Tools + Spatial Data + Environmental Monitoring
↓
Eco Agent System
↓
Human-reviewed Planning, Maintenance, Risk and Governance Decisions
```

---

## Current Development Status

Current status:

- Prototype structure established
- README, License, Roadmap, and Contributing guidelines added
- Basic environmental decision-support concept defined
- Initial agent roles defined
- Simple CLI direction included

In progress:

- clearer example inputs and outputs
- climate-risk interpretation logic
- resilience and maintenance evidence structure
- GIS and simulation-tool integration concepts
- field pilot use-case documentation

Future work:

- open environmental indicator library
- climate insurance evidence interface
- regional resilience pilot examples
- API and data exchange structure
- stronger documentation for contributors

---

## How to Run

Run the full system:

```bash
cd eco_agent_system
python main.py
```

Try a simple check:

```bash
python run_simple_check.py
```

---

## Documentation

- [Roadmap](ROADMAP.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [License](LICENSE)
- [Eco Decision DNA](docs/eco-decision-dna.md)
- [ClimateOS Stewardship and Civilization Care](docs/00_VISION/CLIMATEOS_STEWARDSHIP_AND_CIVILIZATION_CARE.md)
- [ClimateOS Integrity, Long-Horizon, and Human–AI Covenant](docs/00_VISION/CLIMATEOS_INTEGRITY_LONG_HORIZON_AND_HUMAN_AI_COVENANT.md)
- [Build Week Participation and Long-Horizon Alignment CRP](docs/context-packets/2026-07-18_CLIMATEOS_BUILD_WEEK_PARTICIPATION_AND_LONG_HORIZON_CRP.md)
- [Build Week Integrity-to-Submission Next-Thread ACTP](docs/context-packets/2026-07-18_CLIMATEOS_BUILD_WEEK_INTEGRITY_TO_SUBMISSION_NEXT_THREAD_ACTP.md)

---

## Contributing

Contributions are welcome from developers, planners, environmental researchers, engineers, climate specialists, GIS users, local government practitioners, land managers, insurers, and community contributors.

Useful contributions include:

- documentation improvements
- environmental indicators
- climate-risk logic
- GIS or simulation integration ideas
- regional use cases
- testing and example workflows
- resilience and maintenance evidence structures

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## Maintainer

Maintained by **Min Shu / Simon Shu**.

Environmental planner, landscape and sustainability practitioner, and open-source environmental decision-support explorer based in Australia.

---

## License

This project is released under the [MIT License](LICENSE).

---

## Project Status Notice

Eco Agent System is an early-stage experimental prototype.

It is intended for research, learning, open-source collaboration, and human-reviewed decision-support exploration. It should not be used as the sole basis for legal, engineering, financial, insurance, environmental approval, or emergency-management decisions.
