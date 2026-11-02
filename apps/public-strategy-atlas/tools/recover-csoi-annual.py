"""Retry one officially linked 57 MB annual report within an explicit 64 MiB cap.
This changes a local transfer bound, never proxy/TLS/security policy. Temporary
original only; rights/currentness/admission remain UNKNOWN/PENDING.
"""
import datetime,hashlib,json,pathlib,urllib.request,urllib.parse
APP=pathlib.Path(__file__).resolve().parents[1];OUT=pathlib.Path('/tmp/csoi-annual-recovery');OUT.mkdir(exist_ok=True)
source=json.loads((APP/'sources/csoi-source-observations.json').read_text());ipr=next(o for o in source['observations'] if o['id']=='smrc-ipr');old=next(o for o in source['observations'] if o['id']=='smrc-annual-report-2025')
url=old['url'];link=next((l for l in ipr['documentLinks'] if l['url']==url),None)
if not link or urllib.parse.urlsplit(url).hostname!='www.snowymonaro.nsw.gov.au':raise SystemExit('OFFICIAL_DIRECTORY_LINK_REQUIRED')
class Guard(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,request,fp,code,msg,headers,target):
  p=urllib.parse.urlsplit(target)
  if p.scheme!='https' or p.hostname!='www.snowymonaro.nsw.gov.au' or p.username or p.password:raise ValueError('REDIRECT_REQUIRES_REVIEW')
  return super().redirect_request(request,fp,code,msg,headers,target)
row={'id':'smrc-annual-report-2025-retrieved','family':'PERFORMANCE_REPORTING','url':url,'retrievedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'classification':'PUBLIC','rights':'UNKNOWN','currentVersion':'UNKNOWN','legalApplicability':'UNKNOWN','admission':'PENDING','geography':'Snowy Monaro, NSW, Australia; strategic reporting context only','title':link['title'],'knowledgeAnchors':[],'originalBytesCommitted':False}
try:
 with urllib.request.build_opener(Guard()).open(url,timeout=45) as response:
  body=response.read(64*1024*1024+1)
  if len(body)>64*1024*1024:raise ValueError('SOURCE_SIZE_BOUND_64_MIB')
  if response.status!=200 or not body.startswith(b'%PDF'):raise ValueError('ORIGINAL_PDF_REQUIRED')
  row.update(httpStatus=200,resolvedUrl=response.url,mediaType=response.headers.get_content_type(),byteLength=len(body),rawDigest='sha256:'+hashlib.sha256(body).hexdigest(),access='AVAILABLE',byteVerification='PASS_TESTED_HERE');(OUT/'annual-report.pdf').write_bytes(body)
  template=next(o['intakeRecord'] for o in source['observations'] if o.get('intakeRecord'));record=json.loads(json.dumps(template));record.update(id='csoi:'+row['id']+':20261030',family=row['family'],officialUrl=url,directoryUrl=ipr['url'],title=row['title'],recordType='DOCUMENT',mediaType=row['mediaType'],rawDigest=row['rawDigest'],retrievedAt=row['retrievedAt'],extraction={'coverage':'NONE','anchors':[]},lineage={'supersedes':[],'revisionLabel':row['rawDigest']},access={'state':'AVAILABLE','checkedAt':row['retrievedAt'],'reason':'Officially linked original PDF retrieved within explicit 64MiB cap; rights/currentness/admission remain pending.'});row['intakeRecord']=record
  row['stageEvidence']={'DIRECTORY_OBSERVED':{'url':ipr['url'],'directoryDigest':ipr['rawDigest']},'SOURCE_RETRIEVED':{'url':url,'retrievedAt':row['retrievedAt'],'httpStatus':200,'byteLength':len(body),'rawDigest':row['rawDigest']},'RAW_BYTES_VERIFIED':{'rawDigest':row['rawDigest']}}
except Exception as error:row.update(access='UNAVAILABLE',error=str(error),byteVerification='NOT_VERIFIED')
(OUT/'observation.json').write_text(json.dumps(row,indent=2)+'\n');print(json.dumps({k:row.get(k) for k in ['id','httpStatus','access','byteLength','rawDigest','error']},indent=2))
