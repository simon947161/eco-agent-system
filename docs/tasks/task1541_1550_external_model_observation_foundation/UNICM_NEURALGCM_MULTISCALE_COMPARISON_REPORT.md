# UniCM x NeuralGCM Multiscale Comparison Report

Date: 2026-07-14

Status: FIRST_PARALLEL_MODEL_COMPARISON_COMPLETE / RESEARCH_ONLY / NO_EXECUTION

## 1. Decision question

This report asks whether NeuralGCM supplies a sufficiently different and useful
second model perspective for ClimateOS to compare with UniCM before considering
a third model such as GraphCast.

Decision:

`YES — KEEP NEURALGCM AS THE SECOND MODEL WORLD`

GraphCast remains deferred. This report does not authorize GraphCast research,
acquisition, integration or execution.

## 2. Comparison principle

ClimateOS does not seek a universal winner. Each model is treated as a bounded
observer that constructs a partial computational world from selected variables,
scales, mechanisms, training evidence and evaluation rules.

The useful questions are:

1. What does each model make visible?
2. What does each model suppress or omit?
3. At which spatial and temporal scales is its representation meaningful?
4. Which mechanisms are explicit, learned or merely associated?
5. Which outputs can be compared without category error?
6. Where must observations, regional products and human science intervene?

## 3. Evidence status

The UniCM side uses the completed ClimateOS source-orientation record and its
inspected source map. The NeuralGCM side uses its peer-reviewed paper, pinned
official repository metadata, official documentation and the accompanying
Source-and-Observation Research Pack.

Neither model was executed for this report. Published performance statements
remain published claims and were not reproduced by ClimateOS.

## 4. Direct model-world comparison

| Comparison axis | UniCM | NeuralGCM | ClimateOS interpretation |
|---|---|---|---|
| Primary scientific question | How do local climate modes and global inter-mode coupling evolve? | How does the global atmosphere evolve when resolved dynamics interact with learned unresolved physics? | The models ask different questions and should not be ranked on one undifferentiated score. |
| Represented object | Coupled climate modes plus selected gridded ocean physical fields | Global atmospheric state | One reads climate relationships; the other advances atmospheric fields. |
| Dominant time scale | Monthly history and monthly forecast; inspected defaults use 12 historical and 24 predicted steps | Hours-to-days weather trajectories and atmosphere-only simulations from months to decades | NeuralGCM supplies the missing weather-to-climate scale bridge, but not a coupled ocean forecast. |
| Dominant spatial scale | Fixed climate-mode regions and global/coarsened fields | Global 2.8, 1.4 and 0.7 degree grids | Both are global or large-scale observers; neither is a site model. |
| Main variables | SST, wind stress and upper-ocean thermal or thermocline fields | Atmospheric wind structure, temperature, surface pressure and moisture species, with external forcing | The state spaces overlap through forcing and coupling concepts, not through identical variables. |
| Explicit mechanism | No numerical atmospheric or ocean dynamical core was identified in the inspected orientation; interactions are learned by the network | Hydrostatic moist primitive-equation dynamical core | NeuralGCM provides a materially stronger explicit-dynamics counterpoint. |
| Learned mechanism | Spatio-temporal representations, mode interactions and attention | Learned column-local physical tendencies, encoder/decoder corrections and stochastic fields | Attention and learned tendencies have different meanings and cannot be equated. |
| Coupling structure | Learns local mode dynamics and inter-mode relationships | Couples resolved atmospheric dynamics with learned unresolved-process effects; ocean state is prescribed as boundary forcing | UniCM focuses on relation among modes; NeuralGCM focuses on interaction between equation-based and learned atmospheric components. |
| Uncertainty form | Ensemble scripts and multiple training seeds are visible, but available weights and full reproduction remain unresolved | Deterministic and stochastic checkpoints; stochastic variants are evaluated as ensembles | Both need configuration-specific uncertainty records. |
| Main evaluation orientation | Multi-mode forecast skill across climate/ocean datasets | WeatherBench2-style weather skill, physical consistency, stability and atmosphere-only climate statistics | Evaluation frameworks must remain separate from the model registry. |
| Climate interpretation | Learns teleconnection-like mode relationships | Can run AMIP-like atmosphere simulations under prescribed SST and sea ice | Neither independently projects a fully coupled future Earth system. |
| Australian value | Potential macro-driver reference through ENSO and IOD; incomplete driver set for Australia | Potential atmospheric-circulation and weather-field reference over Australia | Their combination may improve questions, not automatically improve local truth. |
| Local readiness | Not admitted | Not admitted | Regional observations, translation and expert review remain mandatory. |

## 5. The two parallel perspectives

### 5.1 UniCM: relationship and climate-mode perspective

UniCM compresses parts of the climate system into named or regionally defined
mode structures and their interactions. Its value is the ability to ask which
large-scale ocean-atmosphere patterns may move together, lead or lag one
another, or influence a multi-mode forecast.

This is a high-altitude view. It can help ClimateOS identify possible global
drivers and teleconnection structures. It does not by itself explain the full
physical path from a mode index to rainfall, heat, fire weather or water state
at an Australian location.

### 5.2 NeuralGCM: evolving atmospheric-field perspective

NeuralGCM represents the atmosphere as an evolving dynamical state. Large-scale
fluid motion is advanced by a numerical dynamical core; unresolved effects are
represented by learned components. Its value is the ability to ask how a
specified initialized and forced atmosphere evolves across weather and climate
timescales.

This is not a ground-level view either. A global atmospheric grid does not
resolve all city, terrain, catchment or site processes. NeuralGCM also depends
on prescribed ocean boundary conditions and does not close the full Earth
system.

### 5.3 Why the difference is valuable

If both models used the same state variables, mechanism and forecast horizon,
their comparison would mainly test implementation differences. Here the
contrast is more informative:

- UniCM foregrounds climate-mode relationships;
- NeuralGCM foregrounds atmospheric dynamics and learned physical tendencies;
- UniCM represents selected ocean-state drivers directly;
- NeuralGCM receives SST and sea ice as external forcing;
- UniCM's inspected forecast frame is monthly;
- NeuralGCM spans weather trajectories and forced atmospheric climate runs.

ClimateOS can therefore examine whether an interpretation survives a change of
model perspective, rather than merely asking whether two networks give similar
numbers.

## 6. Multiscale observation ladder

| Observation level | UniCM contribution | NeuralGCM contribution | Required external anchor |
|---|---|---|---|
| Planetary and inter-basin | Climate-mode state and interaction, including ENSO- and IOD-related structures | Global circulation response and atmospheric state evolution | Reanalysis, ocean observations and climate-science review |
| Global atmosphere-ocean boundary | Selected ocean thermal and wind-stress fields | Atmosphere forced by SST and sea ice | Exact forcing-source and coordinate provenance |
| Continental Australia | Macro-driver relevance, but incomplete Australian driver coverage | Synoptic and large-scale atmospheric field context | Bureau of Meteorology climate-driver, analysis and forecast products |
| Regional Australia | No direct regional-impact admission | Coarse-grid context only; no direct admission | ACCESS regional products, stations, radar, reanalysis and downscaling |
| City or locality | No direct claim | No direct claim | Sydney, Alice Springs or other location-specific observations and qualified review |
| Catchment, project or site | Outside model admission | Outside model admission | Terrain, land, water, ecology, infrastructure and field evidence |

The ladder prevents a result at one level from silently becoming evidence at a
finer level.

## 7. Mechanism crosswalk

### 7.1 Meaningful relationships

| UniCM concept | NeuralGCM concept | Valid comparative question |
|---|---|---|
| SST and upper-ocean state contribute to learned climate-mode evolution | SST is an external boundary forcing for atmospheric evolution | How does ocean-state information enter each computational world? |
| Inter-mode interaction | Interaction of forcing, resolved dynamics and learned physical tendencies | At what layer does each model locate coupling? |
| Monthly mode forecast | Weather rollout or forced climate integration | Which temporal structures are represented, and which are averaged away? |
| Attention or learned relationship | Learned physical tendency within an explicit dynamical advance | What can each learned quantity support as interpretation, and what remains non-causal? |
| Multi-dataset ocean evaluation | Reanalysis, weather benchmark and climate-statistics evaluation | Which truth source and evaluation protocol defines a successful claim? |

### 7.2 Invalid equivalences

The following comparisons are prohibited:

- treating a UniCM attention weight as equivalent to a physical force;
- treating a NeuralGCM learned tendency as a complete observed mechanism;
- comparing a 24-month mode forecast directly with a 10-day atmospheric RMSE;
- treating a named climate-mode region as equal to a model grid cell;
- treating ERA5 agreement as independent observational proof for every use;
- treating global forecast skill as local Australian impact skill;
- interpreting either model's published benchmark as ClimateOS reproduction.

## 8. Four-scale Australian reading examples

These examples define questions only. They are not model outputs or forecasts.

### 8.1 Global climate-driver question

Question: Is a coupled ENSO- or IOD-related state prominent in the UniCM world?

Possible NeuralGCM comparison: Under explicitly matched and verified SST and
sea-ice boundary conditions, what atmospheric circulation structures would be
represented in the NeuralGCM world?

Boundary: similarity would be cross-model consistency evidence, not causal
proof or a regional forecast.

### 8.2 Continental Australia question

Question: Does the atmospheric model represent a broad circulation or moisture
pattern over Australia that is physically compatible with the macro-driver
interpretation?

Required anchor: Bureau of Meteorology driver analysis, reanalysis and expert
review. SAM, MJO and other relevant drivers cannot be omitted because they are
not explicit in the inspected UniCM mode set.

### 8.3 Sydney or Alice Springs question

Question: Does a large-scale atmospheric pattern remain relevant after the
different coastal, continental, topographic and convective settings of these
locations are considered?

Required anchor: location-specific observations, appropriate regional model
products and a translation method. A global cell is not a city forecast.

### 8.4 Snowy Valleys or project-site question

Question: Can a large-scale driver and atmospheric context inform a bounded
hypothesis about rainfall, heat, water, fire or ecology?

Required anchor: catchment and terrain data, local meteorology, domain models,
uncertainty propagation and qualified human review. Neither external model is
admitted to make the impact claim directly.

## 9. First parallel-model comparison protocol

Future comparisons should use the following record for every claim:

1. **Claim unit** — mode state, atmospheric field, statistic, event, regional
   translation or local impact.
2. **Model identity** — exact repository, release, commit, checkpoint and
   configuration.
3. **Observation scale** — spatial support, temporal resolution, horizon and
   aggregation.
4. **Mechanism status** — explicit equation, learned tendency, association,
   attention, diagnostic or external forcing.
5. **Input provenance** — dataset, version, time range, variables, units,
   coordinates, preprocessing and checksum.
6. **Output provenance** — deterministic or stochastic status, member count,
   output cadence and post-processing.
7. **Evaluation contract** — benchmark, truth source, regridding, metric and
   held-out period.
8. **Agreement class** — consistent, partially consistent, divergent,
   incomparable or unresolved.
9. **Boundary statement** — what cannot be inferred at a finer scale.
10. **Human review** — discipline, reviewer role, unresolved disagreement and
    decision authority.

## 10. Divergence is an output, not a failure

The first purpose of a parallel-model architecture is not consensus. It is to
make disagreements legible.

Possible divergence classes include:

- **state-space divergence** — the models do not represent the same variables;
- **scale divergence** — a monthly mode signal has no directly comparable
  weather-field expression;
- **mechanism divergence** — learned association and equation-based dynamics
  support different explanations;
- **forcing divergence** — boundary data or preprocessing differ;
- **evaluation divergence** — metrics, truth sources or regridding differ;
- **regional divergence** — a global relationship does not survive regional
  observations;
- **uncertainty divergence** — deterministic and stochastic outputs answer
  different questions.

ClimateOS should retain these divergences with provenance rather than average
them into a false single confidence number.

## 11. Non-executable research hypotheses

The following hypotheses may guide later Founder-gated work. They do not
authorize an experiment.

| ID | Bounded hypothesis | Evidence required before testing |
|---|---|---|
| PMH01 | Selected UniCM climate-mode states may correspond to distinguishable NeuralGCM large-scale circulation statistics under matched boundary forcing. | Exact mode definition, forcing crosswalk, temporal alignment, pinned models and independent evaluation design |
| PMH02 | NeuralGCM's explicit dynamical structure may expose when a learned UniCM inter-mode relationship lacks an atmospheric pathway at the examined scale. | Mechanism-review protocol and atmospheric-science review |
| PMH03 | Agreement at planetary scale may weaken or reverse at Australian regional scale. | BoM/ACCESS and observation registry, regional method and uncertainty protocol |
| PMH04 | Stochastic atmospheric ensembles may express uncertainty not visible in a single monthly mode trajectory. | Comparable claim unit, ensemble contract and probabilistic metric |
| PMH05 | Some apparent model disagreement may be caused by different averaging and coordinate transformations rather than different science. | Variable, grid, unit, cadence and regridding crosswalk |

## 12. Evaluation-framework separation

WeatherBench2, PhysMetrics and RealBench must remain independent research
objects. They are not model components and they do not automatically validate
regional or consequential use.

For this pair:

- WeatherBench2 is relevant to NeuralGCM weather evaluation;
- a physical-consistency framework may help inspect atmospheric constraints;
- neither framework directly evaluates UniCM's climate-mode task without a
  separate mapping;
- RealBench-style real-world evaluation remains a later independent question;
- Australian regional evaluation requires its own authoritative data and human
  science layer.

## 13. Registry implications

The comparison confirms that one generic external-model record is insufficient.
The ClimateOS Parallel Model Registry Draft should separate:

- model identity and scientific purpose;
- represented system and state variables;
- mechanism type;
- native spatial and temporal scales;
- forcing and initialization contracts;
- deterministic or stochastic status;
- source, weight and data access;
- compute, storage, security and cost;
- evaluation frameworks and truth sources;
- regional applicability;
- prohibited inferences;
- human scientific responsibility;
- research, acquisition, execution and operational admission states.

Model, evaluation framework and data resource must be separate registry object
types linked by explicit relationships.

## 14. Decision on the second model

NeuralGCM provides a valuable contrast with UniCM because:

1. it changes the primary object from climate modes to atmospheric fields;
2. it changes the mechanism from learned mode interaction to hybrid
   equation-based and learned dynamics;
3. it introduces weather-to-climate timescale continuity;
4. it supports deterministic and stochastic model readings;
5. it exposes prescribed boundary forcing as an explicit limitation;
6. it creates meaningful questions about whether macro-driver interpretations
   have compatible atmospheric expressions.

This is sufficient to retain NeuralGCM as the second model world for research.
It is not sufficient to acquire or run the model.

## 15. GraphCast decision gate

GraphCast should not enter the active comparison yet.

Before deciding on a third model, the Founder should review whether the first
pair has produced enough value in these areas:

- model-neutral registry fields;
- mechanism-status distinctions;
- scale-aware claim records;
- divergence categories;
- Australian regional-anchor requirements;
- independent evaluation-framework separation;
- human-review responsibilities.

If a third world is later authorized, GraphCast would add a primarily
data-driven global weather perspective. Its purpose would be to compare a pure
learned weather trajectory with NeuralGCM's hybrid dynamics and UniCM's
climate-mode relationships. That future value does not constitute present
authorization.

## 16. Closure

The first UniCM x NeuralGCM comparison is complete at the source-and-observation
level.

No external model, checkpoint, dataset, runtime, API or paid resource has been
integrated. No local, Australian operational or consequential claim has been
made. The next action is Founder review of this research pair and a separate
decision on whether GraphCast should be admitted to read-only research.
