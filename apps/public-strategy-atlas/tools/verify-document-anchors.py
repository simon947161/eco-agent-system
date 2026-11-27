"""Independently check temporary original bytes and research page anchors.

This is not licence, current-law, geographic or official admission verification.
"""
import argparse,hashlib,json,pathlib
import pypdf

def verify(original,manifest):
    if manifest.get('format')!='csoi-document-research-anchors-1':raise ValueError('ANCHOR_FORMAT')
    body=pathlib.Path(original).read_bytes()
    if len(body)!=manifest['byteLength'] or 'sha256:'+hashlib.sha256(body).hexdigest()!=manifest['rawDigest']:raise ValueError('ORIGINAL_BYTE_MISMATCH')
    if manifest['parserVersion']!='pypdf-'+pypdf.__version__+'-layout-whitespace-1':raise ValueError('PARSER_VERSION_REQUIRES_REVIEW')
    reader=pypdf.PdfReader(original)
    if len(reader.pages)!=manifest['totalPages']:raise ValueError('PAGE_COUNT_MISMATCH')
    checked=[]
    for anchor in manifest['anchors']:
        page=anchor['pdfPage']
        if not isinstance(page,int) or page<1 or page>len(reader.pages):raise ValueError('ANCHOR_PAGE_BOUNDS')
        text=' '.join((reader.pages[page-1].extract_text(extraction_mode='layout') or '').split())
        digest='sha256:'+hashlib.sha256(text.encode()).hexdigest()
        if digest!=anchor['normalizedPageDigest']:raise ValueError('PAGE_ANCHOR_DIGEST_MISMATCH:'+anchor['id'])
        if any(token.casefold() not in text.casefold() for token in anchor['requiredTokens']):raise ValueError('PAGE_ANCHOR_TOKEN_MISMATCH:'+anchor['id'])
        checked.append({'id':anchor['id'],'pdfPage':page,'normalizedPageDigest':digest,'status':'PASS_TESTED_HERE'})
    return {'format':'csoi-document-research-anchor-result-1','sourceId':manifest['sourceId'],'rawDigest':manifest['rawDigest'],'byteLength':len(body),'totalPages':len(reader.pages),'anchors':checked,'status':'PASS_TESTED_HERE','formalSourceExtraction':'NOT_GRANTED','currentVersion':'UNKNOWN','reuseRights':'UNKNOWN','legalApplicability':'UNKNOWN','officialAdmission':'PENDING'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('pdf');parser.add_argument('manifest');parser.add_argument('--out');args=parser.parse_args()
    result=verify(args.pdf,json.loads(pathlib.Path(args.manifest).read_text()))
    text=json.dumps(result,indent=2)+'\n'
    if args.out:pathlib.Path(args.out).write_text(text)
    print(text,end='')
