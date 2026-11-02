/* Browser QA transport only. No network, official retrieval or catalogue update. */
const fs=require('node:fs'),path=require('node:path');
const M=require('../atlas-model.js'),I=require('../atlas-intake.js'),C=require('../sources/public-catalogue.json');
(async()=>{
 const out=process.argv[2];if(!out)throw Error('QA_OUTPUT_DIRECTORY_REQUIRED');fs.mkdirSync(out,{recursive:true});
 const at='2026-10-30T00:00:00Z',digest=await M.objectDigest('QA ONLY simulated bytes');
 const {revisionId,...record}=structuredClone(C.sources[0]);
 Object.assign(record,{id:'qa-retrieval-only',title:'QA ONLY: simulated retrieval, not an official source',publisher:'Repository browser QA',officialUrl:'https://example.invalid/qa-source.pdf',directoryUrl:'https://example.invalid/qa-directory',rawDigest:null,geographicExtent:{label:'QA ONLY; no real geographic applicability'},extraction:{coverage:'NONE',anchors:[]},lineage:{supersedes:[],revisionLabel:'QA ONLY'}});
 const evidence={actor:'browser-qa',at,reason:'QA ONLY simulated observation; no network request or official evidence'};
 let c=await I.registerSource(C,record,{registeredAt:at,reason:evidence.reason});
 c=await I.appendStage(c,record.id,'DIRECTORY_OBSERVED',{...evidence,url:record.directoryUrl,directoryDigest:digest});
 c=await I.appendStage(c,record.id,'SOURCE_RETRIEVED',{...evidence,url:record.officialUrl,retrievedAt:at,httpStatus:200,byteLength:10,rawDigest:digest});
 const cases={retrieved:c};
 cases.verified=await I.appendStage(c,record.id,'RAW_BYTES_VERIFIED',{...evidence,rawDigest:digest});
 cases.withdrawn=await I.correctStage(cases.verified,record.id,'DIRECTORY_OBSERVED',{...evidence,reason:'QA ONLY withdrawal of simulated retrieval'});
 for(const [name,catalogue] of Object.entries(cases)){
  const d=await M.migrateDataset(require('../atlas-data.js'),require('../atlas-accounting.js').cases,catalogue),bundle=await M.exportSnapshot(d);
  if(!await M.verifySnapshot(bundle))throw Error('INVALID_QA_SNAPSHOT');
  fs.writeFileSync(path.join(out,name+'.json'),JSON.stringify(bundle));
 }
 console.log('PASS: three QA-only snapshots generated; public catalogue unchanged, no source fetched');
})().catch(error=>{console.error(error);process.exitCode=1;});
