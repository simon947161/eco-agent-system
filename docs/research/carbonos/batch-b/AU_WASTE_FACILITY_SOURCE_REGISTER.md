# 澳大利亚全国废弃物与污水设施：官方来源调查

Batch B · 2026-11-04 · Issue #131 / Draft PR #132。**来源覆盖九个行政层级，不代表设施普查完成。** 本轮20个唯一来源入口，实际设施记录提取0；不提供全国设施数量或全国排放量。P1-A科学准入PENDING。

## 评审落实

已读取[ChatGPT评审](https://github.com/simon947161/eco-agent-system/pull/132#issuecomment-6620045777)，其对象为9320a8a4e33193af613022eb9b900dbddb5fc1c6。接受的是有界归档，不是20式独立认证。法律版本、摘要级文献、过程参数和不同站点统计窗的问题继续开放。不得以本轮来源等级替代科学准入。

## 来源等级、字段与许可

A：已逐项核查的官方、带日期设施记录；B：已核对官方目录/数据集/指导说明，但未核查个体记录；C：官方入口线索或访问受阻、关键字段未核实。本轮无A记录。等级衡量可用性，不衡量保证或合规。

所有坐标精度目前为null/UNKNOWN，不由小数位推断米级精度。CRS也未从二手描述升级为已核对。数据许可均UNKNOWN_NOT_CHECKED：公开可读不等于可批量再发布，下一步逐数据集读取许可。未抓取设施名单、个人联系人或许可全文。来源访问日期不当成数据年份。

## 来源登记

| ID / 辖区 | 官方来源 | 范围与年份 | 位置 / 身份 | 可用性等级 |
|---|---|---|---|---|
| FED_WASTE / Commonwealth | [Waste and resource recovery infrastructure database](https://www.dcceew.gov.au/environment/protection/publications/waste-resource-recovery-infrastructure-db) | 2022 non-hazardous;2021 hazardous; National historical list; publisher warns outdated; downloads not ingested | Map/catalogue; accuracy UNKNOWN; Source row ID to inspect; not operator name | B / OFFICIAL_WEB_TEXT |
| FED_GA_WW / Commonwealth | [Wastewater Treatment Facilities dataset 151185](https://pid.geoscience.gov.au/dataset/ga/151185) | Primary version not verified; Primary landing inaccessible; secondary metadata suggests June2026 revision; not adopted as verified | Point layer lead; precision UNKNOWN; Dataset151185; feature IDs not inspected | C / PRIMARY_UNAVAILABLE |
| FED_NPR / Commonwealth | [National performance report](https://www.bom.gov.au/water/npr/) | 2024-25; Service-provider reporting, not physical facility census; reporting framework/coverage changes | Reporting regions; not plant geometry; Provider ID + reporting year; not site ID | B / OFFICIAL_WEB_TEXT |
| FED_NPI / Commonwealth | [NPI substances and thresholds](https://www.dcceew.gov.au/environment/protection/npi/substances/substance-list-and-thresholds) | Page updated2022-07-23; report years separate; Threshold-dependent reporting; neither complete facility nor GHG census | No coordinates on this guidance page; NPI facility ID in downstream data, not inspected | B / OFFICIAL_WEB_TEXT |
| NSW_POEO / NSW | [POEO public registers](https://www.epa.nsw.gov.au/Licensing-and-Regulation/Public-registers) | Live portal; per-licence dates; Licensed/regulatory universe; exemptions and small sites require separate coverage | Premises/document location; numeric precision UNKNOWN; EPL number + premises + version | B / OFFICIAL_WEB_TEXT |
| VIC_PERMIT / VIC | [Register of permissioning decisions](https://www.epa.vic.gov.au/public-registers?register=permissions) | Permissions since2021-07-01; overnight updates; Permissions include licences/permits/registrations; pre2021 records separate | Location field; accuracy UNKNOWN; Permission/statutory ID + premises; multiple instruments per site | B / OFFICIAL_WEB_TEXT |
| VIC_MAP / VIC | [Victoria Unearthed EPA licensed sites](https://www.environment.vic.gov.au/sustainability/victoria-unearthed/about-the-data/epa-licenced-sites) | Live layer; row date not inspected; Currently licensed sites subset; overlaps permission register | Points and site boundary polygons; precision UNKNOWN; Licence crosslink; same dataset family as VIC_PERMIT | B / OFFICIAL_WEB_TEXT |
| QLD_EA / QLD | [Environmental authorities search](https://www.apps.des.qld.gov.au/public-register/search/ea.php) | Current and expired/cancelled/surrendered versions; Authority may span activities/locations; historical ERA names differ | Address/lot-plan/locality; not complete spatial solution; Permit Reference + effective date + individual premises | B / OFFICIAL_WEB_TEXT |
| QLD_STP / QLD | [Sewage facilities and monitoring points](https://wetlandinfo.detsi.qld.gov.au/wetlands/assessment/monitoring/point-source-release/sewage-treatment-facilities/) | Page labels last updated2016-01-27; data currency unresolved; Point-source monitoring programme; facility and monitoring-point KML separate | KML points advertised; coordinates not extracted; accuracy UNKNOWN; Facility identity must differ from monitoring point ID | B / OFFICIAL_WEB_TEXT |
| QLD_DATA / QLD | [Environmental authorities machine-readable metadata](https://www.data.qld.gov.au/dataset/environmental-authorities/resource/a9658145-87bd-4258-a689-5aec29d49792) | Portal archive checked2026-10-02; effective dates separate; Same authority family as QLD_EA; do not add counts; Excel long-cell truncation warning | Locations text; no numeric coordinate column in exposed schema; Permit Reference metadata primary key; not physical site key | B / OFFICIAL_WEB_TEXT |
| WA_GUIDE / WA | [Prescribed premises licences and approvals](https://www.wa.gov.au/service/environment/environment-information-services/licences-and-works-approvals-prescribed-premises) | Guidance updated2026-10-06; Prescribed premises scope; approval to construct does not prove operation | Document location; precision UNKNOWN; Licence/works approval + premises + version | B / OFFICIAL_WEB_TEXT |
| WA_SEARCH / WA | [Legacy search landing](https://der.wa.gov.au/) | UNKNOWN; Official search result identifies licence search; direct403 stopped | UNKNOWN; Instrument IDs uninspected | C / SEARCH_TEXT_DIRECT403_STOPPED |
| SA_REGISTER / SA | [Public register](https://www.epa.sa.gov.au/public_register) | UNKNOWN; Official EPA help page confirms licence search; register403 stopped; contents not inspected | UNKNOWN; EPA licence number to inspect | C / OFFICIAL_HELP_CONFIRMED_REGISTER403_STOPPED |
| TAS_MAP / TAS | [EPA regulated premises / LISTmap](https://epa.tas.gov.au/business-industry/site-information) | Documents updated to map within24h; site survey dates UNKNOWN; Level2 activities and contaminated sites; filter categories; not universal facility census | Map locations; search by name/category/coordinates; precision UNKNOWN; Premises key + regulatory document, not each document as site | B / OFFICIAL_WEB_TEXT |
| TAS_WW / TAS | [Wastewater regulatory scope](https://epa.tas.gov.au/business-industry/regulation/wastewater/legislative-context-for-wastewater-management) | Live guidance; individual dates UNKNOWN; Local governments regulate below100kL/day and onsite systems; EPA/TasWater coverage not all systems | No site coordinates on scope page; Separate local/Level2/operator scopes | B / OFFICIAL_WEB_TEXT |
| NT_EPL / NT | [Environment protection licences](https://ntepa.nt.gov.au/your-business/public-registers/licences-and-approvals-register/environment-protection-licences) | Live list; licence dates per document; Includes transport-only companies; exclude mobile handlers from physical-facility count | Document-specific location; UNKNOWN precision; Licence + premises; holder list is not site identity | B / OFFICIAL_WEB_TEXT |
| NT_WDL / NT | [Waste discharge licences](https://ntepa.nt.gov.au/your-business/public-registers/licences-and-approvals-register/waste-discharge-licences) | Live list; licence periods per document; Sewage subcategory includes utility and remote-community entries; also mining/dredging excluded | Discharge point must not substitute plant centroid; accuracy UNKNOWN; WDL number + plant + discharge-point relation | B / OFFICIAL_WEB_TEXT |
| ACT_EPA / ACT | [Environment authorisations register route](https://www.accesscanberra.act.gov.au/city-services/environment-protection-authority) | Live guidance; per-instrument dates UNKNOWN; Authorisations and agreements are distinct; linked portal JS shell only | UNKNOWN; Authorisation ID + premises; agreements not duplicate plant | C / GUIDANCE_READ_REGISTER_JS_SHELL |
| ACT_WASTE / ACT | [Facilities and drop off](https://www.cityservices.act.gov.au/recycling-and-waste/drop-off) | Current page; no common reporting period; Public service facilities not all commercial plants; destroyed/replacement MRF and pilot/planned FOGO distinguished | Street/locality/relocation description; precision UNKNOWN; Physical site + process units; aliases need manual check | B / OFFICIAL_WEB_TEXT |
| ACT_WW / ACT | [Lower Molonglo WQCC](https://www.iconwater.com.au/Water-education/Water-and-sewerage-system/Sewage-Treatment/Lower-Molonglo-Water-Quality-Control-Centre) | Undated operator fact page; current reporting window UNKNOWN; Single official utility facility page; not territory census | No verified numeric plant coordinates; LMWQCC alias, formal site/authorisation ID not extracted | B / OFFICIAL_WEB_TEXT |

## 去重与实体边界

本轮先对source_id和规范URL去重。QLD_EA与QLD_DATA为同一资料家族的不同入口，VIC_MAP与VIC_PERMIT是空间/许可视图；禁止相加。跨来源实体去重尚未执行，因为未导入个体设施。

后续采用四层实体：physical_site、process_unit、operator、regulatory_instrument。保留source_record_id、source_version、valid_from/to及证据链接。优先稳定设施ID交叉表；许可ID仅定位文书，可能一证多址/一址多证。名称标准化与距离只能产生待人工审查候选，不能自动合并；无坐标/精度时不能使用距离规则。厂区内填埋、转运、堆肥是不同过程；排口、监测点和运营商办公室不是设施坐标。迁址、关闭、改名保留历史关系。

设施状态分observed_operational_status、permit_status与planned_status；许可证有效不证明投运。许可容量与实际吞吐、干湿基、单位、年份分别登记；气体收集、火炬、发电、装置滑漏和实测量分别登记，缺失为unknown而非0。

## 证据缺口与下一步

联邦固废库年代较旧；GA污水原始入口本工具不可达，二手元数据不作官方版本证明。SA/WA入口拒绝、ACT登记端仅JS外壳，已停止，不绕过认证。TAS小型/分散污水、NT偏远系统、各州豁免/关闭设施及商业设施仍可能不覆盖。没有全国覆盖率分母。BOM服务商统计不分摊给设施，NPI阈值报告不替代GHG清单。

下一步优先核实可下载数据的许可、列定义、坐标CRS/精度和版本；经同意的数据提取仍先做小样本身份对账，保留冲突。没有必要新建GIS、气象API、数据库或智能体：沿用CarbonOS证据登记与版本、HRS时间语义检查及现有空间工具。批量获取被拒资料、外部请求/付费/私人Council数据均另行报告。

机器字段见JSON/CSV及SOURCE_SCHEMA.json；来源核查摘要不等于完整原网页快照。Slides仅展示研究状态，不运行排放模型。
