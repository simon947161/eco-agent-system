const assert=require('node:assert/strict');
const C=require('./csoi-calendar.js'),M=require('./atlas-model.js'),D=require('./atlas-data.js'),A=require('./atlas-accounting.js');
const clone=x=>structuredClone(x);
(async()=>{
 for(const invalid of ['2025-02-29','2026-02-30','2026-13-01','2026-01-00','2026-1-1','2026-01-01T00:00:00Z'])assert.throws(()=>C.day(invalid));
 assert.equal(C.addDays('2024-02-28',1),'2024-02-29');assert.equal(C.addDays('2024-02-29',1),'2024-03-01');
 assert.equal(C.addMonths('2024-01-31',1),'2024-02-29');assert.equal(C.addMonths('2024-01-31',2),'2024-03-31');
 assert.equal(C.isoWeek('2021-01-01').id,'2020-W53');assert.equal(C.isoWeek('2024-12-30').id,'2025-W01');
 const tasks=C.syntheticTasks(2026),edition=C.annualEdition({year:2026,tasks}),map=C.index(edition);
 assert.equal(C.query(edition,{kind:'DAY',limit:100}).total,365);assert.equal(C.query(C.annualEdition({year:2024}),{kind:'DAY',limit:100}).total,366);
 const fiscal=C.annualEdition({year:2023,yearBasis:'AU_FISCAL'});assert.equal(fiscal.start,'2023-07-01');assert.equal(fiscal.end,'2024-06-30');assert.equal(C.query(fiscal,{kind:'DAY',limit:100}).total,366);
 assert.equal(C.children(edition,edition.editionId).items.filter(n=>n.kind==='QUARTER').length,4);
 const november=C.query(edition,{kind:'MONTH'}).items.find(n=>n.from==='2026-11-01'),week=C.children(edition,november.id).items.find(n=>n.from==='2026-11-02');
 assert(week);assert(C.parents(edition,week.id).some(n=>n.id===november.id));assert(C.children(edition,week.id).items.some(n=>n.date==='2026-11-02'));
 const crossingWeek=C.children(edition,november.id).items.find(n=>n.from==='2026-10-26');assert.equal(C.parents(edition,crossingWeek.id).length,2);assert.equal(C.children(edition,crossingWeek.id,{within:november.id}).items.length,1);
 const task=tasks[0];assert(C.children(edition,'calendar:CALENDAR:2026:day:2026-11-02').items.some(n=>n.id===task.id));
 const types=C.trace(edition,task.id).nodes.map(n=>n.kind);for(const type of ['TASK','DAY','WEEK','MONTH','QUARTER','OPERATING_YEAR','MISSION'])assert(types.includes(type));
 const work=C.children(edition,task.id).items[0],brief=C.children(edition,work.id).items[0],execution=C.children(edition,brief.id).items[0],evidence=C.children(edition,execution.id).items[0];
 assert.equal(work.kind,'WORK_ITEM');assert.equal(brief.kind,'FIELD_BRIEF');assert.equal(execution.state,'UNKNOWN');assert.equal(evidence.kind,'EVIDENCE');assert.equal(evidence.state,'UNKNOWN');
 const follow=C.children(edition,evidence.id).items[0],report=C.children(edition,follow.id).items[0];assert.equal(report.kind,'REPORT');assert(C.trace(edition,report.id).nodes.some(n=>n.id===task.id));
 assert(Object.isFrozen(edition));assert.equal(C.taskCard(task).actualResult,'UNKNOWN');assert.equal(C.taskCard(task).basisState,'SOURCE_OR_REVISION_UNKNOWN');
 assert.equal(C.children(edition,week.id,{limit:2}).nextOffset,2);assert.throws(()=>C.children(edition,week.id,{limit:101}),/BOUNDS/);assert.throws(()=>C.annualEdition({year:2025,tasks}),/OUTSIDE/);
 for(const mutation of [t=>t.approval={state:'APPROVED',governmentApproval:true,evidenceRefs:[]},t=>t.actualHours=2,t=>t.sourceType='COUNCIL_ASSIGNED',t=>t.classification='COUNCIL_PROTECTED',t=>t.customerName='Private name',t=>t.dueDate='2026-11-01']){const t=clone(task);mutation(t);assert.throws(()=>C.validateTask(t));}
 const falseActual=clone(task);falseActual.executionStatus='RECORDED';falseActual.actualHours=3;assert.throws(()=>C.validateTask(falseActual),/WITHOUT_EVIDENCE/);
 for(const mutation of [t=>t.title='Contact fictional@example.invalid',t=>t.nextStep='Phone 0412 345 678',t=>t.discretion='COUNCIL_PROTECTED',t=>t.sourceBasis={nested:{security:'PERSONAL_PRIVATE'}},t=>t.evidenceRefs=[{id:'unknown',revisionId:'sha256:'+'a'.repeat(64),details:{governmentApproval:true}}]]){const t=clone(task);mutation(t);assert.throws(()=>C.taskCard(t),/PUBLIC_DENIED/);assert.throws(()=>C.scenarioPayload(t),/PUBLIC_DENIED/);}
 const publicTask={...clone(task),classification:'PUBLIC',sourceType:'LEGAL_OBLIGATION',applicability:{state:'APPLIES'}};assert.throws(()=>C.validateTask(publicTask),/LEGAL_APPLICABILITY/);
 const common={start:'2024-01-31',until:'2024-05-31',everyMonths:1,applicability:{state:'APPLIES'}};
 assert.deepEqual(C.recurrence(common).dates,['2024-01-31','2024-02-29','2024-03-31','2024-04-30','2024-05-31']);
 assert.equal(C.recurrence({...common,applicability:{state:'UNKNOWN'}}).dates.length,0);assert.equal(C.recurrence({...common,applicability:{state:'DOES_NOT_APPLY'}}).state,'NOT_APPLICABLE');
 assert.throws(()=>C.recurrence({...common,everyDays:7}),/INTERVAL/);assert.throws(()=>C.recurrence({...common,everyMonths:0}),/INTERVAL/);assert.throws(()=>C.recurrence({...common,classification:'PUBLIC'}),/SOURCE_UNKNOWN/);assert.throws(()=>C.recurrence({...common,maxOccurrences:2}),/CAP/);
 const cyc=clone(tasks.slice(0,2));cyc[0].dependencies=[cyc[1].id];cyc[1].dependencies=[cyc[0].id];assert(C.conflicts(cyc).some(x=>x.code==='DEPENDENCY_CYCLE'));assert(C.conflicts(cyc).some(x=>x.code==='DEPENDENCY_AFTER_START'));
 const dangling=clone(task);dangling.dependencies=['absent'];assert(C.conflicts([dangling]).some(x=>x.code==='MISSING_DEPENDENCY'));
 const exported=await C.exportTasks(tasks);assert.deepEqual(await C.importTasks(JSON.stringify(exported)),tasks);
 const sensitive=clone(task);sensitive.discretion='contact person@example.com';await assert.rejects(()=>C.exportTasks([sensitive]),/PUBLIC_DENIED/);
 const corrupt=clone(exported);corrupt.records[0].data.task.title='rewritten';await assert.rejects(()=>C.importTasks(JSON.stringify(corrupt)),/DIGEST/);
 let dataset=await M.migrateDataset(D,A.cases);dataset=await M.registerScenario(dataset,C.scenarioPayload(task));assert(M.domainIndex(dataset).has(task.id));const snapshot=await M.exportSnapshot(dataset);assert(await M.verifySnapshot(snapshot));
 console.log('PASS: Annual Edition leap/fiscal/ISO dates, bounded bidirectional calendar/work/evidence/report navigation, source/approval cards, recurrence applicability/cycle/due guards, private/forged approval rejection, safe portability and existing Atlas snapshot integration');
})().catch(e=>{console.error(e);process.exitCode=1;});
