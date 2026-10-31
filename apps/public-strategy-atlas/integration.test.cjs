const assert=require('node:assert/strict'),M=require('./atlas-model.js'),E=require('./atlas-execution.js'),D=require('./atlas-data.js'),A=require('./atlas-accounting.js'),C=require('./sources/public-catalogue.json');
(async()=>{
 const d=await M.migrateDataset(D,A.cases,C);
 const carbon=E.searchRecords(d,'29.9 t CO2e/person');assert(carbon.items.some(h=>h.record.id==='csp2035-carbon-per-capita-baseline'));
 assert(E.searchRecords(d,'',{kind:'WorkPackage'}).items.length>=2);
 assert(E.searchRecords(d,'LSPS',{kind:'SourceArtifact'}).items.some(h=>h.category==='source'));
 assert(E.searchRecords(d,'',{region:'SYNTHETIC_PLACE',date:'2026-10-29',kind:'StatutoryControl'}).items.every(h=>!h.applicability.startsWith('REJECTED')));
 assert.equal(E.searchRecords(d,'',{date:'2026-02-30'}).total,0);
 const page=E.searchRecords(d,'synthetic',{limit:2});assert.equal(page.items.length,2);assert.equal(page.nextOffset,2);assert.equal(E.searchRecords(d,'synthetic',{limit:2,offset:2}).offset,2);
 assert.deepEqual(E.diffRecords({a:1,b:'unchanged'},{a:2,b:'unchanged'}),[{field:'a',before:1,after:2}]);
 const old=M.domainIndex(d).get('synthetic-water-spend'),receipt=await E.derive(d,{formula:'COST_PER_OUTPUT',inputIds:[old.id,'synthetic-water-output']}),saved=await M.appendCalculation(d,receipt);
 const next=await M.commitDomainRevision(saved,{id:old.id,expectedRevisionId:old.revisionId,patch:{data:{...old.data,value:18000}},reason:'Visible synthetic revision'});assert.equal((await E.verifyDerivation(next,receipt)).status,'INVALIDATED_INPUT_REVISION');
 await assert.rejects(()=>M.commitDomainRevision(d,{id:old.id,expectedRevisionId:old.revisionId,patch:{data:{...old.data,value:-1}},reason:'Invalid finance'}),/INVALID_REVISION/);
 assert(await M.verifySnapshot(await M.exportSnapshot(next)));
 const tabular=M.densityFixture(D,1000,{table:true});assert.deepEqual(M.validateContent(tabular),[]);const root=tabular.contentItems.find(c=>c.id==='density:0');assert.equal(root.table.rows.length,101);root.table.columns[0]=null;assert(M.validateContent(tabular).some(i=>i.startsWith('CONTENT_TABLE')));
 console.log('PASS: unified numeric/unit/source/work search, typed scope filters/pagination, revision diffs and scenario editing with receipt invalidation and invalid finance rejection');
})().catch(e=>{console.error(e);process.exitCode=1});
