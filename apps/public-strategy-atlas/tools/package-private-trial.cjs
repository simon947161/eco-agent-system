/* Build a static deployment from the existing app; never include QA/private files. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const app=path.resolve(__dirname,'..'),manifest=JSON.parse(fs.readFileSync(path.join(app,'.openai/hosting.json')));
if(manifest.project_id!=='appgprj_6ae5b063565c8191802c9d7f7eb3214b'||manifest.static?.directory!=='dist')throw Error('CSOI_HOSTING_IDENTITY_REQUIRED');
const html=fs.readFileSync(path.join(app,'index.html'),'utf8');
const assets=new Set(['index.html','COI_TASK_REGISTRY_V1_7.json',...Array.from(html.matchAll(/(?:src|href)="\.\/([^"#?]+)"/g),m=>m[1])]);
const out=path.join(app,'dist');fs.mkdirSync(out,{recursive:true});
const hashes={};
for(const file of [...assets].sort()){
 if(file.includes('..')||path.isAbsolute(file)||!(/\.(html|css|js|json)$/.test(file)))throw Error('UNSAFE_RUNTIME_ASSET');
 const bytes=fs.readFileSync(path.join(app,file));
 const dest=path.join(out,file);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,bytes);
 hashes[file]='sha256:'+crypto.createHash('sha256').update(bytes).digest('hex');
}
function files(dir,prefix=''){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?files(path.join(dir,e.name),prefix+e.name+'/'):[prefix+e.name]);}
if(files(out).some(file=>!assets.has(file)&&file!=='deployment-assets.json'))throw Error('UNEXPECTED_DIST_FILE');
fs.writeFileSync(path.join(out,'deployment-assets.json'),JSON.stringify({format:'csoi-static-assets-1',project_id:manifest.project_id,applicationBaseline:'13c64f44aa6b6dac40748bb7096a7dadd3d7352d',files:hashes},null,2)+'\n');
console.log('PASS: '+assets.size+' exact existing runtime assets packaged; no test outputs, private imports, dependencies or app behavior changes.');
