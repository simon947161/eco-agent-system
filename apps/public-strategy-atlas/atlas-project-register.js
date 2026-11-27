/* Bounded source-table intake and optional local Project records in the Atlas registry. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
const roots=typeof module!=='undefined'?require('./sources/project-table-roots.js'):root.AtlasProjectTableRoots;
const verified=new WeakSet(), when='2026-11-27T22:15:00.000Z';
const known={DP:'61-21-13',OP:'68-22-10'};
function key(row){return [row.pdfPage,row.table,row.row].join('-');}
function identity(family,row){
 const parent='csoi:knowledge:'+family.toLowerCase()+'2026:november';
 return parent+(key(row)===known[family]?':nimmitabel-water':':table-row:'+key(row));
}
function label(family,row){
 const subject=[...row.places,...row.topics].join(' · ')||'Published project';
 return subject+' · '+family+' p.'+row.pdfPage+' row '+row.row;
}
function deepFreeze(value){if(value&&typeof value==='object'){for(const child of Object.values(value))deepFreeze(child);Object.freeze(value);}return value;}
async function verify(family,table){
 const root=roots[family];
 if(!root||table.sourceId!==root.sourceId||table.rawDigest!==root.rawDigest||await M.objectDigest(table)!==root.digest)
  throw Error('PROJECT_REGISTER_EDITION_MISMATCH');
 deepFreeze(table);verified.add(table);return table;
}
function search(family,table,{query='',code=null,page=null,offset=0,limit=16}={}){
 if(!verified.has(table)||table.sourceId!==roots[family]?.sourceId||!Number.isSafeInteger(limit)||limit<1||limit>100||!Number.isSafeInteger(offset)||offset<0)throw Error('PROJECT_REGISTER_QUERY');
 const terms=query.toLowerCase().trim().split(/\s+/).filter(Boolean);
 const rows=table.rows.filter(r=>(!code||r.codes.includes(code))&&(!page||r.pdfPage===page)&&terms.every(t=>[label(family,r),r.budgetCell,r.resourceCell,...r.codes].join(' ').toLowerCase().includes(t)));
 return {rows:rows.slice(offset,offset+limit),total:rows.length,next:offset+limit<rows.length?offset+limit:null};
}
function coverage(d,family,table){
 if(!verified.has(table)||table.sourceId!==roots[family]?.sourceId)throw Error('PROJECT_REGISTER_EDITION_MISMATCH');
 const index=M.domainIndex(d);
 const registered=table.rows.filter(r=>{
  const knowledge=index.get(identity(family,r))?.data?.csoiRecord?.data;
  return knowledge?.sourceDigest===table.rawDigest&&knowledge.publicKnowledge.anchor.pdfPage===r.pdfPage&&
   (key(r)===known[family]||knowledge.publicKnowledge.facts.receipt?.digest===r.digest);
 }).length;
 const activities=typeof module!=='undefined'?require('./sources/op-project-activities.js'):root.AtlasOpActivityRows;
 const resolved=family==='OP'&&activities?table.gaps.filter(gap=>activities.records.some(n=>{
  const data=index.get(n.id)?.data?.csoiRecord?.data;
  return n.anchor.pdfPage===gap.pdfPage&&n.facts.evidence.physicalRow===gap.row&&data?.sourceDigest===table.rawDigest&&data.publicKnowledge?.category==='PLAN_ACTIVITY_ROW';
 })).length:0;
 return {named:table.rows.length,registered,missing:table.rows.length-registered,unnamedRows:table.gaps.length,resolvedContinuations:resolved,unresolvedContinuations:table.gaps.length-resolved,
  unqualifiedAmounts:table.rows.filter(r=>r.amountAUD!==null).length,officialAdmission:'PENDING',actualSpend:'UNKNOWN'};
}
function releaseInventory(d){
 const index=M.domainIndex(d);
 return Object.entries(roots).map(([family,source])=>{
  const expected=Object.entries(source.rows);
  const found=expected.filter(([address,pin])=>{
   const [pdfPage,table,row]=address.split('-').map(Number);
   const data=index.get(identity(family,{pdfPage,table,row}))?.data?.csoiRecord?.data;
   return data?.sourceDigest===source.rawDigest&&data.publicKnowledge.anchor.pdfPage===pdfPage&&
    (address===known[family]||data.publicKnowledge.facts.receipt?.digest===pin);
  });
  const P=typeof module!=='undefined'?require('./atlas-page-index.js'):root.AtlasPageIndex;
  return {family,expected:expected.length,present:found.length,missing:expected.length-found.length,currentSource:P.edition(d,source.sourceId)?.current===true};
 });
}
function nodeFor(family,row){
 const source=roots[family], parent='csoi:knowledge:'+family.toLowerCase()+'2026:november',locator=family+' November edition, PDF '+row.pdfPage+', table '+row.table+', physical row '+row.row;
 return {id:identity(family,row),kind:'Project',category:'PLAN_TABLE_ROW',code:key(row),parentId:parent,title:label(family,row),
  summary:'Published '+(family==='DP'?'multi-year program':'annual plan')+' project row. Budget cell: '+(row.budgetCell||'UNKNOWN')+'. Actual spend, completion and outcome remain unknown.',
  locator,anchor:{pdfPage:row.pdfPage,normalizedPageDigest:row.pageDigest,parserVersion:'pymupdf-1.26.6-project-table-1',bbox:row.rowBox},
  facts:{sourceRevision:source.rawDigest,actualSpend:'UNKNOWN',actualExecution:'UNKNOWN',actualOutcome:'UNKNOWN',actualOutput:'UNKNOWN',officialAdmission:'PENDING',humanReview:'PENDING',family,receipt:row},
  relations:row.codes.map(code=>({type:'EXPLICIT_DOCUMENT_REFERENCE',targetId:'csoi:knowledge:csp2035:strategy:'+code,locator:locator+', CSP column'}))};
}
async function verifyNode(node,available){
 const family=node.facts.family,row=node.facts.receipt,expected=roots[family]?.rows[key(row)];
 if(!expected||row.digest!==expected||key(row)===known[family])return false;
 const {digest,...fields}=row;
 if(await M.objectDigest(fields)!==expected)return false;
 const printed=nodeFor(family,row);
 // A printed reference may be unresolved in an older snapshot. Every attached
 // reference must be printed, and the full code list stays in the receipt.
 printed.relations=printed.relations.filter(r=>available.has(r.targetId));
 return M.canonical(node)===M.canonical(printed);
}
async function add(d,family,table,selected){
 const K=typeof module!=='undefined'?require('./csoi-knowledge.js'):root.AtlasCSOIKnowledge;
 const P=typeof module!=='undefined'?require('./atlas-page-index.js'):root.AtlasPageIndex;
 if(!verified.has(table)||table.sourceId!==roots[family]?.sourceId||!P.edition(d,table.sourceId)?.current)throw Error('PROJECT_REGISTER_SOURCE_NOT_CURRENT');
 const ids=M.domainIndex(d),chosen=new Set(selected),records=[];
 if(chosen.size!==selected.length||selected.length>500||!selected.length)throw Error('PROJECT_REGISTER_SELECTION');
 for(const row of table.rows){
  if(!chosen.delete(key(row)))continue;
  const existing=ids.get(identity(family,row));
  if(existing){
   const c=existing.data?.csoiRecord?.data;
   if(c?.sourceDigest!==table.rawDigest||c.publicKnowledge?.anchor.pdfPage!==row.pdfPage||
      (key(row)!==known[family]&&c.publicKnowledge?.facts.receipt?.digest!==row.digest))throw Error('PROJECT_REGISTER_ID_CONFLICT');
   continue;
  }
  if(key(row)===known[family])throw Error('PROJECT_REGISTER_EXISTING_PROJECT_MISSING');
  const record=nodeFor(family,row);
  record.relations=record.relations.filter(r=>ids.has(r.targetId));
  records.push(record);
 }
 if(chosen.size)throw Error('PROJECT_REGISTER_ROW_UNKNOWN');
 if(!records.length)return d;
 return K.registerBundle(d,{format:'csoi-public-knowledge-1',sourceId:table.sourceId,sourceRevision:table.rawDigest,sourcePageCount:table.pageCount,rights:'UNKNOWN',currentVersion:'UNKNOWN',officialAdmission:'PENDING',originalBytesCommitted:false,records},{observedAt:when,existingParent:records[0].parentId});
}
async function addActivities(d){
 const b=typeof module!=='undefined'?require('./sources/op-project-activities.js'):root.AtlasOpActivityRows;
 const K=typeof module!=='undefined'?require('./csoi-knowledge.js'):root.AtlasCSOIKnowledge;
 return K.registerBundle(d,b,{observedAt:'2026-11-27T22:24:00.000Z',existingParent:b.records[0].parentId});
}
const api={key,identity,label,search,coverage,releaseInventory,verify,verifyNode,add,addActivities};root.AtlasProjectRegister=api;if(typeof module!=='undefined')module.exports=api;
})(globalThis);
