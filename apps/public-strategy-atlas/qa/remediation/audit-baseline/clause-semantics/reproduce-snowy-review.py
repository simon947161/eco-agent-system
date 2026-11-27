"""Read-only evidence for manually reviewed bounded Snowy DCP observations.
Does not establish whole-document extraction, current law, rights or admission.
"""
from pathlib import Path
import json,csv,hashlib,datetime,zoneinfo
import pypdf
ROOT=Path('/tmp/csoi-integrity-audit-20261031');APP=ROOT/'readonly-head/apps/public-strategy-atlas';OUT=ROOT/'clause-semantics'
outline=json.loads((APP/'sources/snowy-dcp-outline.json').read_text());pdf=ROOT/'originals/smrc-dcp-snowy-2013-amend3.pdf';body=pdf.read_bytes();reader=pypdf.PdfReader(pdf)
assert 'sha256:'+hashlib.sha256(body).hexdigest()==outline['sourceRevision']
texts={page:' '.join((reader.pages[page-1].extract_text(extraction_mode='layout') or '').split()) for page in {n['anchor']['pdfPage'] for n in outline['nodes']}}
notes={
'document':'版本表确有Amendment3/Issue4及2023采用/开始日期；仅为所取PDF的版本观察。',
'A':'PDFp17说明PartA包括格式、法律框架、申请信息及通知要求，概括成立。',
'A1':'PDFp16确有名称/目的/土地范围/同意机关等导言条目；未宣称现行机关。',
'A1:3':'PDFp16§3写SnowyRiverLEP2013土地；研究摘要保留历史范围和当前地块未知。',
'A1:3:exception':'PDFp16§3确实单列T2TyroleanVillageStage3例外；未扩大地域适用。',
'A1:5':'PDFp17§5确有LEP冲突优先及T2例外；未宣称现行法律结论。',
'A2':'PDFp21章节目录确为申请要求；概要未制造具体申请责任。',
'A2:4':'PDFp25正文§4为信息要求，区分Subdivision及后续其他申请；正文编号与p21目录不一致。',
'A2:4:1':'PDFp25正文§4.1为Subdivision，包含根据规模/影响区分minor/major及清单；摘要是有界概括。',
'A2:4:1:drainage':'WRONG：PDFp27/printed12的drainage/stormwater bullet在§4.2 OtherThanSubdivision之下；现有节点标§4.1并挂Subdivision父节点，条款归属与申请类型错误。',
'C':'PDFp17说明PartC为GeneralControls及相关条文按提案类型考虑；摘要不声称每条对所有开发一律适用。',
'C8':'PDFp151目录列冲突/污染/侵蚀沉积雨水/杂草/生态影响，概要成立。',
'C8:2':'PDFp153确将土地污染分背景、目标、控制；原文旧法律引用未被摘要提升成现行结论。',
'C8:3':'PDFp154确有侵蚀、沉积和雨水共同管理讨论；摘要未宣称已发生环境改善。',
'C8:3:3':'PDFp155§3.3确有C8.3-1及C8.3-2控制；摘要与自写证据问题合理，但不是完整逐项提取。',
'C9':'PDFp158目录区分能源效率、水供给、污水处置；概要成立。',
'C9:2':'PDFp163区分可接管网和其他水供给情境；摘要保持实际可用性未知。',
'C9:2:unreticulated':'PDFp164开头明确条件为不可接reticulatedtownwater；摘要条件准确。',
'C9:2:potable':'PDFp164确将该块印成C6.2-3，含住宿/其他用途、储水、专业支持与降低储水条款；摘要保留原标号异常。',
'C9:2:potable:b':'PARTIAL：数值110及L/person/day/住宿情境正确，但原文是容量至少110；摘要及量化记录缺少minimum/≥操作符，不能当作精确需求或无条件设计值。',
'C9:2:potable:c':'PDFp164C6.2-3(c)确为不含住宿开发90L/person/day容量参考；摘要未称实测或现行义务。',
'C9:2:nonpotable':'PDFp164C9.2-4(a)确为峰值使用/入住40L/person/day及供水途径背景；摘要明确历史参考。',
'C9:3':'PDFp165将on-siteeffluent与拟接Councilsewer系统分开，目标涉及土地/地表水/地下水/健康；摘要准确。',
'C9:3:2':'PDFp166§3.2确有连接及土地适宜性控制；摘要不代表批准或实际运营。',
'C9:3:1':'PDFp166(a)对小/近系统地块用encouraged，不是统一强制；摘要保留鼓励语义。',
'C9:3:1:b':'PDFp166(b)同时条件为不可接管网及拟on-site处置，要求土壤/地形适宜性分析；摘要准确。',
'C9:3:1:b:soil':'土壤适宜性是PDFp166(b)明确命名的证据面向；拆为自写子节点未声称已有样本或结果。',
'C9:3:1:b:topography':'地形是PDFp166(b)另一个明确证据面向；自写子节点未声称已有场地评估。',
'C9:3:3':'PDFp166§3.3表区分HighRisk/MinimalRisk及多种土壤特征；摘要不是完成的风险分类。',
'C9:3:4':'PDFp166§3.4确指向另一Council水供给/污水处置规范；摘要正确保留版本和内容缺口。'
}
rows=[]
for n in outline['nodes']:
 key=n['id'].removeprefix('csoi:dcp:snowy2013:');page=n['anchor']['pdfPage'];digest='sha256:'+hashlib.sha256(texts[page].encode()).hexdigest();assert digest==n['anchor']['normalizedPageDigest'];reason=notes[key];status='WRONG' if reason.startswith('WRONG') else 'PARTIAL' if reason.startswith('PARTIAL') else 'VERIFIED_BOUNDED'
 rows.append({'document':'SnowyRiverDCP2013Amendment3','sourceId':outline['sourceId'],'recordId':n['id'],'pdfPage':page,'recordedSection':n['section'],'recordedLocator':n['locator'],'status':status,'manualSemanticReview':True,'pageHashMatch':True,'reason_zh':reason,'wholeClauseCompleteness':'NOT_ESTABLISHED','currentLaw':'UNKNOWN','officialAdmission':'PENDING'})
# Independent positional witness: drainage bullet is after the other-than-subdivision heading.
p27=texts[27];heading=p27.index('4.2.');bullet=p27.index('drainage and stormwater management plans');assert heading<bullet
p164=texts[164];assert 'at least 110 litres' in p164
quant=[]
for ref in outline['referenceMeasurements']:
 v=ref['value'];assert str(v)+' litres' in p164
 quant.append({'recordId':ref['id'],'value':v,'unit':ref['unit'],'pdfPage':164,'printedPage':149,'numericValueAndUnit':'VERIFIED','structuredSemantics':'PARTIAL_MINIMUM_CAPACITY_OPERATOR_MISSING' if v==110 else 'VERIFIED_BOUNDED_HISTORICAL_REFERENCE','actualDemand':'UNKNOWN','operationalCalculation':'NOT_ADMITTED','reason_zh':'110是原文至少容量而不是精确需求。' if v==110 else '数值与单位可追溯，实际需求/峰值人数/当前设计许可并未提供。'})
result={'auditHead':'744ab46b2bec2ad601da0c4ae528694a4c982154','reviewedAtSydney':datetime.datetime.now(zoneinfo.ZoneInfo('Australia/Sydney')).isoformat(),'method':'Manual semantic reading of all30 authored nodes against all15 cited original pages plus exact-page digest checks; not only keyword matching. Questions authored by repository are not official obligations.','parserVersion':pypdf.__version__,'rawDigest':outline['sourceRevision'],'bytes':len(body),'pages':len(reader.pages),'records':rows,'quantitativeReferences':quant,'drainagePositionalWitness':{'pdfPage':27,'otherThanSubdivisionHeadingOffset':heading,'drainageBulletOffset':bullet,'actualSection':'A2§4.2','recordedSection':'A2§4.1','actualCategory':'OTHER_THAN_SUBDIVISION','recordedParent':'SUBDIVISION'},'counts':{s:sum(r['status']==s for r in rows) for s in ['VERIFIED_BOUNDED','PARTIAL','WRONG','NOT_VERIFIED']},'sourceAnomalies':[{'pages':[21,25],'detail_zh':'A2目录将信息要求编号为5/5.1，而实际正文p25为4/4.1；本审计以实际正文控制编号。'},{'pages':[164],'detail_zh':'C9内potableblock原印C6.2-3，现有观察保留该异常，未静默纠正。'}]}
(OUT/'snowy-semantic-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
with (OUT/'snowy-semantic-review.csv').open('w',newline='',encoding='utf-8-sig') as f:
 writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
print(json.dumps(result['counts']));print('PASS exact raw/page bytes; semantic findings include one wrong attribution and one partial minimum-rate representation, not whole-source acceptance.')
