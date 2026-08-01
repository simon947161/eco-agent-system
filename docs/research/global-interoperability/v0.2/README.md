# GGG Global Interoperability v0.2

Bounded RFC and synthetic cross-OS handoff pilot. This package extends the
validated v0.1 mission controls without changing any production or mainline
system.

## Authority

- `AUTHORISE_GGG_V0_2_TRANSPORT_CONTRACT_RFC_ONLY`
- `AUTHORISE_ONE_SYNTHETIC_CROSS_OS_HANDOFF_PILOT`
- `MAINTAIN_NO_EXTERNAL_ACTION_NO_MAINLINE_WRITE`
- `DEFER_REAL_DATA_AND_PRODUCTION_ENFORCEMENT`

## Run

```bash
python3 validator/validate_transport_and_pilot.py
```

The pilot path is `ClimateOS -> BuildingOS -> ECOChain`. All payloads are
synthetic, all writes are local fixture writes, and all external actions are
forbidden.
