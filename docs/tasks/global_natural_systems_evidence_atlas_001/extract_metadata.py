"""Extract factual identifiers and published score labels; never execute source HTML.

Author-only reconstruction from the ignored, once-acquired raw snapshots.
Offline users use the committed factual extracts. No network or inference of scores.
"""
import hashlib
import json
import re
from html import unescape
from html.parser import HTMLParser
from pathlib import Path

T = Path(__file__).resolve().parent
ROOT = T.parents[2]

class M49Table(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = self.cell = False
        self.rows, self.row, self.parts = [], [], []

    def handle_starttag(self, tag, attrs):
        if tag == 'table' and dict(attrs).get('id') == 'downloadTableEN':
            self.active = True
        if not self.active:
            return
        if tag == 'tr': self.row = []
        if tag in ('td', 'th'): self.cell, self.parts = True, []

    def handle_data(self, data):
        if self.active and self.cell: self.parts.append(data)

    def handle_endtag(self, tag):
        if not self.active: return
        if tag in ('td', 'th'):
            self.row.append(' '.join(''.join(self.parts).split()))
            self.cell = False
        if tag == 'tr' and self.row: self.rows.append(self.row)
        if tag == 'table': self.active = False

def extract():
    receipts = {r['id']: r for r in json.loads((T/'evidence/acquisition.json').read_text())}
    raw = {}
    for name in ('m49', 'scorecard', 'ndc'):
        b = (ROOT/f'runtime_data/global_natural_atlas_metadata/{name}.html').read_bytes()
        if hashlib.sha256(b).hexdigest() != receipts[name]['sha256']:
            raise ValueError('RAW_HASH_MISMATCH:'+name)
        raw[name] = b.decode('utf-8-sig')
    parser = M49Table()
    parser.feed(raw['m49'])
    assert parser.rows[0][9] == 'M49 Code'
    assert all(len(row) == 15 for row in parser.rows)
    facts = [dict(zip(parser.rows[0], row)) for row in parser.rows[1:]]
    assert len({r['M49 Code'] for r in facts}) == len(facts) > 200
    css = dict(re.findall(r'\.cmsmasters_toggle_wrap\.(\w+) \.cmsmasters_toggle_title a::after\s*\{\s*content:\s*"(\d+)%";', raw['scorecard']))
    cards = re.findall(r'<div class="cmsmasters_toggle_wrap ([^"]+)" data-tags="([^"]+)">\s*<div class="cmsmasters_toggle_title">.*?<a href="#">(.*?)</a>', raw['scorecard'], re.S)
    score_facts = []
    for classes, tags, name in cards:
        values = [css[c] for c in classes.split() if c in css]
        assert len(values) == 1
        score_facts.append({'name':unescape(name), 'published_percent_label':int(values[0]),
                            'css_class':classes, 'category':tags.replace('all ', ''),
                            'locator':'country toggle title + inline CSS ::after',
                            'basis':'PUBLISHED_CSS_LABEL_NOT_RECALCULATED'})
    assert len({r['name'] for r in score_facts}) == len(score_facts) > 10
    metadata = {k:re.search('"'+k+'":"([^"]+)"',raw['scorecard']).group(1) for k in ('datePublished','dateModified')}
    outputs = {'m49-facts.json':{'source_sha256':receipts['m49']['sha256'], 'table_id':'downloadTableEN','rows':facts},
               'scorecard-facts.json':{'source_sha256':receipts['scorecard']['sha256'], **metadata, 'records':score_facts},
               'content-checks.json':{'m49':'EXPECTED_ENGLISH_TABLE','scorecard':'CSS_AND_COUNTRY_CARDS_VERIFIED',
                   'ndc':'BLOCKED_CHALLENGE_HTML' if '_Incapsula_Resource' in raw['ndc'] else 'UNRECOGNIZED_PAYLOAD',
                   'raw_html_redistributed':False}}
    for name, output in outputs.items():
        (T/'evidence'/name).write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'m49_count':len(facts),'scorecard':score_facts},ensure_ascii=False))

if __name__ == '__main__': extract()
