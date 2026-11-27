const assert = require('node:assert/strict');
const M = require('./atlas-model.js');
const B = require('./csoi-boot.js');
const I = require('./atlas-intake.js');
const K = require('./csoi-knowledge.js');
const P = require('./csoi-paths.js');
const E = require('./atlas-execution.js');
const previous = require('./sources/csoi-default-snapshot.js').snapshot.dataset;
const delta = require('./sources/plan-edition-suffix.js');
const review = require('./sources/plan-editions-20261128.json');
async function test() {
 const d = await B.appendEditionSuffix(previous,delta);
 assert.equal(d.contentItems.length,127);
 assert.equal(d.domain.revisions.length, previous.domain.revisions.length+20);
 assert.equal(d.domain.assertions.length, previous.domain.assertions.length);
 assert.equal(d.domain.sourceCatalogue.sources.length, previous.domain.sourceCatalogue.sources.length+2);
 for(const doc of review.editions) {
  const family=doc.family.toLowerCase(), sourceId='csoi:smrc-'+family+'-2026:20261128';
  const oldId='csoi:smrc-'+family+'-2026:20261030', projectId='csoi:knowledge:'+family+'2026:november:nimmitabel-water';
  const source=d.domain.sourceCatalogue.sources.find(s=>s.id===sourceId);
  assert.deepEqual(source.lineage.supersedes,[oldId]);
  assert.equal(source.rawDigest,doc.rawDigest);
  assert.equal(I.sourceStatus(d.domain.sourceCatalogue,sourceId).stage,'RAW_BYTES_VERIFIED');
  const budget=M.domainIndex(d).get(projectId+':budget');
  assert.equal(budget.data.value,150000);
  assert.equal(budget.data.unit,'AUD');
  assert.equal(K.parents(d,budget.id).length,3);
  assert.equal(budget.data.csoiRecord.data.publicKnowledge.facts.actualSpend,'UNKNOWN');
  const goal=P.inputNeighbours(d,projectId).rows.find(x=>x.type==='EXPLICIT_DOCUMENT_REFERENCE');
  assert.equal(goal.id,'csoi:knowledge:csp2035:strategy:8.2');
  assert.equal(goal.pinStatus,'HEAD_MATCH');
  await assert.rejects(E.derive(d,{formula:'UNIT_CONVERSION',inputIds:[budget.id],outputUnit:'AUD'}),/UNADMITTED_INPUTS/);
 }
 const staged={...previous,domain:{...previous.domain,sourceCatalogue:d.domain.sourceCatalogue}};
 const initialDigest=await M.objectDigest(staged);
 const first=delta.revisions[0].record;
 const options={record:first.data.csoiRecord,kind:first.kind,label:first.label,stationId:first.stationId,reason:'Isolated batch rollback check'};
 await assert.rejects(M.registerResearchBatch(staged,[options,options],entry=>entry),/REGISTRATION_INVALID/);
 assert.equal(await M.objectDigest(staged),initialDigest);
 const stored=await M.exportSnapshot(d);
 assert(await M.verifySnapshot(JSON.parse(JSON.stringify(stored)),delta.datasetDigest));
 const changed=structuredClone(delta);
 changed.revisions.at(-1).record.label+=' altered';
 await assert.rejects(B.appendEditionSuffix(previous,changed),/SUFFIX_INVALID/);
 await assert.rejects(B.appendEditionSuffix(d,delta),/BASE_MISMATCH/);
 assert.equal(await M.objectDigest(previous),delta.baseDigest);
 console.log('PASS two distinct editions, twenty immutable records, duplicate append/corruption rejected, both prior editions and all 127 legacy records preserved, public budget arithmetic rejected');
}
test().catch(e=>{console.error(e);process.exitCode=1;});
