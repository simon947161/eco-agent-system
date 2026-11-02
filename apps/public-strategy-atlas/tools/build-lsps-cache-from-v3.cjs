/* Append normal source records to an exactly verified v3 baseline; full rebuild equivalence is separately tested. */
const fs=require('node:fs'),path=require('node:path'),M=require('../atlas-model.js'),L=require('../csoi-lsps-context.js'),S=require('../csoi-strategy-research.js'),Build=require('./build-csoi-boot.cjs');
(async()=>{
 const snapshot=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),prefix=require('../qa/lsps-completion/baseline-prefix.json');
 if(!await M.verifySnapshot(snapshot)||await M.objectDigest(snapshot.dataset)!==prefix.datasetDigest)throw Error('EXACT_VERIFIED_V3_BASELINE_REQUIRED');
 const dataset=await L.apply(snapshot.dataset,S.bundles()),seed={format:'csoi-default-snapshot-cache-1',inputDigest:await M.objectDigest(Build.inputs()),snapshot:await M.exportSnapshot(dataset)};
 if(!await M.verifySnapshot(seed.snapshot))throw Error('NEW_CACHE_INVALID');
 fs.writeFileSync(path.resolve(__dirname,'../sources/csoi-default-snapshot.js'),`(function(root){const value=${JSON.stringify(seed)};root.CsoiDefaultSnapshot=value;if(typeof module!=='undefined')module.exports=value;})(typeof window!=='undefined'?window:globalThis);\n`);
 console.log('PASS: exact verified v3 baseline plus normal append APIs; full fresh registration equivalence remains a separate mandatory native test.');
})().catch(e=>{console.error(e);process.exitCode=1});
