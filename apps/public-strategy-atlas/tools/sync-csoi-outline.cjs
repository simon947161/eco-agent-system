/* Derive distributable metadata mirrors; authored JSON is the primary research file. */
const fs=require('node:fs'),path=require('node:path'),G=require('../csoi-governance.js');
const app=path.resolve(__dirname,'..'),assets=[['snowy-dcp-outline','CsoiDcpOutline'],['cooma-dcp-outline','CsoiCoomaDcpOutline']];
function validate(outline){
 if(outline.format!=='csoi-public-dcp-outline-1'||outline.originalBytesCommitted!==false||outline.rights!=='UNKNOWN'||outline.currentLaw!=='UNKNOWN'||outline.officialAdmission!=='PENDING'||G.inspectPayload(outline).length)throw Error('PUBLIC_AUTHORED_OUTLINE_REQUIRED');
 if(Object.keys(outline).some(k=>!['format','sourceId','sourceRevision','originalBytesCommitted','rights','currentLaw','officialAdmission','nodes','referenceMeasurements'].includes(k))||!Array.isArray(outline.nodes)||!outline.nodes.length||!Array.isArray(outline.referenceMeasurements))throw Error('OUTLINE_FIELDS');
 for(const node of outline.nodes)require('../csoi-clauses.js').validateNode(node);
 for(const reference of outline.referenceMeasurements)if(Object.keys(reference).some(k=>!['id','clauseId','value','unit','role','label'].includes(k))||!Number.isFinite(reference.value)||reference.value<0||reference.unit!=='L/person/day'||!outline.nodes.some(n=>n.id===reference.clauseId))throw Error('REFERENCE_FIELDS');
 return true;
}
function sync(){
 // Validate all assets before writing any mirror; filenames and public globals are fixed.
 const values=assets.map(([name,global])=>{const outline=JSON.parse(fs.readFileSync(path.join(app,'sources',name+'.json')));validate(outline);return {name,global,outline};});
 for(const {name,global,outline}of values)fs.writeFileSync(path.join(app,'sources',name+'.js'),`(function(root){const value=${JSON.stringify(outline)};root.${global}=value;if(typeof module!=='undefined')module.exports=value;})(typeof window!=='undefined'?window:globalThis);\n`);
 console.log('PASS: authored public outlines mirrored; no original bytes, source admission or facts generated');
}
if(require.main===module)sync();module.exports={validate,sync};
