/* Derive distributable metadata mirrors; authored JSON is the primary research file. */
const fs=require('node:fs'),path=require('node:path'),G=require('../csoi-governance.js');
const app=path.resolve(__dirname,'..'),file=path.join(app,'sources/snowy-dcp-outline.json'),outline=JSON.parse(fs.readFileSync(file));
if(outline.format!=='csoi-public-dcp-outline-1'||outline.originalBytesCommitted!==false||outline.rights!=='UNKNOWN'||outline.currentLaw!=='UNKNOWN'||outline.officialAdmission!=='PENDING'||G.inspectPayload(outline).length)throw Error('PUBLIC_AUTHORED_OUTLINE_REQUIRED');
if(Object.keys(outline).some(k=>!['format','sourceId','sourceRevision','originalBytesCommitted','rights','currentLaw','officialAdmission','nodes','referenceMeasurements'].includes(k)))throw Error('OUTLINE_FIELDS');
for(const node of outline.nodes)require('../csoi-clauses.js').validateNode(node);
for(const reference of outline.referenceMeasurements)if(Object.keys(reference).some(k=>!['id','clauseId','value','unit','role','label'].includes(k))||!Number.isFinite(reference.value)||reference.unit!=='L/person/day'||!outline.nodes.some(n=>n.id===reference.clauseId))throw Error('REFERENCE_FIELDS');
fs.writeFileSync(path.join(app,'sources/snowy-dcp-outline.js'),`(function(root){const value=${JSON.stringify(outline)};root.CsoiDcpOutline=value;if(typeof module!=='undefined')module.exports=value;})(typeof window!=='undefined'?window:globalThis);\n`);
console.log('PASS: authored public JSON mirrored; no original bytes, source admission or facts generated');
