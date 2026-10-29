/* Independent local checkpoint comparison for an exported public/synthetic snapshot. */
const fs=require('node:fs'),m=require('./atlas-model.js');
(async()=>{
 if(!process.argv[2])throw Error('Usage: node verify-snapshot.cjs FILE.json [sha256:expected]');
 const bytes=fs.readFileSync(process.argv[2]);if(bytes.length>10*1024*1024)throw Error('SNAPSHOT_TOO_LARGE');
 if(!await m.verifySnapshot(JSON.parse(bytes.toString('utf8')),process.argv[3]||null))throw Error('SNAPSHOT_INVALID_OR_CHECKPOINT_MISMATCH');
 console.log('PASS: dataset, linked history and content-root receipts match. Integrity only; no official signature or truth guarantee.');
})().catch(e=>{console.error(e.message);process.exitCode=1});
