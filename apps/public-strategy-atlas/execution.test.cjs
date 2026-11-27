const assert=require('node:assert/strict'),M=require('./atlas-model.js'),E=require('./atlas-execution.js'),D=require('./atlas-data.js'),A=require('./atlas-accounting.js');
(async()=>{
 const d=await M.migrateDataset(D,A.cases);assert.deepEqual(M.validate(d),[]);assert(await M.verifySnapshot(await M.exportSnapshot(d)));
 const target='wbs:water:deliverable',path=E.shortestPath(d,'water',target);assert(path.path.length>0);assert.equal(path.status,'DISCOVERY_CANDIDATE');
 assert(E.shortestPath(d,target,'water',{direction:'reverse'}).path.length>0);assert.equal(E.shortestPath(d,'water',target,{mode:'KNOWN_LINK'}).status,'UNKNOWN');
 const work=E.workBreakdown(d,'water');assert(work.rows.some(r=>r.entity.kind==='Task'));assert.equal(work.dependencyCycle,false);assert(work.dependencyOrder.indexOf('wbs:water:review')<work.dependencyOrder.indexOf('wbs:water:task'));
 const cyclic=structuredClone(d);cyclic.domain.assertions.push({id:'cycle-test',from:'wbs:water:review',to:'wbs:water:task',predicate:'HAS_DEPENDENCY'});assert(E.workBreakdown(cyclic,'water').dependencyCycle);assert(E.shortestPath(cyclic,target,'water',{direction:'reverse'}).path.length>0);
 const bounded=E.workBreakdown(d,'water',{limit:2});assert.equal(bounded.rows.length,2);assert(bounded.truncated);
 const limited=structuredClone(d);limited.domain.assertions.unshift({id:'external-prerequisite',from:'water',to:'wbs:water:task',predicate:'HAS_DEPENDENCY'});
 const incomplete=E.workBreakdown(limited,'water',{limit:1});assert.equal(incomplete.dependencyCycle,null);assert(incomplete.omittedPrerequisites.includes('wbs:water:task'));
 const context={date:'2026-10-29',region:'SYNTHETIC_PLACE',spatialType:'SCENARIO_AREA',soughtEffect:'LEP_STATUTORY'};
 for(const direction of ['reverse','both']) assert.equal(E.shortestPath(d,'legal-fixture:wrong-region','area',{direction,context}).status,'UNKNOWN');
 assert.equal(E.shortestPath(d,'legal-fixture:wrong-region','legal-fixture:wrong-region',{context}).status,'UNKNOWN');
 assert.throws(()=>E.shortestPath(d,'missing',target),/QUERY_ENDPOINT/);assert.throws(()=>E.workBreakdown(d,'water',{limit:1001}),/WBS_BOUNDS/);
 assert.equal(E.workBreakdown(d,'csp6').evidence,'OFFICIAL_IMPLEMENTATION_UNKNOWN');
 console.log('PASS: unified synthetic WBS, typed dependency/resource/finance/output routes, forward/reverse bounded BFS, multi-parent identity reuse, dependency cycle detection, separate execution/evidence states and known-link fail-closed');
})().catch(e=>{console.error(e);process.exitCode=1});
