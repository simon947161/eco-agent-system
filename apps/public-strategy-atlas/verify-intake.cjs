/* Offline verification; hashes do not grant source rights or official authority. */
const fs=require('node:fs'),I=require('./atlas-intake.js'),M=require('./atlas-model.js');
(async()=>{
 if(!process.argv[2])throw Error('Usage: node verify-intake.cjs CATALOGUE.json [sha256:checkpoint]');
 const bytes=fs.readFileSync(process.argv[2]);if(bytes.length>10*1024*1024)throw Error('CATALOGUE_TOO_LARGE');const c=JSON.parse(bytes);
 if(!await I.verifyCatalogue(c,process.argv[3]||null))throw Error('INVALID_CATALOGUE');
 console.log('PASS: source revisions, intake gates and event replay; '+await M.objectDigest(c));console.log(JSON.stringify(I.coverage(c),null,2));
})().catch(e=>{console.error(e.message);process.exitCode=1});
