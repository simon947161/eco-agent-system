# Task1505–1509 — UniCM Paper-to-Code Scientific Orientation Map

Date: 2026-07-14

Status: READ_ONLY_ORIENTATION_COMPLETE / NO_EXECUTION

## Scientific claim boundary

The paper introduces UniCM as a unified deep model that learns local climate-mode dynamics together with global inter-mode coupling. It reports improved multi-mode forecast skill and interpretable attention patterns.

ClimateOS records these as **published claims**, not independently reproduced facts.

Attention weights and lead-lag associations are not accepted as causal proof.

## Paper-to-code map

| Published or documented concept | Inspected code location | Orientation finding |
|---|---|---|
| Unified coupled climate-mode forecast | `src/models.py::UniCM` | One model contains a physical-field branch and a climate-mode branch. |
| Dual-branch representation | `UniCM.forward`, `forward_sep` | Mode predictions and gridded physical-field predictions are processed separately and exchange embedded bias/state. |
| Spatio-temporal transformer | `models.py`, `my_tools.py` references | Encoder/decoder stacks use spatial-temporal embeddings and attention layers. |
| Local mode regions | `src/LoadData.py` | Fixed geographic index boxes define ENSO-related and Indian/Atlantic/Pacific modes. |
| Inter-mode interaction | `--mode_interaction`; `val_relative` | Modes may be included jointly; selected mode embeddings are projected back into spatial regions. |
| Historical input | `src/config.py` | Default `his_len=12` monthly steps. |
| Forecast horizon | `src/config.py` | Default `pred_len=24` monthly steps. |
| Multivariate physical state | `src/config.py`, `LoadData.py` | Default five channels. |
| Ensemble evaluation | `src/script/test.sh`, `app_ensemble.py` | Local checkpoints are loaded and evaluated across ERA5, ORAS5, SODA and GODAS. |
| Training ensemble | `src/script/train.sh` | Script iterates seeds 1–20. |
| Reported model size | `src/app_train.py` | Size is calculated only after model initialization; no execution occurred in this batch. |

## Inspected physical variables

The loader names indicate the following primary ocean variables:

| Code name | Scientific interpretation | Status |
|---|---|---|
| `tos` / `sosstsst` | sea-surface temperature | confirmed by naming and loader use |
| `tauu` / `sozotaux` | zonal surface wind stress | confirmed |
| `tauv` / `sometauy` | meridional surface wind stress | confirmed |
| `thetaot300` / `sohtc300` | upper-ocean thermal/heat-content representation to 300 m | exact dataset convention must be checked |
| `t20d` / `so20chgt` | depth/height of the 20 °C isotherm | exact units and sign convention must be checked |

The code normalizes and coarsens inputs and uses monthly sequences. Exact coordinate conventions, masks and variable units require dataset-level verification.

## Climate-mode representation found in code

The inspected loader contains regions or derived indices for:

- ENSO / Niño-related regions;
- North Pacific Meridional Mode;
- South Pacific Meridional Mode;
- Indian Ocean Basin mode;
- Indian Ocean Dipole;
- Southern Indian Ocean Dipole;
- Tropical North Atlantic;
- Niño1+2, Niño3 and Niño4 boxes;
- warm-water volume support fields.

### Important gap

No explicit SAM or MJO mode was identified in the inspected UniCM mode registry.

Therefore:

- UniCM cannot currently be assumed to represent all Australian climate drivers;
- SAM and MJO must remain external or separately governed sources;
- ClimateOS must not translate UniCM output directly into local NSW rainfall, fire, biodiversity or infrastructure claims.

## Code-path limitations

- The README gives expected preprocessed NetCDF directory structures, not a complete end-to-end raw-data preparation recipe.
- Training and test scripts use local filesystem conventions.
- Shell scripts are Linux/macOS oriented.
- The dependency environment pins PyTorch 2.0.1 and CUDA 11.8-era packages.
- Script defaults and CLI defaults differ: `config.py` defaults to 200 epochs, while the supplied training script overrides this to 2 epochs.
- The paper-result configuration cannot be assumed from defaults alone.
- The ensemble script requires locally available checkpoints.

## ClimateOS architectural lesson

UniCM should remain an isolated scientific reference behind a future model-neutral Climate Mode Evidence Adapter.

Required adapter separation:

`published claim → pinned code → verified dataset → bounded output → assurance record → regional translation → expert review`

No UniCM code should be merged directly into the ClimateOS core at Task1521.
