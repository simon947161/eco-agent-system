/* Run every Atlas native regression; preserve failures and emit inspectable results. */
const fs=require('node:fs'),path=require('node:path'),{spawnSync}=require('node:child_process');
const tests=fs.readdirSync(__dirname).filter(n=>n.endsWith('.test.cjs')).sort();
const results=tests.map(test=>{const r=spawnSync(process.execPath,[path.join(__dirname,test)],{encoding:'utf8'});process.stdout.write(r.stdout||'');process.stderr.write(r.stderr||'');return {test,status:!r.error&&r.status===0?'PASS_TESTED_HERE':'FAIL',exit:r.status,error:r.error?.message||null,stdout:r.stdout,stderr:r.stderr};});
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify({runner:'atlas-native-1',results},null,2)+'\n');
console.log(`${results.filter(r=>r.status==='PASS_TESTED_HERE').length}/${results.length} native Atlas suites passed. Browser/source coverage are separate.`);
if(!tests.length||results.some(r=>r.status!=='PASS_TESTED_HERE'))process.exitCode=1;
