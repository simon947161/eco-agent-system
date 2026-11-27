"""Author the registered OP's PDF 107–142 finance/revenue-policy research slice.

Original PDF, extracted full text, contact sheets and pixel crops stay in /tmp.
Only short factual cells, authored summaries and provenance are emitted here.
"""
import argparse
import collections
import csv
import hashlib
import json
import re
import unicodedata
from decimal import Decimal
from pathlib import Path
import fitz

HERE=Path(__file__).resolve().parent
PDF=Path('/tmp/csoi-strategy-completion-20261101/op.pdf')
TMP=Path('/tmp/op-finance-completion-20261102')
SOURCE_SHA='4e0b6440768c6bb902628ec36e43757366be470f583169834a4c7c3d4cf54fd2'
SOURCE_ID='csoi:smrc-op-2026:20261030'
PARSER='pymupdf-1.26.6-text-nfkc-whitespace-v1'
RENDERER='pymupdf-1.26.6-rgb-100dpi-fresh-document-clip-v2'
RAW=PDF.read_bytes()
assert hashlib.sha256(RAW).hexdigest()==SOURCE_SHA
assert fitz.VersionBind=='1.26.6'
DOC=fitz.open(stream=RAW,filetype='pdf')
assert len(DOC)==142
units=[];tables=[];diagnostics=[];visuals=[]

def norm(x):return ' '.join(unicodedata.normalize('NFKC',str(x or '')).split())
def digest(x):return 'sha256:'+hashlib.sha256(x if isinstance(x,bytes) else x.encode()).hexdigest()
def slug(x):return re.sub('[^a-z0-9]+','-',str(x).lower()).strip('-')
def bbox_union(boxes):
    r=fitz.Rect(boxes[0])
    for b in boxes[1:]:r|=fitz.Rect(b)
    return [float(z) for z in r]
def expanded(b,pad=.15):
    r=fitz.Rect(b);r.x0=max(0,r.x0-pad);r.y0=max(0,r.y0-pad);r.x1+=pad;r.y1+=pad
    return list(r)
def anchor(page,bbox,field,**extra):
    b=list(bbox);s=norm(DOC[page-1].get_text('text',clip=fitz.Rect(b)))
    return {'field':field,'pdfPage':page,'bbox':b,'normalizedTextDigest':digest(s),'parserVersion':PARSER,**extra}
def pixel_anchor(page,bbox,field,stem):
    with fitz.open(stream=RAW,filetype='pdf') as d:
        pix=d[page-1].get_pixmap(matrix=fitz.Matrix(100/72,100/72),clip=fitz.Rect(bbox),colorspace=fitz.csRGB,alpha=False)
        h=digest(f'RGB|{pix.width}x{pix.height}|'.encode()+pix.samples)
        f=TMP/(stem+'.png');pix.save(f)
    return anchor(page,bbox,field,rasterDigest=h,renderer=RENDERER,width=pix.width,height=pix.height,nativeTextStatus='IMAGE_FACTS_REQUIRE_PIXEL_REVIEW',localOnlyCrop=str(f))
def unit(page,key,category,section,title,summary,bbox,facts=None,conditions=None,qualifiers=None,anchors=None):
    u={'id':f'csoi:op2026:finance:p{page:03d}:{key}','pdfPage':page,'category':category,'section':section,'title':title,'summary':summary,'bbox':list(bbox),'sourceAnchors':anchors or [anchor(page,bbox,'summary')],'facts':facts or {},'conditions':conditions or [],'qualifiers':qualifiers or [],'cspReferences':[],'lspsReferences':[],'existingRecordIds':[]}
    units.append(u);return u
def cell(raw,unit_symbol,period,meaning=None):
    raw=norm(raw)
    out={'display':raw,'unit':unit_symbol,'currency':'UNKNOWN' if '$' in unit_symbol or unit_symbol.startswith('M') else 'NOT_APPLICABLE','period':period,'meaning':meaning,'status':'PRINTED_VALUE','numericValue':None,'numericValueText':None,'signConvention':'AS_PRINTED'}
    if raw=='':out['status']='BLANK_NOT_ZERO';return out
    if raw in ['-','–','—']:out['status']='DASH_NOT_INTERPRETED_AS_ZERO';return out
    if raw.upper() in ['N/A','NA']:out['status']='PRINTED_NOT_APPLICABLE';return out
    t=raw.replace('$','').replace(',','').replace('%','').strip()
    neg=t.startswith('(') and t.endswith(')')
    if neg:t='-'+t[1:-1];out['signConvention']='PARENTHESES_NEGATIVE'
    if re.fullmatch(r'-?\d+(\.\d+)?',t):
        out['numericValueText']=t;out['numericValue']=int(t) if '.' not in t else float(t)
    else:out['status']='NON_NUMERIC_AS_PRINTED'
    return out
def rowbox(row):return bbox_union([b for b in row.cells if b])
def a_cell(page,row,col,field):
    b=row.cells[col]
    assert b is not None,(page,col)
    return anchor(page,expanded(b),field)
def blocks(page):return {b[5]:b for b in DOC[page-1].get_text('blocks') if b[6]==0}
def prose(page,key,blockids,title,summary,facts=None,conditions=None,qualifiers=None,section='Revenue Policy',category='OP_REVENUE_POLICY'):
    bs=blocks(page);box=bbox_union([bs[i][:4] for i in blockids]);aa=[anchor(page,expanded(bs[i][:4]),'summary',sourceBlockIndex=i) for i in blockids]
    return unit(page,key,category,section,title,summary,box,facts,conditions,qualifiers,aa)
def table_meta(page,key,title,headerbox,columns,unit_symbol,period,section,qualifiers=None):
    tid=f'op-finance:p{page:03d}:{key}'
    meta={'id':tid,'pdfPage':page,'title':title,'section':section,'period':period,'unitAsPrinted':unit_symbol,'currency':'UNKNOWN','columns':columns,'headerAnchor':anchor(page,expanded(headerbox),'tableHeader'),'qualifiers':qualifiers or []}
    tables.append(meta);return meta

# Capital schedule continuation: project rows, not activity allocation or lifetime cost.
capital_count=0
for page in range(107,111):
    tab=DOC[page-1].find_tables().tables[0];data=tab.extract();header=tab.rows[1]
    meta=table_meta(page,'capital','Capital Expenditure Schedule 2026-2027',rowbox(header),[norm(c) for c in data[1]],'$','2026/27','Capital expenditure schedule',['Total Project Value 2026/27 按年度表头保留，不解释为项目全生命周期成本。','这是续页；不能据本子集推算整个 OP 资本支出合计。'])
    section='Unlabelled continuation on this page'
    for ri,raw in enumerate(data[2:],2):
        vals=[norm(v) for v in raw]
        if raw[1] is None and raw[3] is None:
            section=vals[0];continue
        if not vals[3]:continue
        row=tab.rows[ri];key=f'capital-r{ri:02d}';facts={'tableId':meta['id'],'tableSectionAsPrinted':section,'assetGroup':vals[0],'portfolio':vals[1],'carryOver2025_26':vals[2],'projectDescription':vals[3],'budgetStatus':'PLANNED_CAPITAL_SCHEDULE_NOT_ACTUAL','columnValues':[]}
        aa=[a_cell(page,row,c,f'facts.{f}') for c,f in enumerate(['assetGroup','portfolio','carryOver2025_26','projectDescription'])]
        for ci,label in enumerate(['Total Project Value 2026/27','Restricted Funds','Grants','General Fund'],4):
            facts['columnValues'].append({'column':label,**cell(vals[ci],'$','2026/27',label)})
            aa.append(a_cell(page,row,ci,f'facts.columnValues[{ci-4}]'))
        aa.append(meta['headerAnchor'])
        cond=['Carry overs 将在 September quarterly budget review 考虑并更新该表；本表不证明结转已确认。']
        qq=['预算来源列不构成对具体 OP 活动的财务分配证据。']
        if 'TBD' in vals[3]:qq.append('项目名称中 TBD 原样保留，具体安排未确定。')
        if vals[4]=='':qq.append('年度项目值原格为空；三项资金来源虽列 0，也不能将总值补为 0。')
        if vals[0]=='Wastewater' and vals[3].startswith(('Water Mains','Water Treatment')):qq.append('原件 Asset Group 为 Wastewater，但项目名称写 Water；保留源内分类/名称张力，不自行改分类。')
        unit(page,key,'OP_CAPITAL_BUDGET_ROW','Capital expenditure schedule',vals[3],f'年度资本表列出“{vals[3]}”，资产组为 {vals[0]}，项目值原格为 {vals[4] or "空白"}；资金来源与结转状态分列保留。',rowbox(row),facts,cond,qq,aa)
        capital_count+=1
assert capital_count==41
prose(107,'capital-carryover-rule',[3] if False else [b[5] for b in DOC[106].get_text('blocks') if b[6]==0 and 'Carry overs will' in b[4]],'结转预算尚需季度审议','源表说明结转将在九月季度预算审议中考虑，再更新资本表。',{'reviewMonthAsPrinted':'September','approvalState':'NOT_CONFIRMED_BY_THIS_STATEMENT'},['不能将 Yes、No、NA 或空白解释为已实际执行。'],section='Capital expenditure schedule',category='OP_BUDGET_CONDITION')
foot=next(b for b in DOC[110].get_text('blocks') if b[6]==0 and 'Indicates delivery' in b[4])
unit(111,'capital-footnote','OP_DOCUMENT_CONTEXT','Capital expenditure schedule','照片页的不可见文字层','可见原页为设施现场照片。抽取文字层残留星号与 Corporate Projects team 的说明，但原件像素中被照片覆盖；不能当作本页可见脚注或项目完成证据。',list(foot[:4]),{'textLayerObservation':{'marker':'*','namedTeam':'Corporate Projects team'},'textVisibility':'HIDDEN_OR_OCCLUDED_TEXT_LAYER','photoDisposition':'DECORATIVE_OR_CONTEXT_PHOTO_NOT_PROGRESS_EVIDENCE'},qualifiers=['文字层观察与可见原页分开记录；本页没有可见资本金额行。'],anchors=[anchor(111,list(foot[:4]),'facts.textLayerObservation'),pixel_anchor(111,list(DOC[110].rect),'facts.photoDisposition','photo-111')])

# Service tables sometimes share detected grid bounds; each repeated header starts
# a distinct service table. Merged empty rows are layout, not financial zero rows.
service_names={112:['Built and Natural Environment','Communications and Engagement','Community Services'],113:['Corporate Projects','Customer Service','Executive Office ( including Councillors)','Finance'],114:['Governance','Information and Communications Technology','Open Space and Recreation'],115:['People and Organisational Performance','Procurement','Resource and Waste'],116:['Revenue','Strategy Development','Tourism'],117:['Water and Wastewater','Infrastructure','Fleet and Plant']}
service_count=0;service_row_count=0
for page,names in service_names.items():
    collected=[]
    for tab in DOC[page-1].find_tables().tables:
        for ri,raw in enumerate(tab.extract()):
            vals=[norm(v) for v in raw]
            if len(vals)==3:collected.append((tab.rows[ri],vals))
    collected.sort(key=lambda x:rowbox(x[0])[1])
    name_index=-1;phase=None;current=[];meta=None
    for row,vals in collected:
        if vals[1]=='Resource Group':
            name_index+=1;assert name_index<len(names),(page,name_index);name=names[name_index];phase=None;current=[]
            meta=table_meta(page,'service-'+slug(name),name,rowbox(row),['Resource section','Resource Group',vals[2]],"$'000",'2026/27','Service budgets',['原表列明 Draft Budget / proposed，未转为实际收入支出。','禁止直接把各服务表与基金报表相加或当成同一会计口径。'])
            service_count+=1;continue
        if not meta or not vals[2]:continue
        if vals[0] in ['Income','Expenditure']:phase=vals[0]
        role=vals[0] if vals[0] in ['Income Total','Expenditure Total','Grand Total'] else phase+' component'
        # The vertically merged Expenditure label can occur below its first row.
        # The preceding Income Total is the independent boundary in all 19 tables.
        if vals[0]=='Income Total':phase='Expenditure'
        label=vals[1] or vals[0]
        value=cell(vals[2],"$'000",'2026/27',role)
        facts={'tableId':meta['id'],'service':name,'resourceGroup':label,'rowRole':role,'budgetStatus':'DRAFT_BUDGET_AS_PRINTED_NOT_ACTUAL','columnValues':[{'column':'2026/27 Draft Budget',**value}]}
        aa=[a_cell(page,row,2,'facts.columnValues[0]'),meta['headerAnchor']]
        label_col=1 if vals[1] else 0
        if row.cells[label_col]:aa.append(a_cell(page,row,label_col,'facts.resourceGroup'))
        qq=[]
        if label=='Materials & Contracts (including recharges)':qq.append('含 recharges 的支出格以括号列示负值；不能改成正费用。')
        if 'caital' in label:qq.append('原表 caital 拼写保留，未据此改变该行分类。')
        u=unit(page,'service-'+slug(name)+f'-r{len(current)+1:02d}','OP_SERVICE_BUDGET_ROW','Service budgets',name+' — '+label,f'{name} 的{role}原值为 {vals[2]}，单位为千元格式 {"$\'000"}；这是拟议年度预算。',rowbox(row),facts,qualifiers=qq,anchors=aa)
        current.append(u);service_row_count+=1
        if role=='Grand Total':
            byrole={x['facts']['rowRole']:x for x in current if x['facts']['rowRole'] in ['Income Total','Expenditure Total','Grand Total']}
            for component,total in [('Income component','Income Total'),('Expenditure component','Expenditure Total')]:
                rows=[x for x in current if x['facts']['rowRole']==component]
                if rows and total in byrole:
                    calculated=sum(Decimal(x['facts']['columnValues'][0]['numericValueText']) for x in rows)
                    printed=Decimal(byrole[total]['facts']['columnValues'][0]['numericValueText'])
                    if calculated!=printed:diagnostics.append({'type':'DISPLAYED_TABLE_RECONCILIATION_DIFFERENCE','tableId':meta['id'],'pdfPage':page,'check':total+' vs displayed components','calculatedFromDisplayedCells':str(calculated),'sourceDeclared':str(printed),'difference':str(printed-calculated),'unit':"$'000",'interpretation':'可能与显示精度/四舍五入等有关，但原件未说明；不能认定原因，也不改写原值。','sourceUnitIds':[x['id'] for x in rows]+[byrole[total]['id']]})
            if all(k in byrole for k in ['Income Total','Expenditure Total','Grand Total']):
                calc=Decimal(byrole['Income Total']['facts']['columnValues'][0]['numericValueText'])-Decimal(byrole['Expenditure Total']['facts']['columnValues'][0]['numericValueText']);printed=Decimal(byrole['Grand Total']['facts']['columnValues'][0]['numericValueText'])
                if calc!=printed:diagnostics.append({'type':'DISPLAYED_TABLE_RECONCILIATION_DIFFERENCE','tableId':meta['id'],'pdfPage':page,'check':'Grand Total vs displayed income less expenditure','calculatedFromDisplayedCells':str(calc),'sourceDeclared':str(printed),'difference':str(printed-calc),'unit':"$'000",'interpretation':'只报告显示数差异；可能原因未经来源确认，不自动纠正。','sourceUnitIds':[byrole[k]['id'] for k in ['Income Total','Expenditure Total','Grand Total']]})
    assert name_index+1==len(names),(page,name_index)
assert service_count==19

# Fund statements: every printed numeric/dash/blank cell has its own row/column
# anchor. Consolidated is a total scope, never a sixth independently added fund.
fund_rows={}
for page in [120,121]:
    tab=DOC[page-1].find_tables().tables[0];data=tab.extract();title='Income Statement by Fund' if page==120 else 'Cash Flow Summary'
    hi=1 if page==120 else 0
    meta=table_meta(page,'fund-statement',title,rowbox(tab.rows[hi]),['Description','Consolidated','General','Water','Sewer','Waste'],'$000','2026-27 / columns 2027',title,['Consolidated 是汇总列，不与四个基金相加。','破折号与空白分别保留；不自动解释为零。'])
    phase='Income from continuing operations' if page==120 else 'Cash Flows from Operating Activities';fund_rows[page]={}
    for ri,raw in enumerate(data[hi+1:],hi+1):
        vals=[norm(v) for v in raw]
        label=vals[1] if len(vals)>1 else ''
        if not label:continue
        if label in ['Expenses from Continuing Operations','Cash Flows from Operating Activities','Cash Flows from Investing Activities','Cash Flow from Financing Activities']:
            phase=label;continue
        section=phase
        role='SOURCE_LINE_ITEM'
        if label.startswith('Total '):role='SOURCE_DECLARED_TOTAL'
        if page==120 and label.startswith(('Operating Result','Net Operating Result')):
            section='Operating results';role='SOURCE_RESULT'
        if page==121:
            if label.startswith('Net Cash Provided'):role='SOURCE_FLOW_SUBTOTAL'
            if label.startswith('Net Increase'):
                section='Net movement in cash assets';role='SOURCE_CASH_MOVEMENT'
            elif label.startswith('Cash and Cash Equivalents'):
                section='Cash balances';role='SOURCE_BALANCE'
            elif label.startswith('Plus Investments on Hand'):
                section='Investments on hand';role='SOURCE_INVESTMENT_BALANCE'
            elif label.startswith('Total Cash, Cash Equivalents and Investments'):
                section='Cash and investment balances';role='SOURCE_DECLARED_TOTAL'
            elif label.startswith('Forecast'):
                section='Forecast unrestricted funds';role='SOURCE_FORECAST'
        row=tab.rows[ri];facts={'tableId':meta['id'],'rowLabel':label,'statementSection':section,'rowRole':role,'budgetStatus':'PROJECTED_BASE_SCENARIO_NOT_ACTUAL' if page==120 else 'PROJECTED_CASH_FLOW_NOT_ACTUAL','columnValues':[]};aa=[a_cell(page,row,1,'facts.rowLabel'),meta['headerAnchor']]
        for ci,fund in enumerate(['Consolidated','General','Water','Sewer','Waste'],2):
            facts['columnValues'].append({'column':fund,**cell(vals[ci],'$000','2027',label)})
            aa.append(a_cell(page,row,ci,f'facts.columnValues[{ci-2}]'))
        u=unit(page,f'fund-r{ri:02d}','OP_FUND_FINANCIAL_ROW',title,label,f'{title} 的“{label}”按合并、General、Water、Sewer、Waste 五列保存；单位 $000，原表数值及空白/破折号不相互替换。',rowbox(row),facts,anchors=aa)
        fund_rows[page][label]=u

cash=fund_rows[121]
opening=cash['Cash and Cash Equivalents at Beginning of Reporting Period'];closing=cash['Cash and Cash Equivalents at End of Reporting Period'];movement=cash['Net Increase/(Decrease) in Cash Assets Held']
for ci,fund in enumerate(['Consolidated','General','Water','Sewer','Waste']):
    a=Decimal(opening['facts']['columnValues'][ci]['numericValueText']);b=Decimal(closing['facts']['columnValues'][ci]['numericValueText']);printed=Decimal(movement['facts']['columnValues'][ci]['numericValueText'])
    if b-a!=printed:
        diagnostic={'type':'SOURCE_ARITHMETIC_CONFLICT','tableId':movement['facts']['tableId'],'pdfPage':121,'fund':fund,'check':'Printed net increase vs closing minus opening cash','sourceDeclared':str(printed),'calculatedFromDisplayedCells':str(b-a),'difference':str(printed-(b-a)),'unit':'$000','interpretation':'原件基金净变动行与本页期初/期末不一致；保留印刷数字，不能自动替换为计算值，也不声称只是四舍五入。','sourceUnitIds':[opening['id'],closing['id'],movement['id']]};diagnostics.append(diagnostic)
        movement['qualifiers'].append(f'{fund} 的印刷净变动 {printed} 与期末减期初 {b-a} 不一致（单位 $000）；详见独立冲突记录。')

# Definitions are factual vocabulary, not proof of relationships or applicability.
acronym_count=0
for page in [122,123]:
    tab=DOC[page-1].find_tables().tables[0]
    for ri,raw in enumerate(tab.extract()[1:],1):
        vals=[norm(v) for v in raw];row=tab.rows[ri]
        if not vals[0]:continue
        qq=[]
        if vals[0] in ['GST','SoR']:qq.append('原件拼写按印刷保留；未悄然替换为外部标准写法。')
        unit(page,f'acronym-r{ri:02d}','OP_GLOSSARY','Acronyms and abbreviations',vals[0],f'本文件将 {vals[0]} 展开为 {vals[1]}。',rowbox(row),{'abbreviation':vals[0],'definitionAsPrinted':vals[1],'relationStatus':'VOCABULARY_ONLY'},qualifiers=qq,anchors=[a_cell(page,row,0,'facts.abbreviation'),a_cell(page,row,1,'facts.definitionAsPrinted')]);acronym_count+=1

# Authored policy prose, version records, charge tables and figure observations.
exec((HERE/'policy_authoring.py').read_text(),globals())

page_units=collections.defaultdict(list)
for u in units:page_units[u['pdfPage']].append(u['id'])
dispositions={111:'PHOTO_VISUALLY_REVIEWED_TEXT_LAYER_FOOTNOTE_HIDDEN_OR_OCCLUDED_NO_VISIBLE_BUDGET_ROWS',118:'TWO_RASTER_CHARTS_VISUALLY_READ',119:'TWO_RASTER_CHARTS_VISUALLY_READ',124:'APPENDIX_INTRODUCTION_READ',125:'REVENUE_POLICY_COVER_REVIEWED',126:'ACKNOWLEDGEMENT_AND_DECORATIVE_PHOTO_REVIEWED',127:'VERSION_TABLE_AND_DRAFT_ADOPTION_TENSION_REVIEWED',128:'CONTENTS_REVIEWED_NAVIGATION_NOT_NEW_POLICY',132:'FOUR_RATING_MAP_PANELS_VISUALLY_READ_NO_PARCEL_ADMISSION',142:'ENDPAGE_PUBLIC_DOCUMENTS_FEEDBACK_CONTACTS_REVIEWED'}
pages=[]
for page in range(107,143):
    p=DOC[page-1]
    pages.append({'pdfPage':page,'printedPage':None if page==111 else (page if page<=124 else (page-127 if 129<=page<=141 else None)),'disposition':dispositions.get(page,'ALL_VISIBLE_FINANCE_OR_POLICY_UNITS_AUTHORED'),'unitIds':page_units[page],'nativePageTextDigest':digest(norm(p.get_text('text'))),'parserVersion':PARSER,'coverage':'COMPLETE_FOR_ASSIGNED_PAGE_VISIBLE_RESEARCH_SCOPE_NOT_OFFICIAL_ADMISSION','remainingLimits':['Currentness UNKNOWN','Current legal applicability UNKNOWN','Actual execution UNKNOWN','Private ledger/assessment/parcel data not accessed']})
assert len(pages)==36 and all(page['unitIds'] for page in pages)
assert len({u['id'] for u in units})==len(units)
counts=dict(collections.Counter(u['category'] for u in units))
result={'format':'csoi-op-completion-author-part-1','sourceId':SOURCE_ID,'sourceRevision':'sha256:'+SOURCE_SHA,'part':'finance-revenue-policy-pdf107-142','sourcePageCount':142,'sourceBytes':len(RAW),'assignedPdfPages':[107,142],'sourceVersionBoundaries':{'filenameVersion':'v3.1','mainDocumentInternalVersion':'1.3 as separately reviewed in main OP','revenuePolicyAppendixVersion':'1.2 adopted 30/06/2026 / resolution 225/26 on PDF127','workingDraftWordingStillPresent':True,'currentness':'UNKNOWN'},'sourceDenominators':{'assignedPages':36,'capitalProjectRowsInAssignedContinuation':capital_count,'serviceBudgetTables':service_count,'serviceBudgetRows':service_row_count,'fundStatementRows':sum(len(x) for x in fund_rows.values()),'acronymRows':acronym_count,'authoredUnits':len(units),'categories':counts,'tables':len(tables),'visualOccurrences':len(visuals)},'interpretationLimits':['This registered 2026–27 file only; no expansion into other years/projects.','Amounts are plans/estimates/charges as printed, not actual delivery or paid amounts.','Currency code not inferred from dollar sign or location.','No automatic activity-budget allocation or sum across incomparable tables.','All legal provisions are source-attributed policy statements, not independent current legal advice/admission.','Original PDF/full text/crops remain /tmp; output contains authored summaries and short factual cells.'],'pages':pages,'tables':tables,'visuals':visuals,'units':units,'diagnostics':diagnostics}
HERE.mkdir(exist_ok=True,parents=True)
(HERE/'finance-author.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
(HERE/'finance-diagnostics.json').write_text(json.dumps({'sourceRevision':result['sourceRevision'],'diagnostics':diagnostics},ensure_ascii=False,indent=2)+'\n')
with (HERE/'page-coverage.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['pdfPage','printedPage','disposition','unitCount','categories','extracted','implemented','verified','gap'])
    for page in pages:
        rows=[u for u in units if u['pdfPage']==page['pdfPage']]
        w.writerow([page['pdfPage'],page['printedPage'],page['disposition'],len(rows),'|'.join(sorted({u['category'] for u in rows})),'AUTHORED','PENDING_ROOT_INTEGRATION','AUTHOR_ORIGINAL_CHECK_AND_INDEPENDENT_SEMANTIC_READBACK','CURRENTNESS_AND_LEGAL_APPLICABILITY_UNKNOWN; EXTERNAL_FEE_SCHEDULE_NOT_RETRIEVED'])
with (HERE/'unit-coverage.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['id','pdfPage','category','title','sourceAnchorCount','extracted','implemented','verified','gap'])
    for u in units:w.writerow([u['id'],u['pdfPage'],u['category'],u['title'],len(u['sourceAnchors']),'AUTHORED','PENDING_ROOT_INTEGRATION','ORIGINAL_SOURCE_ANCHORS_AND_INDEPENDENT_SEMANTIC_READBACK','CURRENTNESS_UNKNOWN; ACTUAL_EXECUTION_UNKNOWN'])
print(json.dumps(result['sourceDenominators'],ensure_ascii=False))
