"""Rebuild the small research manifest from separately obtained official originals.
Usage: python tools/verify-plan-editions.py DIRECTORY.html DP.pdf OP.pdf [--write]
No original PDF, source table text, or page image is distributed.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import urljoin
import fitz

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'sources/plan-editions-20261128.json'
DIRECTORY = 'https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting'
SOURCE_PATH = '/files/assets/public/v/{}/council/ipr/20262027/{}'
SPECS = {
    'dp': ('2.5',100,61,'7f7bcef8a1950021300cc52b283f59944ee5e72925e6b60d93c15c1428b60f66',
           SOURCE_PATH.format(7,'adopted-dp-2025-2029-2026-revision-v2.5-20261106_adopted-org-chart-update.pdf')),
    'op': ('1.5',141,68,'61d290c41a52ea87f664f57453417367f5d3f0f4dcd8296fb95f29dacc8c0b60',
           SOURCE_PATH.format(6,'adopted-op-2026-2027-v1.5-20261106_-org-str-update-w-revpol.pdf'))
}
def digest(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()
def normal(text):
    return ' '.join(unicodedata.normalize('NFKC',text).split())
def checked(ok, message):
    if not ok:
        raise ValueError(message)
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = set()
    def handle_starttag(self, tag, attrs):
        if tag == 'a' and dict(attrs).get('href'):
            self.urls.add(urljoin(DIRECTORY,dict(attrs)['href']))

def observe(family,path,links):
    version,count,page_number,raw,href = SPECS[family]
    pdf = path.read_bytes()
    url = urljoin(DIRECTORY,href)
    checked(digest(pdf)=='sha256:'+raw and url in links, family+' original or directory mismatch')
    with fitz.open(stream=pdf,filetype='pdf') as doc:
        checked(len(doc)==count,'page denominator changed')
        versions=normal(doc[2].get_text())
        checked(version+' 03/11/2026' in versions and 'working draft' in versions,'version / draft conflict missing')
        page=doc[page_number-1]
        is_dp=family=='dp'
        spans = ({'csp':(37,70),'project':(72,181),'purpose':(182,388),'budget':(388,435),'delivery':(438,558)}
                 if is_dp else {'project':(36,203),'purpose':(205,401),'budget':(404,464),'resources':(465,548),'csp':(549,629),'otherPlans':(630,713),'start':(714,759),'end':(760,805)})
        top,bottom=(429,481) if is_dp else (352,404)
        cells={}
        proof=[]
        for name,(left,right) in spans.items():
            box=[left,top,right,bottom]
            cells[name]=normal(page.get_text(clip=fitz.Rect(box)))
            proof.append({'field':name,'bbox':box,'digest':digest(cells[name].encode())})
        checked(cells['project'].lower()=='nimmitabel strategic water management plan' and cells['csp']=='8.2' and cells['budget']=='$150,000' and '440/25' in cells['purpose'],'row / column mismatch')
        checked(all(term in cells['purpose'].lower() for term in ['drinking water quality','recreational access']), 'missing planning conditions')
        header=normal(page.get_text(clip=fitz.Rect(36,30,page.rect.width-30,99 if is_dp else 81)))
        checked(('Budget for the years identified' if is_dp else 'Annual Budget') in header,'fiscal column header mismatch')
        if is_dp:
            tick=page.get_text(clip=fitz.Rect(475,top,502,bottom)).strip()
            checked(tick=='\uf00c' and cells['delivery']==tick,'delivery tick misplaced')
        else:
            checked([cells[k] for k in ['resources','start','end']]==['Internal/External','2026','2027'],'OP schedule/resources mismatch')
        return {'family':family.upper(),'url':url,'rawDigest':digest(pdf),'byteLength':len(pdf),'pages':count,'version':version,'editionDate':'2026-11-03',
                'retrievedAt':('2026-11-27T21:42:10.246Z' if is_dp else '2026-11-27T21:44:46.269Z'),
                'recordPage':page_number,'versionPageDigest':digest(normal(doc[2].get_text()).encode()),
                'rowPageDigest':digest(normal(page.get_text()).encode()),'rowBox':[36,top,round(page.rect.width)-35,bottom],
                'headerDigest':digest(header.encode()),'cells':proof,'aud':int(re.sub(r'[^0-9]','',cells['budget'])),'csp':cells['csp'],
                'resolution':'440/25','budgetBasis':'MULTIYEAR_PROGRAM' if is_dp else 'ANNUAL_PLAN'}

def main():
    ap=argparse.ArgumentParser()
    for name in ['directory','dp','op']:
        ap.add_argument(name,type=Path)
    ap.add_argument('--write',action='store_true')
    args=ap.parse_args()
    directory=args.directory.read_bytes()
    links=Links()
    links.feed(directory.decode('utf8'))
    result={'format':'atlas-plan-edition-review-1','directoryUrl':DIRECTORY,'directoryDigest':digest(directory),
            'observedAt':'2026-11-27T21:49:00.000Z','parser':'pymupdf-'+fitz.VersionBind+'-nfkc-whitespace-clip-v1',
            'editions':[observe(key,getattr(args,key),links.urls) for key in SPECS]}
    if args.write:
        MANIFEST.write_text(json.dumps(result,indent=2)+'\n')
    else:
        checked(json.loads(MANIFEST.read_text())==result,'edition manifest differs from original')
    print('PASS two PDF byte receipts, directory links, edition conflicts, project and budget columns, water conditions, CSP 8.2 and resolution 440/25')
if __name__=='__main__':
    main()
