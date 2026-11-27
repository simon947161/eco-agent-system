const assert=require('node:assert/strict');
const B=require('./csoi-boot.js'), I=require('./atlas-intake.js'), E=require('./atlas-execution.js');
const P=require('./atlas-plan-comparison.js');
const prior=require('./sources/csoi-default-snapshot.js').snapshot.dataset;
const delta=require('./sources/plan-edition-suffix.js');
const query={left:'csoi:knowledge:dp2026:november:nimmitabel-water',right:'csoi:knowledge:op2026:november:nimmitabel-water',asOf:'2026-11-28',locality:'Nimmitabel'};
async function test() {
 const data=await B.appendEditionSuffix(prior,delta);
 const report=await P.compare(data,query);
 assert.equal(report.status,'SUPPORTED_RESEARCH_CANDIDATE');
 assert.equal(report.officialRelationship,'PENDING');
 assert.deepEqual(report.sides.map(s=>s.budget[0].amount),[150000,150000]);
 assert.deepEqual(report.sides.map(s=>s.budget[0].basis),['MULTIYEAR_PROGRAM','ANNUAL_PLAN']);
 assert.equal(report.budgetTreatment,'KEEP_SEPARATE_NO_ADDITION');
 assert.equal(report.actualOutcome,'UNKNOWN');
 const work=E.workBreakdown(data,'dp');
 assert(work.rows.some(r=>r.id===query.left+':budget'&&r.depth===3&&r.executionState==='UNKNOWN'));
 assert(await P.verify(data,report));
 assert(!await P.verify(data,{...report,actualSpend:0}));
 for(const change of [{locality:'Cooma'},{asOf:'2026-09-01'},{asOf:'2027-07-01'}]) {
  const other=await P.compare(data,{...query,...change});
  assert.equal(other.status,'REJECTED_CANDIDATE');
 }
 await assert.rejects(P.compare(prior,query),/PRINTED_PROJECT_REQUIRED/);
 await assert.rejects(P.compare(data,{...query,asOf:'2026-11-31'}),/CONTEXT/);
 const oldCatalogue=data.domain.sourceCatalogue;
 data.domain.sourceCatalogue=await I.correctStage(oldCatalogue,report.sides[0].source.id,'SOURCE_RETRIEVED',{actor:'QA',at:'2026-11-28T00:00:00Z',reason:'Isolated withdrawal test'});
 const rejected=await P.compare(data,query);
 assert.equal(rejected.status,'REJECTED_CANDIDATE');
 assert(rejected.sides[0].invalidations.includes('DEPENDENCY_SOURCE_BYTES_NOT_CURRENT'));
 assert(!await P.verify(data,report));
 assert.equal(E.applicability(data.domain.entities.find(r=>r.id===query.left),{date:'2026-11-20',region:report.sides[0].region}).status,'UNKNOWN');
 console.log('PASS separate budgets and actuals, common resolution and printed CSP, locality/date/withdrawal rejection, historic replay and legal effective time UNKNOWN');
}
test().catch(e=>{console.error(e);process.exitCode=1;});
