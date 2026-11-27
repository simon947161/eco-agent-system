#!/usr/bin/env python3
"""Pack authored research and explicit source-position inventory; no source prose redistribution."""
import fitz, hashlib, json, re, unicodedata
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
PDF=Path('/tmp/csoi-lsps-completion-20261102/lsps.pdf')
SOURCE=Path('/tmp/csoi-lsps-completion-20261102/narrative-units-source.json')
EXPECTED='9bf75ec6fb98f1d03bad47f5b9cda44e6ffadce3bf452eb5a343b394322f8f47'
assert hashlib.sha256(PDF.read_bytes()).hexdigest()==EXPECTED
pdf=fitz.open(PDF)
source=json.loads(SOURCE.read_text()); original={u['id']:u for p in source for u in p['units']}
old=json.loads((ROOT/'sources/lsps-public-knowledge.json').read_text())
page_info={p['pdfPage']:p for p in json.loads((ROOT/'qa/strategy-completion/lsps/page-inventory.json').read_text())}
map_pages=set([8,16,26,27,28,48,57,60,61,65,66,69,72,75,88]+list(range(105,117)))
def norm(s):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',s)).strip()
def sha(s):return 'sha256:'+hashlib.sha256(s if isinstance(s,bytes) else s.encode()).hexdigest()
def anchor(pn,bbox):
 page=pdf[pn-1]; b=[max(0,bbox[0]-.5),max(0,bbox[1]-.5),min(page.rect.width,bbox[2]+.5),min(page.rect.height,bbox[3]+.5)]
 b=[round(x,3) for x in b]; rect=fitz.Rect(b); tx=norm(page.get_text('text',clip=rect))
 # A fresh document per crop prevents observed cross-page renderer cache state
 # from changing pixels for an otherwise identical source rectangle.
 with fitz.open(PDF) as fresh:
  pix=fresh[pn-1].get_pixmap(matrix=fitz.Matrix(100/72,100/72),clip=rect,colorspace=fitz.csRGB,alpha=False)
 return {'pdfPage':pn,'bbox':b,'sourceTextHash':sha(tx),'cropHash':sha(f'RGB|{pix.width}x{pix.height}|'.encode()+pix.samples),'renderer':'pymupdf-1.26.6-rgb-100dpi-fresh-document-clip-v2'}
anchors={k:anchor(u['pdfPage'],u['bbox']) for k,u in original.items()}
units=[]; consumed={}
def add(ids,kind,summary,conditions='',extra=None):
 us=[original[x] for x in ids]; aa=[anchors[x] for x in ids]; uid='csoi:lsps2020:narrative:'+ids[0]
 txt=' '.join(norm(pdf[a['pdfPage']-1].get_text('text',clip=fitz.Rect(a['bbox']))) for a in aa)
 record={'id':uid,'pdfPage':us[0]['pdfPage'],'printedPage':us[0]['pdfPage']-1,'bbox':aa[0]['bbox'],'heading':page_info[us[0]['pdfPage']]['section'],'unitKind':kind,'summary':summary,'conditions':[{'text':conditions,'sourceEvidence':aa}] if conditions else [],'qualifiers':[{'text':'Historical 2020 source statement; current law, actual delivery and official admission remain unverified.','sourceEvidence':aa}], 'existingActionIds':[], 'inventoryIds':ids,'evidenceAnchors':aa,'sourceTextHash':sha(norm(txt)),'cropHash':aa[0]['cropHash'],'reviewStatus':'AI_INDEPENDENTLY_SEMANTIC_REVIEWED','gaps':[],'citationLimit':'Authored research paraphrase; original source not redistributed.'}
 if extra:record.update(extra)
 for id in ids:
  assert id not in consumed,id
  consumed[id]=uid
 units.append(record)
for line in (OUT/'authored-units.tsv').read_text().splitlines():
 if not line.strip():continue
 cols=line.split('\t'); ids=cols[0].split('+');add(ids,cols[1],cols[2],cols[3] if len(cols)>3 else '')
text_unit_count=len(units)
visual_specs=json.loads((OUT/'visual-units.json').read_text())
visual_image_links={}
for v in visual_specs:
 a=anchor(v['pdfPage'],v['bbox']);uid='csoi:lsps2020:narrative:'+v['id'];pn=v['pdfPage']
 units.append({'id':uid,'pdfPage':pn,'printedPage':pn-1,'bbox':a['bbox'],'heading':page_info[pn]['section'],'unitKind':v['unitKind'],'summary':v['summary'],'conditions':[{'text':v['conditions'],'sourceEvidence':[a]}] if v['conditions'] else [],'qualifiers':[{'text':'Historical visual source; estimates, future scenarios and source-internal scope limits are retained; no current result or official admission.','sourceEvidence':[a]}],'existingActionIds':[],'inventoryIds':[],'imageInventoryIds':[v['imageInventoryId']] if v['imageInventoryId'] else [],'evidenceAnchors':[a],'sourceTextHash':a['sourceTextHash'],'cropHash':a['cropHash'],'visualObservations':v['visualObservations'],'reviewStatus':'AI_INDEPENDENTLY_SEMANTIC_REVIEWED','gaps':[],'citationLimit':'Authored visual interpretation; no original figure reproduced; unlabelled pixel values not fabricated.'})
 if v['imageInventoryId']:visual_image_links[v['imageInventoryId']]=uid
# Link original numbered action occurrences and implementation cells by source anchors.
links={}
for r in old['records']:
 if r['category']!='ACTION':continue
 for ea in r['facts'].get('evidenceAnchors',[]):
  a=ea['anchor']; pn=a['pdfPage'];box=a['bbox']
  for u in source[pn-1]['units']:
   b=u['bbox'];x=(b[0]+b[2])/2;y=(b[1]+b[3])/2
   if box[0]-1<=x<=box[2]+1 and box[1]-3<=y<=box[3]+3:
    links.setdefault(u['id'],[]).append(r['id'])
# Short headings/credits/navigation are explicitly inventoried, not counted as prose.
head=re.compile(r'^(Council Will|Actions|Objectives|MAINTAIN|ENHANCE|CHANGE|Maintain|Maintain and enhance|Maintain enhance and change|The Village feel|Abbreviations|GLOSSARY|Consultation|Legislative Context|Strategic Context|About the Plan|References|Implementation and Monitoring|How will we get there\?|The Future is Bright|20 Year Vision)$',re.I)
explicit_heading_ids=set('p002-b01-u01 p002-b06-u01 p006-b01-u01 p006-b02-u01 p009-b01-u01 p012-b18-u01 p014-b33-u01 p017-b03-u01 p018-b08-u01 p019-b02-u01 p019-b06-u01 p022-b02-u01 p022-b03-u01 p022-b04-u01 p023-b02-u01 p032-b10-u01 p033-b02-u01 p038-b12-u01 p040-b02-u01 p041-b03-u01 p046-b02-u01 p047-b02-u01 p056-b02-u01 p076-b08-u01 p077-b03-u01 p077-b09-u01 p078-b02-u01 p078-b11-u01 p079-b05-u01 p079-b09-u01 p080-b03-u01 p080-b04-u01 p081-b10-u01 p081-b11-u01 p082-b08-u01 p083-b07-u01 p084-b02-u01 p089-b05-u01'.split())
inventory=[]
for u in original.values():
 ident=u['id'];tx=u['text'];pn=u['pdfPage'];a=anchors[ident]
 if ident in consumed: disp='AUTHORED_SUBSTANTIVE';reason='Covered by an authored coherent review unit.';ru=consumed[ident]
 elif ident in links:disp='EXISTING_NUMBERED_ACTION';reason='Source-position overlap with exact existing action evidence; links are provenance, not newly admitted official relationships.';ru=None
 elif tx.isdigit() or tx in ('.',''):disp='NON_SUBSTANTIVE_PAGE_OR_MARK';reason='Page numbering or isolated typographic mark.';ru=None
 elif pn in (3,4):disp='NAVIGATION_CONTENTS';reason='Contents or figure index; source page location retained.';ru=None
 elif ident in explicit_heading_ids or head.match(tx) or ('Specific Actions' in tx) or (len(tx)<170 and re.match(r'^(Planning Priority \d+|Figure \d+|Image[,:]|[A-Za-z’ -]+, [Cc]ourtesy|.*\(.*20\d\d\))',tx)):
  disp='HEADING_OR_CAPTION';reason='Heading or source illustration credit/caption; figure semantics handled separately where substantive.';ru=None
 elif pn in range(90,105):disp='IMPLEMENTATION_TABLE_CONTEXT';reason='Original implementation table heading/column/context; actual rows remain in the existing bundle.';ru=None
 elif pn in [8,16,28,48,57,60,61,65,66,69,72,75,88]+list(range(105,117)):disp='MAP_TEXT_CONTEXT';reason='Map caption or peripheral text; spatial interpretation belongs to separate map review.';ru=None
 else:disp='PENDING_AUTHOR_CLASSIFICATION';reason='Draft: source position retained, substantive status still being authored.';ru=None
 inventory.append({'inventoryId':ident,'pdfPage':pn,'bbox':a['bbox'],'disposition':disp,'reason':reason,'reviewUnitId':ru,'existingActionIds':sorted(set(links.get(ident,[]))),'sourceTextHash':a['sourceTextHash'],'cropHash':a['cropHash'],'evidenceAnchors':[a]})
images=[]
for pn,page in enumerate(pdf,1):
 for bi,b in enumerate(page.get_text('dict')['blocks']):
  if b['type']!=1:continue
  a=anchor(pn,b['bbox']);iid=f'p{pn:03d}-image-b{bi:02d}'
  if iid in visual_image_links:disposition='SUBSTANTIVE_NON_SPATIAL_FIGURE';rid=visual_image_links[iid];reason='Visually read and authored in semantic units.'
  elif pn in map_pages:disposition='SPATIAL_MAP_SEPARATE_REVIEW';rid=f'lsps-map-p{pn:03d}';reason='Spatial content reviewed in qa/lsps-completion/maps/map-review.json; no inferred geometry from text.'
  elif 90<=pn<=104:disposition='EXISTING_TABLE_TICK_EVIDENCE';rid=None;reason='Image tick verified in existing LSPS source bundle; not standalone narrative.'
  elif pn==13:disposition='REFERENCE_COVER_ILLUSTRATION';rid=None;reason='Illustrated covers of historical planning documents; plan relationships are separately authored, not original-document admission.'
  else:disposition='PHOTOGRAPH_OR_DECORATIVE_ILLUSTRATION';rid=None;reason='Photo/logo illustration; no quantitative, spatial or operative policy claim derived from image.'
  images.append({'id':iid,'pdfPage':pn,'bbox':a['bbox'],'sourceImageHash':sha(b['image']),'cropHash':a['cropHash'],'renderer':a['renderer'],'disposition':disposition,'reviewUnitId':rid,'reason':reason})
pages=[]
for pn in range(1,119):
 inv=[i for i in inventory if i['pdfPage']==pn];uu=[u for u in units if any(a['pdfPage']==pn for a in u['evidenceAnchors'])]
 pages.append({'pdfPage':pn,'printedPage':pn-1,'section':page_info[pn]['section'],'normalizedPageDigest':page_info[pn]['normalizedPageDigest'],'disposition':'AUTHORING_IN_PROGRESS' if any(i['disposition']=='PENDING_AUTHOR_CLASSIFICATION' for i in inv) else ('MAP_AND_TEXT_SEPARATELY_REVIEWED' if pn in map_pages else 'NON_MAP_SOURCE_DISPOSITION_COMPLETE'),'unitIds':[u['id'] for u in uu],'inventoryIds':[i['inventoryId'] for i in inv],'imageIds':[i['id'] for i in images if i['pdfPage']==pn],'mapReviewId':f'lsps-map-p{pn:03d}' if pn in map_pages else None,'gaps':['Current legal applicability, actual execution and authorised human admission remain unestablished; source checks and runtime readback are recorded separately.']})
assert not any(i['disposition']=='PENDING_AUTHOR_CLASSIFICATION' for i in inventory)
result={'format':'lsps-narrative-review-1','status':'AUTHOR_COMPLETE_AI_SEMANTIC_REVIEWED','at':datetime.now(timezone.utc).isoformat(),'document':{'sourceId':old['sourceId'],'sourceRevision':old['sourceRevision'],'totalPages':118,'printedAdoptionDate':'2020-05-21','originalBundleSHA256':hashlib.sha256((ROOT/'sources/lsps-public-knowledge.json').read_bytes()).hexdigest(),'reviewScope':'All non-map narrative, policy, conditions, glossary, references and non-spatial figures; spatial maps separately reviewed.','normalization':'NFKC then Unicode whitespace collapse then trim; UTF-8 SHA256.','anchorContract':'Native top-left PDF points, stored expanded bbox is exact clip; no implicit margin. Merged units hash normalized join of evidence-anchor texts in given order.','renderer':'pymupdf-1.26.6-rgb-100dpi-fresh-document-clip-v2','currentLaw':'UNKNOWN','actualExecution':'UNKNOWN','officialAdmission':'PENDING'},'counts':{'pages':118,'inventoryUnits':len(inventory),'authorTextUnits':text_unit_count,'authorVisualUnits':len(visual_specs),'authorReviewUnits':len(units),'independentNonMapChartOccurrences':17,'additionalPurposeListVisuallyReviewed':1,'reviewUnitsByKind':dict(Counter(u['unitKind'] for u in units)),'inventoryByDisposition':dict(Counter(i['disposition'] for i in inventory)),'imagesByDisposition':dict(Counter(i['disposition'] for i in images)),'pendingTextInventory':0,'sourceImages':len(images),'existingActionInventoryUnits':sum(i['disposition']=='EXISTING_NUMBERED_ACTION' for i in inventory)},'pages':pages,'units':units,'inventory':inventory,'images':images,'visualOccurrenceCrosswalk':json.loads((OUT/'visual-occurrence-crosswalk.json').read_text()),'unresolvedGaps':['Independent AI semantic review accepted all512 author units; final source checks and app-node readback are recorded separately, not inferred from this author status.','Current legal versions, cadastral applicability, actual delivery, budget/spend and authorised human admission are not established.','Historical references are inventoried but external cited documents not all independently retrieved and checked.','Unlabelled chart values and absent source definitions remain unknown; no reconstruction by pixel estimates.','No operational monitoring protocol or current performance dataset is inferred from the implementation heading or document-structure diagram.','Spatial map content is separately reviewed; no GIS digitisation or parcel-level applicability created.']}
result['document']['semanticReview']={'status':'AI_INDEPENDENTLY_SEMANTIC_REVIEWED','reviewer':'/root/source_semantic_review','scope':'All512 authored summaries/conditions read against independently read original; final source pixel audit and actual app-node binding separately recorded.','evidencePaths':['qa/lsps-completion/independent-narrative/semantic-readback.json','qa/lsps-completion/independent-narrative/semantic-readback.csv','qa/lsps-completion/independent-narrative/REPORT_ZH.md'],'authorisedHumanAdmission':'PENDING'}
(OUT/'narrative-review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result['counts']))
