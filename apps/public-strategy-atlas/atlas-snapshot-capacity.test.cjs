const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path'),cp=require('node:child_process'),M=require('./atlas-model.js');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'atlas-snapshot-capacity-'));
try{
 assert.equal(M.SNAPSHOT_MAX_BYTES,32*1024*1024);
 const measured=Buffer.byteLength(JSON.stringify(require('./sources/csoi-default-snapshot.js').snapshot));assert(measured>10*1024*1024&&measured<M.SNAPSHOT_MAX_BYTES);
 const file=path.join(temp,'oversize.json'),proof=path.join(temp,'proof.json');const fd=fs.openSync(file,'w');fs.ftruncateSync(fd,M.SNAPSHOT_MAX_BYTES+1);fs.closeSync(fd);fs.writeFileSync(proof,'{}');
 for(const [script,args,message]of [['verify-snapshot.cjs',[file],'SNAPSHOT_TOO_LARGE'],['verify-paths.cjs',[file,proof],'IMPORT_LIMIT']]){const r=cp.spawnSync(process.execPath,[script,...args],{encoding:'utf8'});assert.equal(r.status,1);assert(r.stderr.includes(message));assert(!r.stderr.includes('Unexpected token'));}
 fs.writeFileSync(file,'{}');const invalid=cp.spawnSync(process.execPath,['verify-snapshot.cjs',file],{encoding:'utf8'});assert.equal(invalid.status,1);assert(invalid.stderr.includes('SNAPSHOT_INVALID_OR_CHECKPOINT_MISMATCH'));
 console.log('PASS: measured full OP snapshot fits bounded32MiB transfer; oversized files rejected before parsing, invalid in-limit contents still rejected.');
}finally{fs.rmSync(temp,{recursive:true,force:true});}
