"""Recompute per-page text and thumbnail fingerprints from twelve registered original PDFs."""
import argparse
import hashlib
import json
import subprocess
import unicodedata
from pathlib import Path

import fitz

APP = Path(__file__).resolve().parents[1]
OUT = APP / 'sources' / 'pdf-page-receipts'
ROOTS = APP / 'sources' / 'pdf-page-roots.js'
METHOD = 'pymupdf-1.26.6-nfkc-ws-gray512-v1'
EDITIONS = [
    'smrc-csp-summary', 'smrc-csp-full-2025', 'smrc-lsps-2020',
    'smrc-ltfp-2026', 'smrc-resourcing-2026', 'smrc-water-amp-2025',
    'smrc-annual-report-2025-retrieved', 'smrc-dcp-bombala-2014',
    'smrc-dcp-cooma-2014-amend4', 'smrc-dcp-snowy-2013-amend3',
]
IDS = ['csoi:' + key + ':20261030' for key in EDITIONS] + [
    'csoi:smrc-dp-2026:20261128', 'csoi:smrc-op-2026:20261128',
]

def digest(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()

def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def check_or_write(file, content, write):
    if write:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(content)
    elif file.read_text() != content:
        raise ValueError('Receipt mismatch: ' + file.name)

def index_source(source, directory):
    key = source['rawDigest'].split(':')[1]
    original = (directory / (key + '.pdf')).read_bytes()
    if digest(original) != source['rawDigest']:
        raise ValueError('Original digest mismatch: ' + source['id'])
    rows = []
    with fitz.open(stream=original, filetype='pdf') as pdf:
        for page in pdf:
            text = ' '.join(unicodedata.normalize('NFKC', page.get_text()).split())
            scale = min(1.0, 512 / max(page.rect.width, page.rect.height))
            raster = page.get_pixmap(matrix=fitz.Matrix(scale, scale), colorspace=fitz.csGRAY,
                                     alpha=False, annots=True)
            rows.append([digest(text.encode()), len(text), raster.width, raster.height, digest(raster.samples)])
    return {'method': METHOD, 'sourceId': source['id'], 'rawDigest': source['rawDigest'], 'pages': rows}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--originals', type=Path, required=True, help='Directory of <raw sha256 hex>.pdf files')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    if fitz.VersionBind != '1.26.6':
        raise ValueError('Reproduction requires PyMuPDF 1.26.6')
    script = """const old=require('./sources/csoi-default-snapshot.js').snapshot.dataset.domain.sourceCatalogue;
const sources=[...old.sources,...require('./sources/plan-edition-suffix.js').sources];
console.log(JSON.stringify(sources.map(({id,rawDigest})=>({id,rawDigest}))));"""
    sources = {s['id']: s for s in json.loads(subprocess.check_output(['node', '-e', script], cwd=APP))}
    roots = {}
    for source_id in IDS:
        item = index_source(sources[source_id], args.originals)
        data = canonical(item)
        key = item['rawDigest'][7:]
        check_or_write(OUT / (key + '.json'), data + '\n', args.write)
        roots[source_id] = {'rawDigest': item['rawDigest'], 'pageCount': len(item['pages']), 'digest': digest(data.encode())}
        print(source_id, len(item['pages']), flush=True)
    js = "(function(root){const roots=" + canonical(roots) + ";root.AtlasPdfPageRoots=roots;if(typeof module!=='undefined')module.exports=roots;})(globalThis);\n"
    check_or_write(ROOTS, js, args.write)
    print('PASS', len(roots), 'originals and', sum(r['pageCount'] for r in roots.values()), 'page fingerprints')

if __name__ == '__main__':
    main()
