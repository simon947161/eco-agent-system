/* Offline reproducible snapshot receipt; optional expected digest is an external checkpoint. */
const model=require('./atlas-model.js');
const data=require('./atlas-data.js');
(async()=>{
 const audit=await model.auditSnapshot(data);
 if(process.argv[2]&&process.argv[2]!==audit.datasetDigest)throw Error('CHECKPOINT_MISMATCH');
 console.log(JSON.stringify(audit,null,2));
 if(audit.issues.length||!audit.historyValid)process.exitCode=1;
})().catch(e=>{console.error(e.message);process.exitCode=1});
