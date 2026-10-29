/* Queries operate on AtlasModel identities; synthetic execution is never Council progress. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
function assertions(d){return [...d.assertions,...(d.domain?.assertions||[])];}
function shortestPath(d,from,to,{direction='forward',mode='DISCOVERY_CANDIDATE',maxVisited=10000}={}){
 if(!['forward','reverse','both'].includes(direction)||!['KNOWN_LINK','DISCOVERY_CANDIDATE'].includes(mode)||!Number.isInteger(maxVisited)||maxVisited<1||maxVisited>100000)throw Error('QUERY_BOUNDS');
 const entities=M.domainIndex(d);if(!entities.has(from)||!entities.has(to))throw Error('QUERY_ENDPOINT');
 const edges=assertions(d).filter(a=>!['CONTRADICTED','SUPERSEDED','RETRACTED','CONTESTED'].includes(a.status||a.state));
 // No authority verifier is configured; local claims cannot create KNOWN_LINK.
 if(mode==='KNOWN_LINK')return {status:'UNKNOWN',path:[],nodeIds:[],reason:'No officially admitted authority-backed relationships are configured.',truncated:false};
 const adjacency=new Map();
 function add(a,b,id){if(!adjacency.has(a))adjacency.set(a,[]);adjacency.get(a).push({to:b,id});}
 for(const a of edges){if(direction!=='reverse')add(a.from,a.to,a.id);if(direction!=='forward')add(a.to,a.from,a.id);}
 const queue=[from],seen=new Set([from]),previous=new Map();let found=from===to,i=0;
 while(i<queue.length&&!found&&i<maxVisited){const current=queue[i++];for(const edge of adjacency.get(current)||[]){if(seen.has(edge.to))continue;seen.add(edge.to);previous.set(edge.to,{node:current,edge:edge.id});queue.push(edge.to);if(edge.to===to){found=true;break;}}}
 if(!found)return {status:'UNKNOWN',path:[],nodeIds:[],reason:'No eligible bounded path; context or missing relationships may prevent traversal.',truncated:i>=maxVisited};
 const path=[],nodeIds=[to];let cursor=to;while(cursor!==from){const p=previous.get(cursor);path.push(p.edge);nodeIds.push(p.node);cursor=p.node;}
 return {status:'DISCOVERY_CANDIDATE',path:path.reverse(),nodeIds:nodeIds.reverse(),reason:'Model path only. Synthetic/research links do not establish causation, statutory authority or official implementation.',truncated:false};
}
function workBreakdown(d,stationId,{limit=200}={}){
 if(!Number.isInteger(limit)||limit<1||limit>1000)throw Error('WBS_BOUNDS');
 const entities=M.domainIndex(d);if(!entities.has(stationId))throw Error('WBS_STATION');
 const queue=[{id:stationId,depth:0}],seen=new Set(),rows=[],relations=assertions(d).filter(a=>['HAS_ACTIVITY','RESOURCED_BY','FUNDED_BY','REPORTS_OUTPUT','MEASURED_BY','HAS_DEPENDENCY'].includes(a.predicate));
 for(let i=0;i<queue.length&&rows.length<limit;i++){const row=queue[i];if(seen.has(row.id))continue;seen.add(row.id);const entity=entities.get(row.id);rows.push({...row,entity,executionState:entity?.state||'UNKNOWN',evidenceState:entity?.admission||'UNKNOWN'});for(const a of relations.filter(a=>a.from===row.id)){queue.push({id:a.to,depth:row.depth+1,via:a.id});}}
 const included=new Set(rows.map(r=>r.id));
 const dependencies=relations.filter(a=>a.predicate==='HAS_DEPENDENCY'&&included.has(a.from));
 const pending=new Map(rows.map(r=>[r.id,dependencies.filter(a=>a.from===r.id).map(a=>a.to)])),order=[],ready=[...pending].filter(([,deps])=>!deps.length).map(([id])=>id);
 for(let i=0;i<ready.length;i++){const id=ready[i];if(order.includes(id))continue;order.push(id);for(const [target,deps] of pending){const next=deps.filter(dep=>dep!==id);if(next.length!==deps.length){pending.set(target,next);if(!next.length)ready.push(target);}}}
 return {stationId,rows,dependencies,dependencyOrder:order,dependencyCycle:order.length<rows.length,truncated:queue.some(r=>!seen.has(r.id)),execution:'RESEARCH_ONLY',evidence:'OFFICIAL_IMPLEMENTATION_UNKNOWN',gaps:['Public work ownership, approvals and outputs remain unverified.','Synthetic work states are not Council workflow approvals.']};
}
const api={assertions,shortestPath,workBreakdown};root.AtlasExecution=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
