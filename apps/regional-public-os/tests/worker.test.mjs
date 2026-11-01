import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createWorker} from '../worker/handler.mjs';
const root=new URL('../',import.meta.url);
const index=await readFile(new URL('data/index.json',root),'utf8');
const manifest=JSON.parse(await readFile(new URL('data/manifest.json',root),'utf8'));
const shards={};
for(const s of JSON.parse(index).shards) shards[s.file]=await readFile(new URL('data/'+s.file,root),'utf8');
const bundle={index,indexSha256:manifest.index_sha256,shards,html:'test page',javascript:'test script',release:{adapter:'test'}};
const request=path=>new Request('https://private.example'+path);
const json=async(worker,path)=>{const r=await worker.fetch(request(path));return {status:r.status,body:await r.json()};};
test('February 2026 is precisely the 28 unchanged source records',async()=>{
 const {status,body}=await json(createWorker(bundle),'/api/streamflow?start=2026-02-01&end=2026-02-28');
 assert.equal(status,200);assert.equal(body.rows.length,28);
 assert.deepEqual(body.rows,JSON.parse(shards['2026.json']).filter(r=>r.date>='2026-02-01'));
 assert.ok(body.rows.some(r=>r.quality==='E'));assert.equal(body.coverage_end,'2026-02-28');
 assert.equal(body.source_version,'September, 2026');assert.equal(body.automatic_updates,false);
 assert.equal(body.status,'HISTORICAL_STALE_FOR_CURRENT_USE');assert.equal(body.source_sha256,manifest.source_sha256);
 assert.ok(body.receipt.receipt_id);assert.ok(body.passport.passport_id);assert.ok(body.licence.endsWith('/by/3.0/au/'));
});
test('overlarge, duplicate, malformed and reversed date windows are rejected',async()=>{
 for(const query of ['start=1964-03-01&end=2026-02-28','start=2026-02-30','start=2026-02-05&end=2026-02-01','start=2026-02-01&start=2026-02-02','other=1'])
  assert.equal((await json(createWorker(bundle),'/api/streamflow?'+query)).status,400);
});
test('source ends in February; missing interval is explicit, no fabricated zeroes',async()=>{
 const {body}=await json(createWorker(bundle),'/api/streamflow?start=2026-03-01&end=2026-03-28');
 assert.equal(body.status,'NO_DATA_IN_SELECTED_INTERVAL');assert.equal(body.rows.length,0);assert.equal(body.selected_absent_dates,28);
});
test('corrupt index is rejected before data or provenance is returned',async()=>{
 const {status,body}=await json(createWorker({...bundle,index:index+' '}),'/api/release');
 assert.equal(status,503);assert.equal(body.error,'SNAPSHOT_INTEGRITY_FAILURE');
});
test('modified and missing selected shards fail closed',async()=>{
 for(const bad of ['[]',undefined]){
 const {status,body}=await json(createWorker({...bundle,shards:{...shards,'2026.json':bad}}),'/api/streamflow');
 assert.equal(status,503);assert.deepEqual(body.rows,[]);}
});
test('read-only and no direct raw-shard path',async()=>{
 const worker=createWorker(bundle);
 assert.equal((await worker.fetch(new Request('https://private.example/api/streamflow',{method:'POST'}))).status,405);
 assert.equal((await json(worker,'/data/2026.json')).status,404);
});
test('private responses must not be stored in public caches',async()=>{
 const r=await createWorker(bundle).fetch(request('/api/streamflow'));
 assert.equal(r.headers.get('Cache-Control'),'private, no-store');
 assert.equal(r.headers.get('Access-Control-Allow-Origin'),null);
});
test('separate release index/data hashes identify the full snapshot',async()=>{
 const {body}=await json(createWorker(bundle),'/api/release');
 assert.equal(body.records,22645);assert.equal(body.index_sha256,manifest.index_sha256);
 assert.equal(body.data_package_sha256,manifest.data_package_sha256);
});
