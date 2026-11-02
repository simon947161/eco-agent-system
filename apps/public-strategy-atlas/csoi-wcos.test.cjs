'use strict';
const assert=require('node:assert/strict');
const W=require('./csoi-wcos.js');
let count=0;
function check(name,fn){fn();count++;console.log('PASS '+name);}
check('plan-level read-only fixture contains complete annual/field/report concept chain',()=>{const result=W.adapt(W.syntheticFixture());assert.equal(result.mode,'READ_ONLY');assert.equal(result.sync,'NOT_CONNECTED');assert.match(result.privateCompatibility,/BLOCKED/);assert.deepEqual(result.records.map(r=>r.kind),W.CHAIN);assert.equal(result.governmentAuthority,false);});
check('adapter refuses writes, private and protected records, forged release, arbitrary synthetic labels and PII',()=>{
 for(const classification of ['COUNCIL_PROTECTED','PERSONAL_PRIVATE','APPROVED_RELEASE','UNKNOWN'])assert.throws(()=>W.adapt({...W.syntheticFixture(),classification}),/CLASSIFICATION_DENIED/);
 assert.throws(()=>W.adapt(W.syntheticFixture(),{mode:'SYNC'}),/READ_ONLY/);
 const label=W.syntheticFixture();label.records[0].label='Claimed synthetic but changed private content';assert.throws(()=>W.adapt(label),/UNTRUSTED_SYNTHETIC/);
 const pii=W.syntheticFixture();pii.records[0].address='Do not retain';assert.throws(()=>W.adapt(pii),/PROTECTED_FIELD/);
});
check('public metadata needs trusted review callback and excludes business fields/unsafe URL',()=>{
 const metadata={format:W.FORMAT,classification:'PUBLIC',synthetic:false,sourceKind:'VETTED_PUBLIC_METADATA',records:[{id:'public-rule',kind:'PUBLIC_RULE_METADATA',label:'Public source metadata',url:'https://www.snowymonaro.nsw.gov.au/Water',sourceId:'smrc-backflow',revisionId:'sha256:fixture',locator:'Annual Testing',stationId:'water'}]};
 assert.throws(()=>W.adapt(metadata),/PUBLIC_SOURCE_REVIEW_REQUIRED/);assert.throws(()=>W.adapt(metadata,{verifyPublicSource:()=>false}),/PUBLIC_SOURCE_REVIEW_REQUIRED/);
 assert.equal(W.adapt(metadata,{verifyPublicSource:r=>r.sourceId==='smrc-backflow'}).records.length,1);
 metadata.records[0].url='javascript:alert(1)';assert.throws(()=>W.adapt(metadata,{verifyPublicSource:()=>true}),/UNSAFE_PUBLIC_URL/);
});
check('Food/LTW/Backflow conditional cross-search never grants all approvals by business/property name',()=>{
 assert.equal(W.conditionalServices({businessType:'restaurant'}).food,'UNKNOWN');assert.equal(W.conditionalServices({businessType:'restaurant'}).ltw,'UNKNOWN');assert.equal(W.conditionalServices({businessType:'restaurant'}).backflow,'UNKNOWN');
 const facts=W.conditionalServices({handlesFood:true,dischargesLiquidTradeWaste:false,sewerConnection:true,testableBackflowDevice:false,waterConnection:true});assert.equal(facts.food,'APPLICABLE_FOR_RESEARCH');assert.equal(facts.ltw,'NOT_APPLICABLE');assert.equal(facts.backflow,'NOT_APPLICABLE');assert.equal(facts.officialApproval,'BLOCKED');
 const all=W.conditionalServices({handlesFood:true,dischargesLiquidTradeWaste:true,sewerConnection:true,testableBackflowDevice:true,waterConnection:true});assert.equal(all.ltw,'APPLICABLE_FOR_RESEARCH');assert.equal(all.backflow,'APPLICABLE_FOR_RESEARCH');
});
check('LTW template distinguishes stages/classification/concurrence but cannot decide or approve',()=>{const flow=W.ltwWorkflow({dischargesLiquidTradeWaste:true,sewerConnection:true,ltwCategory:'C'});assert.equal(flow.stages.length,10);assert.equal(flow.category,'C');assert.equal(flow.categoryVerification,'UNKNOWN');assert.equal(flow.stages.find(r=>r.id==='APPROVAL_EVIDENCE').judgment,'FORMAL_DECISION');assert.ok(flow.stages.every(r=>r.completed===false&&r.sourceAnchor==='UNKNOWN'));});
check('backflow schedule requires testable device, date, applicable interval and matching scope',()=>{
 const device={testable:true,deviceType:'SYN-TESTABLE',lastTestDate:'2024-02-29',region:'SYNTHETIC_AREA'},rule={classification:'SYNTHETIC_SCENARIO',intervalMonths:12,deviceTypes:['SYN-TESTABLE'],region:'SYNTHETIC_AREA'};
 const due=W.backflowDue(device,rule,'2025-02-28');assert.equal(due.status,'DUE');assert.equal(due.dueDate,'2025-02-28');assert.equal(due.officialCompliance,'UNKNOWN');
 assert.equal(W.backflowDue(device,rule,'2025-03-01').status,'OVERDUE');assert.equal(W.backflowDue({...device,lastTestDate:'2025-02-28'},rule,'2025-03-01').status,'NOT_YET_DUE');
 assert.equal(W.backflowDue({propertyType:'commercial'},rule,'2025-03-01').status,'UNKNOWN');assert.equal(W.backflowDue({...device,testable:false},rule,'2025-03-01').status,'NOT_APPLICABLE');
 for(const bad of [{...rule,intervalMonths:null},{...rule,region:'OTHER'},{...rule,validTo:'2023-01-01'},{...rule,classification:'ADMITTED'}])assert.equal(W.backflowDue(device,bad,'2025-03-01').status,'UNKNOWN');
 assert.equal(W.backflowDue({...device,lastTestDate:'2025-02-30'},rule,'2025-03-01').status,'UNKNOWN');assert.throws(()=>W.backflowDue(device,rule,'2025-02-30'),/AS_OF_DATE/);
});
check('four judgment classes retain review boundaries and formal decisions are blocked',()=>{for(const kind of W.JUDGMENTS){const result=W.judgment(kind,{statement:'Synthetic question',sourceIds:[],reviewer:'synthetic-reviewer'});assert.equal(result.governmentApproval,false);if(kind==='FORMAL_DECISION')assert.equal(result.status,'BLOCKED');if(kind==='RULE')assert.equal(result.status,'UNKNOWN');}assert.throws(()=>W.judgment('OFFICIALLY_APPROVED'),/JUDGMENT_CLASS/);});
check('summary is synthetic only and never releases a small real aggregate',()=>{const rows=W.syntheticFixture().records;assert.equal(W.summary(rows,{synthetic:true}).denominator,12);assert.throws(()=>W.summary(rows),/REAL_RECORD/);assert.throws(()=>W.summary([{id:'customer-1'}],{synthetic:true}),/REAL_RECORD/);assert.throws(()=>W.summary(rows,{minimumCellSize:1,synthetic:true}),/SUMMARY_BOUNDS/);});
console.log('csoi-wcos: '+count+' groups PASS');
