# Batch C — extreme-weather observations and multi-gas evidence readiness

2026-11-04 · Issue #131 · Draft PR #132 · **EVIDENCE_PREPARATION_ONLY / SCIENCE_PENDING**.

Read [ChatGPT B3 review #6626795633](https://github.com/simon947161/eco-agent-system/pull/132#issuecomment-6626795633), reviewing `f249128117650c3772cb848734d109541353c5d9`. B3 acceptance is limited; this C package awaits independent review.

Deliverables: [six dated climate records](CLIMATE_EVENT_REGISTER.json), [evidence matrix](EVIDENCE_MATRIX.md), [climate-index context](CLIMATE_INDEX_CONTEXT.json), [source ledger](SOURCES.json), [Cooma audit](COOMA_PUBLIC_AUDIT.md), [facility follow-up](FACILITY_FOLLOWUP.json), [relationship diagram](RELATIONSHIP_MAP.md), [quality/protocol](PROTOCOL_AND_QUALITY.md), [ten-page Slides](index.html), [handoff](NEXT_SESSION.md).

Observations: BOM historical summaries provide two hot-day maxima, two 2019 annual low-rainfall records, Cooma 6 June 2016 daily rainfall and Rockhampton March 2017 wet-month context. All are published values; no derived emissions or fitted model. Rockhampton local daily storm amount is still UNKNOWN. Cooma licence 6194 is verifiable as a **2017 historical document**, not current authorisation. Prior three facility candidates are preserved. All facility geometry/current gas data remain UNKNOWN.

Interpretation: climate evidence is sufficient for source planning and review, not a station-to-facility exposure join or greenhouse-gas response claim. Numerical index series, process measurements, completeness and calibration remain missing. All values, source reading depths and limitations are explicitly registered. No raw HTTP body snapshots; hashes apply only to authored package. No restricted-source retries.

## Review questions

1. Are reported-day versus monthly/annual windows clearly distinguished, including the Rockhampton rainfall gap?
2. Are low-rainfall years framed conservatively as drought context, not established facility water stress?
3. Is the 2017 Cooma licence link properly separated from current permit/operator/geometry validity?
4. Are retrospective index phases kept separate from forecast vintages and outside-window events?
5. Does the relationship graph expose the blocked exposure/process/flux links without implying causality?
6. What minimum public measurement pack would justify a later bounded specification? No experiment is authorised by this package.

## Conversation Radar

- Knowledge: weather observation, regional climate phase, facility condition and gas flux have different temporal/spatial support.
- Idea: preserve an assertion-level evidence graph with blocked links visible.
- Decision: move to climate evidence without recurring tiny identity searches; keep four candidates partial and source vintages explicit.
- Risks: preliminary summaries, unknown daily QC, selection bias, source reuse limits, old permits, false spatial joins.
- Open: storm-day Rockhampton values, matched index series, current facility instruments and measured process/flux series.
- Next: ChatGPT review; then bounded public-source gap prioritisation. Separate Founder approval for experiments.
- Keywords: ClimateOS, CarbonOS, EcoEngine, Cooma, Rockhampton, BOM, CH4, N2O, CO2, MRV, extreme climate.
