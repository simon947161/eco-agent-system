"""Verify row ownership and planned actions from the merged OP PDF 23 project cell."""
import argparse
import hashlib
import json
from pathlib import Path
import unicodedata
import fitz

APP=Path(__file__).resolve().parents[1]
SOURCE='csoi:smrc-op-2026:20261128'
PARENT='csoi:knowledge:op2026:november:table-row:23-6-2'
ACTIONS=[
 ('Work management systems','Introduce connected work management, timesheet and safety functions.','time sheeting'),
 ('Field work scheduling','Begin coordinating job planning, dispatch and field work through digital tools.','field mobility'),
 ('Asset and finance automation','Automate administrative steps in asset and financial records.','financial management'),
 ('Operational monitoring','Connect systems to support operational monitoring and safety.','operational monitoring'),
]
def norm(v):return ' '.join(unicodedata.normalize('NFKC',v or '').split())
def sha(b):return 'sha256:'+hashlib.sha256(b).hexdigest()
def box(v):return [int(round(x,2)) if round(x,2).is_integer() else round(x,2) for x in v]
def main():
 p=argparse.ArgumentParser();p.add_argument('original',type=Path);p.add_argument('--write',action='store_true');a=p.parse_args()
 src=json.loads((APP/'sources/project-table-op.json').read_text());raw=a.original.read_bytes()
 if sha(raw)!=src['rawDigest'] or fitz.VersionBind!='1.26.6':raise ValueError('Source or parser mismatch')
 with fitz.open(stream=raw,filetype='pdf') as pdf:
  page=pdf[22];tables=[t for t in page.find_tables().tables if 'Annual' in str(t.extract()[0])];assert len(tables)==1
  t=tables[0];grid=t.extract();parent=fitz.Rect(t.rows[1].cells[0]);nodes=[]
  assert norm(grid[1][0])=='Technology, Automation and Integration'
  for i,(title,summary,phrase) in enumerate(ACTIONS,1):
   r=list(map(norm,grid[i]));desc=fitz.Rect(t.rows[i].cells[1])
   if not (parent.y0<=desc.y0<desc.y1<=parent.y1 and abs(parent.x1-desc.x0)<.01 and (i==1 or t.rows[i].cells[0] is None)):raise ValueError('Merged subject does not own row')
   if phrase not in r[1] or r[2:]!=['TBD','Internal/External','12.2 12.3','Council resolution 364/25','2026','2027']:raise ValueError('Unexpected row facts')
   loc=f'OP v1.5, PDF 23, project table 6, physical row {i+1}'
   evidence={'mergedSubjectBox':box(parent),'descriptionBox':box(desc),'descriptionDigest':sha(r[1].encode()),'physicalRow':i+1,'subjectRow':2,'budgetCell':'TBD','resourceCell':'Internal/External','printedYears':['2026','2027'],'resolution':'364/25','codes':['12.2','12.3']}
   nodes.append({'id':PARENT+':activity:'+str(i+1),'kind':'Activity','category':'PLAN_ACTIVITY_ROW','code':'23-6-'+str(i+1),'parentId':PARENT,'title':title,'summary':summary,'locator':loc,'anchor':{'pdfPage':23,'normalizedPageDigest':sha(norm(page.get_text()).encode()),'parserVersion':'pymupdf-1.26.6-merged-subject-v1','bbox':box(desc)},'facts':{'sourceRevision':src['rawDigest'],'actualExecution':'UNKNOWN','actualSpend':'UNKNOWN','actualOutput':'UNKNOWN','actualOutcome':'UNKNOWN','officialAdmission':'PENDING','humanReview':'PENDING','evidence':evidence},'relations':[{'type':'EXPLICIT_DOCUMENT_REFERENCE','targetId':'csoi:knowledge:csp2035:strategy:'+code,'locator':loc+', CSP column'} for code in evidence['codes']]})
  if abs(parent.y1-t.rows[5].cells[0][1])>.01:raise ValueError('The next project must begin at the merged cell boundary')
  data={'format':'csoi-public-knowledge-1','sourceId':SOURCE,'sourceRevision':src['rawDigest'],'sourcePageCount':len(pdf),'rights':'UNKNOWN','currentVersion':'UNKNOWN','officialAdmission':'PENDING','originalBytesCommitted':False,'records':nodes}
 out=APP/'sources/op-project-activities.js';js="(function(root){const v="+json.dumps(data,sort_keys=True,separators=(',',':'),ensure_ascii=False)+";root.AtlasOpActivityRows=v;if(typeof module!=='undefined')module.exports=v;})(globalThis);\n"
 if a.write:out.write_text(js)
 elif out.read_text()!=js:raise ValueError('Activity receipt mismatch')
 print('PASS four distinct planned activities and exact shared subject boundaries; three unnamed cells resolved, no actual work, costs or outcome asserted')
if __name__=='__main__':main()
