# Bondo–Tumut Wind Project and Source Evidence Register v0.1

Date: 2026-07-14  
Status: PUBLIC_METADATA_ACQUIRED / RAW_WIND_TIMESERIES_NOT_ACQUIRED / NO_VIABILITY_CONCLUSION  
Task: ClimateOS Task1591–1600

## 1. Project identity

| Field | Verified value | Authority |
|---|---|---|
| Project | Bondo Wind Farm | NSW Planning Portal |
| NSW application | SSD-86276211 | NSW Planning Portal |
| NSW assessment | State Significant Development | NSW Planning Portal |
| NSW stage | Prepare EIS; current page shows Amend SEARs | NSW Planning Portal |
| NSW LGA | Snowy Valleys | NSW Planning Portal |
| Indicative capacity | approximately 1.2 GW | NSW Planning Portal |
| Turbines | up to 149 in current NSW record | NSW Planning Portal |
| Storage | two 400 MW / 1,600 MWh BESS systems | NSW Planning Portal |
| Commonwealth referral | EPBC 2026/10465 | NSW and EPBC portals |
| Location framing | within/around Bondo State Forest, east of Tumut | NSW, EPBC and developer records |
| Construction state | NOT STARTED in verified planning record | inference from current assessment stage; must be rechecked |
| Operating data | NONE — proposed project is not operational | planning-state inference |

The developer site uses an indicative count of 164 turbines and describes continuing surveys. The current NSW Planning Portal record uses up to 149. This is a live design difference, not an error to be silently averaged.

## 2. Controlling project sources

All accessed 2026-07-14.

1. [NSW Planning Portal — Bondo Wind Farm](https://www.planningportal.nsw.gov.au/major-projects/projects/bondo-wind-farm)  
   Controlling state planning status and current proposal description.
2. [Australian EPBC Public Portal — Bondo Wind Farm](https://epbcpublicportal.environment.gov.au/all-referrals/project-referral-summary/?id=91a0bb3b-f91c-f111-8341-002248989885)  
   Commonwealth referral description, indicative project area and proposed permanent meteorological masts.
3. [Bondo Wind Farm project site](https://bondowindfarm.com.au/)  
   Proponent description, indicative layout, community material and stated program. Not independent scientific validation.
4. [NSW Planning Portal — Saddletop Wind Farm](https://www.planningportal.nsw.gov.au/major-projects/projects/saddletop-wind-farm)  
   Nearby separate proposal; retained only to prevent project-identity confusion.
5. [NSW Planning Portal — Jeremiah Wind Farm](https://www.planningportal.nsw.gov.au/major-projects/projects/jeremiah-wind-farm)  
   Separate nearby proposal shown as withdrawn; not the selected study project.

## 3. Wind evidence source register

| Source object | Support | Access/licence state | Task decision |
|---|---|---|---|
| [BoM average monthly wind velocity maps](https://www.bom.gov.au/climate/maps/averages/wind-velocity/) | BARRA2-derived monthly average wind speed, 1991–2020; 10, 50, 100, 150 and 200 m layers; about 0.125 degree / 12.5 km | Public page; maps/graphs/diagrams state CC BY 4.0 unless otherwise noted | ADMIT for regional climatological screening only |
| [BoM atmospheric reanalysis](https://www.bom.gov.au/government-and-industry/research-and-development/research-and-development-projects/atmospheric-reanalysis) | BARRA2 system description and coverage from 1979 | Public metadata; raw archive access separate | ADMIT metadata; BLOCK bulk archive |
| [BoM Weather Station Directory](https://www.bom.gov.au/climate/data/stations/) | station identity, elements and record availability | Some monthly/daily data free; extracted data may incur charges | ADMIT metadata; station-level licence check required |
| [BoM Climate Data Online](https://www.bom.gov.au/climate/data/) | daily/monthly statistics and historical observations | Public interface; dataset-specific terms apply | ADMIT discovery; do not assume redistribution right |
| [BoM Daily Weather Observations](https://www.bom.gov.au/climate/dwo/) | daily strongest gust and 9am/3pm wind where observed | Public pages; not all stations/elements; commercial reuse not assumed | ADMIT bounded review; raw redistribution blocked pending terms |
| [BoM NSW observations](https://www.bom.gov.au/nsw/observations/nswall.shtml) | recent station wind; wind instruments may be 3 m or 10 m AGL | Public operational observations; free text products may be non-commercial | CONTEXT only; not a five-year archive |
| [BoM Tumut climate statistics](https://www.bom.gov.au/climate/averages/tables/cw_072046.shtml) | historical station summary; wind coverage is limited | Public summary | ADMIT only as a station-coverage warning |
| [BoM copyright](https://www.bom.gov.au/copyright) | general requirement to check page- and dataset-specific terms | Some content CC BY; other content subject to data licence | CONTROLLING licence rule |
| [BoM data catalogue licence guide](https://www.bom.gov.au/metadata/catalogue/license.shtml) | unregistered, registered and paid access categories | dataset-specific use, redistribution and commercial constraints | CONTROLLING admission gate |
| [BoM data services](https://www.bom.gov.au/resources/data-services) | some public text products free/non-commercial; extensive datasets may be paid | price not established | PAID/COMMERCIAL path blocked |
| NCI BARRA archive | large reanalysis archive | registration/allocation and terms require separate verification | BLOCKED in this task |
| Proponent met-mast / LiDAR records | probable site-specific wind evidence | not public in sources reviewed | REQUIRED LATER; no access authority |

## 4. Licence interpretation

“Visible on a website” does not mean “free to copy into GitHub.”

- The BoM monthly wind-map page explicitly marks maps, graphs and diagrams as CC BY 4.0 unless otherwise noted.
- Other BoM observations may be free to view but have non-commercial or dataset-specific constraints.
- Data extraction can incur charges.
- GitHub may contain URLs, metadata, checksums, code and redistributable summaries.
- Raw files may be committed only when the exact source licence permits redistribution and the file is small.
- Attribution for admitted CC BY material should use: “Bureau of Meteorology, © Commonwealth of Australia, licensed under CC BY 4.0,” with source URL and access date.

## 5. Acquired evidence state

Acquired in this task:

- project status and identity metadata;
- proposal-scale metadata;
- public source and licence metadata;
- aggregate climatology product identity;
- station-discovery and observation-product identity.

Not acquired:

- raw hourly or sub-hourly station time series;
- raw BARRA2 grids;
- ACCESS fields;
- ADFD grids;
- proponent met-mast or LiDAR data;
- turbine power curves;
- site layout GIS;
- terrain, forestry, ecology, noise or grid-connection datasets.

## 6. Current evidence decision

`PROJECT_CONTEXT_CONFIRMED / PUBLIC_REGIONAL_SCREENING_DESIGNABLE / SITE_WIND_RESOURCE_UNSUPPORTED`

The public record is sufficient to justify a bounded evidence study. It is not sufficient to determine whether the proposed wind farm has an adequate wind resource.
