# ClimateOS CRP Harvest — Radar 07 to v2 Action Routing

**Date:** 2026-09-01  
**Source:** Radar 07 — China Green Development Law / Environmental Digital Capability  
**Destination:** ClimateOS v2 Architecture Review  
**Status:** ACTION INPUT / NOT A SCIENTIFIC CONCLUSION  

## Core Knowledge Points

1. China environmental governance is moving from static regulation toward time-aware, digitally managed evidence systems. The 2026 Ecological Environment Code transition reinforces the need for legal-version and rule-lineage handling in ClimateOS.
2. China is building national-scale environmental intelligence infrastructure spanning monitoring stations, satellites, automated warning, data infrastructure, high-quality datasets, sovereign computing and institutional services.
3. Environmental AI capability does not always appear as a public API. Capability may be delivered through institutional cooperation, local deployment, hardware terminals, national data infrastructure, sovereign computing or controlled project access.
4. MAZU/FengYun remain strategically important external-provider candidates, but public developer API/SDK/self-service access remains unverified. ClimateOS must not infer technical connectability from international promotion or successful overseas deployment.
5. Cross-border data access is becoming more structured through national data-infrastructure and international-cooperation pilots, but access remains data-class-, jurisdiction-, provider- and project-specific.
6. Remote sensing, automated environmental monitoring and machine-assisted evidence are increasingly entering formal regulatory and technical-standard structures.
7. Governance responsibility increasingly depends not only on what happened, but on what information and evidence were reasonably available at the time a decision was made.

## Idea Points

1. Upgrade the External Environmental Intelligence Provider Registry into an **Environmental Intelligence Access Contract** rather than a simple provider/API list.
2. Add **Decision-Time Evidence State** so ClimateOS can reconstruct what was knowable before an event, not only validate conclusions after the event.
3. Add **Temporal Legal State / Rule Lineage** to preserve historical and current regulatory applicability.
4. Model environmental intelligence as a chain:

```text
Provider / Authority
→ Dataset / Observation Network
→ Access Channel
→ Processing / Compute Location
→ Model / Service
→ Evidence Object
→ Local Interpretation
→ Time-Bounded Answer
→ Human Review
```

5. Treat public information, public data, developer access, institutional access, local deployment, hardware delivery and sovereign infrastructure as separate capability states.
6. Extend Evidence Passport to represent remote-sensing provenance, monitoring-method quality, institutional credentials, data-processing location and decision-time availability.

## Wish Points

1. ClimateOS should eventually consume lawful Chinese, Australian, European and other environmental evidence through a common neutral evidence envelope without requiring all ecosystems to use the same application or cloud.
2. ClimateOS should provide anticipatory local environmental intelligence before the intervention window closes, while keeping uncertainty explicit and preserving human authority.
3. MAZU/FengYun should be connectable when a lawful and technically verified access path becomes available, without requiring major architectural redesign.
4. The same architecture should work for Cooma and other local communities rather than remaining a national/global intelligence layer.

## Reasoning Points

1. Waiting for official confirmation as the first allowable conclusion defeats the anticipatory purpose of ClimateOS; official confirmation should instead be one evidence-maturity stage.
2. Early intervention can be justified under lower evidence maturity when actions are low-regret and reversible, while high-cost or irreversible actions require stronger evidence and human review.
3. National environmental intelligence systems will not necessarily expose open developer APIs; interoperability must therefore support multiple access modes and governance conditions.
4. Local intelligence requires a tree-to-leaf translation: global driver → regional signal → local terrain/water/ecology/infrastructure → consequence → decision window.
5. A public dataset or state-backed platform cannot be assumed to be exportable, machine-accessible, reusable or legally compatible with ClimateOS merely because it exists.

## Key Decisions

1. Do **not** create a new ClimateOS radar or a MAZU-specific development branch from this Radar result.
2. Keep MAZU/FengYun as high-priority external-provider candidates, but do not build a dedicated connector until an official technical access route is verified.
3. Feed this Radar result into the existing ClimateOS v2 Architecture Review rather than starting another task-number sequence.
4. ClimateOS v2 architecture review should explicitly evaluate the following additions:
   - Decision-Time Evidence State;
   - Temporal Legal State / Rule Lineage;
   - Environmental Intelligence Access Contract;
   - Provider Access-State taxonomy;
   - Sovereign compute/data-residency fields;
   - remote-sensing/monitoring evidence-quality fields.
5. GEGG company-development and international-commercial routing remains outside ClimateOS; only technical/evidence interoperability stays here.

## Unresolved Questions

1. Which Chinese high-quality data sets are currently available in meteorology, hydrology, ecology, pollution, natural resources and remote sensing, and under what machine-access terms?
2. What environmental nodes exist in the national data infrastructure and international data-cooperation pilot zones?
3. Will MAZU, FengYun Earth or related services expose official developer APIs, SDKs, research accounts or institutional application procedures?
4. What are the precise licence, data-residency, export and result-sharing conditions for each candidate Chinese provider?
5. Which remote-sensing and monitoring standards become final and should be mapped into ClimateOS evidence-quality requirements?
6. How should Decision-Time Evidence State interact with Early-Warning Evidence Maturity and retrospective validation?

## Next Actions

### A. ClimateOS v2 Architecture Review — include in current review package

1. Add `Decision-Time Evidence State` to the v2 architecture proposal.
2. Add `Temporal Legal State / Rule Lineage` to the governance architecture.
3. Replace simple Provider Registry assumptions with an `Environmental Intelligence Access Contract` covering:
   - jurisdiction;
   - provider identity;
   - dataset/service identity;
   - public-information status;
   - public-data status;
   - developer access;
   - institutional access;
   - local deployment;
   - hardware delivery;
   - sovereign infrastructure dependency;
   - data residency;
   - inference/processing location;
   - licence;
   - cost;
   - cross-border basis;
   - result exportability;
   - provenance and audit requirements.
4. Add remote-sensing/monitoring evidence-quality fields to the Evidence Passport design.
5. Connect these additions to the existing Tree-to-Leaf and Time-Bounded Answer architecture rather than creating parallel systems.

### B. Cooma scientific track — do not derail

1. Continue current unfinished real-evidence work, including the Mittagang historical-flow intake and first bounded scientific characterisation.
2. Use the new provider/access concepts only where they directly improve Cooma evidence acquisition or interpretation.
3. Do not postpone the first real local assessment while waiting for MAZU or Chinese data access.

### C. Radar 07 watch-only continuation

Continue monitoring:

- MAZU/FengYun API, SDK, account and institutional-access routes;
- environmental high-quality datasets;
- national environmental-monitoring network machine access;
- international data-cooperation pilot environmental scenarios;
- remote-sensing monitoring standards;
- rule-transition and implementation developments relevant to ClimateOS.

## Project Keywords

`ClimateOS v2`  
`Radar 07`  
`Decision-Time Evidence`  
`Early Warning`  
`Environmental Intelligence Access Contract`  
`External Provider`  
`MAZU`  
`FengYun`  
`Sovereign Compute`  
`Data Residency`  
`Temporal Legal State`  
`Rule Lineage`  
`Remote Sensing Evidence`  
`Evidence Passport`  
`China–Global Interoperability`  
`Tree-to-Leaf`  
`Cooma`

## Mission Control Routing Note

This CRP is an input to the existing ClimateOS v2 Architecture Review. It does not authorize a new implementation batch, external contact, data acquisition, procurement, public warning, legal conclusion or MAZU integration. Any implementation should be selected through the v2 Founder Decision Package after architecture review and unfinished-PR disposition.
