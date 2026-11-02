'use strict';
// Audit-only observations against unchanged production modules. No admitted law.
const assert=require('node:assert/strict'),path=require('node:path');
const APP=path.resolve(__dirname,'../../..');
const G=require(path.join(APP,'csoi-governance.js'));
const L=require(path.join(APP,'csoi-layers.js'));
const W=require(path.join(APP,'csoi-wcos.js'));
const P=require(path.join(APP,'csoi-pages.js'));
(async()=>{
 const source=await L.source({id:'csoi:closure:synthetic-source',ownerModule:'CSOI_OPERATIONS',security:'PUBLIC',sourceClass:'SYNTHETIC',judgment:'OBSERVATION',authority:'INDEPENDENT_RESEARCH',scope:{region:'SYNTHETIC_PLACE',boundary:'SYNTHETIC_CLOSURE_CHECK',period:{from:'2026-01-01',to:'2026-12-31'}},inputs:[],data:{title:'Authored synthetic observation; not a Council record'},sensitivity:{personalData:false,confidential:false,reidentifiable:false},provenance:{contentMode:'SYNTHETIC',rights:{mode:'SYNTHETIC_OWNED',basis:'Independent audit synthetic fixture'}},observedAt:'2026-11-02T00:00:00Z'});
 const normal=await L.normalize(source,{id:'csoi:closure:synthetic-normal',identities:[{type:'WORK_EVENT',id:'SYNTHETIC-ONLY',validFrom:'2026-01-01',validTo:'2026-12-31'}]});
 const counterevidence=['Synthetic contrary observation retained, not resolved'],unknowns=['Actual applicability UNKNOWN'];
 const rows=[];
 for(const judgment of ['RULE','OBSERVATION','EVIDENCE_INFERENCE','DISCRETION','UNKNOWN']){
  const rule=judgment==='RULE'?{sourceId:source.id,sourceRevision:source.revisionId,locator:'synthetic condition only',legalRole:'SYNTHETIC_RULE_NOT_LAW',applicability:'UNKNOWN'}:null;
  const record=await L.statement(normal,{id:'csoi:closure:'+judgment.toLowerCase(),judgment,text:'Synthetic '+judgment+' statement',counterevidence,unknowns,rule});
  assert.equal(record.layer,'L2');assert.equal(record.judgment,judgment);assert.equal(record.data.judgment,judgment);
  assert.deepEqual(record.data.counterevidence,counterevidence);assert.deepEqual(record.data.unknowns,unknowns);
  assert.equal(record.data.officialDecision,false);assert.equal(record.authority,'INDEPENDENT_RESEARCH');
  assert.equal(record.inputs[0].revisionId,normal.revisionId);assert(await G.verifyRecord(record));
  rows.push({judgment,layer:record.layer,counterevidencePreserved:true,unknownPreserved:true,officialDecision:record.data.officialDecision});
 }
 await assert.rejects(()=>L.statement(normal,{id:'csoi:closure:formal',judgment:'FORMAL_DECISION',text:'Unsupported official decision'}),/STATEMENT_REQUIRED/);
 await assert.rejects(()=>L.statement(normal,{id:'csoi:closure:rule-missing',judgment:'RULE',text:'No rule source'}),/RULE_SOURCE_AND_APPLICABILITY_REQUIRED/);
 for(const field of ['sourceId','sourceRevision','locator','legalRole','applicability']){
  const rule={sourceId:source.id,sourceRevision:source.revisionId,locator:'synthetic',legalRole:'SYNTHETIC_RULE_NOT_LAW',applicability:'UNKNOWN'};delete rule[field];
  await assert.rejects(()=>L.statement(normal,{id:'csoi:closure:missing-'+field,judgment:'RULE',text:'Incomplete synthetic rule',rule}),/RULE_SOURCE_AND_APPLICABILITY_REQUIRED/);
 }
 const formal=W.judgment('FORMAL_DECISION',{statement:'Synthetic decision request',sourceIds:[source.id],reviewer:'SYNTHETIC_REVIEWER'});
 assert.equal(formal.status,'BLOCKED');assert.equal(formal.governmentApproval,false);assert.equal(formal.reviewer,null);
 assert.equal(W.judgment('RULE',{statement:'Missing source'}).status,'UNKNOWN');
 console.log(JSON.stringify({task:'COI-023',status:'PASS_ACTUALLY_TESTED',observations:rows,formalDecision:'BLOCKED',missingRuleFieldsRejected:5}));
 const fixture=[{id:'synthetic:food',title:'Food reference research',kind:'WorkPackage',sourceId:'source:registered',classification:'SYNTHETIC',scope:{region:'SYNTHETIC_PLACE',period:{from:'2026-07-01',to:'2027-06-30'},legalRole:'Food Act reference only'},data:{unit:'count'}},{id:'synthetic:unknown',title:'Unknown scope',kind:'ContentBlock',classification:'SYNTHETIC',data:{}}];
 const before=structuredClone(fixture),positive={q:'food',year:'2026',region:'SYNTHETIC_PLACE',law:'Food Act',source:'source:registered',work:'WorkPackage',unit:'count'},negative={q:'never-present-text',year:'2028',region:'OTHER_REGION',law:'OTHER_LAW',source:'OTHER_SOURCE',work:'OTHER_WORK',unit:'ML'};
 for(const [key,value]of Object.entries(positive))assert.deepEqual(P.queryFilter(fixture,{[key]:value}).map(x=>x.id),['synthetic:food'],key);
 for(const [key,value]of Object.entries(negative))assert.equal(P.queryFilter(fixture,{[key]:value}).length,0,key);
 assert.deepEqual(P.queryFilter(fixture,positive).map(x=>x.id),['synthetic:food']);assert.deepEqual(fixture,before);
 console.log(JSON.stringify({task:'COI-074',status:'PASS_ACTUALLY_TESTED',filterDimensions:Object.keys(positive),positiveChecks:7,negativeChecks:7,combinedFilter:'PASS',unknownScopeExcluded:true,fixtureUnchanged:true,limitation:'Recorded references only; no legal corpus completeness or applicability claim'}));
})().catch(error=>{console.error(error);process.exitCode=1;});
