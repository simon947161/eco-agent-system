# ClimateOS Task1681–1690 — Cooma Official Source Identity and Zero-Download Metadata Admission Pilot

Status: implementation complete; independent Founder review required

Base main HEAD: `708aa9f5231e52aea85f4d280214070618ef1c52`

Access date: 2026-07-17

## Purpose

This batch gives ClimateOS a first real, public Cooma source directory without
pretending that public websites form a complete local database. It records page
identity, publisher, visible date or version state, declared geography, source
tier and admission boundary. It retains no downloaded document, dataset, page
body, customer, worksite or operational record.

## Task map

| Task | Closed result |
|---|---|
| 1681 | Verify current main after PR #72 and the later post-1700 track commit |
| 1682 | Define six source-authority tiers |
| 1683 | Verify the Cooma-Monaro LEP and DCP official landing identities |
| 1684 | Verify the South East and Tablelands 2036/2041 transition pages |
| 1685 | Verify Council water and wastewater landing identities |
| 1686 | Verify one Bureau station-metadata identity without downloading observations |
| 1687 | Verify bounded Snowy Hydro and Murrumbidgee context identities |
| 1688 | Quarantine one official news item as a discovery lead only |
| 1689 | Implement metadata schema, validator, preview and negative tests |
| 1690 | Close the pilot and return an independent Founder Gate |

## Verified identity set

Ten official HTML pages were inspected. Nine admit metadata for reference only;
one Council news page remains discovery-only. The set spans NSW legislation,
NSW Planning, Snowy Monaro Regional Council, the Bureau of Meteorology, Snowy
Hydro and the Australian Government environment department.

The bounded inspection verified that:

- an official Cooma-Monaro Local Environmental Plan 2013 page exists and showed
  an in-force version state at access time;
- the Council publishes a Cooma-Monaro DCP landing page, but the linked PDF was
  not downloaded or reviewed;
- NSW Planning simultaneously exposes the 2036 regional plan and a draft 2041
  review pathway, so transition state must be retained rather than silently
  choosing one as the final future plan;
- Council water and wastewater overview pages exist, but they are not treated as
  a complete asset or operational database;
- the Bureau publishes a Cooma Airport AWS station metadata page, but no station
  data or claim of Cooma representativeness was admitted;
- Snowy Hydro publishes a Snowy 2.0 proponent page, which is not independent
  project-performance evidence;
- a federal Murrumbidgee Valley context page exists, but its broad geography does
  not establish a Cooma catchment or local ecological state.

No specific Cooma-focused CSIRO official page was identified within this small
search. That is a deferred search state, not a finding that no such work exists.

## Zero-download definition

The authorized browser inspection read public HTML pages. The repository retains
only title, publisher, canonical URL, visible date/version state, declared
geography, access date and admission state, plus ClimateOS governance
annotations. No PDF, attachment, dataset or raw page body was downloaded into
the repository.

## Non-conclusions

This batch forms no conclusion about Cooma's environment, water quality,
catchment condition, planning effect, legal position, infrastructure state,
project performance, operational work or compliance. Public-site completeness
is explicitly `NOT_ASSUMED_COMPLETE`.
