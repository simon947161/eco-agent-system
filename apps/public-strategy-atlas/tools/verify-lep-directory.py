"""Verify the Council's published LEP instrument and mapped-exception pointers."""
import argparse
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path

APP=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.urls.add(dict(attrs).get('href'))
def main():
    p=argparse.ArgumentParser();p.add_argument('original',type=Path);p.add_argument('access',type=Path);p.add_argument('--write',action='store_true');a=p.parse_args()
    raw=a.original.read_bytes();access=json.loads(a.access.read_text())
    digest='sha256:'+sha256(raw).hexdigest()
    if digest!=access['rawDigest']:raise ValueError('Directory edition changed')
    parser=Links();parser.urls=set();parser.feed(raw.decode())
    regions={'epi-2012-0302':'Bombala','epi-2013-0614':'Cooma-Monaro','epi-2013-0700':'Snowy River'}
    records=[]
    for ident,area in regions.items():
        matches=[r for r in access['observations'] if r['url'].endswith('/'+ident) and r['url'] in parser.urls]
        if len(matches)!=1 or matches[0]['httpStatus']!=403:raise ValueError('Current instrument access differs: '+ident)
        records.append({'id':ident,'formerArea':area,'url':matches[0]['url'],'httpStatus':403})
    mapped=[r for r in access['observations'] if r['url'] in parser.urls and 'planningportal.nsw.gov.au' in r['url']]
    if len(mapped)!=1 or mapped[0]['httpStatus']!=200 or 'catalyst precinct' not in raw.decode().lower():raise ValueError('Mapped exception directory changed')
    data={'source':access['directory'],'rawDigest':digest,'checkedOn':'2026-11-28','instruments':records,'exceptionDirectory':mapped[0]['url'],'currentLaw':'UNKNOWN','parcelApplicability':'UNKNOWN','officialAdmission':'PENDING'}
    js="(function(root){const v="+json.dumps(data,sort_keys=True,separators=(',',':'))+";root.AtlasLepDirectory=v;if(typeof module!=='undefined')module.exports=v;})(globalThis);\n"
    out=APP/'sources/lep-directory-20261128.js'
    if a.write:out.write_text(js)
    elif out.read_text()!=js:raise ValueError('Directory receipt mismatch')
    print('PASS three directory-listed former areas, recorded 403 for current instrument URLs and 200 for the Planning Portal directory; parcel and effective law remain UNKNOWN')
if __name__=='__main__':main()
