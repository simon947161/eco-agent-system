"""Bounded official-public metadata supplement. No source text is redistributed."""
import concurrent.futures,datetime,hashlib,html,json,pathlib,re,urllib.request,urllib.parse
APP=pathlib.Path(__file__).resolve().parents[1];TMP=pathlib.Path('/tmp/csoi-legislation-v17');TMP.mkdir(exist_ok=True)
class Guard(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,request,fp,code,msg,headers,url):
  before=urllib.parse.urlsplit(request.full_url);after=urllib.parse.urlsplit(url)
  if after.scheme!='https' or after.hostname!=before.hostname:raise ValueError('REDIRECT_REQUIRES_REVIEW')
  return super().redirect_request(request,fp,code,msg,headers,url)
opener=urllib.request.build_opener(Guard())
targets=[('nsw-food-act','FOOD_LEGISLATION','https://legislation.nsw.gov.au/view/html/inforce/current/act-2003-043'),('nsw-public-health-act','PUBLIC_HEALTH_LEGISLATION','https://www.legislation.nsw.gov.au/view/html/inforce/current/act-2010-127'),('nsw-public-health-regulation','PUBLIC_HEALTH_LEGISLATION','https://legislation.nsw.gov.au/view/html/inforce/current/sl-2022-0502'),('nsw-local-government-act','LOCAL_GOVERNMENT_LEGISLATION','https://legislation.nsw.gov.au/view/html/inforce/current/act-1993-030')]
def fetch(target):
 id,family,url=target;at=datetime.datetime.now(datetime.timezone.utc).isoformat();row={'id':id,'family':family,'url':url,'retrievedAt':at,'classification':'PUBLIC','rights':'UNKNOWN','currentVersion':'UNKNOWN','legalApplicability':'UNKNOWN','admission':'PENDING','geography':'NSW, Australia; local applicability requires review','knowledgeAnchors':[],'originalBytesCommitted':False}
 try:
  with opener.open(url,timeout=25) as response:
   body=response.read(4*1024*1024+1)
   if len(body)>4*1024*1024:raise ValueError('TRANSFER_CAP_EXCEEDED')
   digest='sha256:'+hashlib.sha256(body).hexdigest();title=re.search('<title>(.*?)</title>',body.decode('utf-8','replace'),re.S|re.I)
   row.update(httpStatus=response.status,resolvedUrl=response.url,mediaType=response.headers.get_content_type(),byteLength=len(body),rawDigest=digest,title=html.unescape(re.sub('<[^>]+>',' ',title.group(1))).strip() if title else id,access='AVAILABLE',byteVerification='PASS_TESTED_HERE')
   (TMP/(id+'.html')).write_bytes(body)
   template=json.loads((APP/'sources/csoi-source-observations.json').read_text())['observations'][0]['intakeRecord'];record=json.loads(json.dumps(template));record.update(id='csoi:'+id+':20261030',family=family,publisher='NSW Parliamentary Counsel / NSW legislation website',officialUrl=url,directoryUrl=url,title=row['title'],recordType='DOCUMENT',mediaType=row['mediaType'],rawDigest=digest,retrievedAt=at);record['geographicExtent']={'type':'STATE','label':'NSW, Australia','parcelApplicability':'UNKNOWN'};record['lineage']={'supersedes':[],'revisionLabel':digest};record['access']={'state':'AVAILABLE','checkedAt':at,'reason':'Actual official-public HTTPS body and original-byte digest; current consolidation/effect remains unreviewed.'};row['intakeRecord']=record
   row['stageEvidence']={'DIRECTORY_OBSERVED':{'url':url,'directoryDigest':digest},'SOURCE_RETRIEVED':{'url':url,'retrievedAt':at,'byteLength':len(body),'httpStatus':200,'rawDigest':digest},'RAW_BYTES_VERIFIED':{'rawDigest':digest}}
 except Exception as error:row.update(httpStatus=getattr(error,'code',None),access='UNAVAILABLE',error=str(error),byteVerification='NOT_VERIFIED')
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,targets))
(TMP/'observations.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps([{k:r.get(k) for k in ['id','httpStatus','access','byteLength','title','error']} for r in rows],indent=2))
