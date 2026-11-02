'use strict';
// Audit-only Node preload. Observe the actual files loaded by unchanged tests.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),Module=require('node:module');
const app=path.resolve(__dirname,'../../..'),output=process.env.CSOI_READBACK_MODULE_RECEIPT;
const loaded=new Map();
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
for(const extension of ['.js','.json']){
 const original=Module._extensions[extension];
 Module._extensions[extension]=function(module,filename){
  if(!filename.startsWith(app+path.sep))return original(module,filename);
  const before=hash(filename);const result=original(module,filename);const after=hash(filename);
  loaded.set(filename,{file:filename,sha256AtLoad:before,sha256AfterLoad:after,stableDuringLoad:before===after});return result;
 };
}
process.on('exit',()=>{if(output)fs.writeFileSync(output,JSON.stringify({format:'actual-node-module-load-sha256-1',entry:process.argv[1],modules:[...loaded.values()]},null,2)+'\n');});
