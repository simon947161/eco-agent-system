"""Build bounded original-page evidence for water service inventory, finance and reporting."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import fitz

APP=Path(__file__).resolve().parents[1]
OUT=APP/'sources/service-context-20261128.json'
def digest(data):
    return 'sha256:'+hashlib.sha256(data).hexdigest()
def norm(value):
    return ' '.join(unicodedata.normalize('NFKC',value).split())
def anchor(doc,page,box=None):
    return {'pdfPage':page,'normalizedPageDigest':digest(norm(doc[page-1].get_text()).encode()),
            'parserVersion':'pymupdf-'+fitz.VersionBind+'-nfkc-whitespace-v1',**({'bbox':box} if box else {})}
def build(source,path,role):
    pdf=path.read_bytes()
    if digest(pdf)!=source['rawDigest']:
        raise ValueError('Source bytes differ: '+source['id'])
    with fitz.open(stream=pdf,filetype='pdf') as doc:
        if role=='asset':
            page,period,boundary=8,'2025–2035 asset plan; inventory observation date UNKNOWN','Council water network, service-wide'
            items=[('water-mains','Water mains length','NETWORK_LENGTH',315,'km',[56,116,360,132],r'315\s*km.*water mains'),
                   ('reservoirs','Reservoir inventory','ASSET_COUNT',25,'reservoirs',[56,161,320,178],r'25 reservoirs'),
                   ('average-supply','Average network water supply','AVERAGE_FLOW_RATE',7.5,'ML/day',[56,58,465,89],r'7\.5M litres of water per day')]
            qualifier='Network-wide inventory and average supply. Local project share, observation interval and design capacity are unknown. The nearby asset-value chart labels wastewater; no valuation is derived.'
            sections=['Water service infrastructure','Water network inventory and supply']
        elif role=='report':
            page,period,boundary=34,'FY2024-25','Reticulated water supplies sampled across the Council area'
            items=[('water-samples','Water samples reported for FY2024–25','REPORTED_SAMPLE_COUNT',536,'samples',[25,49,815,89],r'gathering 536 samples over the reporting year')]
            qualifier='The annual report counts samples across the supplied network. The number passing, the Nimmitabel subset and the effect of any later project are unknown.'
            sections=['Drinking-water sampling']
        else:
            page,period,boundary=26,'2026–2036 financial plan','Water-service fund across the Council area'
            items=[('water-fund','Water-service revenue boundary','FUND_CONTEXT',None,None,[69,321,518,360],r'water supply service is accounted for through a restricted fund')]
            qualifier='The financial plan distinguishes water-service revenues from the general fund. A named project allocation or payment cannot be inferred from this passage.'
            sections=['Long-term financial plan','Water revenue · section 4.4.4']
        common={'sourceRevision':source['rawDigest'],'boundary':boundary,'sourcePeriod':period,'actualOutcome':'UNKNOWN','actualSpend':'UNKNOWN','officialAdmission':'PENDING','humanReview':'PENDING'}
        prefix='csoi:knowledge:service-context:'+role
        def record(id,kind,cat,parent,title,summary,p,extra,box=None):
            return {'id':id,'kind':kind,'category':cat,'code':id.split(':')[-1],'parentId':parent,'title':title,
                    'summary':summary,'locator':f'{source["title"]}, PDF {p}'+(', LTFP printed p.15' if role=='fund' and p==26 else ''),
                    'anchor':anchor(doc,p,box),'facts':{**common,**extra},'relations':[]}
        name={'asset':'Water Asset Management Plan 2025–2035','report':'Annual Report 2024–25','fund':'Resourcing Strategy · 2026 revision'}[role]
        records=[record(prefix,'DocumentRevision','SERVICE_DOCUMENT',None,name,'Bounded public-source research for water-service context.',1,{'totalPages':len(doc),'reviewedPages':[1,page]})]
        parent=prefix
        for i,section in enumerate(sections):
            key=prefix+':section:'+str(i+1)
            records.append(record(key,'ContentBlock','SOURCE_SECTION',parent,section,qualifier,page,{'qualifier':qualifier}))
            parent=key
        for key,title,nature,value,unit,box,pattern in items:
            text=norm(doc[page-1].get_text(clip=fitz.Rect(box)))
            if not re.search(pattern,text,re.I):raise ValueError('Cell mismatch: '+key)
            extra={'qualifier':qualifier,'cellDigest':digest(text.encode())}
            if nature=='FUND_CONTEXT':kind,cat='ResourceAccount','FUND_CONTEXT';extra['projectAllocation']='UNKNOWN'
            else:
                kind,cat='QuantifiedObservation','SERVICE_OBSERVATION'
                extra.update(nature=nature,computability='NOT_COMPUTABLE',baseline={'value':value,'scale':1,'unit':unit,'role':'PUBLISHED_SERVICE_OBSERVATION'})
            records.append(record(prefix+':'+key,kind,cat,parent,title,qualifier,page,extra,box))
        return {'format':'csoi-public-knowledge-1','sourceId':source['id'],'sourceRevision':source['rawDigest'],'sourcePageCount':len(doc),'rights':'UNKNOWN','currentVersion':'UNKNOWN','officialAdmission':'PENDING','originalBytesCommitted':False,'records':records}
def main():
    ap=argparse.ArgumentParser()
    for role in ['asset','report','fund']:ap.add_argument(role,type=Path)
    ap.add_argument('--write',action='store_true')
    args=ap.parse_args()
    sources={s['id']:s for s in json.loads((APP/'sources/csoi-catalogue.json').read_text())['sources']}
    ids={'asset':'smrc-water-amp-2025','report':'smrc-annual-report-2025-retrieved','fund':'smrc-resourcing-2026'}
    data=[build(sources['csoi:'+sid+':20261030'],getattr(args,role),role) for role,sid in ids.items()]
    if args.write:OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    elif json.loads(OUT.read_text())!=data:raise ValueError('Service manifest differs from original')
    print('PASS original asset plan, annual report and resourcing strategy: raw bytes, page anchors and bounded observations')
if __name__=='__main__':main()
