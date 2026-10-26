import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=path.resolve(fileURLToPath(new URL('..',import.meta.url)));
const repo=path.resolve(root,'../..');
const read=p=>readFile(path.join(root,p),'utf8');
const index=await read('data/index.json'), manifest=JSON.parse(await read('data/manifest.json'));
if(createHash('sha256').update(index).digest('hex')!==manifest.index_sha256) throw new Error('Index digest mismatch');
const shards={};
for(const shard of JSON.parse(index).shards) {
  const text=await read('data/'+shard.file);
  if(createHash('sha256').update(text).digest('hex')!==shard.sha256) throw new Error('Shard digest mismatch: '+shard.file);
  shards[shard.file]=text;
}
const javascript=await readFile(path.join(repo,'cczps_lite/environmental_question_runtime/static/streamflow.js'),'utf8');
const sourceCommit=execFileSync('git',['rev-parse','HEAD'],{cwd:repo,encoding:'utf8'}).trim();
const bundle={index,indexSha256:manifest.index_sha256,shards,javascript,html:await read('worker/page.html'),
  release:{github_repository:'simon947161/eco-agent-system',github_commit:sourceCommit,adapter:'p02-sites-v1',snapshot_baseline:manifest.source_code_baseline}};
const handler=await read('worker/handler.mjs');
await mkdir(path.join(root,'dist/server'),{recursive:true});
await mkdir(path.join(root,'dist/.openai'),{recursive:true});
await writeFile(path.join(root,'dist/server/index.js'),handler+'\nexport default createWorker('+JSON.stringify(bundle)+');\n');
await writeFile(path.join(root,'dist/.openai/hosting.json'),await read('.openai/hosting.json'));
console.log(JSON.stringify({github_commit:sourceCommit,index_sha256:manifest.index_sha256,data_package_sha256:manifest.data_package_sha256}));
