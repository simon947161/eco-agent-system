/* Export an audit input copy; never writes to source or the knowledge store. */
const fs=require('node:fs'),path=require('node:path');
const root='/tmp/csoi-integrity-audit-20261031',app=path.join(root,'readonly-head/apps/public-strategy-atlas');
const seed=require(path.join(app,'sources/csoi-default-snapshot.js'));
fs.mkdirSync(path.join(root,'coverage'),{recursive:true});
fs.writeFileSync(path.join(root,'coverage/default-dataset.json'),JSON.stringify(seed.snapshot.dataset));
console.log('PASS: snapshot copied to audit output only; source unchanged.');
