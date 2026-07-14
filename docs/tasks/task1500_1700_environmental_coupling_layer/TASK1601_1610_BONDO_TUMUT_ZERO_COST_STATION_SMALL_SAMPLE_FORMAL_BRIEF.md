# ClimateOS Task1601–1610 — Bondo–Tumut Zero-Cost Station Eligibility and Small-Sample Wind Evidence Formal Brief

Date: 2026-07-14  
Status: FOUNDER_AUTHORIZED / ZERO_COST_PUBLIC_SAMPLE / NO_SITE_WIND_CONCLUSION  
Repository: `simon947161/eco-agent-system`  
Branch: `agent/task1601-1610-bondo-station-small-sample`  
Base merge commit: `820d3d822a57cc2cdabe3a8b1ceaf2f08304da62`

## 1. Authorization and inherited controls

The Founder authorized merge of PR #63 and Task1601–1610.

Execution uses the conservative defaults inherited from Task1591–1600:

- zero-cost, no-registration public sources only;
- public webpage review and a minimal station sample;
- no account, FTP, NCI, cloud-object or paid access;
- no raw source data committed to GitHub;
- GitHub receives provenance, methods and derived summaries;
- no reviewer contact;
- no wind-resource, energy-yield, planning, safety, investment or project-viability conclusion.

PR #63 was merged at `820d3d822a57cc2cdabe3a8b1ceaf2f08304da62`.

## 2. Project and study-area lock

Primary object: proposed Bondo Wind Farm.

Controlling public identity:

- NSW application `SSD-86276211`;
- EPBC referral `2026/10465`;
- predominantly within State forest and plantation areas at Bondo, Wee Jasper, Billapaloola and Red Hill;
- approximately 15 km north-east of Tumut in the EPBC public description;
- current planning stage, not an operating wind farm.

The EPBC public record identifies a 41,923 ha project area and an indicative layout attachment. No machine-readable authoritative project polygon was acquired in this task. Exact station-to-boundary distance therefore remains blocked.

## 3. Task claim

`PUBLIC_STATION_SAMPLE_DEMONSTRATES_REPRESENTATIVENESS_LIMITS`

Question:

> Do accessible public station observations provide enough comparable evidence to characterize Bondo site wind, or do they instead demonstrate the need for project-area measurements and stronger spatial evidence?

## 4. Task map

| Task | Deliverable |
|---|---|
| 1601 | Merge lineage, authorization and scope lock |
| 1602 | Authoritative project-boundary availability check |
| 1603 | Public station candidate discovery |
| 1604 | Station identity, location, elevation and record check |
| 1605 | Wind statistic, time-support and instrument-height check |
| 1606 | Zero-cost June–July 2026 sample acquisition |
| 1607 | Pre-registered descriptive-statistic run |
| 1608 | Representativeness and uncertainty assessment |
| 1609 | Licence, storage, human-review and cost gate |
| 1610 | Closure and next-gate decision |

## 5. Selected public stations

Two contrasting public stations were selected for a bounded demonstration:

1. Wagga Wagga AMO, station `072150`, latitude 35.16°S, longitude 147.46°E, elevation 212 m;
2. Cabramurra SMHEA AWS, station `072161`, latitude 35.94°S, longitude 148.38°E, elevation 1,482 m.

They bracket different regional exposures. Neither is admitted as representative of the Bondo plantation/ridge project area.

Tumut public climate-summary records do not provide an adequate current wind series. Tumbarumba combines data sources and does not solve project-area representativeness. Portable emergency-service stations are not admitted for climatology.

## 6. Sample window

- Wagga Wagga: 2026-06-01 to 2026-07-14 public Daily Weather Observation pages;
- Cabramurra: 2026-06-01 to 2026-07-10 on the public pages available during review;
- June Cabramurra page was prepared before 30 June and contains 29 reported days;
- July is provisional and subject to later Bureau correction.

The sample is a method demonstration, not the planned 2021–2026 evidence series.

## 7. Admitted variables

- daily maximum wind gust speed, km/h, 24 hours to midnight;
- 9am wind speed, km/h, 10-minute mean before 9am;
- 3pm wind speed, km/h, 10-minute mean before 3pm.

Wind instrument height is `UNVERIFIED` for both stations in the public material reviewed. This blocks height-equivalent comparison with project hub height.

## 8. Permitted statistics

- available count and page-relative completeness;
- arithmetic mean;
- median;
- linearly interpolated P90 and P95;
- maximum;
- calm frequency for the 9am/3pm fields where the page reports Calm.

No Weibull fitting, vertical extrapolation, capacity factor, energy yield or cross-station skill score is authorized.

## 9. Sources

Accessed 2026-07-14:

- [NSW Planning Portal — Bondo Wind Farm](https://www.planningportal.nsw.gov.au/major-projects/projects/bondo-wind-farm)
- [EPBC Public Portal — Bondo Wind Farm](https://epbcpublicportal.environment.gov.au/all-referrals/project-referral-summary/?id=91a0bb3b-f91c-f111-8341-002248989885)
- [BoM Wagga Wagga June 2026 Daily Weather Observations](https://www.bom.gov.au/climate/dwo/202606/html/IDCJDW2139.202606.shtml)
- [BoM Wagga Wagga current Daily Weather Observations](https://www.bom.gov.au/climate/dwo/IDCJDW2139.latest.shtml)
- [BoM Cabramurra June 2026 Daily Weather Observations](https://www.bom.gov.au/climate/dwo/202606/html/IDCJDW2023.202606.shtml)
- [BoM Cabramurra current Daily Weather Observations](https://www.bom.gov.au/climate/dwo/IDCJDW2023.latest.shtml)
- [BoM Wagga Wagga station climate statistics](https://www.bom.gov.au/climate/averages/tables/cw_072150.shtml)
- [BoM Cabramurra station climate statistics](https://www.bom.gov.au/climate/averages/tables/cw_072161.shtml)
- [BoM Daily Weather Observation notes](https://www.bom.gov.au/climate/dwo/IDCJDW0000.shtml)

## 10. Hard stop

Do not start Task1611+, obtain paid or registered data, contact candidate reviewers, infer Bondo hub-height wind, estimate energy yield or merge the resulting Draft PR automatically.
