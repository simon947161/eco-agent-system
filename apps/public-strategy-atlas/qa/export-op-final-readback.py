"""Small actual source-bundle/cache readback, linked to the prior PDF-first semantic review."""
from pathlib import Path
import csv,datetime,hashlib,json
APP=Path(__file__).resolve().parents[1];OUT=APP/'qa/op-completion-20261102';sha=lambda b:hashlib.sha256(b).hexdigest()
def digest(v):return 'sha256:'+sha(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
raw=(APP/'sources/op-completion-review.json').read_bytes();bundle=json.loads(raw)
review=json.loads((OUT/'independent/model-readback-review.json').read_text());assert review['bundleSHA256']==sha(raw)and not review['failures']
cache_raw=(APP/'sources/csoi-default-snapshot.js').read_bytes();cache=json.loads(cache_raw.decode().split('const value=',1)[1].split(';root.CsoiDefaultSnapshot=',1)[0]);entities={e['id']:e for e in cache['snapshot']['dataset']['domain']['entities']};reviews={r['id']:r for r in review['rows']}
findings=json.loads((OUT/'independent/author-findings.json').read_text());target_ids={f['recordIds'][0]for f in findings['findings']}
rows=[];samples=[];sample_keys=set()
for node in bundle['records']:
 e=entities[node['id']];actual=e['data']['csoiRecord']['data']['publicKnowledge'];assert actual['facts']==node['facts'] and actual['anchor']==node['anchor']
 for unit in actual['facts'].get('units',[]):
  h=digest(unit);r=reviews[unit['id']];source_unit=next(u for u in node['facts']['units']if u['id']==unit['id']);assert digest(source_unit)==r['semanticUnitDigest']and r['fullStructureMatchesReviewedAuthor'];assert unit==source_unit
  rows.append({'unitId':unit['id'],'pdfPages':','.join(map(str,unit.get('pages',[unit['pdfPage']]))),'actualUnitSHA256':h.removeprefix('sha256:'),'reviewedSourceUnitSHA256':r['semanticUnitDigest'].removeprefix('sha256:'),'matchesPriorIndependentSemanticReview':True,'unitFieldsMatchBootCache':True})
  page=node['anchor']['pdfPage'];cat=unit['category'];key=(page,cat)
  if (page in [28,29,30,73,111,116,120,121,132,140]and key not in sample_keys)or unit['id']in target_ids or (29 in unit.get('pages',[])and 30 in unit.get('pages',[])):
   sample_keys.add(key);samples.append({'unitId':unit['id'],'cacheEntityId':e['id'],'cacheRevisionId':e['revisionId'],'actualFullUnitDigest':h,'page':page,'category':cat,'summary':unit['summary'],'conditions':unit['conditions'],'qualifiers':unit['qualifiers'],'facts':unit['facts'],'sourceAnchorCount':len(unit['sourceAnchors']),'sourceLocations':[{k:a[k]for k in ['field','pdfPage','bbox','normalizedTextDigest','parserVersion']if k in a}for a in unit['sourceAnchors'][:3]],'reviewedSourceUnitDigest':r['semanticUnitDigest'],'sampleOmissions':'Sample omits full source anchor text and repeated rows; full unit digest binds every original field.'})
assert len(rows)==911 and len({r['unitId']for r in rows})==911
with (OUT/'final-actual-unit-readback.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
sample_dir=OUT/'final-samples';sample_dir.mkdir(exist_ok=True);sample_index=[]
for i,sample in enumerate(samples,1):
 name=f"{i:02d}-p{sample['page']:03d}-{sample['category']}.json";body=(json.dumps(sample,ensure_ascii=False,indent=2)+'\n').encode();(sample_dir/name).write_bytes(body);sample_index.append({k:sample[k]for k in ['unitId','page','category','summary','actualFullUnitDigest','reviewedSourceUnitDigest']}|{'file':'final-samples/'+name,'bytes':len(body),'sha256':sha(body)})
expected_names={Path(x['file']).name for x in sample_index}
for old in sample_dir.glob('*.json'):
 if old.name not in expected_names:old.unlink()
receipt={'format':'op-final-source-and-boot-cache-readback-1','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_ALL_911_ACTUAL_UNITS','sourceBundle':{'file':'sources/op-completion-review.json','bytes':len(raw),'sha256':sha(raw)},'bootCache':{'file':'sources/csoi-default-snapshot.js','bytes':len(cache_raw),'sha256':sha(cache_raw)},'originalPDF':{'sha256':bundle['sourceRevision'],'pages':142},'independentPDFReview':'independent/REPORT_ZH.md','independentActualProjectionComparison':'independent/model-readback-review.json','semanticsLimit':'This readback proves byte/structure transfer of all previously independently PDF-reviewed units; hash equality alone is not semantic review. Source conflicts and unknowns are retained.','unitCount':911,'recordCount':143,'numericEncodingNote':'Source Python JSON can encode integral coordinates as1.0; JavaScript boot serialization encodes1. Both are JSON numbers. Exact facts/anchors and every unit compare structurally equal; source digest matches prior semantic review; actual cache unit digests are reported separately. Native OP tests also use JavaScript strict deep equality.','unitsWithDifferentNumberEncoding':sum(r['actualUnitSHA256']!=r['reviewedSourceUnitSHA256']for r in rows),'matrix':{'file':'final-actual-unit-readback.csv','sha256':sha((OUT/'final-actual-unit-readback.csv').read_bytes())},'samples':sample_index,'exporterImplementationNotes':['The first exporter assumed Python and JavaScript would encode integral JSON numbers identically; explicit separate digests now retain both encodings while full fields compare equal.','Finance units use pdfPage without the optional services pages array; the exporter now reads that existing schema. These were exporter assumptions, not source changes.']}
(OUT/'final-actual-readback-samples.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'matrixBytes':(OUT/'final-actual-unit-readback.csv').stat().st_size,'sampleCount':len(samples),'sampleBytes':(OUT/'final-actual-readback-samples.json').stat().st_size}))
