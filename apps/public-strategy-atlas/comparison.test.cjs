'use strict';
const assert=require('node:assert/strict');
const M=require('./atlas-model.js'),E=require('./atlas-execution.js'),B=require('./atlas-data.js'),A=require('./atlas-accounting.js'),C=require('./sources/public-catalogue.json');
const clone=structuredClone;let count=0;
async function check(label,run){await run();count++;console.log('PASS '+label);}
const field=(comparison,name)=>comparison.checks.find(c=>c.field===name);
(async()=>{
 const d=await M.migrateDataset(B,A.cases,C),before=await M.objectDigest(d);
 await check('current comparison pins exact content identities and does not perform finance arithmetic',async()=>{
  const c=await E.compareRecords(d,{left:{id:'synthetic-water-budget'},right:{id:'synthetic-water-spend'}});
  assert.equal(c.left.revisionId,M.domainIndex(d).get('synthetic-water-budget').revisionId);assert.equal(c.left.historical,false);assert.equal(c.left.facts.value,30000);assert.equal(c.right.facts.value,24000);assert.equal(field(c,'financialRole').status,'CONFLICT');assert.equal(field(c,'observationRole').status,'CONFLICT');assert.equal(c.compatibility.arithmeticAllowed,false);assert.equal(c.arithmetic,'NOT_PERFORMED');assert.equal(c.officialRelationship,'UNKNOWN');assert.ok(!Object.hasOwn(c,'variance'));assert.ok(!Object.hasOwn(c,'delta'));
 });
 await check('historical pin resolves retained version after current revision changes',async()=>{
  const old=M.domainIndex(d).get('synthetic-water-spend');const changed=await M.commitDomainRevision(d,{id:old.id,expectedRevisionId:old.revisionId,patch:{data:{...old.data,value:25000}},reason:'Synthetic comparison revision test',observedAt:'2026-10-30T00:00:00Z'});
  const c=await E.compareRecords(changed,{left:{id:old.id,revisionId:old.revisionId},right:{id:old.id}});
  assert.equal(c.left.historical,true);assert.equal(c.right.historical,false);assert.equal(c.left.facts.value,24000);assert.equal(c.right.facts.value,25000);assert.notEqual(c.left.contentDigest,c.right.contentDigest);assert.equal(field(c,'logicalId').status,'MATCH');assert.equal(field(c,'revisionId').status,'CONFLICT');assert.equal(field(c,'value').status,'CONFLICT');
  const another=M.domainIndex(d).get('synthetic-water-budget');await assert.rejects(()=>E.compareRecords(changed,{left:{id:old.id,revisionId:another.revisionId},right:{id:old.id}}),/COMPARISON_REVISION_NOT_FOUND/);
 });
 await check('missing identities and revision pins are rejected without substituting current objects',async()=>{
  await assert.rejects(()=>E.compareRecords(d,{left:{id:'missing'},right:{id:'water'}}),/COMPARISON_RECORD_NOT_FOUND/);
  await assert.rejects(()=>E.compareRecords(d,{left:{id:'water',revisionId:'missing-old-version'},right:{id:'water'}}),/COMPARISON_REVISION_NOT_FOUND/);
  await assert.rejects(()=>E.compareRecords(d,{left:{id:'water',revisionId:null},right:{id:'water'}}),/COMPARISON_REVISION_REQUIRED/);
  await assert.rejects(()=>E.compareRecords(d,{left:{id:'water',source:'untrusted override'},right:{id:'water'}}),/COMPARISON_ID_REQUIRED/);
 });
 await check('tampered current record or history fails snapshot verification before rendering',async()=>{
  const altered=clone(d);altered.domain.entities.find(r=>r.id==='synthetic-water-spend').data.value=1;
  await assert.rejects(()=>E.compareRecords(altered,{left:{id:'synthetic-water-spend'},right:{id:'water'}}),/COMPARISON_SNAPSHOT_INVALID/);
  const history=clone(d);history.domain.revisions[0].record.label='Forged historical record';
  await assert.rejects(()=>E.compareRecords(history,{left:{id:'water'},right:{id:'area'}}),/COMPARISON_SNAPSHOT_INVALID/);
 });
 await check('legacy stations, content and source catalogue use existing exact identities',async()=>{
  const stationPin=await M.objectDigest(B.nodes.find(r=>r.id==='csp')),contentPin=await M.objectDigest(B.contentItems.find(r=>r.id==='csp:content')),station=await E.compareRecords(B,{left:{id:'csp',revisionId:stationPin},right:{id:'csp:content',revisionId:contentPin}});assert.equal(station.left.category,'station');assert.equal(station.right.category,'content');assert.equal(station.left.revisionId,stationPin);assert.equal(station.right.revisionId,contentPin);assert.equal(station.left.declaredVersionId,'synthetic-v1:csp');
  await assert.rejects(()=>E.compareRecords(B,{left:{id:'csp',revisionId:'synthetic-v1:csp'},right:{id:'water'}}),/COMPARISON_REVISION_NOT_FOUND/);
  const relabelled=clone(B);relabelled.nodes.find(r=>r.id==='csp').detail='Different public fixture payload with the same declared version label';await assert.rejects(()=>E.compareRecords(relabelled,{left:{id:'csp',revisionId:stationPin},right:{id:'water'}}),/COMPARISON_REVISION_NOT_FOUND/);
  const c=await E.compareRecords(d,{left:{id:'smrc-csp-full'},right:{id:'smrc-dp-current'}});assert.equal(c.left.category,'source');assert.equal(c.left.revisionId,C.sources.find(s=>s.id==='smrc-csp-full').revisionId);assert.equal(c.left.facts.rawDigest,null);assert.equal(field(c,'rawDigest').status,'UNKNOWN');assert.equal(field(c,'sourceUrl').status,'UNKNOWN');
  const source=await E.compareRecords(B,{left:{id:'synthetic-source'},right:{id:'synthetic-source'}});assert.equal(source.left.category,'legacy-source');assert.match(source.left.revisionId,/^sha256:/);assert.equal(source.left.facts.rawDigest,B.sources.find(s=>s.id==='synthetic-source').rawDigest);
 });
 await check('same unknown method or scope is not a compatibility match and null is never zero',async()=>{
  const c=await E.compareRecords(d,{left:{id:'synthetic-water-spend'},right:{id:'synthetic-water-spend'}});assert.equal(field(c,'method').status,'UNKNOWN');assert.equal(field(c,'spatialType').status,'UNKNOWN');assert.equal(c.compatibility.status,'UNKNOWN');
  let extra=await M.registerScenario(d,{id:'comparison:null',kind:'QuantifiedObservation',label:'Synthetic null quantity',stationId:'water',data:{status:'SYNTHETIC',unit:'ML',value:'UNKNOWN',period:'FY2026-27',area:'SYNTHETIC_PLACE',boundary:'DEMO_WATER_SERVICE'},reason:'Test unknown quantity'});
  extra=await M.registerScenario(extra,{id:'comparison:zero',kind:'QuantifiedObservation',label:'Synthetic zero quantity',stationId:'water',data:{status:'SYNTHETIC',unit:'ML',value:0,period:'FY2026-27',area:'SYNTHETIC_PLACE',boundary:'DEMO_WATER_SERVICE'},reason:'Test zero quantity'});
  const unknown=await E.compareRecords(extra,{left:{id:'comparison:null'},right:{id:'comparison:zero'}});assert.equal(unknown.left.facts.value,'UNKNOWN');assert.equal(unknown.left.facts.valueState,'UNKNOWN');assert.equal(unknown.right.facts.value,0);assert.equal(field(unknown,'value').status,'UNKNOWN');
  const noValue=await E.compareRecords(d,{left:{id:'wbs:water:task'},right:{id:'synthetic-water-spend'}});assert.equal(noValue.left.facts.value,null);assert.equal(field(noValue,'value').left,null);
 });
 await check('unit, stock/flow, fiscal interval, region and actual/planned roles remain distinct',async()=>{
  let scoped=await M.registerScenario(d,{id:'comparison:flow',kind:'QuantifiedObservation',label:'Synthetic actual flow rate',stationId:'water',data:{status:'SYNTHETIC',value:12,unit:'ML/day',quantityNature:'FLOW_RATE',actual:true,area:'OTHER_SYNTHETIC_AREA',period:'FY2025-26',boundary:'DEMO_WATER_SERVICE'},reason:'Comparison negative fixture'});
  const volume=await E.compareRecords(scoped,{left:{id:'synthetic-water-output'},right:{id:'comparison:flow'}});for(const key of ['unit','quantityNature','period','region'])assert.equal(field(volume,key).status,'CONFLICT');
  const rate=await E.compareRecords(d,{left:{id:'csp2035-carbon-per-capita-baseline'},right:{id:'synthetic-water-cost-per-ml'}});assert.equal(field(rate,'unit').status,'CONFLICT');assert.equal(field(rate,'period').status,'UNKNOWN');assert.deepEqual(rate.left.facts.rawPeriod,A.cases[0].metric.period);assert.equal(rate.officialRelationship,'UNKNOWN');
  scoped=await M.registerScenario(scoped,{id:'comparison:target',kind:'QuantifiedObservation',label:'Synthetic target',stationId:'water',data:{status:'SYNTHETIC',value:12,unit:'ML/day',target:true,area:'OTHER_SYNTHETIC_AREA',period:'FY2025-26',boundary:'DEMO_WATER_SERVICE'},reason:'Target not actual'});
  const role=await E.compareRecords(scoped,{left:{id:'comparison:flow'},right:{id:'comparison:target'}});assert.equal(field(role,'observationRole').status,'CONFLICT');assert.equal(field(role,'observationRole').left,'ACTUAL');assert.equal(field(role,'observationRole').right,'TARGET');
 });
 await check('protected payloads, unknown classification and forged approved releases are denied',async()=>{
  for(const classification of ['PERSONAL_PRIVATE','COUNCIL_PROTECTED','APPROVED_RELEASE','UNKNOWN']){const protectedBase=clone(B);protectedBase.nodes[0].classification=classification;await assert.rejects(()=>E.compareRecords(protectedBase,{left:{id:'csp'},right:{id:'water'}}),/COMPARISON_PUBLIC/);}
  const nested=clone(B);nested.nodes[0].localOverlay={security:'APPROVED_RELEASE',approvedBy:'self'};await assert.rejects(()=>E.compareRecords(nested,{left:{id:'csp'},right:{id:'water'}}),/COMPARISON_PUBLIC/);
  const pii=clone(B);pii.nodes[0].emailAddress='synthetic@example.org';await assert.rejects(()=>E.compareRecords(pii,{left:{id:'csp'},right:{id:'water'}}),/COMPARISON_PUBLIC/);
  for(const key of ['privacy','permission','confidentiality']){const marked=clone(B);marked.nodes[0].localOverlay={[key]:'PRIVATE'};await assert.rejects(()=>E.compareRecords(marked,{left:{id:'csp'},right:{id:'water'}}),/COMPARISON_PUBLIC/);}
  const body=clone(B);body.nodes[0].localOverlay={fullText:'simulated undistributable original body'};await assert.rejects(()=>E.compareRecords(body,{left:{id:'csp'},right:{id:'water'}}),/SOURCE_BODY_NOT_PERMITTED/);
 });
 await check('percent denominators, financial rates and legal roles participate in compatibility',async()=>{
  const base={status:'SYNTHETIC',value:20,unit:'percent',area:'QA_SYNTHETIC_AREA',boundary:'QA_SYNTHETIC_SERVICE',period:'FY2026-27',spatialType:'SERVICE_AREA',quantityNature:'RATIO',method:'synthetic-compare-1',observationRole:'ACTUAL',denominator:10};
  let data=d;const add=async(id,patch,kind='QuantifiedObservation')=>{data=await M.registerScenario(data,{id,kind,label:'Synthetic comparison negative '+id,stationId:'water',data:{...base,...patch},reason:'Independent comparison regression'});};
  await add('comparison:percent-a',{});await add('comparison:percent-b',{denominator:100});const pct=await E.compareRecords(data,{left:{id:'comparison:percent-a'},right:{id:'comparison:percent-b'}});assert.equal(field(pct,'denominator').applicable,true);assert.equal(pct.compatibility.status,'CONFLICT');
  await add('comparison:rate-a',{unit:'AUD/ML',quantityNature:'FINANCIAL_RATE',denominator:'ML',currencyBasis:'2026AUD',costClass:'CAPEX',lineId:'QA-line',type:'ACTUAL_EXPENDITURE'});await add('comparison:rate-b',{unit:'AUD/ML',quantityNature:'FINANCIAL_RATE',denominator:'ML',currencyBasis:'2025AUD',costClass:'OPEX',lineId:'QA-line',type:'ACTUAL_EXPENDITURE'});const rate=await E.compareRecords(data,{left:{id:'comparison:rate-a'},right:{id:'comparison:rate-b'}});assert(rate.left.facts.financial);assert.equal(field(rate,'currencyBasis').applicable,true);assert.equal(field(rate,'currencyBasis').status,'CONFLICT');assert.equal(field(rate,'costClass').status,'CONFLICT');assert.equal(rate.compatibility.status,'CONFLICT');
  await add('comparison:legal-a',{unit:'ha',quantityNature:'PHYSICAL_STOCK',legalState:'ADOPTED',legalRole:'LEP_STATUTORY_CONTROL'},'StatutoryControl');await add('comparison:legal-b',{unit:'ha',quantityNature:'PHYSICAL_STOCK',legalState:'ADOPTED',legalRole:'DCP_GUIDANCE'},'StatutoryControl');const legal=await E.compareRecords(data,{left:{id:'comparison:legal-a'},right:{id:'comparison:legal-b'}});assert.equal(field(legal,'legalRole').status,'CONFLICT');assert.equal(legal.compatibility.status,'CONFLICT');assert.equal(legal.officialRelationship,'UNKNOWN');
  await add('comparison:nested-unknown-a',{denominator:{population:'UNKNOWN'}});await add('comparison:nested-unknown-b',{denominator:{population:'UNKNOWN'}});const unknown=await E.compareRecords(data,{left:{id:'comparison:nested-unknown-a'},right:{id:'comparison:nested-unknown-b'}});assert.equal(field(unknown,'denominator').status,'UNKNOWN');assert.equal(unknown.compatibility.status,'UNKNOWN');
  await add('comparison:zero-denominator',{denominator:0});const zero=await E.compareRecords(data,{left:{id:'comparison:zero-denominator'},right:{id:'comparison:zero-denominator'}});assert.equal(field(zero,'denominator').status,'UNKNOWN');assert.equal(field(zero,'denominator').left,0);assert.equal(zero.compatibility.status,'UNKNOWN');
  await add('comparison:structured-denominator',{denominator:{population:0,unit:'person'}});const structured=await E.compareRecords(data,{left:{id:'comparison:structured-denominator'},right:{id:'comparison:structured-denominator'}});assert.equal(field(structured,'denominator').status,'UNKNOWN');assert.equal(structured.compatibility.status,'UNKNOWN');
 });
 await check('calendar execution roles use the actual task schema without inventing outcomes',async()=>{
  const C=require('./csoi-calendar.js'),task=clone(C.syntheticTasks(2026)[0]);let data=await M.registerScenario(d,C.scenarioPayload(task));const prior=M.domainIndex(data).get(task.id),recorded={...prior.data,csoiTask:{...task,executionStatus:'RECORDED'}};data=await M.commitDomainRevision(data,{id:task.id,expectedRevisionId:prior.revisionId,patch:{data:recorded},reason:'Synthetic recorded task comparison',observedAt:'2026-10-30T03:00:00Z'});const result=await E.compareRecords(data,{left:{id:task.id,revisionId:prior.revisionId},right:{id:task.id}});assert.equal(field(result,'observationRole').left,'PLANNED_RESEARCH');assert.equal(field(result,'observationRole').right,'RECORDED_EXECUTION');assert.equal(field(result,'observationRole').status,'CONFLICT');assert.equal(result.arithmetic,'NOT_PERFORMED');
 });
 await check('inert public source text stays data, source state and unknowns are retained',async()=>{
  const inert=clone(B);inert.nodes[0].detail='<img src=x onerror=alert(1)> literal public fixture';const c=await E.compareRecords(inert,{left:{id:'csp'},right:{id:'water'}});assert.equal(c.left.record.detail,inert.nodes[0].detail);assert.equal(c.arithmetic,'NOT_PERFORMED');assert.equal(c.officialRelationship,'UNKNOWN');assert.equal(field(c,'sourceRevision').status,'UNKNOWN');
 });
 assert.equal(await M.objectDigest(d),before);console.log('PASS dataset remains byte-identical after all comparisons');count++;
 console.log('comparison: '+count+' groups PASS');
})().catch(error=>{console.error(error);process.exitCode=1;});
