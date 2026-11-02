const assert=require('node:assert/strict');
const d=require('./atlas-data.js'),m=require('./atlas-model.js');
(async()=>{
 const cryptoNode=require('node:crypto');
 for(const size of [0,1,3,55,56,63,64,65,127,128,1000,100000]){const bytes=cryptoNode.randomBytes(size);assert.equal(m.sha256(bytes),cryptoNode.createHash('sha256').update(bytes).digest('hex'));}
 assert.deepEqual(m.validate(d),[]);
 assert(await m.verifyEvents(d.events));
 assert.equal(await m.digest(new Uint8Array(require('node:fs').readFileSync(require('node:path').join(__dirname,'qa/synthetic-source.txt')))),d.contentBlocks[0].digest);
 assert.equal(m.applicability(d.assertions[0],d.revisions[0],{date:'2026-99-99',region:'SYNTHETIC_REGION'}),'UNKNOWN');
 assert.equal(m.paths(d,'csp','water').length,2);
 assert.equal(m.paths(d,'lsps','scope').length,2);
 assert.equal(m.paths(d,'csp','candidate').length,0);
 assert.equal(m.paths(d,'csp','candidate',{includeCandidates:true}).length,1);
 const bad=structuredClone(d);bad.assertions[0].status='EXPLICIT_OFFICIAL';assert(m.validate(bad).some(x=>x.startsWith('OFFICIAL_WITHOUT_EVIDENCE')));
 bad.assertions[1].to='missing';assert(m.validate(bad).some(x=>x.startsWith('MISSING_TARGET')));
 assert.equal(m.applicability(d.assertions[0],d.revisions[0],{date:'2025-01-01',region:'SYNTHETIC_REGION'}),'VERSION_OR_SCOPE_CONFLICT');
 assert.equal(m.applicability(d.assertions[0],d.revisions[0],{date:'2026-06-01',region:'OTHER'}),'VERSION_OR_SCOPE_CONFLICT');
 assert.equal(m.applicability(d.assertions[0],d.revisions[0],{}),'UNKNOWN');
 assert.equal(await m.objectDigest({b:2,a:1}),await m.objectDigest({a:1,b:2}));
 assert.notEqual(await m.digest(new Uint8Array([1])),await m.digest(new Uint8Array([2])));
 const event={id:'demo-add',type:'ADD',objectId:'e1',actor:'synthetic-reviewer',reason:'fixture only',observedAt:'2026-10-29T00:00:00Z'};
 const first=await m.appendEvent([],event);const second=await m.appendEvent(first,{...event,id:'demo-retract',type:'RETRACT',reason:'synthetic counterevidence'});
 assert.equal(first.length,1);assert(await m.verifyEvents(second));
 const tampered=structuredClone(second);tampered[0].reason='rewritten';assert.equal(await m.verifyEvents(tampered),false);
 await assert.rejects(()=>m.appendEvent(first,event),/DUPLICATE_EVENT/);
 assert.deepEqual(m.validate(null),['DATASET_REQUIRED']);
 const nullRecord=structuredClone(d);nullRecord.sources[0]=null;assert(m.validate(nullRecord).includes('OBJECT_REQUIRED:sources'));
 const cases=[
  ['unsafe URL',x=>x.sources[0].url='javascript:alert(1)','UNSAFE_SOURCE_URL'],
  ['broken source revision',x=>x.sources[0].revisionId='absent','SOURCE_REVISION'],
  ['digest mismatch',x=>x.revisions[0].rawDigest='sha256:'+'0'.repeat(64),'REVISION_SOURCE'],
  ['invalid calendar',x=>x.revisions[0].validFrom='2026-02-30','REVISION_SCOPE'],
  ['out of scope assertion',x=>x.assertions[0].region='OTHER','ASSERTION_SCOPE'],
  ['broken support',x=>x.assertions[0].evidenceRefs=[{sourceId:'absent',blockId:'absent',revisionId:'synthetic-v1',locator:'p1'}],'BROKEN_EVIDENCE_REF'],
  ['broken counterevidence',x=>x.assertions[0].counterevidenceRefs=[{}],'BROKEN_EVIDENCE_REF'],
  ['hypothesis reference',x=>x.hypotheses[0].assertionIds=['absent'],'INVALID_HYPOTHESIS'],
  ['missing falsifier',x=>x.hypotheses[0].counterevidence=[],'INVALID_HYPOTHESIS'],
  ['duplicate edge',x=>x.edges.push(x.edges[0]),'DUPLICATE_OR_MISSING_ID']
 ];
 for(const [name,mutate,code] of cases){const copy=structuredClone(d);mutate(copy);assert(m.validate(copy).some(i=>i.startsWith(code)),name);}
 const audit=await m.auditSnapshot(d);assert.equal(audit.historyValid,true);assert.deepEqual(audit.issues,[]);
 const altered=structuredClone(d);altered.nodes[0].label='changed';assert.notEqual((await m.auditSnapshot(altered)).datasetDigest,audit.datasetDigest);
 const discovery=m.discover(d);assert.equal(discovery[0].paths.length,2);assert.equal(discovery[0].conclusion,'REQUIRES_REVIEW');assert(discovery[0].counterevidence.length);
 console.log('PASS: 10 additional admission rejection cases; snapshot tamper; discovery explanations and falsifier');
 console.log('PASS: schema, multipath, candidate exclusion, false official promotion, missing target, time/region rejection, unknown context, canonical digest, byte tamper, append/retract, history tamper, duplicate event');
})().catch(e=>{console.error(e);process.exitCode=1});
