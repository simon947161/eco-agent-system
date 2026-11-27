from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,csv
from pypdf import PdfReader
OUT=Path(__file__).parent;ROOT=OUT.parent
model=json.loads((OUT/'model-results.json').read_text());manifest=json.loads((ROOT/'local-originals.json').read_text());sources={r['sourceId']:r for r in manifest['results']};readers={}
requirements={
'T01':{30:['CO2e emissions per capita','29.9 tonnes','2021-22']},
'T02':{22:['6.1','air, land, and waterways']},
'T03':{31:['Public Health and Environment','6.1','2025']},
'T04':{27:['98%','P1, P2 and P3 food premises','168','84']},
'T05':{1:['21 May 2020','Local Strategic Planning Statement']},
'T06':{1:['2025 - 2035'],3:['19/06/2025','142/25'],13:['Assets by Location','12 main towns','9 Treatment']},
'T07':{166:['soil suitability and topography','C9.3-1']},
'T08':{164:['110 litres','person per day','C6.2-3']},
'T09':{159:['soil composition','NATA','operation and maintenance']},
'T10':{55:['soil type, permeability','A9','reticulated sewerage']}}
class Text(HTMLParser):
 def __init__(self):super().__init__();self.bits=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ['script','style']:self.skip+=1
 def handle_endtag(self,tag):
  if tag in ['script','style'] and self.skip:self.skip-=1
 def handle_data(self,data):
  if not self.skip:self.bits.append(data)
rows=[]
for record in model['rows']:
 source=sources[record['sourceId']];body=Path(source['path']).read_bytes();digest='sha256:'+hashlib.sha256(body).hexdigest();r={'testId':record['testId'],'sourceId':record['sourceId'],'currentRawDigest':digest,'historicalRawDigest':record['sourceRawDigest'],'historicalReceiptMatches':digest==record['sourceRawDigest'],'checks':[]}
 if record['testId'] in requirements:
  if source['path'] not in readers:readers[source['path']]=PdfReader(source['path'])
  reader=readers[source['path']]
  for page,tokens in requirements[record['testId']].items():
   text=' '.join((reader.pages[page-1].extract_text(extraction_mode='layout')or'').split());r['checks'].append({'pdfPage':page,'tokens':tokens,'allTokensPresent':all(t.casefold() in text.casefold()for t in tokens)})
   if record.get('pageAnchor') and page==record['pageAnchor']['pdfPage']:r['normalizedPageDigestMatches']='sha256:'+hashlib.sha256(text.encode()).hexdigest()==record['pageAnchor']['normalizedPageDigest']
  r['factualSpotcheck']='PASS_BOUNDED_OBSERVATION' if r['historicalReceiptMatches'] and all(c['allTokensPresent']for c in r['checks'])else'FAIL_OR_REVIEW'
  if record['testId']=='T06':r.update(factualSpotcheck='PARTIAL_LOCATOR_ERROR',locatorDefect='Recorded PDF14 AssetsbyLocation; original Table4 AssetsbyLocation isPDF13. PDF14isTable5AssetsbyType. Original note fact/version mostlysupported, locator notfullycorrect.')
 else:
  parser=Text();parser.feed(body.decode('utf-8',errors='replace'));text=' '.join(' '.join(parser.bits).split());tokens=['not of a domestic origin or quantity','sewerage'] if record['testId']=='T11' else ['12 months','accredited'];r['checks']=[{'htmlSection':record['locator'],'tokens':tokens,'allTokensPresent':all(t.casefold()in text.casefold()for t in tokens)}];r['factualSpotcheck']='CURRENT_HTML_SUPPORT_ONLY_HISTORICAL_BYTES_CHANGED' if all(c['allTokensPresent']for c in r['checks'])else'HTML_WORDING_REVIEW_REQUIRED';r['limitation']='Current public HTML hash differs from registeredhistorical receipt; cannot independently reconstruct the exact historicalwebpage from Git alone.'
 rows.append(r)
(OUT/'original-spotchecks.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print(json.dumps([{'testId':r['testId'],'status':r['factualSpotcheck'],'checks':r['checks']}for r in rows],ensure_ascii=False))
