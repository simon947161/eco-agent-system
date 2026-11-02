const assert=require('node:assert/strict');
 const M=require('./atlas-model.js'),C=require('./csoi-clauses.js'),R=require('./csoi-review-work.js'),G=require('./csoi-governance.js'),I=require('./atlas-intake.js'),Fix=require('./csoi-remediation.js');
const original=require('./qa/remediation/corrections-original-verification.json');

// The new default cache retains the original prefix. Reconstruct that historical
// fixture from retained revisions rather than shipping another knowledge store.
function auditBaseline(){
 const d=structuredClone(require('./sources/csoi-default-snapshot.js').snapshot.dataset),b=original.baseline;
 d.domain.revisions=d.domain.revisions.slice(0,b.revisionCount);d.domain.events=d.domain.events.slice(0,b.eventCount);
 d.domain.sourceCatalogue.sources=d.domain.sourceCatalogue.sources.slice(0,b.sourceCount);d.domain.sourceCatalogue.events=d.domain.sourceCatalogue.events.slice(0,b.sourceEventCount);
 const retained=new Map(d.domain.revisions.map(revision=>[revision.logicalId,{...structuredClone(revision.record),revisionId:revision.id}]));
 d.domain.entities=b.entityIds.map(id=>retained.get(id));d.domain.assertions=b.assertionIds.map(id=>retained.get(id));return d;
}
(async()=>{
 assert.deepEqual(require('./sources/knowledge-corrections.js'),Fix.manifest);
 const before=auditBaseline(),digest=await M.objectDigest(before),catalogueDigest=await M.objectDigest(before.domain.sourceCatalogue);
 assert.equal(digest,original.baseline.datasetDigest);assert(await M.verifySnapshot(await M.exportSnapshot(before)));
 const oldWrong=M.domainIndex(before).get(Fix.manifest.replacement.oldId),oldAmp=M.domainIndex(before).get(Fix.manifest.waterAmp.id),oldMinimum=M.domainIndex(before).get(Fix.manifest.minimumReference.referenceId);
 assert.equal(oldWrong.data.csoiRecord.data.dcpClause.parentId,'csoi:dcp:snowy2013:A2:4:1');assert(oldAmp.provenance.locator.includes('14'));assert.equal(oldMinimum.data.csoiRecord.data.measurement.operator,undefined);
 const result=await Fix.apply(before),d=result.dataset;
 assert.equal(await M.objectDigest(before),digest,'caller dataset was not mutated');assert.equal(result.changes.length,30);
 assert.deepEqual(d.domain.revisions.slice(0,before.domain.revisions.length),before.domain.revisions);assert.deepEqual(d.domain.events.slice(0,before.domain.events.length),before.domain.events);
 assert.equal(await M.objectDigest(d.domain.sourceCatalogue),catalogueDigest);assert.equal(d.contentItems.length,127);assert.equal(d.domain.entities.length,137);assert.equal(d.domain.assertions.length,48);
 const wrong=M.domainIndex(d).get(oldWrong.id),fixed=M.domainIndex(d).get(Fix.manifest.replacement.newId),amp=M.domainIndex(d).get(oldAmp.id),minimum=M.domainIndex(d).get(oldMinimum.id);
 assert.equal(wrong.data.csoiRecord.state,'WITHDRAWN');assert(!(await C.status(d,wrong.id)).current);assert.equal(Fix.replacementFor(wrong.id).id,fixed.id);assert.equal(Fix.replacementFor('unrelated'),null);
 assert.equal(fixed.data.csoiRecord.data.dcpClause.parentId,'csoi:dcp:snowy2013:A2:4:2');assert.equal(fixed.data.csoiRecord.data.dcpClause.anchor.pdfPage,27);assert(fixed.data.csoiRecord.data.dcpClause.conditions.some(x=>x.includes('type and scale')));assert((await C.status(d,fixed.id)).current);
 for(const change of result.changes){assert.equal(change.newRecord.data.csoiRecord.observedAt,Fix.manifest.observedAt);const event=d.domain.events.find(e=>e.objectId===change.newRevisionId);assert.equal(event.observedAt,Fix.manifest.observedAt);}
 const template=require('./sources/snowy-dcp-outline.json').nodes[0],source=Fix.manifest.sources.find(s=>s.id==='snowy-drainage');
 for(const observedAt of [null,'2026-02-30T12:00:00.000Z','not-a-date','2020-01-01T12:00:00.000Z'])await assert.rejects(()=>C.registerOutline(before,{sourceId:source.sourceId,sourceRevision:source.rawDigest,nodes:[{...template,id:'csoi:qa:invalid-correction-time'}],observedAt}),/CLAUSE_OBSERVATION_TIME/);
 const dateOnly=structuredClone(before.domain.sourceCatalogue.sources.find(s=>s.id===source.sourceId));delete dateOnly.revisionId;dateOnly.id='csoi:qa:date-only-source';dateOnly.retrievedAt='2026-10-30';dateOnly.lineage.supersedes=[];
 let catalogue=await I.createCatalogue([dateOnly],{registeredAt:'2026-10-30'});for(const [stage,evidence]of [['DIRECTORY_OBSERVED',{url:dateOnly.directoryUrl,directoryDigest:dateOnly.rawDigest}],['SOURCE_RETRIEVED',{url:dateOnly.officialUrl,retrievedAt:dateOnly.retrievedAt,byteLength:source.byteLength,httpStatus:200,rawDigest:dateOnly.rawDigest}],['RAW_BYTES_VERIFIED',{rawDigest:dateOnly.rawDigest}]])catalogue=await I.appendStage(catalogue,dateOnly.id,stage,{...evidence,actor:'QA',at:'2026-10-30',reason:'QA date-only receipt compatibility; not an additional official source'});
 const dateBase=await M.migrateDataset(require('./atlas-data.js'),require('./atlas-accounting.js').cases,catalogue),dateRegistered=await C.registerOutline(dateBase,{sourceId:dateOnly.id,sourceRevision:dateOnly.rawDigest,nodes:[{...template,id:'csoi:qa:date-only-default'}]});assert.equal(M.domainIndex(dateRegistered).get('csoi:qa:date-only-default').data.csoiRecord.observedAt,'2026-10-30');
 assert.equal(amp.data.csoiRecord.data.locator,Fix.manifest.waterAmp.locator);assert.equal(amp.provenance.locator,Fix.manifest.waterAmp.locator);assert.notEqual(amp.revisionId,oldAmp.revisionId);
 const notes=d.domain.entities.filter(e=>e.id.startsWith('csoi:source-note:'));assert.equal(notes.length,25);
 for(const n of notes){const record=n.data.csoiRecord,s=d.domain.sourceCatalogue.sources.find(s=>s.id===record.data.sourceId);assert(record.inputs.some(i=>i.id===s.id&&i.revisionId===s.revisionId));assert.equal(record.data.sourceDigest,s.rawDigest);assert.equal(record.provenance.url,s.officialUrl);}
 assert.equal(minimum.data.csoiRecord.data.measurement.operator,'MINIMUM');assert.equal(minimum.data.csoiRecord.data.measurement.comparison,'>=');assert.equal(minimum.data.value,110);assert.equal(minimum.data.unit,'L/person/day');
 assert.equal(minimum.data.operator,'MINIMUM');assert.equal(minimum.data.comparison,'>=');
 const leaf=M.domainIndex(d).get(Fix.manifest.minimumReference.clauseId);assert(minimum.data.csoiRecord.inputs.some(i=>i.id===leaf.id&&i.revisionId===leaf.revisionId));assert(leaf.data.csoiRecord.data.dcpClause.conditions.some(x=>x.includes('at least110')));
 assert(d.domain.entities.every(e=>e.admission!=='ADMITTED'));assert(await M.verifySnapshot(await M.exportSnapshot(d)));
 const again=await Fix.apply(d);assert.equal(again.changes.length,0);assert.equal(await M.objectDigest(again.dataset),await M.objectDigest(d));
 assert(result.changes.every(c=>c.newRevisionId&&c.newRecord&&c.original.sourceId&&c.original.rawDigest&&c.original.officialUrl&&c.reason));
 const plan=await R.register(before,{clauseId:oldWrong.id,date:'2026-11-03',plannedHours:1}),withPlan=await Fix.apply(plan.dataset),planEntity=M.domainIndex(withPlan.dataset).get(plan.id);
 assert(!(await R.status(withPlan.dataset,planEntity)).inputPinsCurrent);assert.equal(planEntity.data.csoiRecord.data.reviewPlan.actualHours,'UNKNOWN');assert(await M.verifySnapshot(await M.exportSnapshot(withPlan.dataset)));
 await assert.rejects(()=>R.register(withPlan.dataset,{clauseId:oldWrong.id,date:'2026-11-04',plannedHours:1}),/CONTEXT_STALE/);
 const ampRecord=oldAmp.data.csoiRecord,other=before.domain.sourceCatalogue.sources.find(s=>s.id==='csoi:smrc-csp-full-2025:20261030'),foreign=await G.makeRecord({...ampRecord,data:{...ampRecord.data,sourceId:other.id,sourceDigest:other.rawDigest},provenance:{...ampRecord.provenance,url:other.officialUrl,sourceRevision:other.rawDigest}});
 const foreignDataset=await M.reviseResearchRecord(before,{id:oldAmp.id,expectedRevisionId:oldAmp.revisionId,record:foreign,reason:'QA consistent public source change must not receive a different document correction'});await assert.rejects(()=>Fix.apply(foreignDataset),/TARGET_SOURCE_CONFLICT/);
 const missingClause=await G.makeRecord({...oldMinimum.data.csoiRecord,inputs:oldMinimum.data.csoiRecord.inputs.filter(i=>i.id!==Fix.manifest.minimumReference.clauseId)}),withoutClause=await M.reviseResearchRecord(before,{id:oldMinimum.id,expectedRevisionId:oldMinimum.revisionId,record:missingClause,reason:'QA lost reference-to-clause pin'}),repaired=await Fix.apply(withoutClause),repairedReference=M.domainIndex(repaired.dataset).get(oldMinimum.id),repairedClause=M.domainIndex(repaired.dataset).get(Fix.manifest.minimumReference.clauseId);
 assert(repairedReference.data.csoiRecord.inputs.some(i=>i.id===repairedClause.id&&i.revisionId===repairedClause.revisionId));assert(await M.verifySnapshot(await M.exportSnapshot(repaired.dataset)));assert.equal((await Fix.apply(repaired.dataset)).changes.length,0);
 console.log('PASS: retained135entity audit history;30append-only corrections;correctnon-subdivision drainage;AMPTable4PDF13;25source-note pins;110minimum capacity;stale old review plan;idempotent migration;127items/48assertions/source register unchanged and no official admission');
})().catch(error=>{console.error(error);process.exitCode=1});
