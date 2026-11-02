"""Read-only public source audit; no catalogue/source revision is changed."""
import concurrent.futures,datetime,hashlib,json,pathlib,urllib.request,urllib.parse
ROOT=pathlib.Path('/tmp/csoi-integrity-audit-20261031')
APP=ROOT/'readonly-head/apps/public-strategy-atlas'
OBS=json.loads((APP/'sources/csoi-source-observations.json').read_text())['observations']
SELECTED=[o for o in OBS if o.get('httpStatus')==200 and o.get('rawDigest')]
HOSTS={urllib.parse.urlparse(o[k]).hostname for o in SELECTED for k in ['url','resolvedUrl'] if o.get(k)}
class SafeRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  u=urllib.parse.urlparse(newurl)
  if u.scheme!='https' or u.username or u.password or u.hostname not in HOSTS:raise ValueError('UNREGISTERED_REDIRECT_HOST')
  return super().redirect_request(req,fp,code,msg,headers,newurl)
def fetch(o):
 r={'observationId':o['id'],'sourceId':o['intakeRecord']['id'],'url':o['url'],'historicalRawDigest':o['rawDigest'],'historicalByteLength':o['byteLength'],'historicalRetrievedAt':o['retrievedAt'],'mediaType':o['mediaType'],'checkedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rights':'UNKNOWN_OR_PENDING_NO_REDISTRIBUTION','attempts':1}
 p=ROOT/'originals'/(o['id']+('.pdf' if o['mediaType']=='application/pdf' else '.html'))
 try:
  bound=min(65*1024*1024,int(o['byteLength'])+1024*1024)
  opener=urllib.request.build_opener(SafeRedirect())
  with opener.open(urllib.request.Request(o['url'],headers={'User-Agent':'CSOI-readonly-integrity-audit/1.0'}),timeout=45) as response:
   r['httpStatus']=response.status;r['resolvedUrl']=response.url;r['contentType']=response.headers.get('Content-Type');h=hashlib.sha256();n=0
   with p.open('wb') as out:
    while chunk:=response.read(1024*1024):
     n+=len(chunk)
     if n>bound:raise ValueError('AUDIT_BYTE_LIMIT')
     h.update(chunk);out.write(chunk)
  r.update(path=str(p),byteLength=n,rawDigest='sha256:'+h.hexdigest(),receiptMatch=n==o['byteLength'] and 'sha256:'+h.hexdigest()==o['rawDigest'],status='RETRIEVED_CURRENT_PUBLIC_COPY')
  if o['mediaType']=='application/pdf':
   if not p.read_bytes()[:1024].lstrip().startswith(b'%PDF-'):raise ValueError('NOT_PDF_PREFIX')
   from pypdf import PdfReader
   r['pages']=len(PdfReader(p).pages)
 except Exception as error:
  p.unlink(missing_ok=True);r.update(status='UNVERIFIED',error=type(error).__name__+':'+str(error)[:300])
 return r
if __name__=='__main__':
 first=next(o for o in SELECTED if o['id']=='smrc-csp-full-2025');results=[fetch(first)]
 print(json.dumps(results[0]),flush=True)
 if results[0]['status']=='RETRIEVED_CURRENT_PUBLIC_COPY':
  with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
   for r in pool.map(fetch,[o for o in SELECTED if o['id']!=first['id']]):results.append(r);print(json.dumps(r),flush=True)
 (ROOT/'local-originals.json').write_text(json.dumps({'auditHead':'744ab46b2bec2ad601da0c4ae528694a4c982154','results':results,'originalsRedistributable':False},indent=2)+'\n')
