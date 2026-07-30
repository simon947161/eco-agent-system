# Task2101–2110 Real Run Evidence and Validation

## Source identity

| Field | Result |
|---|---|
| Publisher | Australian Bureau of Meteorology |
| Product | Hydrologic Reference Stations daily streamflow |
| Station | 410033 — Murrumbidgee River at Mittagang Crossing |
| Unit | ML/day |
| Coverage | 1964-03-01 to 2024-02-29 |
| Rows | 21,915 |
| Source SHA-256 | `12740d6edc884b3f7a960935215cdff1bdbe5bd85c9c9a96d3aa219272d31534` |
| Retrieval status | HTTP 200, zero cost |

The 2026-07-30 retrieval reproduced the exact content digest recorded in
PR #108. Raw rows remain in gitignored local evidence storage.

## Data-quality profile

| Check | Result |
|---|---:|
| Missing calendar dates | 0 |
| Blank flow values | 0 |
| Duplicate dates | 0 |
| Invalid rows | 0 |
| A — best available | 11,280 / 51.5% |
| B — good | 7,192 / 32.8% |
| C — poor | 156 / 0.7% |
| E — unreliable | 3,287 / 15.0% |
| G — gap filled | 0 / 0.0% |

The source header says gaps were filled with a daily rainfall-runoff model,
while no published row carries code G. The implementation records this tension
and does not invent a resolution.

## Independently spot-checked calculations

The highest-impact values were recomputed with Python `statistics.median`
outside the implementation path:

| Calculation | Independent result | Implementation result |
|---|---:|---:|
| All-published daily median | 148.956278 ML/day | 148.956 ML/day |
| A+B daily median | 142.087056 ML/day | 142.087 ML/day |
| September daily median | 461.772130 ML/day | 461.772 ML/day |
| Quality counts | A 11,280; B 7,192; C 156; E 3,287 | exact match |

## Main descriptive indicators

| Method | P10 | Median | P90 | Maximum |
|---|---:|---:|---:|---:|
| All published | 37.325 | 148.956 | 802.422 | 38,352.186 |
| A+B screen | 36.029 | 142.087 | 707.575 | 25,583.446 |

All values are ML/day. The A+B median is 4.61% below the all-published median.
That difference is reported as method sensitivity, not measurement
uncertainty.

Seasonal all-published medians:

| Season | Median ML/day |
|---|---:|
| Summer (DJF) | 90.894 |
| Autumn (MAM) | 64.110 |
| Winter (JJA) | 210.344 |
| Spring (SON) | 354.764 |

These values describe the admitted historical record only. They do not explain
causes and do not predict a future season.

## Reproducibility

- identical source bytes and identical `issued_at` produced a byte-for-byte
  identical output directory;
- focused tests: 4 passed;
- full suite: pending final PR verification;
- JSON parse: required before publication;
- SVGs were rasterised and visually inspected;
- charts use labelled units, declared periods, zero baselines where applicable,
  and no dual axes;
- annual chart states that it is not a formal trend test.

## Visual QA findings

1. Monthly chart clearly separates all-published median, A+B median and P10/P90.
2. Quality composition makes the temporal quality shift visible and prevents
   the annual line from being read without its primary caveat.
3. Annual medians show large variability but carry no fitted trend line or
   causal annotation.
4. All figures state station, period or method boundary in title/subtitle.

## Validation assessment

**Overall:** `SHARE WITH CAVEATS / FOUNDER EVIDENCE REVIEW`

Ready for:

- repository review;
- reproducibility review;
- method discussion;
- preparation of a later near-current evidence gate.

Not ready for:

- L3 environmental assessment;
- formal trend or change-point language;
- present-day water condition;
- operational, engineering or public communication.

## Required hydrology review questions

1. Is A+B an appropriate sensitivity screen for this HRS product?
2. How should the source gap-fill statement be reconciled with zero G-coded
   rows?
3. What serial-dependence, seasonality and quality treatment is required before
   trend analysis?
4. For which later local question is gauge 410033 spatially representative?
