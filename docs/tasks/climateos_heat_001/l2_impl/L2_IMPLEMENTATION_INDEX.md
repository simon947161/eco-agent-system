# HEAT–001 L2 implementation index

## Current status

`INCONCLUSIVE / MODEL_NOT_READY_FOR_RANKING`: two paired SYNTHETIC central annual cases passed service, tank, periodicity and high-loop energy checks at dt=60 s, dx=25 m. The required three-level time and space convergence suite was not executed because measured CPU runtime projects above the frozen 180 s budget. No L/T recommendation or downstream authorization is made.

## Authorization and immutable provenance

- Implementation authorization: [Issue #183](https://github.com/simon947161/eco-agent-system/issues/183).
- Accepted design: [PR #182 at `8b08152670406ec57de443facd5d589060a675b0`](https://github.com/simon947161/eco-agent-system/pull/182).
- P1 accepted synthetic reference: [PR #179 at `5a2039a2753142b2eb17665da2dba6c4a8648b14`](https://github.com/simon947161/eco-agent-system/pull/179).
- P0 science: [PR #174 at `de0b951e5644696e956c20cc03ab848e5742be70`](https://github.com/simon947161/eco-agent-system/pull/174).
- P0-A geometry: [PR #177 at `369ee6b9703fedb54ca4da684920e6c23825d6ca`](https://github.com/simon947161/eco-agent-system/pull/177).
- ARCH–P0 read-only research: [PR #180 at `4c078aefa90ea9206dd789578682b489bf27e29e`](https://github.com/simon947161/eco-agent-system/pull/180).
- Gate v1.0.1 committed before L2 output: `a351247e92a673dc39a2136822ed8fe3e5a65231`; contract SHA-256 `60861f0fc5c34e14f7c66feff10b70b7680e61809cbf27e3df9225c4232a9c7b`.
- Implementation is on independent branch `codex/heat-001-l2-synthetic-implementation-20261127`, based on main; all predecessor PRs remain open, Draft and unmerged.

## Contents

- `L2_FROZEN_SYNTHETIC_CONTRACT.json`, `L2_IMPLEMENTATION_GATE.md`, `L2_FREEZE_SHA_RECEIPT.json`, deterministic gate validator, immutable P1 synthetic fixture copies.
- `l2_model.py`, `run_l2.py`, `independent_replay.py`, component tests and standard-library run instructions.
- `outputs/`: paired L/T hourly compressed rows and annual JSON for the central dt=60 s, dx=25 m level only.
- `docs/`: implementation, analytic, conservation/convergence, spatial comparison, failure/uncertainty and Founder acceptance records.
- `figures/l2_synthetic_system.svg`: new editable SVG; accepted P0-A/P1/L2 figures are linked by fixed commit SHA and left untouched.
- `L2_TEST_LOG.txt`, `L2_RUN_RECEIPT.json`, `doc_check.py`: exact commands, test/independent replay results, artifact SHA-256s and deterministic Markdown-link check.
- `CRP_AND_PERMISSION_LOG.md`: scope, access and non-actions.

## Reproduction commands

From this folder using Python 3.14.4 or compatible Python 3 standard library:

```text
python -B L2_GATE_VALIDATOR.py
python -B -m unittest -v tests.test_l2_model
python -B independent_replay.py L 60 25
python -B independent_replay.py T 60 25
```

To reproduce a central case, run `python -B run_l2.py L 60 25` or `python -B run_l2.py T 60 25`; these commands create outputs. Existing compressed outputs are frozen review artifacts. No convergence run is included; the resource stop is documented in `docs/L2_CONSERVATION_CONVERGENCE.md`.

## Founder decision requested

At the Draft PR HEAD, select `REQUEST REPAIR / EVIDENCE` or `HOLD`. `ACCEPT L2 SYNTHETIC` requires resolved convergence evidence. No automatic advancement to 3D/P2, live site data, CFD, production, merge or deployment.
