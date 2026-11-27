/* Build a portable extended Atlas snapshot from the two verified public editions. */
const fs=require('node:fs');
const M=require('../atlas-model.js'),B=require('../csoi-boot.js'),R=require('../atlas-project-register.js');
async function run(){
 const pack=process.argv.includes('--write-cache');
 const target=process.argv.slice(2).find(a=>a!=='--write-cache');
 let d=await B.appendEditionSuffix(require('../sources/csoi-default-snapshot.js').snapshot.dataset,require('../sources/plan-edition-suffix.js'));
 const base=d;
 for(const family of ['DP','OP']){
  const t=await R.verify(family,require('../sources/project-table-'+family.toLowerCase()+'.json'));
  d=await R.add(d,family,t,t.rows.map(R.key));
 }
 const snapshot=await M.exportSnapshot(d);
 if(!await M.verifySnapshot(snapshot))throw Error('REGISTER_SNAPSHOT_INVALID');
 const data=JSON.stringify(snapshot);
 if(Buffer.byteLength(data)>M.SNAPSHOT_MAX_BYTES)throw Error('REGISTER_SNAPSHOT_EXCEEDS_IMPORT_LIMIT');
 const delta={format:'atlas-plan-edition-suffix-1',baseDigest:await M.objectDigest(base),datasetDigest:await M.objectDigest(d),sources:[],sourceEvents:[],revisions:d.domain.revisions.slice(base.domain.revisions.length),events:d.domain.events.slice(base.domain.events.length)};
 const bytes=Buffer.from(JSON.stringify(delta));
 const packed={byteLength:bytes.length,compressed:require('node:zlib').gzipSync(bytes,{level:9}).toString('base64')};
 const script="(function(root){const data="+JSON.stringify(packed)+";root.AtlasProjectRegisterCache=data;if(typeof module!=='undefined')module.exports=data;})(globalThis);\n";
 const path=require('node:path').join(__dirname,'../sources/project-register-cache.js');
 if(pack)fs.writeFileSync(path,script);
 else if(fs.readFileSync(path,'utf8')!==script)throw Error('PROJECT_REGISTER_CACHE_MISMATCH');
 if(target)fs.writeFileSync(target,data,{flag:'wx'});
 console.log('PASS',d.domain.entities.length,'entities',d.domain.revisions.length,'revisions',Buffer.byteLength(data),'bytes',snapshot.receipt?.datasetDigest||await M.objectDigest(d));
}
run().catch(e=>{console.error(e);process.exitCode=1;});
