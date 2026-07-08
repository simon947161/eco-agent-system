# Task183 Document Hierarchy Registry

## Purpose

Task183 describes document hierarchy metadata so that future work can avoid confusing standards, guidance, project pages, questionnaires, legal materials, and supporting documents.

This registry is metadata-only.

## Generic Hierarchy Model

```text
Framework family
-> Standard / report / recommendation / questionnaire / official notice
-> Guidance / methodology / technical note / basis document / portal version
-> FAQ / tool / support material / webinar / project page
-> Archive / prior version / consultation / exposure draft / correction
```

## Framework Hierarchy Registry

| Framework | Hierarchy metadata |
| --- | --- |
| IPCC | IPCC -> assessment cycle -> synthesis / working group / special / methodology report -> chapter / section / annex / figure / table -> factsheet / review-process material / error-handling material |
| ISSB / IFRS | IFRS Foundation -> ISSB -> IFRS Sustainability Disclosure Standards -> IFRS S1 / IFRS S2 -> amendments / taxonomy / related active projects / completed projects -> support and application materials |
| ASRS | AASB -> Australian Sustainability Reporting Standards -> Pronouncements Web Portal -> current / future / by-reporting-period version -> standard / amendment -> basis / explanatory / knowledge-hub material |
| TNFD | TNFD -> recommendations -> versioned recommendation document -> additional guidance / sector guidance / financial institution guidance -> webinars / adoption materials / support resources |
| GHG Protocol | GHG Protocol -> standard family -> standard / guidance -> corrections / appendices / tools / reporting templates -> FAQs / training / under-development materials |
| GRI | GRI -> GSSB -> standards -> topic standards -> final standard / project page / exposure draft / basis for conclusions -> submissions / FAQs / interpretations |
| CDP | CDP -> disclosure cycle -> question bank -> questionnaire / guidance / scoring methodology -> portal material -> public scores / data products |
| China source ecosystem | Official authority -> notice / regulation / standard / market rule / database / methodology -> technical guidance / consultation / implementation material -> FAQ / interpretation / local or market support material |

## Hierarchy Risk Flags

| Risk flag | Meaning |
| --- | --- |
| Guidance-not-standard | Supporting guidance must not be treated as standard text. |
| Project-not-final | Project pages, exposure drafts, consultations, and beta releases must not be treated as final text. |
| Questionnaire-not-law | Questionnaire or scoring method material must not be treated as regulation without review. |
| Portal-period-sensitive | Portal-selected standard may vary by reporting period. |
| Translation-sensitive | Working translations must not replace official source text. |
| Authority-segment-needed | Source family has multiple official authorities and must not be flattened. |

## Boundary

Hierarchy metadata does not compare framework authority or rank source quality.
