/* atlas-1: bounded, offline evidence contracts. Hashes prove bytes, not truth. */
(function(root){
'use strict';
const statuses=new Set(['EXPLICIT_OFFICIAL','RESEARCH_INFERRED','HYPOTHESIS_ONLY','SYNTHETIC','UNKNOWN','CONTRADICTED','SUPERSEDED']);
function canonical(v){
 if(v===null||typeof v==='boolean'||typeof v==='string')return JSON.stringify(v);
 if(typeof v==='number'){if(!Number.isFinite(v))throw Error('NON_FINITE');return JSON.stringify(v);}
 if(Array.isArray(v))return '['+v.map(canonical).join(',')+']';
 if(v&&Object.getPrototypeOf(v)===Object.prototype)return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';
 throw Error('UNSUPPORTED_VALUE');
}
async function digest(bytes){if(!(bytes instanceof Uint8Array))throw Error('BYTES_REQUIRED');return 'sha256:'+Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');}
async function objectDigest(value){return digest(new TextEncoder().encode(canonical(value)));}
function applicability(assertion,revision,context){
 if(!revision||!context?.date||!context?.region||!revision.validFrom||!revision.validTo||!revision.region)return 'UNKNOWN';
 if(![context.date,revision.validFrom,revision.validTo].every(x=>/^\d{4}-\d{2}-\d{2}$/.test(x)&&Number.isFinite(Date.parse(x))&&new Date(x).toISOString().slice(0,10)===x)||revision.validFrom>revision.validTo)return 'UNKNOWN';
 if(context.region!==revision.region||context.date<revision.validFrom||context.date>revision.validTo)return 'VERSION_OR_SCOPE_CONFLICT';
 if(assertion.revisionId!==revision.id)return 'VERSION_OR_SCOPE_CONFLICT';
 return assertion.status==='SYNTHETIC'?'SYNTHETIC_ONLY':'REQUIRES_REVIEW';
}
function validate(d){
 const issues=[];if(d.schemaVersion!=='atlas-1')issues.push('SCHEMA_VERSION');
 for(const key of ['sources','revisions','nodes','assertions','hypotheses','contentBlocks','events','edges'])if(!Array.isArray(d[key]))issues.push('ARRAY_REQUIRED:'+key);
 if(issues.length)return issues;
 for(const key of ['sources','revisions','nodes','assertions','hypotheses','contentBlocks']){const seen=new Set();for(const o of d[key]){if(!o.id||seen.has(o.id))issues.push('DUPLICATE_OR_MISSING_ID:'+key);seen.add(o.id);}}
 const nodes=new Map(d.nodes.map(n=>[n.id,n])),revs=new Map(d.revisions.map(r=>[r.id,r])),sources=new Map(d.sources.map(s=>[s.id,s]));
 for(const b of d.contentBlocks)if(!Number.isInteger(b.offset)||b.offset<0||!Number.isInteger(b.length)||b.length<1||!/^sha256:[a-f0-9]{64}$/.test(b.digest)||!sources.has(b.sourceId))issues.push('INVALID_BLOCK:'+b.id);
 for(const n of d.nodes)if(!n.logicalId||!n.versionId||!revs.has(n.revisionId))issues.push('NODE_IDENTITY:'+n.id);
 for(const e of d.edges)if(!nodes.has(e.from)||!nodes.has(e.to)||!d.assertions.some(a=>a.id===e.id&&a.from===e.from&&a.to===e.to))issues.push('EDGE_TARGET:'+e.id);
 for(const a of d.assertions){
  if(!nodes.has(a.from)||!nodes.has(a.to))issues.push('MISSING_TARGET:'+a.id);
  if(!statuses.has(a.status)||!revs.has(a.revisionId)||!a.assertedBy||!Array.isArray(a.evidenceRefs)||!Array.isArray(a.counterevidenceRefs))issues.push('INVALID_ASSERTION:'+a.id);
  if(a.status==='EXPLICIT_OFFICIAL'){
   const r=revs.get(a.revisionId);
   if(!a.reviewedBy||a.reviewStatus!=='APPROVED'||!a.evidenceRefs?.length||r?.classification==='SYNTHETIC'||nodes.get(a.from)?.status==='SYNTHETIC'||nodes.get(a.to)?.status==='SYNTHETIC')issues.push('OFFICIAL_WITHOUT_EVIDENCE:'+a.id);
   for(const e of a.evidenceRefs||[])if(sources.get(e.sourceId)?.verification!=='VERIFIED'||!e.locator||e.revisionId!==a.revisionId)issues.push('UNVERIFIED_ANCHOR:'+a.id);
  }
 }
 return issues;
}
function paths(d,from,to,{includeCandidates=false,maxDepth=8,limit=10}={}){
 if(!Number.isInteger(maxDepth)||maxDepth<1||maxDepth>20||!Number.isInteger(limit)||limit<1||limit>100)throw Error('BOUNDS_REQUIRED');
 const results=[];function visit(id,visited,path){if(results.length>=limit)return;if(id===to){results.push(path);return;}if(path.length>=maxDepth)return;
 for(const a of d.assertions){if(a.from!==id||visited.has(a.to)||['CONTRADICTED','SUPERSEDED','UNKNOWN'].includes(a.status)||(!includeCandidates&&['HYPOTHESIS_ONLY','RESEARCH_INFERRED'].includes(a.status)))continue;visit(a.to,new Set([...visited,a.to]),[...path,a.id]);}}
 visit(from,new Set([from]),[]);return results;
}
async function verifyEvents(events){let previous=null;const ids=new Set();for(let i=0;i<events.length;i++){const {digest:hash,...payload}=events[i];if(ids.has(payload.id)||payload.sequence!==i||payload.previousDigest!==previous||await objectDigest(payload)!==hash)return false;ids.add(payload.id);previous=hash;}return true;}
async function appendEvent(events,event){
 if(!await verifyEvents(events))throw Error('INVALID_HISTORY');
 if(!event.id||!event.objectId||!event.actor||!event.reason||!event.observedAt||!['ADD','REVIEW','CONTEST','RETRACT','SUPERSEDE'].includes(event.type))throw Error('INVALID_EVENT');
 if(events.some(e=>e.id===event.id))throw Error('DUPLICATE_EVENT');
 const payload={id:event.id,type:event.type,objectId:event.objectId,actor:event.actor,reason:event.reason,observedAt:event.observedAt,sequence:events.length,previousDigest:events.at(-1)?.digest??null};
 return [...events,Object.freeze({...payload,digest:await objectDigest(payload)})];
}
const api={canonical,digest,objectDigest,validate,applicability,paths,appendEvent,verifyEvents};root.AtlasModel=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
