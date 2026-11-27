const assert=require('node:assert/strict'),M=require('./atlas-model.js'),P=require('./csoi-paths.js');
(async()=>{
 const d=structuredClone(require('./sources/csoi-default-snapshot.js').snapshot.dataset),request={left:[{from:'csoi:published-plan:food-2026:target',to:'csp6',mode:'STRUCTURED'}],right:[{from:'csoi:dcp-reference:snowy:potable-accommodation',to:'csoi:smrc-dcp-snowy-2013-amend3:20261030',mode:'STRUCTURED'}]};
 const left=await P.discover(d,request.left[0]),right=await P.discover(d,request.right[0]),expected=await P.comparePathSets(d,{left:[left.path.core.spec],right:[right.path.core.spec]});
 const exportOriginal=M.exportSnapshot;let exports=0;M.exportSnapshot=async value=>{exports++;return exportOriginal(value);};let actual;try{actual=await P.compareEndpointSets(d,request);}finally{M.exportSnapshot=exportOriginal;}assert.equal(exports,1);assert.deepEqual(actual,expected);assert.equal(actual.officialUse,'REJECTED_UNKNOWN_ADMISSION');assert.equal(actual.core.arithmetic,'NOT_PERFORMED');assert.equal(actual.right[0].core.nodePins.length,9);assert((await P.verifyComparison(d,actual)).integrity);
 const isolated=structuredClone(d),pending=P.compareEndpointSets(isolated,request);isolated.domain.entities[0].label='Caller mutation after transaction started';assert.deepEqual(await pending,expected);await assert.rejects(()=>P.compareEndpointSets(isolated,request));
 await assert.rejects(()=>P.compareEndpointSets(d,{...request,left:Array(5).fill(request.left[0])}),/PATH_SET_BOUNDS/);
 await assert.rejects(()=>P.compareEndpointSets(d,{...request,left:[{...request.left[0],trusted:true}]}),/PATH_ENDPOINT_FIELDS/);
 await assert.rejects(()=>P.compareEndpointSets(d,{...request,left:[{from:'missing-record',to:'csp6'}]}),/PATH_UNKNOWN/);
 assert.equal(await M.objectDigest(d),require('./qa/op-completion-20261102/cache-build-receipt.json').digest);
 console.log('PASS: endpoint discovery and path comparison share one fully verified isolated transaction, exact old proofs, unchanged admission/lineage, caller-mutation isolation, invalid snapshot and bounded/missing endpoint rejection.');
})().catch(e=>{console.error(e);process.exitCode=1});
