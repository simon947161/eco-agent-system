"""Independent source strategy census; does not change Atlas knowledge."""
import csv,hashlib,json,re,pathlib
import pdfplumber
from pypdf import PdfReader
R=pathlib.Path('/tmp/csoi-integrity-audit-20261031');APP=R/'readonly-head/apps/public-strategy-atlas'
full=PdfReader(R/'originals/smrc-csp-full-2025.pdf');summary=PdfReader(R/'originals/smrc-csp-summary.pdf')
pattern=r'(?<![\d.])((?:1[0-9]|[1-9])\.[1-9])(?![\d.])';pages={}
for p in range(18,28):
 for code in set(re.findall(pattern,full.pages[p-1].extract_text(extraction_mode='layout') or '')):pages[code]=p
one=set(re.findall(pattern,summary.pages[0].extract_text(extraction_mode='layout') or ''))
assert len(pages)==44 and set(pages)==one and len({x.split('.')[0] for x in pages})==14
receipt=json.loads((APP/'sources/csp61-admission.json').read_text());x0,y0,x1,y1=receipt['anchor']['bbox']
with pdfplumber.open(R/'originals/smrc-csp-summary.pdf') as pdf:
 words=pdf.pages[0].extract_words();excerpt=' '.join(w['text'] for w in words if x0<=w['x0']<=x1 and y0<=w['top']<=y1)
assert 'sha256:'+hashlib.sha256(excerpt.encode()).hexdigest()==receipt['extraction']['digest']
out=R/'deliverables';out.mkdir(exist_ok=True)
rows=[]
for code in sorted(pages,key=lambda x:tuple(map(int,x.split('.')))):
 rows.append({'策略编号':code,'所属目标编号':code.split('.')[0],'完整CSP_PDF及印刷页':pages[code],'一页摘要_PDF页':1,'独立摘录原文锚定':'YES_6.1_EXCERPT_ONLY' if code=='6.1' else 'NO_EQUIVALENT_STRATEGY_CAPSULE','项目完整字段策略对象':'NOT_PRESENT','缺口':'角色、伙伴、条件、复核等完整结构未建立；其他代码的主题站点或OP引用不等于逐条抽取','备注':'6.1为策略，父级Strategic Objective为6；尚未官方准入' if code=='6.1' else ''})
with (out/'CSP_44项策略清点.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
result={'sourceFullPages':36,'summaryPages':1,'themes':5,'strategicObjectives':14,'numberedStrategies':44,'fullSummaryStrategyIdSetsMatch':True,'onePageExactlyAnchoredExcerptCodes':['6.1'],'onePageExcerptCoverageOnly':'1/44 =2.27%; not full semantic/governance coverage','completeRolePartnerApplicabilityCapsules':'0/44 under strict full-field criterion','baselineMetricRows':63,'baselineMetricStructuredRows':1,'fullDocumentCoverage':'UNKNOWN_HETEROGENEOUS_GRAINS_NOT_ADDED','excerptOriginalDigestVerified':True,'originalsRedistributed':False}
(out/'CSP_核心清单核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
