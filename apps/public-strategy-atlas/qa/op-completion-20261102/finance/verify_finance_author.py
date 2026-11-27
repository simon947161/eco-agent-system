"""Re-read original PDF cells and anchors; do not import or run the author builder.

Semantic guards below are bounded checks against the actual source and reviewed
pixels. This is not a claim that a hash proves the meaning of every sentence.
"""
import copy
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
import fitz

HERE=Path(__file__).resolve().parent
PDF=Path('/tmp/csoi-strategy-completion-20261101/op.pdf')
SHA='4e0b6440768c6bb902628ec36e43757366be470f583169834a4c7c3d4cf54fd2'
PARSER='pymupdf-1.26.6-text-nfkc-whitespace-v1'
RENDERER='pymupdf-1.26.6-rgb-100dpi-fresh-document-clip-v2'
RAW=PDF.read_bytes()
assert hashlib.sha256(RAW).hexdigest()==SHA
assert fitz.VersionBind=='1.26.6'
DOC=fitz.open(stream=RAW,filetype='pdf')
assert len(DOC)==142
DATA=json.loads((HERE/'finance-author.json').read_text())
def norm(s):return ' '.join(unicodedata.normalize('NFKC',s).split())
def sha(s):return 'sha256:'+hashlib.sha256(s if isinstance(s,bytes) else s.encode()).hexdigest()
def native(page,box):return norm(DOC[page-1].get_text(clip=fitz.Rect(box)))
def uid(page,key):return f'csoi:op2026:finance:p{page:03d}:{key}'
def must(ok,message):
    if not ok:raise AssertionError(message)
def get_path(obj,path):
    for p in re.findall(r'[^.\[\]]+',path):obj=obj[int(p)] if isinstance(obj,list) else obj[p]
    return obj
def source_for(u):return ' '.join(native(a['pdfPage'],a['bbox']) for a in u['sourceAnchors'])
def byid(data):return {u['id']:u for u in data['units']}
def num(x):
    s=x.replace('$','').replace(',','').replace('%','').strip()
    if s.startswith('(') and s.endswith(')'):s='-'+s[1:-1]
    return Decimal(s)

def verify_cells(data):
    n=0;anchored=0
    for u in data['units']:
        for a in u['sourceAnchors']:
            if not re.fullmatch(r'facts\.columnValues\[\d+\]|facts\.maximumRebate',a['field']):continue
            value=get_path(u,a['field']);s=native(a['pdfPage'],a['bbox']);n+=1
            must(s==value['display'],f"source cell differs: {u['id']} {a['field']}")
            if s=='':status='BLANK_NOT_ZERO'
            elif s in ['-','–','—']:status='DASH_NOT_INTERPRETED_AS_ZERO'
            elif s.upper()=='N/A':status='PRINTED_NOT_APPLICABLE'
            else:status='PRINTED_VALUE'
            must(value['status']==status,f"cell status differs: {u['id']}")
            if status=='PRINTED_VALUE':
                must(num(s)==Decimal(str(value['numericValue'])),f"numeric value differs: {u['id']}")
                must(num(s)==Decimal(value['numericValueText']),f"numeric text differs: {u['id']}")
                must(value['signConvention']==('PARENTHESES_NEGATIVE' if s.startswith('(') else 'AS_PRINTED'),f"sign differs: {u['id']}")
            else:must(value['numericValue'] is None and value['numericValueText'] is None,f"blank/dash/NA manufactured value: {u['id']}")
            must(value['currency']=='UNKNOWN' if '$' in value['unit'] else value['currency']=='NOT_APPLICABLE',f"unprinted currency: {u['id']}")
            cat=u['category'];i=int(re.search(r'\[(\d+)\]',a['field']).group(1)) if '[' in a['field'] else None
            if cat=='OP_CAPITAL_BUDGET_ROW':
                expected=['Total Project Value 2026/27','Restricted Funds','Grants','General Fund']
                must(value['column']==expected[i] and value['unit']=='$' and value['period']=='2026/27','capital column/year/unit')
            elif cat=='OP_SERVICE_BUDGET_ROW':
                must(value['unit']=="$'000" and value['period']=='2026/27' and value['column']=='2026/27 Draft Budget','service unit/year/column')
            elif cat=='OP_FUND_FINANCIAL_ROW':
                must(value['column']==['Consolidated','General','Water','Sewer','Waste'][i] and value['unit']=='$000' and value['period']=='2027','fund column/year/unit')
            elif cat=='OP_REVENUE_CHARGE_ROW':
                must(value['column']==['2027','2026'][i] and value['unit']=='$' and value['period']==['2027','2026'][i],'charge year/unit')
            elif cat=='OP_REVENUE_RATE_ROW':
                must(value['column']==['Base','Ad Valorem','Yield','% of yield','% from base rate'][i] and value['unit']==['$','rate in dollar','$','%','%'][i] and value['period']=='2026/2027','rate column/year/unit')
            elif cat=='OP_REVENUE_REBATE':
                must(value['unit']=='$' and value['period']=='Per annum','rebate unit/period')
        # Every emitted column-value object needs its own direct source cell.
        for i,v in enumerate(u['facts'].get('columnValues',[])):
            must(any(a['field']==f'facts.columnValues[{i}]' for a in u['sourceAnchors']),f"missing numeric anchor: {u['id']}");anchored+=1
    must(n==543 and anchored==540,'full numeric-cell coverage changed')
    return n

def verify_roles(data):
    groups=defaultdict(list);count=0
    for u in data['units']:
        if u['category']=='OP_SERVICE_BUDGET_ROW':groups[u['facts']['tableId']].append(u)
    must(len(groups)==19,'service table missing')
    for key,rows in groups.items():
        rows.sort(key=lambda u:u['bbox'][1]);page=rows[0]['pdfPage'];r=fitz.Rect(rows[0]['bbox'])
        for u in rows:r|=fitz.Rect(u['bbox'])
        # Read total labels and y positions independently from original word layout.
        lines=DOC[page-1].get_text('dict',clip=r)['blocks']
        income_y=None;printed_totals={}
        for b in lines:
            for line in b.get('lines',[]):
                text=norm(''.join(s['text'] for s in line['spans']))
                if text in ['Income Total','Expenditure Total','Grand Total']:
                    y=(line['bbox'][1]+line['bbox'][3])/2;printed_totals[text]=y
                    if text=='Income Total':income_y=y
        for u in rows:
            y=(u['bbox'][1]+u['bbox'][3])/2
            matches=[name for name,ty in printed_totals.items() if u['bbox'][1]<=ty<=u['bbox'][3]]
            expected=matches[0] if matches else ('Income component' if income_y is not None and y<income_y else 'Expenditure component')
            must(u['facts']['rowRole']==expected,f"service role crosses original total boundary: {u['id']}")
            must(u['facts']['columnValues'][0]['meaning']==expected and expected in u['summary'],f"service meaning/summary stale: {u['id']}")
            count+=1
    must(count==155,'service row missing')
    us=byid(data)
    expectations={(120,'fund-r08'):('SOURCE_LINE_ITEM','Income from continuing operations'),(120,'fund-r19'):('SOURCE_RESULT','Operating results'),(120,'fund-r21'):('SOURCE_RESULT','Operating results'),(121,'fund-r15'):('SOURCE_CASH_MOVEMENT','Net movement in cash assets'),(121,'fund-r17'):('SOURCE_BALANCE','Cash balances'),(121,'fund-r19'):('SOURCE_BALANCE','Cash balances'),(121,'fund-r20'):('SOURCE_INVESTMENT_BALANCE','Investments on hand'),(121,'fund-r22'):('SOURCE_DECLARED_TOTAL','Cash and investment balances'),(121,'fund-r23'):('SOURCE_FORECAST','Forecast unrestricted funds')}
    for (p,key),(role,section) in expectations.items():
        u=us[uid(p,key)];must(u['facts']['rowRole']==role and u['facts']['statementSection']==section,'fund role/section meaning changed')
        must(u['facts']['rowLabel'] in source_for(u),'fund source label missing')
    return count

def verify_semantics(data):
    us=byid(data)
    photo=us[uid(111,'capital-footnote')]
    must(photo['facts']['textVisibility']=='HIDDEN_OR_OCCLUDED_TEXT_LAYER' and photo['category']=='OP_DOCUMENT_CONTEXT','hidden text promoted to visible footnote')
    must('HIDDEN_OR_OCCLUDED' in next(p['disposition'] for p in data['pages'] if p['pdfPage']==111),'photo disposition changed')
    fuel=us[uid(129,'fuel-surcharge')]
    must('This surcharge is not currently applied' in source_for(fuel) and fuel['facts']['chargeCurrentlyAppliedAsPrinted'] is False,'fuel surcharge falsely active')
    oldarea=us[uid(134,'clause-1-2-5')]
    must('will not apply' in source_for(oldarea) and 'former Snowy River' in source_for(oldarea) and 'Council resolution' in source_for(oldarea),'original old-area exception not anchored')
    must('Snowy River' in oldarea['facts']['exceptionRegion'] and any('resolution' in x for x in oldarea['conditions']),'old-area resolution condition omitted')
    sr=us[uid(129,'srv')]
    must(sr['facts']['fourYearSRVPercent']==52.48 and sr['facts']['ratePegRelationship']=='INCLUDED_NOT_ADDITIONAL','SRV rate peg double counted')
    pension=us[uid(140,'pensioner-rebate-1')]
    must('Ordinary rates' in source_for(pension) and '250' in source_for(pension),'pension rebate original missing')
    must(pension['facts']['combinedScope'] is True and pension['facts']['maximumRebate']['numericValue']==250,'pensioner combined maximum changed')
    borrow=us[uid(140,'restricted-fund-borrowing')]
    must('approved by the minister before money can be used' in source_for(borrow) and any('先于资金使用' in c for c in borrow['conditions']),'restricted fund prior approval omitted')
    exclusions=us[uid(139,'ossm-exclusions')]['facts']['excludedCharges']
    must(len(exclusions)==5 and any('Transfer' in x for x in exclusions) and any('Re-inspection' in x for x in exclusions),'OSSM annual fee made all-inclusive')
    other=us[uid(119,'chart-expenditure-funds')]['facts']['series'][2]
    must(other['role']=='COMPOSITE_PARENT' and other['amountMillion']==26.94,'Other figure incorrectly additive fifth fund')
    for page,key,amounts in [(118,'income-types',[.68,1.13,1.32,2.16,4.79,20.55,24.09,51.37]),(118,'income-funds',[65.95,13.15,14.69,12.30]),(119,'expenditure-types',[30.35,2.19,33.69,41.84]),(119,'expenditure-funds',[65.51,15.62,26.94,14.46,12.48])]:
        must([v['amountMillion'] for v in us[uid(page,'chart-'+key)]['facts']['series']]==amounts,'manually reviewed original pixel labels changed')
    # Source's unreconciled fund values must survive; we neither fix nor suppress them.
    cash=us[uid(121,'fund-r15')]['facts']['columnValues']
    must([x['numericValue'] for x in cash]==[-424,585,616,616,616],'source-conflicted cash row silently repaired')
    conflicts=[d for d in data['diagnostics'] if d['type']=='SOURCE_ARITHMETIC_CONFLICT']
    must({d['fund'] for d in conflicts}=={'General','Water','Sewer','Waste'},'cash conflict omitted')
    required={'SOURCE_SERVICE_FREQUENCY_AND_GEOGRAPHY_CONFLICT','SOURCE_GEOGRAPHIC_SCOPE_DIFFERENCE','SOURCE_FREQUENCY_ROW_AMBIGUITY','SOURCE_VERSION_STATUS_TENSION','SOURCE_LEGISLATION_YEAR_TYPO_OR_CONFLICT'}
    must(required.issubset({d['type'] for d in data['diagnostics']}),'source policy conflict omitted')
    must(len([d for d in data['diagnostics'] if d['type']=='DISPLAYED_TABLE_RECONCILIATION_DIFFERENCE'])==8,'service diagnostics stale after role correction')
    must(data['sourceVersionBoundaries']['currentness']=='UNKNOWN','currentness invented')

anchor_count=0;pixel_count=0
for u in DATA['units']:
    for a in u['sourceAnchors']:
        must(a['parserVersion']==PARSER and sha(native(a['pdfPage'],a['bbox']))==a['normalizedTextDigest'],f"original text anchor differs: {u['id']}");anchor_count+=1
        if 'rasterDigest' in a:
            must(a['renderer']==RENDERER,'only fresh-document v2 renderer is allowed')
            with fitz.open(stream=RAW,filetype='pdf') as fresh:
                pix=fresh[a['pdfPage']-1].get_pixmap(matrix=fitz.Matrix(100/72,100/72),clip=fitz.Rect(a['bbox']),colorspace=fitz.csRGB,alpha=False)
                must(sha(f'RGB|{pix.width}x{pix.height}|'.encode()+pix.samples)==a['rasterDigest'],'original raster mismatch')
            pixel_count+=1
for page in DATA['pages']:
    must(page['nativePageTextDigest']==sha(native(page['pdfPage'],DOC[page['pdfPage']-1].rect)),'page text hash differs')
must({p['pdfPage'] for p in DATA['pages']}==set(range(107,143)),'assigned page omitted')
must(len(byid(DATA))==428 and sum(len(p['unitIds']) for p in DATA['pages'])==428,'unit coverage')
for p in DATA['pages']:
    must(set(p['unitIds'])=={u['id'] for u in DATA['units'] if u['pdfPage']==p['pdfPage']},'page-unit mismatch')
numeric=verify_cells(DATA);roles=verify_roles(DATA);verify_semantics(DATA)

negative_results=[]
def negative(name,mutate,check):
    bad=copy.deepcopy(DATA);mutate(bad)
    try:check(bad)
    except (AssertionError,KeyError) as e:negative_results.append({'case':name,'outcome':'REJECTED','reason':str(e)});return
    raise AssertionError('negative accepted: '+name)
def modify(data,p,key,path,value):
    target=byid(data)[uid(p,key)];pieces=re.findall(r'[^.\[\]]+',path)
    for q in pieces[:-1]:target=target[int(q)] if isinstance(target,list) else target[q]
    last=pieces[-1];target[int(last) if isinstance(target,list) else last]=value
negative('source value corrupted without changing source anchor',lambda x:modify(x,120,'fund-r02','facts.columnValues[0].display','51,374'),verify_cells)
negative('fund column label swapped with unchanged numbers',lambda x:modify(x,120,'fund-r02','facts.columnValues[1].column','Water'),verify_cells)
negative('thousand dollar unit changed to dollar',lambda x:modify(x,120,'fund-r02','facts.columnValues[0].unit','$'),verify_cells)
negative('charge comparison year reversed',lambda x:modify(x,139,'ossm-charge','facts.columnValues[0].period','2026'),verify_cells)
negative('fleet negative cost changed to positive',lambda x:modify(x,117,'service-fleet-and-plant-r06','facts.columnValues[0].numericValue',1331),verify_cells)
swim=next(u for u in DATA['units'] if u['category']=='OP_CAPITAL_BUDGET_ROW' and u['facts']['columnValues'][0]['status']=='BLANK_NOT_ZERO')
negative('blank swimming capital value manufactured as zero',lambda x:byid(x)[swim['id']]['facts']['columnValues'][0].update(status='PRINTED_VALUE',numericValue=0,numericValueText='0',display='0'),verify_cells)
negative('expense row moved across original income-total boundary',lambda x:modify(x,116,'service-tourism-r04','facts.rowRole','Income component'),verify_roles)
negative('net asset gain misclassified as total',lambda x:modify(x,120,'fund-r08','facts.rowRole','SOURCE_DECLARED_TOTAL'),verify_roles)
negative('cash balance misclassified as financing flow',lambda x:modify(x,121,'fund-r19','facts.statementSection','Cash Flow from Financing Activities'),verify_roles)
negative('occluded footnote promoted to visible evidence',lambda x:modify(x,111,'capital-footnote','facts.textVisibility','VISIBLE'),verify_semantics)
negative('fuel surcharge falsely activated',lambda x:modify(x,129,'fuel-surcharge','facts.chargeCurrentlyAppliedAsPrinted',True),verify_semantics)
negative('former Snowy River resolution condition removed',lambda x:modify(x,134,'clause-1-2-5','conditions',[]),verify_semantics)
negative('pensioner combined cap split',lambda x:modify(x,140,'pensioner-rebate-1','facts.combinedScope',False),verify_semantics)
negative('composite Other counted as independent fifth fund',lambda x:modify(x,119,'chart-expenditure-funds','facts.series[2].role','CATEGORY'),verify_semantics)
negative('source FOGO conflict suppressed',lambda x:x.update(diagnostics=[d for d in x['diagnostics'] if d['type']!='SOURCE_SERVICE_FREQUENCY_AND_GEOGRAPHY_CONFLICT']),verify_semantics)
negative('unreconciled original cash movement silently corrected',lambda x:modify(x,121,'fund-r15','facts.columnValues[1].numericValue',2935),verify_cells)
negative('required source cash row missing',lambda x:x.update(units=[u for u in x['units'] if u['id']!=uid(121,'fund-r15')]),verify_cells)
receipt={'format':'csoi-op-finance-original-source-verification-1','sourceRevision':'sha256:'+SHA,'authorSha256':sha((HERE/'finance-author.json').read_bytes()),'status':'PASS_BOUNDED_SOURCE_POSITION_NUMERIC_AND_SPECIFIED_SEMANTIC_CHECKS','checked':{'pages':36,'units':428,'nativeAnchors':anchor_count,'freshV2PixelAnchors':pixel_count,'directNumericSourceCells':numeric,'serviceRowsAgainstOriginalIncomeTotalPositions':roles,'negativeCases':len(negative_results)},'negativeResults':negative_results,'limitations':['Native text hashes cannot prove visibility or semantic completeness. PDF111 explicitly records occluded text.','Four chart figures and four rating-map panels had manual original pixel review; chart amounts are guarded, no GIS/parcel applicability inferred.','Policy meaning beyond named guards depends on authored reading and separate independent semantic review, not schema/hash counts.','No app/browser/deployment checks in this finance author task.']}
(HERE/'finance-source-verification.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt['checked'],ensure_ascii=False))
