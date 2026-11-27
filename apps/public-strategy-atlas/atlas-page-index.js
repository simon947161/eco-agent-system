/* Read-only projections of exact source editions in the existing Atlas registry. */
(function(root){
'use strict';
const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel;
const I=typeof module!=='undefined'?require('./atlas-intake.js'):root.AtlasIntake;
const roots=typeof module!=='undefined'?require('./sources/pdf-page-roots.js'):root.AtlasPdfPageRoots;
const method='pymupdf-1.26.6-nfkc-ws-gray512-v1';
const verified=new WeakSet();
function edition(d,id){
 const source=d.domain?.sourceCatalogue?.sources.find(s=>s.id===id), receipt=roots[id];
 if(!source||!receipt||source.rawDigest!==receipt.rawDigest)return null;
 const stage=I.sourceStatus(d.domain.sourceCatalogue,id).stage;
 return {source,receipt,stage,current:I.STAGES.indexOf(stage)>=I.STAGES.indexOf('RAW_BYTES_VERIFIED')};
}
async function verify(d,id,body){
 const selected=edition(d,id);
 if(!selected||!body||body.method!==method||body.sourceId!==id||body.rawDigest!==selected.source.rawDigest||
    !Array.isArray(body.pages)||body.pages.length!==selected.receipt.pageCount||await M.objectDigest(body)!==selected.receipt.digest)
  throw Error('PDF_PAGE_RECEIPT_MISMATCH');
 for(const row of body.pages)Object.freeze(row);
 Object.freeze(body.pages);Object.freeze(body);verified.add(body);return body;
}
function pageView(d,id,body,page){
 const selected=edition(d,id);
 if(!verified.has(body)||!selected||body.rawDigest!==selected.source.rawDigest||body.sourceId!==id)throw Error('PDF_EDITION_MISMATCH');
 if(!Number.isInteger(page)||page<1||page>body.pages.length)throw Error('PDF_PAGE_OUT_OF_RANGE');
 const [textDigest,characters,width,height,rasterDigest]=body.pages[page-1], anchored=[],priorPages=new Map();
 const earlierIds=new Set(selected.source.lineage.supersedes);
 for(const record of d.domain.entities){
  const data=record.data?.csoiRecord?.data, anchor=data?.publicKnowledge?.anchor;
  if(!anchor||anchor.normalizedPageDigest!==textDigest)continue;
  if(data.sourceId===id&&data.sourceDigest===body.rawDigest&&anchor.pdfPage===page)anchored.push(record);
  if(earlierIds.has(data.sourceId)&&data.publicKnowledge.category==='OP_PAGE'){
   const earlier=d.domain.sourceCatalogue.sources.find(s=>s.id===data.sourceId&&s.rawDigest===data.sourceDigest);
   if(earlier)priorPages.set(earlier.id+'#'+anchor.pdfPage,{record,page:anchor.pdfPage});
  }
 }
 // Repeated text and nearly empty pages are weak edition matches. Historical
 // annotations and approval state stay attached to the earlier document.
 const historicalMatch=characters>=80&&priorPages.size===1&&body.pages.filter(row=>row[0]===textDigest).length===1
  ? [...priorPages.values()][0]:null;
 return {page,total:body.pages.length,textDigest,characters,width,height,rasterDigest,anchored,historicalMatch,current:selected.current,
  interpretation:anchored.length?'HAS_PINNED_RECORDS':'PAGE_INTERPRETATION_PENDING',legalApplicability:'UNKNOWN',officialAdmission:'PENDING'};
}
const api={edition,verify,pageView};root.AtlasPageIndex=api;if(typeof module!=='undefined')module.exports=api;
})(globalThis);
