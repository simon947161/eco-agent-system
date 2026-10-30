'use strict';
const assert=require('node:assert/strict'),M=require('./atlas-model.js'),A=require('./atlas-accounting.js'),B=require('./atlas-data.js'),W=require('./csoi-work.js');
const clone=structuredClone;
let count=0;
function check(name,fn){fn();count++;console.log('PASS '+name);}
(async()=>{
 const fixture=W.syntheticFixture();
 check('service/object/type denominators separate properties, events, issues and actual outcomes',()=>{
  const c=W.coverage(fixture.items,'2026-10-30');assert.equal(c.uniqueObjects,5);assert.equal(c.uniqueProperties,2);assert.equal(c.eligible,3);assert.equal(c.planned,2);assert.equal(c.completed,1);assert.equal(c.overdue,1);assert.equal(c.unknown,1);assert.equal(c.notEligible,1);assert.equal(c.completedInspectionEvents,1);assert.equal(c.openIssues,1);assert.equal(c.coverage,1/3);assert.equal(c.byService.FOOD.unknown,1);assert.equal(c.environmentalOutcome,'UNKNOWN');assert.equal(c.compliance,'UNKNOWN');
 });
 check('duplicate denominator input deduplicates objects/events and rejects conflicting values',()=>{
  const repeated={...clone(fixture.items[0]),id:'SYN-REG-FOOD-DUPLICATE'};const c=W.coverage([...fixture.items,repeated],'2026-10-30');assert.equal(c.uniqueObjects,5);assert.equal(c.duplicateRowsRemoved,1);assert.equal(c.completedInspectionEvents,1);assert.equal(c.openIssues,1);
  repeated.eligible=false;assert.throws(()=>W.coverage([...fixture.items,repeated],'2026-10-30'),/CONFLICTING_DENOMINATOR/);
  assert.throws(()=>W.coverage([...fixture.items,clone(fixture.items[0])],'2026-10-30'),/DUPLICATE_RECORD_ID/);
 });
 check('unknown eligibility and inspection need are not false zeros or compliance',()=>{
  const empty=W.coverage([],'2026-10-30');assert.equal(empty.coverage,'UNKNOWN');const rows=clone(fixture.items);rows[0].requiredVisits='UNKNOWN';const c=W.coverage(rows,'2026-10-30');assert.equal(c.requiredInspectionEvents,'UNKNOWN');assert.equal(c.completed,0);assert.equal(c.inspectedObjects,1);assert.equal(c.unknown,1);assert.equal(c.compliance,'UNKNOWN');
 });
 check('completion, issue closure, dates and real protected objects require evidence',()=>{
  for(const classification of ['COUNCIL_PROTECTED','PERSONAL_PRIVATE','APPROVED_RELEASE'])assert.throws(()=>W.coverage([{...fixture.items[0],classification}],'2026-10-30'),/PROTECTED_INPUT_DENIED/);
  const mixed=clone(fixture.items);mixed[0].period='FY2025-26';assert.throws(()=>W.coverage(mixed,'2026-10-30'),/COUNT_SCOPE_MISMATCH/);
  const noEvidence=clone(fixture.items);delete noEvidence[0].events[0].evidenceId;assert.throws(()=>W.coverage(noEvidence,'2026-10-30'),/EXECUTION_EVIDENCE/);
  const closed=clone(fixture.items);closed[0].issues[0].state='CLOSED';assert.throws(()=>W.coverage(closed,'2026-10-30'),/CLOSURE_EVIDENCE/);
  const future=clone(fixture.items);future[0].events[0].completedAt='2027-01-01';assert.throws(()=>W.coverage(future,'2026-10-30'),/EXECUTION_EVIDENCE/);
  assert.throws(()=>W.coverage(fixture.items,'2026-02-30'),/AS_OF_DATE/);
 });
 check('hours preserve six phases and measured/estimated/assumed categories; no dollar conversion',()=>{
  const result=W.workload(fixture.tasks);assert.equal(result.totals.ESTIMATED,2.75);assert.equal(result.totals.ASSUMED,4.25);assert.equal(result.totals.MEASURED,0);assert.equal(result.actualSpend,'UNKNOWN');assert.equal(Object.keys(result.byPhase).length,6);
  const measured=clone(fixture.tasks);measured[0].phases.field.measurement='MEASURED';const m=W.workload(measured);assert.equal(m.totals.MEASURED,1);assert.equal(m.totals.ESTIMATED,1.75);
  const missing=clone(fixture.tasks);delete missing[0].phases.field;assert.equal(W.workload(missing).unknownPhases,1);
  const bad=clone(fixture.tasks);bad[0].phases.field.hours=-1;assert.throws(()=>W.workload(bad),/PHASE_HOURS/);
  assert.throws(()=>W.workload([...fixture.tasks,fixture.tasks[0]]),/DUPLICATE_TASK/);
 });
 check('resource demand needs explicit annual capacity and never creates personnel/spend claims',()=>{
  const unknown=W.resources(fixture.tasks);assert.equal(unknown.plannedFteEquivalent,'UNKNOWN');const result=W.resources(fixture.tasks,{annualProductiveHoursPerPerson:1400});assert.equal(result.plannedFteEquivalent,7/1400);assert.equal(result.vehicleHours,1.25);assert.equal(result.skills['SYN-INSPECTION-SKILL'],1);assert.equal(result.personnelHeadcount,'UNKNOWN');assert.equal(result.actualSpend,'UNKNOWN');
  assert.throws(()=>W.resources(fixture.tasks,{annualProductiveHoursPerPerson:0}),/PRODUCTIVE_CAPACITY/);const tasks=clone(fixture.tasks);tasks[0].phases.field.hours='UNKNOWN';assert.equal(W.resources(tasks,{annualProductiveHoursPerPerson:1400}).plannedFteEquivalent,'UNKNOWN');
 });
 const dataset=await M.migrateDataset(B,A.cases);
 check('three ledgers reuse existing identities and reverse trace stops at unsupported official mapping',()=>{
  const ledger=W.ledgerSummary(dataset,'water');assert.ok(ledger.physical.some(r=>r.id==='synthetic-water-output'));assert.ok(ledger.financial.some(r=>r.id==='synthetic-water-spend'));assert.equal(ledger.actualOutcome,'UNKNOWN');const trace=W.reverseTrace(dataset,'synthetic-water-spend');assert.equal(trace.stationId,'water');assert.ok(trace.incoming.length>0);assert.ok(trace.path.nodeIds.includes('water'));assert.equal(trace.officialMapping,'UNKNOWN');assert.match(trace.breaks[0],/does not prove/);
 });
 await assert.rejects(()=>W.receipt({classification:'COUNCIL_PROTECTED',count:5}),/PROTECTED_INPUT_DENIED/);await assert.rejects(()=>W.receipt({address:'disallowed'}),/PROTECTED_FIELD_DENIED/);
 await assert.rejects(()=>W.receipt({note:'fictional@example.invalid'}),/PUBLIC_PAYLOAD_DENIED/);await assert.rejects(()=>W.receipt({nested:{security:'APPROVED_RELEASE'}}),/PROTECTED_INPUT_DENIED/);
 const receipt=await W.receipt({fixture,coverage:W.coverage(fixture.items,'2026-10-30')});
 assert.deepEqual(await W.verifyReceipt(receipt,receipt.input),{integrity:true,current:true,status:'CURRENT'});const changed=clone(receipt.input);changed.fixture.items[0].revisionId='changed';assert.equal((await W.verifyReceipt(receipt,changed)).status,'STALE_INPUT_RECALCULATE');const forged=clone(receipt);forged.input.coverage.completed=99;assert.equal((await W.verifyReceipt(forged,receipt.input)).integrity,false);count++;console.log('PASS calculation input receipts detect corruption and changed revisions');
 const derived=await W.derive(dataset,{formula:'COST_PER_OUTPUT',inputIds:['synthetic-water-spend','synthetic-water-output']});assert.equal(derived.result.value,2000);assert.equal((await W.verifyDerivation(dataset,derived)).current,true);await assert.rejects(()=>W.derive(dataset,{formula:'PER_CAPITA_TOTAL',inputIds:['csp2035-carbon-per-capita-baseline','synthetic-water-output']}),/UNADMITTED_INPUTS/);const land=await W.derive(dataset,{formula:'UNIT_CONVERSION',inputIds:['synthetic-land-area'],outputUnit:'km2'});assert.equal(land.result.value,.5);count++;console.log('PASS inherited water/carbon/land unit and finance engines preserve source gates');
 console.log('csoi-work: '+count+' groups PASS');
})().catch(e=>{console.error(e);process.exitCode=1;});
