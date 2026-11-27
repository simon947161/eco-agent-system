"""Rebuild the November DP/OP project table receipts from exact original files."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata

import fitz

APP=Path(__file__).resolve().parents[1]
DIR=APP/'sources'
HEADERS={
 'DP':['CSP Link','Strategy/Major Project','Details','Project Budget for the years identified','Delivery Years','','',''],
 'OP':['Major Project/Infrastructure Delivery','Description','Annual Budget','Resources','CSP Link Strategy Action','Other Plans & Strategy Links','Start','End'],
}
TOPICS={
 'water treatment':'Water treatment','water supply':'Water supply','water management':'Water planning','watermain':'Water mains','water mains':'Water mains','water security':'Water security',
 'sewer':'Sewerage','sewage':'Sewerage','reservoir':'Reservoir','stormwater':'Stormwater','drainage':'Drainage','pump':'Pumping','intake':'Intake','pipeline':'Pipeline',
 'biosecurity':'Biosecurity','sagittaria':'Aquatic weed control','biodiversity':'Biodiversity','weed':'Weed control','compost':'Composting','flaring':'Biogas flaring','street bins':'Street bins',
 'waste':'Waste services','flood':'Flood management','trail':'Trail','footpath':'Footpath','bridge':'Bridge','road':'Road','swimming':'Swimming facilities','aquatic':'Aquatic facilities',
 'cemetery':'Cemetery','showground':'Showground','saleyard':'Saleyard','asset':'Asset management','parks':'Parks','recreation':'Recreation','reserve':'Reserve',
 'workforce':'Workforce planning','employee':'Workforce','health':'Health','safety':'Safety','policy':'Policy','land':'Land','strategy':'Strategy','planning':'Planning',
 'financial':'Finance','audit':'Audit','cash':'Cash management','rates':'Rates','supplier':'Supplier management','contract':'Contracts','ict':'ICT','technology':'Technology','cloud':'Cloud systems',
 'customer':'Customer service','volunteer':'Volunteering','leaders':'Leadership','service':'Service planning','security':'Security','aged care':'Aged care',
}
PLACES=['East Jindabyne','Jindabyne','Nimmitabel','Berridale','Bombala','Cooma','Adaminaby','Dalgety','Delegate','Kalkite','Murrumbidgee','North Ridge','Lake Wallace','Monaro']
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(b):return 'sha256:'+hashlib.sha256(b).hexdigest()
def norm(t):return ' '.join(unicodedata.normalize('NFKC',t or '').split())
def build(edition,path):
 family=edition['family'];dp=family=='DP';raw=path.read_bytes()
 if sha(raw)!=edition['rawDigest']:raise ValueError('Wrong original for '+family)
 rows=[];gaps=[];tables=0
 with fitz.open(stream=raw,filetype='pdf') as doc:
  for p in doc:
   text=norm(p.get_text());page=p.number+1
   if 'major project' not in text.lower() or 'budget' not in text.lower():continue
   for table in p.find_tables().tables:
    cells=table.extract();h=list(map(norm,cells[0]))
    if h!=HEADERS[family]:continue
    tables+=1
    for number,rawrow in enumerate(cells[1:],2):
     r=list(map(norm,rawrow))
     if dp and r[4:]==['25/26','26/27','27/28','28/29']:continue
     label=r[1 if dp else 0];coords=table.rows[number-1].cells
     if not label:
      gaps.append({'pdfPage':page,'table':tables,'row':number,'status':'UNNAMED_OR_CONTINUATION','cellsDigest':sha(canonical(r).encode())});continue
     budget=r[3 if dp else 2]
     plain=re.fullmatch(r'\$\s*([\d,]+)',budget)
     codes=list(dict.fromkeys(re.findall(r'\b\d+\.\d+\b',r[0 if dp else 4])))
     topics=list(dict.fromkeys(t for k,t in TOPICS.items() if k in label.lower()))[:3]
     places=[t for t in PLACES if re.search(r'\b'+re.escape(t)+r'\b',label,re.I)]
     if 'East Jindabyne' in places and 'Jindabyne' in places:places.remove('Jindabyne')
     rects=[fitz.Rect(c) for c in coords if c];box=rects[0]
     for rect in rects[1:]:box|=rect
     fields=['csp','subject','description','budget','year1','year2','year3','year4'] if dp else ['subject','description','budget','resources','csp','otherPlans','start','end']
     item={'pdfPage':page,'table':tables,'row':number,'rowBox':[int(round(x,2)) if round(x,2).is_integer() else round(x,2) for x in box],
       'pageDigest':sha(text.encode()),'cellDigest':sha(canonical(dict(zip(fields,r))).encode()),
       'topics':topics,'places':places,'codes':codes,'budgetCell':budget,'amountAUD':int(plain[1].replace(',','')) if plain else None,
       'budgetBasis':'MULTIYEAR_PROGRAM' if dp else 'ANNUAL_PLAN','resourceCell':'UNKNOWN' if dp else r[3] or 'UNKNOWN',
       'years':[v for v,mark in zip(['2025/26','2026/27','2027/28','2028/29'],r[4:]) if mark=='\uf00c'] if dp else r[6:8]}
     item['digest']=sha(canonical(item).encode());rows.append(item)
 return {'method':'atlas-project-table-cells-1','sourceId':'csoi:smrc-'+family.lower()+'-2026:20261128','rawDigest':edition['rawDigest'],'pageCount':edition['pages'],'tableCount':tables,'rows':rows,'gaps':gaps}

def main():
 a=argparse.ArgumentParser();a.add_argument('--dp',type=Path,required=True);a.add_argument('--op',type=Path,required=True);a.add_argument('--write',action='store_true');args=a.parse_args()
 if fitz.VersionBind!='1.26.6':raise ValueError('Reproduction requires PyMuPDF 1.26.6')
 roots={}
 for e in json.loads((DIR/'plan-editions-20261128.json').read_text())['editions']:
  item=build(e,getattr(args,e['family'].lower()));out=DIR/('project-table-'+e['family'].lower()+'.json');data=canonical(item)+'\n'
  if args.write:out.write_text(data)
  elif out.read_text()!=data:raise ValueError('Receipt mismatch '+out.name)
  roots[e['family']]={'sourceId':item['sourceId'],'rawDigest':item['rawDigest'],'pageCount':item['pageCount'],'digest':sha(data.rstrip().encode()),'rows':{f"{r['pdfPage']}-{r['table']}-{r['row']}":r['digest'] for r in item['rows']}}
  print(e['family'],item['tableCount'],'tables',len(item['rows']),'named rows',len(item['gaps']),'unresolved continuations',sha(data.rstrip().encode()),flush=True)
 js="(function(root){const v="+canonical(roots)+";root.AtlasProjectTableRoots=v;if(typeof module!=='undefined')module.exports=v;})(globalThis);\n"
 out=DIR/'project-table-roots.js'
 if args.write:out.write_text(js)
 elif out.read_text()!=js:raise ValueError('Project table receipt roots differ')
if __name__=='__main__':main()
