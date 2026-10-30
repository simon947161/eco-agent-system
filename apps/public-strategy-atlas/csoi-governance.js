/* Public/synthetic CSOI contracts. Classification and analytical layer are independent. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
const FORMAT='csoi-record-1';
const MODULES=Object.freeze({
 ATLAS_CORE:Object.freeze({namespace:'atlas',owns:'source, content, semantic graph, immutable revisions and audit',dependsOn:[]}),
 CSOI_OPERATIONS:Object.freeze({namespace:'csoi',owns:'public/synthetic layered work, resources, calendar and draft assistance',dependsOn:['ATLAS_CORE']}),
 WCOS_ADAPTER:Object.freeze({namespace:'wcos-adapter',owns:'read-only abstract interface; never copies protected operational records',dependsOn:['ATLAS_CORE','CSOI_OPERATIONS']}),
 PHE_PUBLIC_PACK:Object.freeze({namespace:'phe',owns:'official-public reference knowledge; local assignments UNKNOWN',dependsOn:['ATLAS_CORE','CSOI_OPERATIONS']})
});
const SECURITY=Object.freeze(['PUBLIC','PERSONAL_PRIVATE','COUNCIL_PROTECTED','APPROVED_RELEASE']);
const LAYERS=Object.freeze(['L0','L1','L2','L3','L4','L5']);
const JUDGMENTS=Object.freeze(['RULE','OBSERVATION','EVIDENCE_INFERENCE','DISCRETION','FORMAL_DECISION','UNKNOWN']);
const SOURCES=Object.freeze(['PUBLIC_AUTHORITY','SYNTHETIC','INDEPENDENT_RESEARCH']);
const hash=/^sha256:[a-f0-9]{64}$/;
const idPattern=/^[a-z][a-z0-9-]*:[A-Za-z0-9][A-Za-z0-9:._/-]{0,190}$/;
const operations=new Set(['STORAGE','IMPORT','EXPORT','SCREENSHOT','DISPLAY']);
const RECORD_KEYS=new Set(['format','id','revisionId','ownerModule','layer','security','sourceClass','judgment','authority','scope','inputs','data','sensitivity','provenance','observedAt','state','previousRevisionId','history','aggregation']);
const PROVENANCE_KEYS=new Set(['contentMode','rights','url','locator','sourceRevision','rawDigest','retrievedAt','publisher','title']);
const forbiddenKeys=new Set(['__proto__','prototype','constructor']);
function plain(x){return !!x&&typeof x==='object'&&!Array.isArray(x)&&Object.getPrototypeOf(x)===Object.prototype;}
function day(s){return typeof s==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(s)&&Number.isFinite(Date.parse(s))&&new Date(s).toISOString().slice(0,10)===s;}
function safeURL(s){try{const u=new URL(s);return u.protocol==='https:'&&!u.username&&!u.password;}catch{return false;}}
function logicalId(moduleName,key){const module=MODULES[moduleName];if(!module||typeof key!=='string'||!/^[A-Za-z0-9][A-Za-z0-9:._/-]{0,160}$/.test(key))throw Error('CSOI_ID_BOUNDARY');return module.namespace+':'+key;}
function dependencies(moduleName,requested){return !!MODULES[moduleName]&&Array.isArray(requested)&&requested.every(k=>MODULES[moduleName].dependsOn.includes(k));}
// Bounded conservative screening complements, but cannot replace, authorised human review.
function inspectPayload(value){
 const issues=new Set(),queue=[{value,key:'',depth:0,ancestors:new Set()}];let visited=0;
 while(queue.length){const current=queue.pop(),v=current.value,k=current.key.toLowerCase();
  if(++visited>10000||current.depth>40){issues.add('PAYLOAD_BOUNDS');break;}
  if(typeof v==='string'){
   if(v.length>20000)issues.add('TEXT_BOUNDS');
   if(/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i.test(v)||/(?:\+61\s?\d|\b04\d{2})[\d\s()-]{6,}/.test(v))issues.add('POSSIBLE_PERSONAL_DATA');
   if(/\b(?:COUNCIL_PROTECTED|PERSONAL_PRIVATE|COMMERCIAL_IN_CONFIDENCE|CONFIDENTIAL_INTERNAL|EMPLOYEE_ONLY)\b/.test(v))issues.add('PROTECTED_CONTENT_MARKER');
   if(/^(?:javascript|data|vbscript):/i.test(v.trim()))issues.add('UNSAFE_URL_SCHEME');
   if(['authority','admission','decisionstatus','approvalstatus'].includes(k)&&['ADMITTED','COUNCIL_APPROVED','OFFICIAL_APPROVED','APPROVED'].includes(v))issues.add('UNVERIFIED_OFFICIAL_PROMOTION');
  }else if(v&&typeof v==='object'){
   if(current.ancestors.has(v)){issues.add('PAYLOAD_CYCLE');continue;}const ancestors=new Set(current.ancestors);ancestors.add(v);
   if(!Array.isArray(v)&&!plain(v)){issues.add('PLAIN_JSON_REQUIRED');continue;}
   for(const [key,child] of Object.entries(v)){
    if(forbiddenKeys.has(key))issues.add('UNSAFE_OBJECT_KEY');
    if(/^(customerName|personalName|streetAddress|residentialAddress|dateOfBirth|employeeId|customerId|phoneNumber|emailAddress|apiKey|accessToken|password|secret)$/i.test(key)&&child!==null&&child!==''&&child!==false)issues.add('SENSITIVE_FIELD');
    if(/^(containsPII|personalData|commercialConfidential|confidential|reidentifiable|governmentApproval|councilApproved)$/i.test(key)&&child===true)issues.add('SENSITIVE_OR_OFFICIAL_FLAG');
    queue.push({value:child,key,depth:current.depth+1,ancestors});
   }
  }else if(typeof v==='number'&&!Number.isFinite(v))issues.add('NON_FINITE');
  else if(!['boolean','number','undefined'].includes(typeof v)&&v!==null)issues.add('PLAIN_JSON_REQUIRED');
 }
 return [...issues].sort();
}
function validateRecord(record){
 const issues=[];if(!plain(record))return ['CSOI_RECORD_REQUIRED'];
 if(Object.keys(record).some(k=>!RECORD_KEYS.has(k)))issues.push('CSOI_UNKNOWN_RECORD_FIELD');
 if(record.format!==FORMAT)issues.push('CSOI_FORMAT');
 if(!MODULES[record.ownerModule]||typeof record.id!=='string'||!idPattern.test(record.id)||!record.id.startsWith((MODULES[record.ownerModule]?.namespace||'INVALID')+':'))issues.push('CSOI_ID_BOUNDARY');
 if(!hash.test(record.revisionId||''))issues.push('CSOI_REVISION');
 if(!SECURITY.includes(record.security))issues.push('SECURITY_CLASSIFICATION_REQUIRED');
 if(!LAYERS.includes(record.layer))issues.push('DATA_LAYER_REQUIRED');
 if(!SOURCES.includes(record.sourceClass))issues.push('SOURCE_CLASS_REQUIRED');
 if(!JUDGMENTS.includes(record.judgment))issues.push('JUDGMENT_REQUIRED');
 if(record.authority!=='INDEPENDENT_RESEARCH')issues.push('COUNCIL_AUTHORITY_NOT_DELEGATED');
 if(record.judgment==='FORMAL_DECISION')issues.push('FORMAL_DECISION_NOT_AUTHORISED');
 if(plain(record.scope)&&(Object.keys(record.scope).some(k=>!['region','boundary','period'].includes(k))||plain(record.scope.period)&&Object.keys(record.scope.period).some(k=>!['from','to'].includes(k))))issues.push('SCOPE_UNKNOWN_FIELD');
 if(!plain(record.scope)||typeof record.scope.region!=='string'||!record.scope.region||typeof record.scope.boundary!=='string'||!record.scope.boundary||!plain(record.scope.period)||!day(record.scope.period.from)||!day(record.scope.period.to)||record.scope.period.from>record.scope.period.to)issues.push('SCOPE_REQUIRED');
 if(!Array.isArray(record.inputs)||record.inputs.some(r=>!plain(r)||typeof r.id!=='string'||!hash.test(r.revisionId||''))||new Set(record.inputs.map(r=>r.id)).size!==record.inputs.length)issues.push('INPUT_IDENTITIES_REQUIRED');
 if(plain(record.sensitivity)&&Object.keys(record.sensitivity).some(k=>!['personalData','confidential','reidentifiable'].includes(k)))issues.push('SENSITIVITY_UNKNOWN_FIELD');
 if(!plain(record.data)||!plain(record.sensitivity)||['personalData','confidential','reidentifiable'].some(k=>typeof record.sensitivity[k]!=='boolean'))issues.push('DATA_AND_SENSITIVITY_REQUIRED');
 if(plain(record.provenance)&&(Object.keys(record.provenance).some(k=>!PROVENANCE_KEYS.has(k))||plain(record.provenance.rights)&&Object.keys(record.provenance.rights).some(k=>!['mode','basis'].includes(k))))issues.push('PROVENANCE_UNKNOWN_FIELD');
 if(!plain(record.provenance)||!['SYNTHETIC','METADATA_ONLY','SHORT_EXCERPT','RESEARCH_SUMMARY'].includes(record.provenance.contentMode))issues.push('CONTENT_MODE_REQUIRED');
 if(record.sourceClass==='PUBLIC_AUTHORITY'&&(!safeURL(record.provenance?.url)||typeof record.provenance?.locator!=='string'||!record.provenance.locator||!record.provenance.sourceRevision))issues.push('OFFICIAL_PUBLIC_PROVENANCE_REQUIRED');
 if(!plain(record.provenance?.rights)||!['SYNTHETIC_OWNED','METADATA_ONLY','PERMITTED_SHORT_EXCERPT','PERMITTED_REUSE','UNKNOWN'].includes(record.provenance.rights.mode)||typeof record.provenance.rights.basis!=='string'||!record.provenance.rights.basis||record.provenance.rights.basis.length>1000)issues.push('RIGHTS_BASIS_REQUIRED');
 if(record.sourceClass==='SYNTHETIC'&&(record.provenance?.contentMode!=='SYNTHETIC'||record.provenance?.rights?.mode!=='SYNTHETIC_OWNED')||record.sourceClass!=='SYNTHETIC'&&(record.provenance?.contentMode==='SYNTHETIC'||record.provenance?.rights?.mode==='SYNTHETIC_OWNED'))issues.push('SYNTHETIC_RIGHTS_MISMATCH');
 if(record.sourceClass==='PUBLIC_AUTHORITY'&&!['METADATA_ONLY','SHORT_EXCERPT'].includes(record.provenance?.contentMode))issues.push('PUBLIC_SOURCE_CONTENT_MODE');
 if(record.sourceClass==='INDEPENDENT_RESEARCH'&&(record.provenance?.contentMode!=='RESEARCH_SUMMARY'||record.provenance?.rights?.mode!=='PERMITTED_REUSE'))issues.push('RESEARCH_CONTENT_MODE');
 if(record.provenance?.url&&!safeURL(record.provenance.url))issues.push('UNSAFE_PROVENANCE_URL');
 if(record.state!==undefined&&!['ACTIVE','WITHDRAWN'].includes(record.state))issues.push('RECORD_STATE');
 if(record.previousRevisionId!==undefined&&record.previousRevisionId!==null&&!hash.test(record.previousRevisionId))issues.push('PREVIOUS_REVISION_ID');
 if(record.history!==undefined&&(!Array.isArray(record.history)||record.history.length>1000||record.history.some(e=>!plain(e)||Object.keys(e).some(k=>!['id','type','objectId','actor','reason','observedAt','sequence','previousDigest','digest'].includes(k))||typeof e.reason!=='string'||e.reason.length>1000||typeof e.actor!=='string'||e.actor.length>100)))issues.push('HISTORY_CONTRACT');
 if(record.aggregation!==undefined&&(!plain(record.aggregation)||Object.keys(record.aggregation).some(k=>!['minimumCell','cellCounts','reidentificationReviewed','complementaryDisclosureChecked'].includes(k))))issues.push('AGGREGATION_CONTRACT');
 if(record.observedAt===undefined||typeof record.observedAt!=='string'||!Number.isFinite(Date.parse(record.observedAt)))issues.push('OBSERVED_AT_REQUIRED');
 return [...new Set(issues)];
}
function assessPublic(record,{operation='EXPORT'}={}){
 const reasons=validateRecord(record);if(!operations.has(operation))reasons.push('PUBLIC_OPERATION_UNKNOWN');
 if(record?.security==='PERSONAL_PRIVATE'||record?.security==='COUNCIL_PROTECTED')reasons.push('PUBLIC_CHANNEL_DENIED');
 if(record?.security==='APPROVED_RELEASE')reasons.push('RELEASE_AUTHORITY_NOT_CONFIGURED');
 if(record?.security!=='PUBLIC')reasons.push('PUBLIC_ONLY');
 if(record?.sensitivity&&Object.values(record.sensitivity).some(v=>v===true))reasons.push('SENSITIVE_CONTENT_DENIED');
 const p=record?.provenance,d=record?.data||{};
 if(p?.contentMode==='METADATA_ONLY'){
  const permitted=new Set(['title','publisher','url','sourceRevision','adoptedAt','effectiveFrom','effectiveTo','retrievedAt','rawDigest','byteLength','mediaType','family','status','stationId','gap','licence','rightsStatus']);
  if(Object.keys(d).some(k=>!permitted.has(k)))reasons.push('METADATA_FIELD_NOT_PERMITTED');
  if(p.rights?.mode!=='METADATA_ONLY'&&p.rights?.mode!=='PERMITTED_REUSE')reasons.push('METADATA_RIGHTS_REQUIRED');
 }else if(p?.contentMode==='SHORT_EXCERPT'){
  if(!['PERMITTED_SHORT_EXCERPT','PERMITTED_REUSE'].includes(p.rights?.mode)||typeof d.excerpt!=='string'||d.excerpt.length>500||!d.excerpt||!p.url||!p.locator)reasons.push('SHORT_EXCERPT_NOT_PERMITTED');
  // A short excerpt permission must not accidentally carry an entire body in another field.
  if(Object.keys(d).some(k=>!['title','excerpt','note','sourceRevision','status'].includes(k))||typeof d.note==='string'&&d.note.length>1000)reasons.push('EXCERPT_FIELD_NOT_PERMITTED');
 }else if(p?.contentMode==='RESEARCH_SUMMARY'&&p.rights?.mode!=='PERMITTED_REUSE'&&record?.sourceClass!=='INDEPENDENT_RESEARCH')reasons.push('RESEARCH_RIGHTS_REQUIRED');
 if(p?.rights?.mode==='UNKNOWN')reasons.push('REUSE_PERMISSION_UNKNOWN');
 const a=record?.aggregation;
 if(a){if(!plain(a)||!Number.isInteger(a.minimumCell)||a.minimumCell<5||!Array.isArray(a.cellCounts)||!a.cellCounts.length||a.cellCounts.some(n=>!Number.isInteger(n)||n<a.minimumCell)||a.reidentificationReviewed!==true||a.complementaryDisclosureChecked!==true)reasons.push('SMALL_CELL_OR_DISCLOSURE_RISK');}
 reasons.push(...inspectPayload(record));
 return {allowed:reasons.length===0,operation,security:record?.security||'UNKNOWN',layer:record?.layer||'UNKNOWN',reasons:[...new Set(reasons)].sort(),humanReview:'REQUIRED_FOR_RELEASE_OR_OFFICIAL_USE'};
}
function assertPublic(record,options){const assessment=assessPublic(record,options);if(!assessment.allowed)throw Error('CSOI_PUBLIC_DENIED:'+assessment.reasons.join(','));return record;}
async function makeRecord(input){
 const structural=inspectPayload(input).filter(x=>['PAYLOAD_BOUNDS','PAYLOAD_CYCLE','PLAIN_JSON_REQUIRED','NON_FINITE','UNSAFE_OBJECT_KEY'].includes(x));if(structural.length)throw Error('CSOI_PAYLOAD_INVALID:'+structural.join(','));
 const {revisionId:ignored,...payload}=structuredClone(input);
 const record={...payload,format:FORMAT,revisionId:await M.objectDigest({...payload,format:FORMAT})};
 const issues=validateRecord(record);if(issues.length)throw Error(issues.join(','));return Object.freeze(record);
}
async function verifyRecord(record){try{if(validateRecord(record).length)return false;const {revisionId,...payload}=record;return await M.objectDigest(payload)===revisionId&&(!record.history||await M.verifyEvents(record.history));}catch{return false;}}
async function exportPublic(records){
 if(!Array.isArray(records)||records.length>10000)throw Error('CSOI_EXPORT_BOUNDS');
 for(const record of records){assertPublic(record,{operation:'EXPORT'});if(!await verifyRecord(record))throw Error('CSOI_RECORD_DIGEST');}
 const payload={format:'csoi-public-bundle-1',records,trust:'SELF_ATTESTED',officialAuthority:false};return {...payload,digest:await M.objectDigest(payload)};
}
async function importPublic(text){
 if(typeof text!=='string'||new TextEncoder().encode(text).length>2*1024*1024)throw Error('CSOI_IMPORT_BOUNDS');
 const bundle=JSON.parse(text);if(!plain(bundle)||bundle.format!=='csoi-public-bundle-1'||!Array.isArray(bundle.records)||bundle.records.length>10000||bundle.officialAuthority!==false||bundle.trust!=='SELF_ATTESTED')throw Error('CSOI_BUNDLE_FORMAT');
 const {digest,...payload}=bundle;if(await M.objectDigest(payload)!==digest)throw Error('CSOI_BUNDLE_DIGEST');
 for(const record of bundle.records){assertPublic(record,{operation:'IMPORT'});if(!await verifyRecord(record))throw Error('CSOI_RECORD_DIGEST');}return structuredClone(bundle.records);
}
function authority(record,{action='RESEARCH'}={}){return {allowed:action==='RESEARCH'&&record?.authority==='INDEPENDENT_RESEARCH',action,officialDecision:false,systemOfRecord:'COUNCIL_AUTHORISED_SYSTEM',reason:'Atlas/CSOI cannot issue, approve, send or overwrite Council business records; no authority verifier is configured.'};}
const api={FORMAT,MODULES,SECURITY,LAYERS,JUDGMENTS,logicalId,dependencies,inspectPayload,validateRecord,assessPublic,assertPublic,makeRecord,verifyRecord,exportPublic,importPublic,authority};
root.AtlasCSOIGovernance=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
