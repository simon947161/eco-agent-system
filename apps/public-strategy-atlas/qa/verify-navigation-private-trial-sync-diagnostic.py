"""Exact live assets plus actual click navigation via supported Sites service auth.

No owner identity is simulated. Credential arrives over hidden stdin and is kept
only in memory; every credentialed request is GET to the exact approved origin.
"""
import sys,termios,json,urllib.request,urllib.error,urllib.parse,ssl,datetime,hashlib,os,uuid,concurrent.futures,gzip,time,tempfile
from pathlib import Path
from playwright.sync_api import Page
settings=termios.tcgetattr(sys.stdin.fileno());settings[3]&=~termios.ECHO;termios.tcsetattr(sys.stdin.fileno(),termios.TCSANOW,settings)
print('Ready for supported Site service credential JSON on hidden stdin.',flush=True)
c=json.loads(sys.stdin.readline());base=c['url'].rstrip('/');assert base=='https://council-strategy-intelligence.minshu.chatgpt.site'
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/navigation-repair-20261102/live-runs'/uuid.uuid4().hex;OUT.mkdir(parents=True,exist_ok=False)
print('Isolated live evidence directory: '+str(OUT),flush=True)
report={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':base,'auth':'Supported service access; no owner identity/session emulated','ownerInteractiveLogin':'NOT_TESTED','anonymous':[],'assets':[],'network':[]};manifest=json.loads((APP/'dist/deployment-assets.json').read_text());report['canonicalApplicationSha']=manifest['applicationSourceCommit']
def save():(OUT/'live-validation.json').write_text(json.dumps(report,indent=2)+'\n')
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args):return None
def get(url,auth):
 assert url.startswith(base+'/')
 headers={'Accept-Encoding':'gzip'}
 if auth:headers['OAI-Sites-Authorization']='Bearer '+c['token']
 opener=urllib.request.build_opener(NoRedirect,urllib.request.HTTPSHandler(context=ssl.create_default_context()))
 try:r=opener.open(urllib.request.Request(url,headers=headers),timeout=30)
 except urllib.error.HTTPError as e:r=e
 wire=r.read();encoding=r.headers.get('Content-Encoding','identity');assert encoding in ['identity','gzip'],encoding
 body=gzip.decompress(wire)if encoding=='gzip'else wire
 headers=dict(r.headers);headers['X-QA-Wire-Bytes']=str(len(wire));headers['X-QA-Wire-Encoding']=encoding;headers['X-QA-Decoded-Bytes']=str(len(body))
 return r.code,headers,body
try:
 for path in ['/','/csoi-pages.js','/sources/csoi-default-snapshot.js']:
  code,headers,body=get(base+path,False);assert code in [401,403],(path,code);report['anonymous'].append({'path':path,'status':code});save()
 def check(pair):
  name,expected=pair;code,headers,body=get(base+'/'+name,True)
  if name=='index.html'and code in [301,302,303,307,308]:
   assert urllib.parse.urljoin(base+'/'+name,headers.get('Location',headers.get('location','')))==base+'/';code,headers,body=get(base+'/',True)
  assert code==200,(name,code);actual='sha256:'+hashlib.sha256(body).hexdigest();assert actual==expected,name
  return {'file':name,'sha256':actual,'status':'EXACT'}
 pairs=list(manifest['files'].items())+[('deployment-assets.json','sha256:'+hashlib.sha256((APP/'dist/deployment-assets.json').read_bytes()).hexdigest())]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:report['assets']=list(pool.map(check,pairs))
 save();print('PASS anonymous denial and '+str(len(report['assets']))+' exact live files',flush=True)
 native=Page.goto;forwarding=tempfile.TemporaryDirectory(prefix='csoi-live-forward-')
 def goto(page,url,*args,**kw):
  if not getattr(page,'_csoi_nav_routed',False):
   page.on('pageerror',lambda error:report.setdefault('browserErrors',[]).append(str(error)[:1000]))
   def serve(route):
    request=route.request;assert request.method=='GET'and request.url.startswith(base+'/');started=time.monotonic();code,headers,body=get(request.url,True)
    report['network'].append({'path':urllib.parse.urlsplit(request.url).path,'status':code,'bytes':int(headers['X-QA-Decoded-Bytes']),'wireBytes':int(headers['X-QA-Wire-Bytes']),'wireEncoding':headers['X-QA-Wire-Encoding'],'seconds':round(time.monotonic()-started,3)})
    assert code==200,(report['network'][-1]['path'],code)
    # Playwright fulfillment expects decoded bytes. Use its supported path form
    # to avoid serializing large bodies through the Python-to-Node JSON channel.
    headers={k.lower():v for k,v in headers.items()if k.lower()not in ['content-length','content-encoding','transfer-encoding','connection','set-cookie','x-qa-wire-bytes','x-qa-wire-encoding','x-qa-decoded-bytes']}
    assert 'content-type'in headers,request.url
    response_file=Path(forwarding.name)/uuid.uuid4().hex;response_file.write_bytes(body)
    try:route.fulfill(status=code,headers=headers,content_type=headers['content-type'],path=str(response_file))
    finally:response_file.unlink()
    report['network'][-1]['forwardedSeconds']=round(time.monotonic()-started,3)
   page.route(base+'/**',serve);page._csoi_nav_routed=True
  try:return native(page,url,*args,**kw)
  except BaseException:
   try:report['timeoutState']=page.context.new_cdp_session(page).send('Runtime.evaluate',{'expression':"JSON.stringify({ready:document.readyState,notice:document.getElementById('startupMessage')?.textContent,count:document.getElementById('contentCount')?.textContent,url:location.href})",'returnByValue':True,'timeout':2000})
   except Exception as diagnostic:report['diagnosticFailure']=str(diagnostic)[:500]
   raise
 Page.goto=goto
 os.environ['ATLAS_TEST_URL']=base+'/';os.environ['ATLAS_NAV_OUTPUT']=str(OUT/'navigation');os.environ['ATLAS_NAV_MODE']='live real Chromium with supported service access, not owner login'
 script=APP/'qa/csoi-navigation-browser.py';report['scriptSha256']=hashlib.sha256(script.read_bytes()).hexdigest();exec(compile(script.read_text(),str(script),'exec'),{'__file__':str(script),'__name__':'__main__'})
 report['status']='PASS';save();print('PASS final deployed actual click navigation, visible records, deep links, history, refresh and persisted local values; owner login remains NOT_TESTED',flush=True)
except BaseException as e:report.update(status='FAILED',failure={'type':type(e).__name__,'message':str(e)[:2500]});save();raise
finally:
 if 'forwarding'in globals():forwarding.cleanup()
