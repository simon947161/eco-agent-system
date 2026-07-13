# Task1545–1546 — UniCM Computational Reading and Scale Boundary Map

Date: 2026-07-14

Status: STATIC READING COMPLETE / NO EXECUTION

## Computational route

Published source and fixed code
→ preprocessed NetCDF inputs
→ spatial cropping, coarsening and normalization
→ 12-month multivariate physical history
→ physical-field and climate-mode embeddings
→ dual spatio-temporal transformer branches
→ cross-representation information exchange
→ 24-month physical-field and climate-mode predictions
→ checkpoint and seed ensemble evaluation
→ reported climate-mode metrics

## Reading record

| Stage | What the code world does | Current evidence | Boundary |
|---|---|---|---|
| Source | fixed v1.0 source tree | integrity verified | source identity only |
| Data intake | loads preprocessed CMIP6, ERA5, ORAS5, SODA and GODAS files | filenames and variables mapped | raw-to-derived pipeline incomplete |
| Transformation | crops, coarsens, interpolates, fills, deseasonalizes and normalizes | static code evidence | exact units, calendars, grids and masks unresolved |
| History | uses monthly sequences, default length 12 | config/code evidence | not a local observation record |
| Representation | builds physical and mode branches | code and paper mapping | latent states are not observed mechanisms |
| Coupling | exchanges information between branch representations and modes | code/published claim | attention and association are non-causal |
| Forecast | default 24 monthly steps | config evidence | local forecast translation absent |
| Evaluation | expects local checkpoints and several reanalysis datasets | scripts/README | no official weights found |
| Ensemble | seed and ensemble scripts exist | source evidence | calibration unverified |

## Scale boundary map

| Source claim or output | Native frame | Required bridge | Prohibited direct interpretation |
|---|---|---|---|
| climate-mode index | basin/mode | authoritative mode definition and validation | local weather fact |
| physical-field output | global/coarsened ocean grid | grid, variable and unit verification | site exposure |
| lead-lag signal | mode/system | independent statistical assessment | causal mechanism |
| attention pattern | learned latent relation | scientific hypothesis review | physical proof |
| ENSO/IOD state | global/basin | Australian driver assessment | NSW rainfall amount |
| global monthly forecast | planetary/basin monthly | regional climate translation | city or asset warning |
| ensemble spread | model-run collection | calibration and interpretation | probability unless calibrated |

## Cross-scale translation chain required for Australia

UniCM climate-mode state
→ authoritative Australian climate-driver context
→ regional rainfall and temperature observations or reanalysis
→ local water, land, ecology, fire or infrastructure evidence
→ explicit translation method
→ uncertainty propagation
→ Australian scientific review
→ bounded governance interpretation

Each arrow is an independent evidence transformation.

## Transferable structural lessons

Potentially transferable:

- coupled-state representation;
- local/global information exchange;
- lead-lag hypothesis discovery;
- joint modelling rather than isolated agent outputs;
- explicit separation of fields and derived indices;
- multi-seed comparison.

Not directly transferable:

- specific learned weights;
- fixed mode boxes as universal regional definitions;
- paper metrics as local skill;
- attention weights as causal relationships;
- data preprocessing assumptions without reconstruction;
- model outputs as decision recommendations.

## Reading conclusion

UniCM is valuable as a computational-world reference for coupled representation.

Its principal ClimateOS contribution at this stage is structural understanding, not an executable or locally admitted forecast.
