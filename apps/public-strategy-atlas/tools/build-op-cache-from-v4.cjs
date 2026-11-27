/* Append normal source records to the exactly verified v4 baseline. */
const fs=require('node:fs'),path=require('node:path'),M=require('../atlas-model.js'),O=require('../csoi-op-review.js'),S=require('../csoi-strategy-research.js'),Build=require('./build-csoi-boot.cjs');
(async()=>{
 const snapshot=JSON.parse(fs.readFileSync(process.argv[2],'utf8')),prefix=require('../qa/op-completion-20261102/baseline-prefix.json');
 if(!await M.verifySnapshot(snapshot)||await M.objectDigest(snapshot.dataset)!==prefix.datasetDigest)throw Error('EXACT_VERIFIED_V4_BASELINE_REQUIRED');
 const dataset=await O.apply(snapshot.dataset,S.bundles()),seed={format:'csoi-default-snapshot-cache-1',inputDigest:await M.objectDigest(Build.inputs()),snapshot:await M.exportSnapshot(dataset)};
 if(!await M.verifySnapshot(seed.snapshot))throw Error('NEW_CACHE_INVALID');
 fs.writeFileSync(path.resolve(__dirname,'../sources/csoi-default-snapshot.js'),`(function(root){const value=${JSON.stringify(seed)};root.CsoiDefaultSnapshot=value;if(typeof module!=='undefined')module.exports=value;})(typeof window!=='undefined'?window:globalThis);\n`);
 console.log('PASS: verified v4 prefix plus normal append APIs; full fresh registration equivalence remains a separate mandatory test.');
})().catch(e=>{console.error(e);process.exitCode=1});
