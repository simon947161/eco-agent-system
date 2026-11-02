"""Reproduce the CSP summary byte/anchor checks from a supplied public PDF.
No network call, PDF redistribution, licence inference or admission approval.
Usage: python verify-source.py PDF_PATH [RECORD_PATH]
Requires pdfplumber, available in the engineering runtime.
"""
import hashlib,json,pathlib,sys
import pdfplumber
record_path=pathlib.Path(sys.argv[2]) if len(sys.argv)>2 else pathlib.Path(__file__).with_name('sources')/'csp61-admission.json'
r=json.loads(record_path.read_text())
b=pathlib.Path(sys.argv[1]).read_bytes()
if hashlib.sha256(b).hexdigest()!=r['rawDigest'].removeprefix('sha256:'):raise SystemExit('RAW_DIGEST_MISMATCH')
with pdfplumber.open(sys.argv[1]) as pdf:
 if len(pdf.pages)!=r['anchor']['pageCount']:raise SystemExit('PAGE_COUNT_MISMATCH')
 page=pdf.pages[r['anchor']['page']-1]
 box=r['anchor']['bbox'];words=[w for w in page.extract_words() if box[0]<=w['x0']<box[2] and box[1]<=w['top']<box[3]]
 text=' '.join(w['text'] for w in words)
 if text!=r['extraction']['text']:raise SystemExit('ANCHOR_TEXT_MISMATCH')
 if 'sha256:'+hashlib.sha256(text.encode()).hexdigest()!=r['extraction']['digest']:raise SystemExit('EXTRACT_DIGEST_MISMATCH')
print('PASS: original PDF bytes, page count, bounded anchor extraction and excerpt digest. Admission/permission approval is not implied.')
