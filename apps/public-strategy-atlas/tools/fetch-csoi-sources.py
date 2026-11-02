"""Bounded official-public source observation. No TLS/proxy bypass or automatic admission.

Writes original bytes only to the requested temporary directory and a small metadata
receipt there. Review source rights before committing excerpts or extraction output.
Usage: python tools/fetch-csoi-sources.py --out /tmp/csoi-sources
Optional --documents retrieves selected official Council PDF links (50 MiB/file).
"""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import html.parser
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

SEEDS = [
 ('smrc-ipr', 'STRATEGY_DIRECTORY', 'https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting'),
 ('smrc-csp-summary', 'CSP', 'https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/csp/csp-2035-plan-on-a-page.pdf'),
 ('smrc-landuse', 'SPATIAL_PLANNING', 'https://www.snowymonaro.nsw.gov.au/Building-and-Planning/Strategic-Planning/Land-Use-Planning'),
 ('smrc-ltw', 'LTW', 'https://www.snowymonaro.nsw.gov.au/Environment-Waste-and-Weeds/Environmental-and-Public-Health/Public-Health/Liquid-Trade-Waste'),
 ('smrc-backflow', 'BACKFLOW', 'https://www.snowymonaro.nsw.gov.au/Water-and-Wastewater/Water-Supply/Backflow-Prevention-Program'),
 ('nsw-ltw', 'LTW', 'https://www.water.nsw.gov.au/our-work/local-water-utilities/liquid-trade-waste'),
 ('nsw-food-partnership', 'FOOD', 'https://www.foodauthority.nsw.gov.au/retail/food-regulation-partnership'),
 ('nsw-health-act', 'PUBLIC_HEALTH', 'https://www.health.nsw.gov.au/phact/pages/default.aspx'),
 ('nsw-health-reporting', 'PUBLIC_HEALTH_REPORTING', 'https://www.health.nsw.gov.au/environment/Pages/local-government-authority-reporting.aspx'),
 ('nsw-health-pools', 'POOLS_SPAS', 'https://www.health.nsw.gov.au/environment/water/Pages/swimming-pools.aspx'),
 ('nsw-health-legionella', 'COOLING_WARM_WATER', 'https://www.health.nsw.gov.au/environment/legionellacontrol/Pages/default.aspx'),
 ('nsw-health-skin', 'SKIN_PENETRATION', 'https://www.health.nsw.gov.au/environment/skinpenetration/Pages/default.aspx'),
 ('nsw-olg-ossm', 'OSSM', 'https://www.olg.nsw.gov.au/councils/council-certification-and-compliance/on-site-sewage-management/'),
]
HOSTS = frozenset(urllib.parse.urlsplit(url).hostname for _, _, url in SEEDS)
MAX_BYTES = 50 * 1024 * 1024

class SameHostRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urllib.parse.urlsplit(newurl)
        initial = urllib.parse.urlsplit(req.full_url)
        if target.scheme != 'https' or target.hostname != initial.hostname or target.username or target.password:
            raise urllib.error.URLError('REDIRECT_REQUIRES_REVIEW: ' + newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.capture_title = False
        self.title = []
        self.text = []
        self.links = []
        self.link = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style', 'noscript'):
            self.hidden += 1
        if tag == 'title':
            self.capture_title = True
        if tag == 'a':
            self.link = {'href': attrs.get('href', ''), 'text': ''}
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.hidden = max(0, self.hidden - 1)
        if tag == 'title':
            self.capture_title = False
        if tag == 'a' and self.link:
            self.links.append(self.link)
            self.link = None
    def handle_data(self, text):
        if self.capture_title:
            self.title.append(text)
        if not self.hidden and text.strip():
            self.text.append(text.strip())
        if self.link:
            self.link['text'] += text

def observe(spec, out):
    source_id, family, url = spec
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname not in HOSTS or parsed.username or parsed.password:
        raise ValueError('OFFICIAL_PUBLIC_HOST_REQUIRED')
    result = {'id': source_id, 'family': family, 'url': url, 'retrievedAt': dt.datetime.now(dt.timezone.utc).isoformat(), 'classification': 'PUBLIC', 'rights': 'UNKNOWN', 'currentVersion': 'UNKNOWN', 'legalApplicability': 'UNKNOWN', 'admission': 'PENDING', 'geography': 'NSW, Australia; local applicability requires review'}
    try:
        opener = urllib.request.build_opener(SameHostRedirect())
        request = urllib.request.Request(url, headers={'User-Agent': 'ClimateOS-Public-Research/1.7'})
        with opener.open(request, timeout=45) as response:
            body = response.read(MAX_BYTES + 1)
            if len(body) > MAX_BYTES:
                raise ValueError('SOURCE_SIZE_BOUND')
            result.update(httpStatus=response.status, resolvedUrl=response.url, mediaType=response.headers.get_content_type(), byteLength=len(body), rawDigest='sha256:' + hashlib.sha256(body).hexdigest())
            suffix = '.pdf' if body.startswith(b'%PDF') else '.html'
            (out / (source_id + suffix)).write_bytes(body)
            if suffix == '.html':
                page = Page()
                page.feed(body.decode('utf-8', errors='replace'))
                result['title'] = ' '.join(' '.join(page.title).split())
                links = []
                for link in page.links:
                    absolute = urllib.parse.urljoin(response.url, link['href'])
                    target = urllib.parse.urlsplit(absolute)
                    if target.scheme == 'https' and target.hostname == parsed.hostname and not target.username and not target.password and '.pdf' in target.path.lower():
                        entry = {'url': absolute, 'title': ' '.join(link['text'].split())[:240]}
                        if entry not in links:
                            links.append(entry)
                result['documentLinks'] = links[:150]
                # Text is for local research only and must not be committed wholesale.
                (out / (source_id + '.txt')).write_text('\n'.join(page.text))
            result['access'] = 'AVAILABLE'
    except urllib.error.HTTPError as error:
        result.update(httpStatus=error.code, access='UNAVAILABLE', failure='HTTP_' + str(error.code))
    except (urllib.error.URLError, ValueError, TimeoutError, OSError) as error:
        result.update(access='UNAVAILABLE', failure=str(error)[:300])
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--documents', action='store_true')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        observations = list(pool.map(lambda seed: observe(seed, args.out), SEEDS))
    if args.documents:
        candidates = []
        patterns = [r'csp.*2035.*(endorsed|adopted)', r'delivery.*2025.*2029', r'operational.*2026.*2027', r'resourcing.*strategy', r'financial.*plan', r'annual.*report', r'local.*strategic.*planning.*statement']
        for pattern in patterns:
            found = next((link for obs in observations if obs['id'] in ('smrc-ipr', 'smrc-landuse') for link in obs.get('documentLinks', []) if re.search(pattern, link['url'] + ' ' + link['title'], re.I)), None)
            if found and found['url'] not in [item[2] for item in candidates]:
                candidates.append(('smrc-doc-' + str(len(candidates) + 1), 'STRATEGIC_DOCUMENT', found['url']))
        # 4-way concurrency and at most 7 x 50 MiB protects bounded local intake.
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            observations.extend(pool.map(lambda seed: observe(seed, args.out), candidates))
    receipt = {'format': 'csoi-public-source-observations-1', 'observedAt': dt.datetime.now(dt.timezone.utc).isoformat(), 'policy': 'Inherited proxy and TLS verification; official-public hosts; same-host HTTPS redirects only; no automatic admission', 'originalBytesCommitted': False, 'observations': observations}
    (args.out / 'observations.json').write_text(json.dumps(receipt, indent=2) + '\n')
    for obs in observations:
        print(obs['id'], obs.get('httpStatus'), obs.get('byteLength'), obs.get('access'), obs.get('failure', ''))

if __name__ == '__main__':
    main()
