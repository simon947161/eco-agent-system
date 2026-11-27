const assert=require('node:assert/strict'),M=require('./atlas-model.js'),E=require('./atlas-execution.js'),D=require('./atlas-data.js'),A=require('./atlas-accounting.js');
(async()=>{
 let d=await M.migrateDataset(D,A.cases);const context={date:'2026-10-29',region:'SYNTHETIC_PLACE',spatialType:'SCENARIO_AREA',soughtEffect:'LEP_STATUTORY'};
 const candidates=await E.candidates(d,'legal-fixture:current',{context,limit:100});const wrong=candidates.find(c=>c.to==='legal-fixture:wrong-region');assert(wrong);assert.equal(wrong.status,'REJECTED_CANDIDATE');assert(wrong.rejectionReasons.includes('REJECTED_REGION'));assert(await E.verifyCandidate(d,wrong));
 assert(candidates.find(c=>c.to==='legal-fixture:draft').rejectionReasons.includes('REJECTED_DRAFT'));assert(candidates.find(c=>c.to==='legal-fixture:expired').rejectionReasons.includes('REJECTED_TIME'));
 await assert.rejects(()=>M.recordResearchReview(d,{candidate:wrong,question:'Does this control apply?',decision:'APPROVED_FOR_RESEARCH',reason:'Ignore region'}),/RESEARCH_REVIEW_INVALID/);
 d=await M.recordResearchReview(d,{candidate:wrong,question:'Does this control apply?',decision:'CONTESTED',reason:'Wrong synthetic jurisdiction'});assert(await M.verifySnapshot(await M.exportSnapshot(d)));assert(d.domain.entities.some(e=>e.kind==='ReviewDecision'&&e.data.decision==='CONTESTED'));
 await assert.rejects(()=>M.recordResearchReview(d,{candidate:wrong,question:'Official?',decision:'ADMITTED',reason:'forged'}),/RESEARCH_REVIEW_INVALID/);
 const forged={...wrong,status:'ADMITTED'};assert.equal(await E.verifyCandidate(d,forged),false);
 // Re-hashing edited explanations cannot reproduce the historical search verdict.
 for(const patch of [{rejectionReasons:[]},{signals:['EXPLICIT_REFERENCE']},{sourceNodeIds:[wrong.from,wrong.to]}, {falsifier:'Arbitrary'}, {basis:{...wrong.basis,count:0}}]){
  const {digest,...payload}={...wrong,...patch};
  assert.equal(await E.verifyCandidate(d,{...payload,digest:await M.objectDigest(payload)}),false);
 }
 const {digest:unused,basis,...legacy}=wrong;
 Object.assign(legacy,{format:'atlas-discovery-candidate-1',ruleVersion:'atlas-scope-signals-1'});
 assert(await E.verifyCandidate(d,{...legacy,digest:await M.objectDigest(legacy)}));
 const positive=(await E.candidates(d,'synthetic-water-spend',{limit:100})).find(c=>c.to==='synthetic-water-budget');
 assert(positive&&E.candidateReviewState(d,positive).eligible);
 d=await M.recordResearchReview(d,{candidate:positive,question:'Compare the two research fixtures?',decision:'APPROVED_FOR_RESEARCH',reason:'Compatible synthetic scope'});
 const budget=M.domainIndex(d).get(positive.to);
 d=await M.commitDomainRevision(d,{id:budget.id,expectedRevisionId:budget.revisionId,patch:{data:{...budget.data,sourceLost:true}},reason:'Simulated withdrawal'});
 assert(await E.verifyCandidate(d,positive));
 assert(E.candidateReviewState(d,positive).reasons.includes('DISCOVERY_ENDPOINT_CHANGED'));
 assert(E.candidateReviewState(d,positive).reasons.includes('REJECTED_SOURCE_LOST'));
 await assert.rejects(()=>M.recordResearchReview(d,{candidate:positive,question:'Reuse old receipt?',decision:'APPROVED_FOR_RESEARCH',reason:'Stale'}),/RESEARCH_REVIEW_INVALID/);
 d=await M.recordResearchReview(d,{candidate:positive,question:'Withdraw the earlier research decision?',decision:'RETRACTED',reason:'Synthetic source withdrawn'});
 assert(await M.verifySnapshot(await M.exportSnapshot(d)));
 const reversed=(await E.candidates(d,budget.id,{limit:100})).find(c=>c.to===positive.from);
 assert(reversed.rejectionReasons.includes('REJECTED_SOURCE_LOST'));
 const carbon=M.domainIndex(d).get('csp2035-carbon-per-capita-baseline');
 d=await M.registerScenario(d,{id:'false-carbon-price',kind:'QuantifiedObservation',stationId:'csp6',label:'Synthetic CO2e emissions per capita price confusion',data:{...carbon.data,id:'false-carbon-price',status:'SYNTHETIC',unit:'AUD/t_CO2e'},reason:'False dimensional meaning QA'});
 assert((await E.candidates(d,carbon.id,{limit:100})).find(c=>c.to==='false-carbon-price').rejectionReasons.includes('REJECTED_UNIT_MEANING'));
 const source=M.domainIndex(d).get('synthetic-water-spend');d=await M.registerScenario(d,{id:'lost-source',kind:'FinancialEntry',stationId:'water',label:'Synthetic water spend with lost source',data:{...source.data,id:'lost-source',sourceLost:true},reason:'Source-loss QA'});
 d=await M.registerScenario(d,{id:'different-year-spend',kind:'FinancialEntry',stationId:'water',label:'Synthetic water spend different year',data:{...source.data,id:'different-year-spend',period:'FY2025-26'},reason:'Wrong year QA'});
 assert((await E.candidates(d,source.id,{limit:100})).find(c=>c.to==='different-year-spend').rejectionReasons.includes('REJECTED_PERIOD'));
 const lost=(await E.candidates(d,source.id,{limit:100})).find(c=>c.to==='lost-source');assert(lost.rejectionReasons.includes('REJECTED_SOURCE_LOST'));
 assert.equal(E.shortestPath(d,'csp6','lsps',{mode:'KNOWN_LINK'}).status,'UNKNOWN');
 for(const candidate of candidates){assert(candidate.ruleVersion&&candidate.rationale&&candidate.alternativeExplanation&&candidate.falsifier);assert.equal(candidate.knownLink,'UNKNOWN');}
 console.log('PASS: explainable versioned multi-signal candidates with trace paths/alternatives/falsifiers/counterevidence, wrong-region/draft/period/source-loss rejections, persistent local review and forged official promotion prevention');
})().catch(e=>{console.error(e);process.exitCode=1});
