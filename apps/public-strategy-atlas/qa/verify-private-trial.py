import sys,termios,json,hashlib,datetime,subprocess,concurrent.futures,urllib.parse
from pathlib import Path
import urllib.request,urllib.error,ssl,types
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl): return None
class Requests:
 @staticmethod
 def get(url,headers=None,allow_redirects=False,timeout=30):
  opener=urllib.request.build_opener(NoRedirect,urllib.request.HTTPSHandler(context=ssl.create_default_context()))
  try: response=opener.open(urllib.request.Request(url,headers=headers or {}),timeout=timeout)
  except urllib.error.HTTPError as e: response=e
  return types.SimpleNamespace(status_code=response.code,content=response.read(),headers=response.headers)
requests=Requests()
from playwright.sync_api import Page,sync_playwright,expect
settings=termios.tcgetattr(sys.stdin.fileno());settings[3]&=~termios.ECHO;termios.tcsetattr(sys.stdin.fileno(),termios.TCSANOW,settings)
print('Ready for supported Site service credential JSON (hidden stdin).',flush=True)
args=json.loads(sys.stdin.readline());token=args['token'];base=args['url'].rstrip('/');assert base=='https://council-strategy-intelligence.minshu.chatgpt.site'
app=Path(__file__).resolve().parents[1];out=app/'qa/private-trial';out.mkdir(exist_ok=True)
record={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':base,'authMode':'Supported Sites service access; no visitor identity or sign-in emulation','ownerSignedInBrowser':'NOT_TESTED_NO_OWNER_SESSION','anonymous':[],'assets':[],'browserSuites':[]}
def save(): (out/'live-validation.json').write_text(json.dumps(record,indent=2)+'\n')
for path in ['/', '/atlas.js','/sources/csoi-default-snapshot.js']:
 r=requests.get(base+path,allow_redirects=False,timeout=30,headers={'Accept':'text/html'})
 loc=urllib.parse.urlsplit(r.headers.get('Location',''))
 blocked=r.status_code in [301,302,303,307,308,401,403] and b'function mount(bridge' not in r.content
 record['anonymous'].append({'path':path,'status':r.status_code,'redirectOrigin':loc.scheme+'://'+loc.netloc if loc.netloc else None,'redirectPath':loc.path,'blocked':blocked});save();assert blocked,'Anonymous content unexpectedly accessible'
print('PASS: anonymous root and protected JS assets denied or redirected to sign-in',flush=True)
manifest=json.loads((app/'dist/deployment-assets.json').read_text())
def check(item):
 file,digest=item;r=requests.get(base+'/'+file,headers={'OAI-Sites-Authorization':'Bearer '+token},allow_redirects=False,timeout=30)
 if r.status_code in [301,302,303,307,308]:
  location=urllib.parse.urljoin(base+'/'+file,r.headers.get('Location',''))
  parsed=urllib.parse.urlsplit(location)
  print('Observed asset redirect:',file,r.status_code,parsed.netloc,parsed.path,flush=True)
  assert file=='index.html' and location==base+'/', 'UNEXPECTED_ASSET_REDIRECT'
  r=requests.get(location,headers={'OAI-Sites-Authorization':'Bearer '+token},allow_redirects=False,timeout=30)
 assert r.status_code==200,(file,r.status_code)
 actual='sha256:'+hashlib.sha256(r.content).hexdigest();assert actual==digest,file
 return {'file':file,'sha256':actual,'status':'PASS_EXACT_DEPLOYED_BYTES'}
record['assets']=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(check,manifest['files'].items()));save()
print('PASS: all 35 deployed runtime assets byte-match the canonical packaged application',flush=True)
# Platform service authentication is scoped to this exact Site. Fetch without
# following redirects, then preserve the real response; no visitor headers forged.
native_goto=Page.goto
network=[]
def guarded_goto(page,url,*pos,**kw):
 if not getattr(page,'_csoi_service_routed',False):
  def serve(route):
   request=route.request;assert request.url.startswith(base+'/');assert request.method=='GET'
   response=requests.get(request.url,headers={'OAI-Sites-Authorization':'Bearer '+token},allow_redirects=False,timeout=30)
   assert response.status_code==200,(urllib.parse.urlsplit(request.url).path,response.status_code)
   headers={k:v for k,v in response.headers.items() if k.lower() not in ['content-length','content-encoding','transfer-encoding','connection','set-cookie']}
   route.fulfill(status=response.status_code,headers=headers,body=response.content)
  page.route(base+'/**',serve);page._csoi_service_routed=True
  page.on('request',lambda r:network.append({'method':r.method,'origin':urllib.parse.urlsplit(r.url).netloc}))
 return native_goto(page,url,*pos,**kw)
Page.goto=guarded_goto
for name in ['csoi-phe-context-browser.py','e0-browser.py']:
 script=app/'qa'/name;source=script.read_text().replace('http://127.0.0.1:8877',base)
 if name.startswith('csoi'):
  source=source.replace("OUT=APP/'qa/csoi'","OUT=Path("+repr(str(out))+')')
 else: source=source.replace("OUT = Path(__file__).resolve().parent / 'e0'","OUT = Path("+repr(str(out))+')')
 exec(compile(source,str(script),'exec'),{'__file__':str(script),'__name__':'__main__'})
 record['browserSuites'].append({'script':name,'status':'PASS_ON_DEPLOYED_SITE_WITH_SERVICE_AUTH'});save()
record['network']={'requests':len(network),'mutationRequests':[r for r in network if r['method'] not in ['GET','HEAD']],'externalOrigins':sorted(set(r['origin'] for r in network if r['origin'] and r['origin']!=urllib.parse.urlsplit(base).netloc))}
assert not record['network']['mutationRequests'];assert not record['network']['externalOrigins']
record['status']='PASS';save();print('PASS: live PHE/source/review/calendar/export/import/withdrawal plus route-first layout, explicit IndexedDB save/load and stale-tab conflict. Owner-interactive sign-in remains untested.',flush=True)
