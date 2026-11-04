"""Authored official-source catalogue and offline slides; no facility/emission inference."""
from pathlib import Path
import csv,json,hashlib,html,re
B=Path(__file__).resolve().parent
rows=[]
def add(id,j,agency,title,url,types,period,coverage,location,identity,activity,control,tier='B',access='OFFICIAL_WEB_TEXT',licence='UNKNOWN_NOT_CHECKED'):
 rows.append(dict(source_id=id,jurisdiction=j,publisher=agency,title=title,canonical_url=url,facility_types=types,reporting_period=period,coverage_limit=coverage,location_representation=location,coordinate_accuracy_m=None,crs='UNKNOWN',identity_key=identity,operational_status='SOURCE_SPECIFIC_NOT_EXTRACTED',throughput_availability=activity,gas_control_availability=control,data_licence=licence,evidence_tier=tier,access_status=access,checked_date='2026-11-04',facility_records_extracted=0,science_admission='PENDING'))
add('FED_WASTE','Commonwealth','DCCEEW','Waste and resource recovery infrastructure database','https://www.dcceew.gov.au/environment/protection/publications/waste-resource-recovery-infrastructure-db','landfill;organics;transfer;recycling;hazardous','2022 non-hazardous;2021 hazardous','National historical list; publisher warns outdated; downloads not ingested','Map/catalogue; accuracy UNKNOWN','Source row ID to inspect; not operator name','Workbook fields not inspected; capacity not actual throughput','UNKNOWN')
add('FED_GA_WW','Commonwealth','Geoscience Australia','Wastewater Treatment Facilities dataset 151185','https://pid.geoscience.gov.au/dataset/ga/151185','wastewater;lagoon candidate','Primary version not verified','Primary landing inaccessible; secondary metadata suggests June2026 revision; not adopted as verified','Point layer lead; precision UNKNOWN','Dataset151185; feature IDs not inspected','UNKNOWN','UNKNOWN','C','PRIMARY_UNAVAILABLE')
add('FED_NPR','Commonwealth','BOM','National performance report','https://www.bom.gov.au/water/npr/','wastewater','2024-25','Service-provider reporting, not physical facility census; reporting framework/coverage changes','Reporting regions; not plant geometry','Provider ID + reporting year; not site ID','Provider aggregate indicators in Part B; no site allocation','Provider GHG indicators; not site capture')
add('FED_NPI','Commonwealth','DCCEEW','NPI substances and thresholds','https://www.dcceew.gov.au/environment/protection/npi/substances/substance-list-and-thresholds','reporting-facility crosscheck','Page updated2022-07-23; report years separate','Threshold-dependent reporting; neither complete facility nor GHG census','No coordinates on this guidance page','NPI facility ID in downstream data, not inspected','Not a throughput census','Not CH4 capture inventory')
add('NSW_POEO','NSW','NSW EPA','POEO public registers','https://www.epa.nsw.gov.au/Licensing-and-Regulation/Public-registers','landfill;organics;transfer;recycling;wastewater candidates','Live portal; per-licence dates','Licensed/regulatory universe; exemptions and small sites require separate coverage','Premises/document location; numeric precision UNKNOWN','EPL number + premises + version','Licence conditions/studies may contain capacity; actual volumes unverified','Document-specific; UNKNOWN')
add('VIC_PERMIT','VIC','EPA Victoria','Register of permissioning decisions','https://www.epa.vic.gov.au/public-registers?register=permissions','landfill;organics;transfer;recycling;wastewater candidates','Permissions since2021-07-01; overnight updates','Permissions include licences/permits/registrations; pre2021 records separate','Location field; accuracy UNKNOWN','Permission/statutory ID + premises; multiple instruments per site','Performance statements linked; no site extraction','Conditions/performance statements; UNKNOWN')
add('VIC_MAP','VIC','Victorian Government','Victoria Unearthed EPA licensed sites','https://www.environment.vic.gov.au/sustainability/victoria-unearthed/about-the-data/epa-licenced-sites','licensed waste;wastewater candidates','Live layer; row date not inspected','Currently licensed sites subset; overlaps permission register','Points and site boundary polygons; precision UNKNOWN','Licence crosslink; same dataset family as VIC_PERMIT','UNKNOWN','UNKNOWN')
add('QLD_EA','QLD','Queensland Government','Environmental authorities search','https://www.apps.des.qld.gov.au/public-register/search/ea.php','landfill;organics;transfer;recycling;wastewater candidates','Current and expired/cancelled/surrendered versions','Authority may span activities/locations; historical ERA names differ','Address/lot-plan/locality; not complete spatial solution','Permit Reference + effective date + individual premises','Annual returns separately available; no actual quantities extracted','Document-specific; UNKNOWN')
add('QLD_STP','QLD','Queensland Government WetlandInfo','Sewage facilities and monitoring points','https://wetlandinfo.detsi.qld.gov.au/wetlands/assessment/monitoring/point-source-release/sewage-treatment-facilities/','wastewater;lagoon candidate','Page labels last updated2016-01-27; data currency unresolved','Point-source monitoring programme; facility and monitoring-point KML separate','KML points advertised; coordinates not extracted; accuracy UNKNOWN','Facility identity must differ from monitoring point ID','Monitoring programme does not imply daily inflow data','UNKNOWN')
add('QLD_DATA','QLD','Queensland Open Data','Environmental authorities machine-readable metadata','https://www.data.qld.gov.au/dataset/environmental-authorities/resource/a9658145-87bd-4258-a689-5aec29d49792','same as QLD_EA','Portal archive checked2026-10-02; effective dates separate','Same authority family as QLD_EA; do not add counts; Excel long-cell truncation warning','Locations text; no numeric coordinate column in exposed schema','Permit Reference metadata primary key; not physical site key','Activities not measured throughput','UNKNOWN')
add('WA_GUIDE','WA','DWER / WA Government','Prescribed premises licences and approvals','https://www.wa.gov.au/service/environment/environment-information-services/licences-and-works-approvals-prescribed-premises','landfill;organics;transfer;recycling;wastewater candidates','Guidance updated2026-10-06','Prescribed premises scope; approval to construct does not prove operation','Document location; precision UNKNOWN','Licence/works approval + premises + version','Permitted capacity may be in documents; not actual annual volume','UNKNOWN')
add('WA_SEARCH','WA','DWER','Legacy search landing','https://der.wa.gov.au/','same as WA_GUIDE','UNKNOWN','Official search result identifies licence search; direct403 stopped','UNKNOWN','Instrument IDs uninspected','UNKNOWN','UNKNOWN','C','SEARCH_TEXT_DIRECT403_STOPPED')
add('SA_REGISTER','SA','EPA South Australia','Public register','https://www.epa.sa.gov.au/public_register','licensed waste;wastewater candidates','UNKNOWN','Official EPA help page confirms licence search; register403 stopped; contents not inspected','UNKNOWN','EPA licence number to inspect','UNKNOWN','UNKNOWN','C','OFFICIAL_HELP_CONFIRMED_REGISTER403_STOPPED')
add('TAS_MAP','TAS','EPA Tasmania','EPA regulated premises / LISTmap','https://epa.tas.gov.au/business-industry/site-information','landfill;organics;recycling;wastewater candidates','Documents updated to map within24h; site survey dates UNKNOWN','Level2 activities and contaminated sites; filter categories; not universal facility census','Map locations; search by name/category/coordinates; precision UNKNOWN','Premises key + regulatory document, not each document as site','Permit/notice-specific; UNKNOWN','UNKNOWN')
add('TAS_WW','TAS','EPA Tasmania','Wastewater regulatory scope','https://epa.tas.gov.au/business-industry/regulation/wastewater/legislative-context-for-wastewater-management','wastewater;lagoon candidate','Live guidance; individual dates UNKNOWN','Local governments regulate below100kL/day and onsite systems; EPA/TasWater coverage not all systems','No site coordinates on scope page','Separate local/Level2/operator scopes','Threshold is regulatory scope not throughput observation','UNKNOWN')
add('NT_EPL','NT','NT EPA','Environment protection licences','https://ntepa.nt.gov.au/your-business/public-registers/licences-and-approvals-register/environment-protection-licences','landfill;transfer;recycling;listed-waste processing','Live list; licence dates per document','Includes transport-only companies; exclude mobile handlers from physical-facility count','Document-specific location; UNKNOWN precision','Licence + premises; holder list is not site identity','Listed-waste company summary is handling permission, not quantity','UNKNOWN')
add('NT_WDL','NT','NT EPA','Waste discharge licences','https://ntepa.nt.gov.au/your-business/public-registers/licences-and-approvals-register/waste-discharge-licences','wastewater;lagoon candidate','Live list; licence periods per document','Sewage subcategory includes utility and remote-community entries; also mining/dredging excluded','Discharge point must not substitute plant centroid; accuracy UNKNOWN','WDL number + plant + discharge-point relation','Monitoring reports may contain discharge, not always influent','UNKNOWN')
add('ACT_EPA','ACT','Access Canberra','Environment authorisations register route','https://www.accesscanberra.act.gov.au/city-services/environment-protection-authority','regulated waste;wastewater candidates','Live guidance; per-instrument dates UNKNOWN','Authorisations and agreements are distinct; linked portal JS shell only','UNKNOWN','Authorisation ID + premises; agreements not duplicate plant','UNKNOWN','UNKNOWN','C','GUIDANCE_READ_REGISTER_JS_SHELL')
add('ACT_WASTE','ACT','ACT City Services','Facilities and drop off','https://www.cityservices.act.gov.au/recycling-and-waste/drop-off','landfill;organics;transfer;recycling','Current page; no common reporting period','Public service facilities not all commercial plants; destroyed/replacement MRF and pilot/planned FOGO distinguished','Street/locality/relocation description; precision UNKNOWN','Physical site + process units; aliases need manual check','No common annual activity series','Mugga gas-to-energy described; measured capture UNKNOWN')
add('ACT_WW','ACT','Icon Water','Lower Molonglo WQCC','https://www.iconwater.com.au/Water-education/Water-and-sewerage-system/Sewage-Treatment/Lower-Molonglo-Water-Quality-Control-Centre','wastewater','Undated operator fact page; current reporting window UNKNOWN','Single official utility facility page; not territory census','No verified numeric plant coordinates','LMWQCC alias, formal site/authorisation ID not extracted','Approximate daily facts not matched audited annual series','Biosolids incineration described; CH4 control UNKNOWN')

def write(n,t): (B/n).write_text(t,encoding='utf-8',newline='\n')
write('AU_WASTE_FACILITY_SOURCE_REGISTER.json',json.dumps(rows,ensure_ascii=False,indent=2))
with (B/'AU_WASTE_FACILITY_SOURCE_REGISTER.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
write('SOURCE_SCHEMA.json',json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Official source catalogue, not facility census','type':'array','items':{'type':'object','required':list(rows[0]),'additionalProperties':False,'properties':{k:({'type':['number','null'],'minimum':0} if k=='coordinate_accuracy_m' else {'type':'integer','minimum':0} if k=='facility_records_extracted' else {'enum':['A','B','C']} if k=='evidence_tier' else {'enum':['PENDING']} if k=='science_admission' else {'type':'string'}) for k in rows[0]}}},indent=2))
intro='''# 澳大利亚全国废弃物与污水设施：官方来源调查

Batch B · 2026-11-04 · Issue #131 / Draft PR #132。**来源覆盖九个行政层级，不代表设施普查完成。** 本轮20个唯一来源入口，实际设施记录提取0；不提供全国设施数量或全国排放量。P1-A科学准入PENDING。

## 评审落实

已读取[ChatGPT评审](https://github.com/simon947161/eco-agent-system/pull/132#issuecomment-6620045777)，其对象为9320a8a4e33193af613022eb9b900dbddb5fc1c6。接受的是有界归档，不是20式独立认证。法律版本、摘要级文献、过程参数和不同站点统计窗的问题继续开放。不得以本轮来源等级替代科学准入。

## 来源等级、字段与许可

A：已逐项核查的官方、带日期设施记录；B：已核对官方目录/数据集/指导说明，但未核查个体记录；C：官方入口线索或访问受阻、关键字段未核实。本轮无A记录。等级衡量可用性，不衡量保证或合规。

所有坐标精度目前为null/UNKNOWN，不由小数位推断米级精度。CRS也未从二手描述升级为已核对。数据许可均UNKNOWN_NOT_CHECKED：公开可读不等于可批量再发布，下一步逐数据集读取许可。未抓取设施名单、个人联系人或许可全文。来源访问日期不当成数据年份。

## 来源登记

'''
table='| ID / 辖区 | 官方来源 | 范围与年份 | 位置 / 身份 | 可用性等级 |\n|---|---|---|---|---|\n'
for r in rows:table+=f'| {r["source_id"]} / {r["jurisdiction"]} | [{r["title"]}]({r["canonical_url"]}) | {r["reporting_period"]}; {r["coverage_limit"]} | {r["location_representation"]}; {r["identity_key"]} | {r["evidence_tier"]} / {r["access_status"]} |\n'
write('AU_WASTE_FACILITY_SOURCE_REGISTER.md',intro+table+'''
## 去重与实体边界

本轮先对source_id和规范URL去重。QLD_EA与QLD_DATA为同一资料家族的不同入口，VIC_MAP与VIC_PERMIT是空间/许可视图；禁止相加。跨来源实体去重尚未执行，因为未导入个体设施。

后续采用四层实体：physical_site、process_unit、operator、regulatory_instrument。保留source_record_id、source_version、valid_from/to及证据链接。优先稳定设施ID交叉表；许可ID仅定位文书，可能一证多址/一址多证。名称标准化与距离只能产生待人工审查候选，不能自动合并；无坐标/精度时不能使用距离规则。厂区内填埋、转运、堆肥是不同过程；排口、监测点和运营商办公室不是设施坐标。迁址、关闭、改名保留历史关系。

设施状态分observed_operational_status、permit_status与planned_status；许可证有效不证明投运。许可容量与实际吞吐、干湿基、单位、年份分别登记；气体收集、火炬、发电、装置滑漏和实测量分别登记，缺失为unknown而非0。

## 证据缺口与下一步

联邦固废库年代较旧；GA污水原始入口本工具不可达，二手元数据不作官方版本证明。SA/WA入口拒绝、ACT登记端仅JS外壳，已停止，不绕过认证。TAS小型/分散污水、NT偏远系统、各州豁免/关闭设施及商业设施仍可能不覆盖。没有全国覆盖率分母。BOM服务商统计不分摊给设施，NPI阈值报告不替代GHG清单。

下一步优先核实可下载数据的许可、列定义、坐标CRS/精度和版本；经同意的数据提取仍先做小样本身份对账，保留冲突。没有必要新建GIS、气象API、数据库或智能体：沿用CarbonOS证据登记与版本、HRS时间语义检查及现有空间工具。批量获取被拒资料、外部请求/付费/私人Council数据均另行报告。

机器字段见JSON/CSV及SOURCE_SCHEMA.json；来源核查摘要不等于完整原网页快照。Slides仅展示研究状态，不运行排放模型。
''')
receipts=[{'source_id':r['source_id'],'url':r['canonical_url'],'checked_date':r['checked_date'],'access_status':r['access_status'],'capture_type':'WEB_RESEARCH_SUMMARY_NOT_RAW_BODY','raw_body_sha256':None,'observation':r['coverage_limit']} for r in rows]
write('evidence/source_observations.json',json.dumps(receipts,ensure_ascii=False,indent=2))
write('evidence/access_gaps.json',json.dumps({'no_retry':True,'gaps':[{'url':'https://pid.geoscience.gov.au/dataset/ga/151185','result':'tool inaccessible'},{'url':'https://der.wa.gov.au/','result':'403'},{'url':'https://www.epa.sa.gov.au/public_register','result':'403'},{'url':'https://services.accesscanberra.act.gov.au/s/public-registers/epa-registers?registerid=environment-protection-authorisation-search','result':'JS shell; no facility data'}],'secondary_ga_metadata':'https://researchdata.edu.au/wastewater-treatment-facilities-wms/4065495','secondary_ga_not_admitted_as_primary':True,'qld_cautions':'https://www.qld.gov.au/environment/management/licences-permits/public-register/faq','sa_help':'https://ask.your.epa.sa.gov.au/knowledgebase/article/KA-01117/en-us'},indent=2))

# Reuse the locally verified P1-A layout and navigation; replace page contents only.
old=(B.parent/'p1a/index.html').read_text(encoding='utf-8')
topics=[('范围与门槛','全国来源地图，先明确能知道什么','20个来源入口覆盖联邦与八州领地。设施提取为0；没有全国设施数量或排放估计。科学准入PENDING。',rows[:4]),('联邦基线','不同数据库，承担不同问题','DCCEEW历史固废设施库、BOM服务商报告、NPI阈值说明与GA污水线索不能直接相加。',rows[:4]),('NSW · VIC','许可与空间图层必须关联','许可证、厂址、过程单元、运营商分开建键。旧许可及豁免覆盖尚未验证。',rows[4:7]),('Queensland','同一资料家族，不重复计数','EA门户和开放数据是同源入口；污水厂与监测点KML是不同实体。',rows[7:10]),('WA · SA','访问缺口如实保留','WA指导页面可读，旧入口403；SA官方帮助确认登记入口，但登记页403。没有认证或权限绕过。',rows[10:13]),('Tasmania · NT','监管范围不等于全部设施','TAS Level2与小型/现场污水分属不同范围；NT运输企业不能当固定设施，排口不能当厂址。',rows[13:17]),('ACT','运营、计划与替代设施分开','公共投放点、FOGO试点/规划、MRF重建与污水处理厂需各自状态和时间。',rows[17:]),('精度与去重','未知精度保留未知','坐标精度null、CRS UNKNOWN；不能用小数位估精度。名称/距离只生成待核候选，不自动合并。',[]),('证据成熟度','A/B/C是可用性，不是科学保证','本轮仅目录级B与受限C；没有逐设施核查A级。数据许可未核实，公开可读不代表可批量再发布。',[]),('下一轮协议','先定义问题与数据门槛','只准备极端气候与多气体协议。无数值实验、无计算器、无部署或合并；需独立审查和Founder另行批准实验。',[])]
sections=[]
for i,(label,title,body,items) in enumerate(topics):
 cards=''.join('<article><h3>'+html.escape(r['jurisdiction']+' · '+r['source_id'])+'</h3><p>'+html.escape(r['coverage_limit'])+'</p><p class="quiet">'+html.escape(r['reporting_period'])+' · '+r['evidence_tier']+'</p></article>' for r in items)
 sources=''.join('<li><b>'+r['source_id']+'</b><p>'+html.escape(r['access_status']+' / precision UNKNOWN / licence UNKNOWN')+'</p><a target="_blank" rel="noopener noreferrer" href="'+html.escape(r['canonical_url'])+'">官方来源 ↗</a></li>' for r in items)
 sections.append(f'<section class="page" id="page-{i+1}" {"hidden" if i else ""}><div class="eyebrow">BATCH B / {i+1:02} · {label}</div><h1 tabindex="-1">{title}</h1><p class="lead">{body}</p><div class="cards">{cards}</div><div class="callout">LOCAL_VERIFIED是工件状态。科学准入PENDING；来源覆盖不等于设施覆盖。</div><a href="AU_WASTE_FACILITY_SOURCE_REGISTER.md">来源登记与缺口 →</a> · <a href="EXTREME_CLIMATE_MULTIGAS_RESEARCH_PROTOCOL.md">下一轮协议 →</a><details class="sources"><summary>展开来源与证据状态</summary><ul>{sources or "<li>方法规则见本目录登记表；本页无新增观测。</li>"}</ul></details></section>')
start=old.index('<section class="page"');end=old.index('<div class="progress"',start)
old=old[:start]+''.join(sections)+old[end:]
nav=''.join(f'<button type="button" data-page="{i}"><span>{i+1:02}</span>{x[0]}</button>' for i,x in enumerate(topics))
old=re.sub(r'(<nav aria-label="研究章节">).*?(</nav>)',lambda m:m[1]+nav+m[2],old,flags=re.S)
old=old.replace('P1A-001','BATCH-B').replace('自然环境甲烷研究','澳大利亚官方设施来源调查')
write('index.html',old)
print('Built 20 source rows; 9 jurisdiction levels; 10 slides; 0 facility records')
