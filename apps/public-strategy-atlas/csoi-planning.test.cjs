const assert=require('node:assert/strict'),M=require('./atlas-model.js'),X=require('./csoi-intake.js'),E=require('./atlas-execution.js');
(async()=>{
 const d=await X.registerSummaries(await M.migrateDataset(require('./atlas-data.js'),require('./atlas-accounting.js').cases,require('./sources/csoi-catalogue.json')),require('./sources/csoi-source-observations.json'));
 const rows=d.domain.entities.filter(e=>e.id.startsWith('csoi:published-plan:food-2026:'));assert.equal(rows.length,5);assert(rows.every(r=>r.admission==='PENDING'));
 const target=rows.find(r=>r.id.endsWith(':target')),funded=rows.find(r=>r.id.endsWith(':funded')),kpi=rows.find(r=>r.id.endsWith(':service-kpi'));assert.equal(target.data.value,84);assert.equal(funded.data.unit,'UNKNOWN');assert.equal(kpi.data.value,98);assert.equal(kpi.data.unit,'percent');assert.equal(target.data.csoiRecord.data.actualOutput,'UNKNOWN');
 assert(await M.verifySnapshot(await M.exportSnapshot(d)));await assert.rejects(()=>E.derive(d,{formula:'UNIT_CONVERSION',inputIds:[target.id],outputUnit:'count'}),/UNADMITTED_INPUTS/);
 const bad=structuredClone(d);bad.domain.entities.find(e=>e.id===target.id).data.value=999;assert(M.validate(bad).some(issue=>issue.includes('MEASUREMENT_RECEIPT_MISMATCH')));
 const req=d.domain.sourceCatalogue.sources.find(s=>s.recordType==='REQUIREMENT'&&s.directoryUrl==='https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting');if(req){const status=require('./atlas-intake.js').sourceStatus(d.domain.sourceCatalogue,req.id);assert.notEqual(status.ownerType,'ENVIRONMENT_ADMIN');assert.equal(status.access.state,'NOT_CHECKED');}
 console.log('PASS: exact reviewed OP bytes/anchor bind five planning records, unknown volume units stay unknown, target/funded/actual/money are distinct, source candidates stay pending and false typed values are rejected');
})().catch(e=>{console.error(e);process.exitCode=1});
