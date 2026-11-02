/* Append-only corrections to selected public research records in the Atlas domain. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
const G=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;
const C=typeof module!=='undefined'?require('./csoi-clauses.js'):root.AtlasCSOIClauses;
const supplied=typeof module!=='undefined'?require('./sources/knowledge-corrections.json'):root.CsoiKnowledgeCorrections;
const PLAN=structuredClone(supplied);
function freeze(value){if(value&&typeof value==='object'){Object.freeze(value);for(const child of Object.values(value))freeze(child);}return value;}
freeze(PLAN);
function need(ok,code){if(!ok)throw Error(code);}
function item(d,id){return M.domainIndex(d).get(id);}
function inner(entity){return entity?.data?.csoiRecord||null;}
function source(d,id){return d.domain?.sourceCatalogue?.sources.find(s=>s.id===id)||null;}
function anchor(sourceId,page){const found=PLAN.sources.find(s=>s.sourceId===sourceId)?.anchors.find(a=>a.pdfPage===page);need(found,'REMEDIATION_ORIGINAL_ANCHOR_REQUIRED');return {pdfPage:found.pdfPage,normalizedPageDigest:found.normalizedPageDigest,parserVersion:found.parserVersion};}
function replacementFor(id){return id===PLAN.replacement.oldId?{id:PLAN.replacement.newId,parentId:PLAN.replacement.newParentId,reason:PLAN.replacement.reason}:null;}
function targetSource(entity,evidence){const record=inner(entity);need(record&&record.data.sourceId===evidence.sourceId&&record.data.sourceDigest===evidence.rawDigest&&record.provenance.url===evidence.officialUrl&&record.provenance.sourceRevision===evidence.rawDigest,'REMEDIATION_TARGET_SOURCE_CONFLICT');}
function citation(d,entity){const record=inner(entity),s=source(d,record?.data.sourceId);return {sourceId:s?.id||null,sourceRevisionId:s?.revisionId||null,officialUrl:s?.officialUrl||null,rawDigest:s?.rawDigest||null,locator:record?.provenance.locator||null,currentLaw:'UNKNOWN',rights:'UNKNOWN',officialAdmission:'PENDING'};}
function addChange(changes,d,before,after,operation,reason){changes.push({id:after.id,operation,reason,oldRevisionId:before?.revisionId||null,newRevisionId:after.revisionId,oldRecord:before?structuredClone(before):null,newRecord:structuredClone(after),original:citation(d,after),correctionManifestTime:PLAN.observedAt});}
async function revise(d,changes,id,patch,reason,operation){
 const before=item(d,id);need(inner(before),'REMEDIATION_RECORD_REQUIRED');const old=inner(before);
 const record=await G.makeRecord({...old,...patch,observedAt:PLAN.observedAt});
 const next=await M.reviseResearchRecord(d,{id,expectedRevisionId:before.revisionId,record,reason});
 addChange(changes,next,before,item(next,id),operation,reason);return next;
}
async function apply(dataset){
 need(PLAN?.format==='csoi-knowledge-corrections-1'&&PLAN.rights==='UNKNOWN'&&PLAN.currentLaw==='UNKNOWN'&&PLAN.officialAdmission==='PENDING','REMEDIATION_MANIFEST_REQUIRED');
 need(await M.verifySnapshot(await M.exportSnapshot(dataset)),'REMEDIATION_DATASET_INVALID');
 let d=dataset;const changes=[];
 if(!d.domain)return {dataset:d,changes,status:'NOT_APPLICABLE_LEGACY_DATASET'};
 for(const evidence of PLAN.sources){const s=source(d,evidence.sourceId);if(s)need(s.rawDigest===evidence.rawDigest&&s.officialUrl===evidence.officialUrl,'REMEDIATION_SOURCE_REVISION_CONFLICT');}

 // Preserve the original wrong-ID record as a withdrawn historical observation.
 const snowySource=PLAN.sources.find(s=>s.id==='snowy-drainage'),ampSource=PLAN.sources.find(s=>s.id==='water-amp-locator');
 const wrong=item(d,PLAN.replacement.oldId);
 if(wrong)targetSource(wrong,snowySource);
 if(inner(wrong)&&inner(wrong).state!=='WITHDRAWN'){
  const old=inner(wrong),summary='Withdrawn after original-page review: this drainage/stormwater observation was assigned to subdivision section4.1. The original PDF27/printed12 places it under section4.2 (other than subdivision). Use '+PLAN.replacement.newId+'. Current applicability and official admission remain pending.';
  d=await revise(d,changes,wrong.id,{state:'WITHDRAWN',data:{...old.data,summary}},PLAN.replacement.reason,'WITHDRAW_WRONG_APPLICATION_TYPE');
 }
 for(const [id,parentId]of [[PLAN.replacement.newParentId,'csoi:dcp:snowy2013:A2'],[PLAN.replacement.newId,PLAN.replacement.newParentId]]){const existing=item(d,id);if(existing){targetSource(existing,snowySource);need(existing.data.csoiRecord.data.dcpClause?.parentId===parentId&&M.canonical(existing.data.csoiRecord.data.dcpClause.anchor)===M.canonical(anchor(snowySource.sourceId,27)),'REMEDIATION_REPLACEMENT_ID_CONFLICT');}}
 if(item(d,'csoi:dcp:snowy2013:A2')&&(!item(d,PLAN.replacement.newParentId)||!item(d,PLAN.replacement.newId))){
  const nodes=[{id:PLAN.replacement.newParentId,parentId:'csoi:dcp:snowy2013:A2',section:'A2 section4.2',label:'Development applications other than subdivision',locator:'PDF page27, printed page12; A2 section4.2 Development Application (Other Than Subdivision)',summary:'Own observation of the non-subdivision application-information section. Its minimum submission list and conditional additional material are distinct from the preceding subdivision list. No current legal applicability or Council instruction is established.',category:'SECTION',conditions:['Identify the application type and the proposed development context before considering this historical list.'],exceptions:[],obligations:[],anchor:anchor(snowySource.sourceId,27)},{id:PLAN.replacement.newId,parentId:PLAN.replacement.newParentId,section:'A2 section4.2 conditional additional information',label:'Conditional drainage and stormwater information — non-subdivision',locator:'PDF page27, printed page12; A2 section4.2, additional information depending on development type and scale',summary:'The non-subdivision section says drainage and stormwater management plans may also be required depending on the development type and scale. This is a conditional source observation, not a subdivision requirement, approved work, or Council assignment.',category:'CLAUSE',conditions:['The original wording is conditional on the type and scale of the proposed development.','Current law, actual proposal scope and authorised review remain unresolved.'],exceptions:[],obligations:['Research question: does the relevant non-subdivision proposal require this supporting information after current-source review?'],anchor:anchor(snowySource.sourceId,27)}];
  for(const node of nodes){if(item(d,node.id))continue;const next=await C.registerOutline(d,{sourceId:snowySource.sourceId,sourceRevision:snowySource.rawDigest,nodes:[node],observedAt:PLAN.observedAt});addChange(changes,next,null,item(next,node.id),'ADD_CORRECT_APPLICATION_TYPE',PLAN.replacement.reason);d=next;}
 }

 // Every old source-note capsule is retained; only a new current revision gains
 // the exact source input. The Water AMP correction is in the same revision.
 const noteIds=d.domain.entities.filter(e=>e.id.startsWith(PLAN.sourceNoteBindings.idPrefix)&&inner(e)).map(e=>e.id);
 for(const id of noteIds){
  const before=item(d,id),record=inner(before),s=source(d,record.data.sourceId);
  need(s&&record.data.sourceDigest===s.rawDigest&&record.provenance.url===s.officialUrl&&record.provenance.sourceRevision===s.rawDigest,'REMEDIATION_SOURCE_NOTE_BINDING_CONFLICT');
  const pinned=record.inputs.some(i=>i.id===s.id&&i.revisionId===s.revisionId),isAmp=id===PLAN.waterAmp.id,ampNeedsCorrection=isAmp&&(record.data.locator!==PLAN.waterAmp.locator||record.provenance.locator!==PLAN.waterAmp.locator);
  if(isAmp)targetSource(before,ampSource);
  if(pinned&&!ampNeedsCorrection)continue;
  const inputs=pinned?record.inputs:[...record.inputs,{id:s.id,revisionId:s.revisionId}];
  const patch={inputs};
  if(ampNeedsCorrection){patch.data={...record.data,locator:PLAN.waterAmp.locator};patch.provenance={...record.provenance,locator:PLAN.waterAmp.locator};}
  d=await revise(d,changes,id,patch,ampNeedsCorrection?PLAN.waterAmp.reason+' '+PLAN.sourceNoteBindings.reason:PLAN.sourceNoteBindings.reason,ampNeedsCorrection?'CORRECT_LOCATOR_AND_PIN_SOURCE':'PIN_SOURCE_VERSION');
 }

 const minimum=PLAN.minimumReference,clause=item(d,minimum.clauseId);
 if(inner(clause)){
  targetSource(clause,snowySource);
  const record=inner(clause),condition='Historical accommodation capacity minimum: at least110 L/person/day (>=110), with peak occupancy/use context in preceding(a); not actual demand.';
  if(!record.data.dcpClause.conditions.includes(condition)){
   const data={...record.data,summary:'The printed C6.2-3(b), within C9, asks an accommodation proposal to demonstrate potable-water capacity of at least110 litres/person/day. The preceding(a) concerns peak occupancy or use. This is a historical minimum-capacity reference, not measured demand or a current duty.',dcpClause:{...record.data.dcpClause,conditions:[...record.data.dcpClause.conditions,condition]}};
   d=await revise(d,changes,clause.id,{data},minimum.reason,'PRESERVE_MINIMUM_CAPACITY_SEMANTICS');
  }
 }
 const reference=item(d,minimum.referenceId),currentClause=item(d,minimum.clauseId);
 if(inner(reference)&&inner(currentClause)){
  targetSource(reference,snowySource);
  const record=inner(reference),measurement=record.data.measurement;
  need(measurement.value===minimum.value&&measurement.unit===minimum.unit,'REMEDIATION_REFERENCE_VALUE_CONFLICT');
  if(measurement.operator!==minimum.operator||measurement.comparison!==minimum.comparison||!record.inputs.some(i=>i.id===currentClause.id&&i.revisionId===currentClause.revisionId)){
   const data={...record.data,summary:'Own observation of a historical minimum potable-water capacity: at least110 L/person/day for accommodation, in peak occupancy/use context. Not actual water demand, delivery, expenditure, outcome, or verified current applicability.',measurement:{...measurement,operator:minimum.operator,comparison:minimum.comparison,applicationContext:'Historical accommodation minimum capacity; peak occupancy/use context; actual population and demand UNKNOWN.'}};
   const inputs=[...record.inputs.filter(i=>i.id!==currentClause.id),{id:currentClause.id,revisionId:currentClause.revisionId}];
   d=await revise(d,changes,reference.id,{data,inputs},minimum.reason,'PRESERVE_MINIMUM_REFERENCE_AND_CLAUSE_PIN');
  }
 }
 need(await M.verifySnapshot(await M.exportSnapshot(d)),'REMEDIATION_RESULT_INVALID');
 return {dataset:d,changes,status:changes.length?'CORRECTIONS_APPENDED':'ALREADY_APPLIED'};
}
const api={apply,replacementFor,manifest:PLAN};root.AtlasCSOIRemediation=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
