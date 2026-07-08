# Task194 Translation Governance Review

## Purpose

Task194 defines the translation governance review required before non-English or multilingual source material may support future mapping or evidence reasoning.

This task does not translate, interpret, or compare source text.

## Translation Metadata Fields

| Field | Requirement |
| --- | --- |
| Official language | Required for every selected citation unit. |
| Official translation | Record only where published by an official or authorized source. |
| Working translation | Internal navigation aid only; cannot support claims. |
| Translation authority | Official owner, authorized translator, human reviewer, machine translation, or unknown. |
| Translation review status | Not reviewed, machine-only, human reviewed, legal/domain reviewed, or official translation. |
| Translation uncertainty marker | Required for machine, partial, ambiguous, or unofficial translations. |
| Translation review date | Required before future use in mapping or reasoning. |
| Reviewer role | Translator, domain reviewer, legal/regulatory reviewer, or Founder reviewer. |

## Translation Review Workflow

```text
Official source located
-> official language recorded
-> official translation checked
-> working translation marked if used
-> human translation review required where no official translation exists
-> domain/legal review required where source authority or jurisdiction matters
-> uncertainty marker retained until review is complete
-> future mapping remains blocked until translation gate is satisfied
```

## Framework Translation Requirements

| Framework family | Translation governance requirement |
| --- | --- |
| IPCC | Record official language and official translation status per report or factsheet. |
| ISSB / IFRS | Check IFRS translation and licensing pathways before non-English reuse. |
| ASRS | English baseline; any non-English working translation requires review. |
| TNFD | Check official recommendation/guidance language and translation status before reuse. |
| GHG Protocol | Record official language per standard/guidance document; translated inventory use requires review. |
| GRI | Check official translation availability through GRI resource pathways. |
| CDP | Check cycle-specific questionnaire and guidance language before reuse. |
| China source ecosystem | Official Chinese text is primary unless an official English source is located; working translation requires human and domain/legal review before future use. |

## Translation Uncertainty Marker

Recommended marker:

```text
TRANSLATION_REVIEW_REQUIRED
```

This marker must remain attached to any future citation unit that uses non-official or unreviewed translation.

## Boundary

Translation governance does not authorize translated claims, legal interpretations, or jurisdictional conclusions.
