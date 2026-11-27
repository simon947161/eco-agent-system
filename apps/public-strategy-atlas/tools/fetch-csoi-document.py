"""Fetch one exact registered official-public PDF lead, with bounded inherited HTTPS.

Original bytes and receipt stay under /tmp. No retries, policy changes or admission.
"""
import argparse,datetime,hashlib,json,pathlib,urllib.error,urllib.parse,urllib.request

APP=pathlib.Path(__file__).resolve().parents[1]
HOST='www.snowymonaro.nsw.gov.au'
def safe_url(url):
    p=urllib.parse.urlsplit(url)
    return p.scheme=='https' and p.hostname==HOST and not p.username and not p.password and not p.port and not p.query and not p.fragment and p.path.startswith('/files/assets/public/')

class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self):self.chain=[]
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if not safe_url(newurl) or len(self.chain)>=3:raise urllib.error.URLError('REDIRECT_REQUIRES_REVIEW')
        self.chain.append({'from':req.full_url,'to':newurl,'httpStatus':code})
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent',required=True);parser.add_argument('--match',required=True);parser.add_argument('--id',required=True)
    parser.add_argument('--out',required=True);parser.add_argument('--max-mib',type=int,default=50,choices=range(1,97))
    args=parser.parse_args();out=pathlib.Path(args.out).resolve()
    if not str(out).startswith('/tmp/') or not args.id.replace('-','').isalnum():raise SystemExit('TEMPORARY_PUBLIC_STORAGE_REQUIRED')
    source=json.loads((APP/'sources/csoi-source-observations.json').read_text())
    parent=next(o for o in source['observations'] if o['id']==args.parent and o.get('byteVerification')=='PASS_TESTED_HERE')
    leads=[lead for lead in parent.get('documentLinks',[]) if args.match in lead['url']]
    if len(leads)!=1 or not safe_url(leads[0]['url']):raise SystemExit('EXACT_REGISTERED_PUBLIC_PDF_LEAD_REQUIRED')
    lead=leads[0];out.mkdir(parents=True,exist_ok=True);handler=Redirects();limit=args.max_mib*1024*1024
    record={'id':args.id,'url':lead['url'],'title':lead['title'],'parentObservationId':parent['id'],'directoryUrl':parent['url'],'directoryDigest':parent['rawDigest'],'retrievedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rights':'UNKNOWN','currentVersion':'UNKNOWN','legalApplicability':'UNKNOWN','admission':'PENDING','originalBytesCommitted':False,'requestLimits':{'maxBytes':limit,'timeoutSeconds':45,'maximumRedirects':3},'proxy':'INHERITED','tlsVerification':True,'selectedRequestAttempts':1}
    partial=out/(args.id+'.part');target=out/(args.id+'.pdf')
    try:
        digest=hashlib.sha256();count=0
        with urllib.request.build_opener(handler).open(lead['url'],timeout=45) as response,partial.open('wb') as dest:
            if response.status!=200:raise ValueError('HTTP_NOT_200')
            if not safe_url(response.url):raise ValueError('FINAL_URL_REQUIRES_REVIEW')
            if response.headers.get('Content-Length') and int(response.headers['Content-Length'])>limit:raise ValueError('SOURCE_SIZE_BOUND')
            first=True
            while True:
                block=response.read(min(1024*1024,limit-count+1))
                if not block:break
                if first and not block.startswith(b'%PDF-'):raise ValueError('ORIGINAL_PDF_HEADER_REQUIRED')
                first=False;count+=len(block)
                if count>limit:raise ValueError('SOURCE_SIZE_BOUND')
                digest.update(block);dest.write(block)
            if not count:raise ValueError('EMPTY_ORIGINAL')
            record.update(httpStatus=response.status,resolvedUrl=response.url,mediaType=response.headers.get_content_type(),byteLength=count,rawDigest='sha256:'+digest.hexdigest(),access='AVAILABLE',byteVerification='PASS_TESTED_HERE',failureClassification=None)
        partial.replace(target);record['workspacePath']=str(target)
    except Exception as error:
        partial.unlink(missing_ok=True)
        status=error.code if isinstance(error,urllib.error.HTTPError) else None
        record.update(httpStatus=status,access='UNAVAILABLE',byteVerification='NOT_VERIFIED',error=str(error),failureClassification='ENVIRONMENT_POLICY_BLOCKED' if 'Tunnel connection failed: 403' in str(error) else 'HTTP_ACCESS_DENIED' if status==403 else 'HTTP_ERROR' if status else 'TRANSFER_OR_TRANSPORT_FAILURE')
    record['redirects']=handler.chain;record['httpExchanges']=1+len(handler.chain)
    (out/(args.id+'-receipt.json')).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record.get(k) for k in ['id','httpStatus','byteLength','rawDigest','httpExchanges','access','failureClassification','error']},indent=2))
    if record['access']!='AVAILABLE':raise SystemExit(1)

if __name__=='__main__':main()
