# Climate–facility–greenhouse-gas evidence map

Solid source relationships identify evidence lineage. Dashed arrows are proposed research questions, NOT established effects. No numerical model is attached.

```mermaid
flowchart TD
 B[Official BOM historical summaries] --> O[Dated station observations: six records]
 I[Retrospective ENSO / IOD / SAM context] -. contextual only .-> O
 L[Historical Cooma licence 6194 / B3 Council evidence] --> F[Four partial facility candidates]
 O -. BLOCKED: geometry and representativeness .-> X[Actual facility weather exposure]
 F -. BLOCKED: identity and operational validity .-> X
 X -. HYPOTHESIS: lag and confounders .-> P[Process temperature / moisture / redox / load]
 P -. measurement required .-> M[CH4: generation / oxidation / capture / emitted flux]
 P -. measurement required .-> N[N2O: nitrogen pathways and emitted flux]
 P -. source boundary required .-> C[CO2: biogenic and fossil separately]
 W[Outage / maintenance / operational changes] -. confounders .-> P
 W -. meters required .-> E[Imported energy / fuel / refrigerants]
 M --> G[Scientific review gate: PENDING]
 N --> G
 C --> G
 E --> G
```

No edge permits inference from an extreme-weather observation to a measured gas change. No national aggregation, ACCU accounting or spatial join. See [matrix](EVIDENCE_MATRIX.md) for machine-reviewable meaning of link states.
