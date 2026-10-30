const assert=require('node:assert/strict'),M=require('./atlas-model.js'),C=require('./csoi-calendar.js'),A=require('./csoi-assistant.js');
(async()=>{
 const task=structuredClone(C.syntheticTasks(2026)[0]),source={url:'https://example.invalid/rule',locator:'QA',revisionId:'sha256:'+'a'.repeat(64)};
 const forged={...task,classification:'PUBLIC',sourceType:'LEGAL_OBLIGATION',sourceBasis:source,applicability:{state:'APPLIES',sourceVerified:true}};assert.throws(()=>C.validateTask(forged),/AUTHORITY_NOT_CONFIGURED/);
 assert.equal(C.recurrence({start:'2026-01-01',until:'2026-12-31',everyMonths:12,classification:'PUBLIC',sourceBasis:source,applicability:{state:'APPLIES',sourceVerified:true}}).state,'PENDING_AUTHORISED_RULE_REVIEW');
 const d=await M.migrateDataset(require('./atlas-data.js'),require('./atlas-accounting.js').cases,require('./sources/public-catalogue.json'));
 const payload=C.scenarioPayload(task);payload.data.csoiTask.note='fictional@example.invalid';await assert.rejects(()=>M.registerScenario(d,payload),/INVALID_SCENARIO/);
 const protectedTask=C.scenarioPayload(task);protectedTask.data.csoiTask.classification='COUNCIL_PROTECTED';await assert.rejects(()=>M.registerScenario(d,protectedTask),/INVALID_SCENARIO/);
 const edition=C.annualEdition({year:2026,tasks:C.syntheticTasks(2026)}),draft=structuredClone(A.compileWeek(edition,{date:'2026-11-02',capacityHours:8})),draftPayload=A.scenarioPayload(draft);draftPayload.data.assistantDraft.managerAgreement=true;await assert.rejects(()=>M.registerScenario(d,draftPayload),/INVALID_SCENARIO/);
 const before=Date.now(),stored=await M.registerScenario(d,C.scenarioPayload(task));assert(Date.parse(stored.domain.events.at(-1).observedAt)>=before);assert(await M.verifySnapshot(await M.exportSnapshot(stored)));
 console.log('PASS: calendar/assistant capsules stay governed in legacy snapshots; claimed statutory verification cannot authorise tasks/recurrence, and new audit events use actual execution time');
})().catch(e=>{console.error(e);process.exitCode=1});
