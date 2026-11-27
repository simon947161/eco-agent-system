// Append the normal domain registrations, then serialize only the immutable suffix.
const fs = require('node:fs');
const path = require('node:path');
const M = require('../atlas-model.js');
const I = require('../atlas-intake.js');
const K = require('../csoi-knowledge.js');
const manifest = require('../sources/plan-editions-20261128.json');
const base = require('../sources/csoi-default-snapshot.js').snapshot.dataset;

function definitions(edition) {
 const family = edition.family.toLowerCase();
 const dp = family === 'dp';
 const title = dp ? 'Delivery Program 2025–2029' : 'Operational Plan 2026–2027';
 const sourceId = 'csoi:smrc-'+family+'-2026:20261128';
 const root = 'csoi:knowledge:'+family+'2026:november';
 const project = root+':nimmitabel-water';
 const registryId = 'csoi:smrc-'+family+'-2026:20261030';
 const common = {sourceRevision:edition.rawDigest, actualExecution:'UNKNOWN', actualSpend:'UNKNOWN',
  actualOutput:'UNKNOWN', actualOutcome:'UNKNOWN', humanReview:'PENDING', officialAdmission:'PENDING'};
 function node(suffix, kind, category, name, summary, facts, parentId, relations=[]) {
  const isRoot = !parentId;
  const pdfPage = isRoot ? 3 : edition.recordPage;
  const locator = title+' v'+edition.version+', PDF '+pdfPage+', '+(isRoot ? 'version register' : 'water operations projects, Nimmitabel row');
  return {id:root+suffix, kind, category, code:family.toUpperCase()+'-'+category, parentId, title:name, summary, locator,
   anchor:{pdfPage, normalizedPageDigest:isRoot ? edition.versionPageDigest : edition.rowPageDigest,
    parserVersion:manifest.parser,...(isRoot ? {} : {bbox:edition.rowBox})}, facts:{...common,...facts}, relations};
 }
 const rootNode = node('', 'DocumentRevision','PLAN_EDITION',title+' · v'+edition.version,
  'The version register records an organisational chart update on 3 November 2026.', {
   versionLabel:edition.version, editionDate:edition.editionDate,totalPages:edition.pages,reviewedPages:[3,edition.recordPage],
   versionConflict:'The directory identifies an adopted document. The version page also retains draft wording. Its legal currency and effective dates require independent confirmation.'},null);
 const work = node(':nimmitabel-water','Project','PLAN_PROJECT',family.toUpperCase()+' · Nimmitabel drinking-water planning',
  'Council lists preparation of a plan for the town water supply and consideration of recreational access to the supply dam.',{
   locality:'Nimmitabel', resolution:edition.resolution, cspCode:edition.csp, projectPeriod:'2026/27',
   plannedOutput:'Water supply management plan',condition:'Consider recreational access while protecting drinking-water quality. Access permission and delivery remain unknown.',
   sourceCellDigests:edition.cells},root);
 work.relations.push({type:'EXPLICIT_DOCUMENT_REFERENCE',targetId:'csoi:knowledge:csp2035:strategy:'+edition.csp,locator:work.locator+', CSP column'});
 const amount = node(':nimmitabel-water:budget','QuantifiedObservation','PLAN_BUDGET',
  family.toUpperCase()+' · Nimmitabel '+(dp?'program':'annual')+' budget',
  dp?'Amount printed for the project over the indicated delivery years.':'Amount printed in the annual project budget column.',{
   baseline:{value:edition.aud,scale:1,unit:'AUD',role:'PUBLISHED_PROJECT_BUDGET'}, budgetBasis:edition.budgetBasis,computability:'NOT_COMPUTABLE',
   timeInterval:{from:dp?'2025-07-01':'2026-07-01',to:dp?'2029-06-30':'2027-06-30',basis:dp?'Four-year program envelope; the project row marks 2026/27.':'Annual plan FY2026/27.'},
   duplicateCostRisk:'NO_ADDITION_ACROSS_PLAN_LEVELS'},project);
 const records=[rootNode,work,amount];
 if (!dp) records.push(node(':nimmitabel-water:resources','ResourceAccount','PLAN_RESOURCES',
  'Nimmitabel · planned resource types','The OP marks both internal and external resources. Hours, rates, contracts and funding shares remain unknown.',{
   resourceBasis:'Internal and external',labourHours:'UNKNOWN',fundingAllocation:'UNKNOWN'},project));
 return {title,registryId,bundle:{format:'csoi-public-knowledge-1',sourceId,sourceRevision:edition.rawDigest,sourcePageCount:edition.pages,
  rights:'UNKNOWN',currentVersion:'UNKNOWN',officialAdmission:'PENDING',originalBytesCommitted:false,records}};
}

async function appendEdition(dataset, edition) {
 const {title,registryId,bundle}=definitions(edition);
 const prior=dataset.domain.sourceCatalogue.sources.find(s=>s.id===registryId);
 if (!prior || prior.rawDigest===edition.rawDigest) throw Error('DISTINCT_PRIOR_EDITION_REQUIRED');
 const record={...structuredClone(prior),id:bundle.sourceId,title:title+' · November 2026 v'+edition.version,officialUrl:edition.url,
  rawDigest:edition.rawDigest,retrievedAt:edition.retrievedAt,adoptedAt:null,effectiveFrom:null,effectiveTo:null,amendedAt:null,supersededAt:null,currentAsOf:null,
  extraction:{parser:manifest.parser,version:'plan-row-review-1',coverage:'PARTIAL',totalPages:edition.pages,extractedPages:[],anchors:[]},
  lineage:{supersedes:[prior.id],revisionLabel:'Observed document edition '+edition.version+'; legal supersession UNKNOWN'},
  access:{state:'AVAILABLE',checkedAt:edition.retrievedAt,reason:'Edition downloaded from the official directory and independently rehashed.'}};
 delete record.revisionId;
 let catalogue=await I.registerSource(dataset.domain.sourceCatalogue,record,{registeredAt:edition.retrievedAt,reason:'Register a distinct observed edition; retain previous page and byte receipts.'});
 const evidence={actor:'independent-public-research',at:edition.retrievedAt,reason:'Observed official directory link and downloaded original; rights and legal currency pending.'};
 const stages = [
  ['DIRECTORY_OBSERVED',{url:manifest.directoryUrl,directoryDigest:manifest.directoryDigest}],
  ['SOURCE_RETRIEVED',{url:edition.url,httpStatus:200,retrievedAt:edition.retrievedAt,byteLength:edition.byteLength,rawDigest:edition.rawDigest}],
  ['RAW_BYTES_VERIFIED',{rawDigest:edition.rawDigest}]
 ];
 for(const [stage,details] of stages) catalogue=await I.appendStage(catalogue,record.id,stage,{...evidence,...details});
 return K.registerBundle({...dataset,domain:{...dataset.domain,sourceCatalogue:catalogue}},bundle);
}

function suffix(previous,next) {
 if(next.length<previous.length || next.slice(0,previous.length).some((v,i)=>M.canonical(v)!==M.canonical(previous[i]))) throw Error('HISTORICAL_PREFIX_CHANGED');
 return next.slice(previous.length);
}
async function build() {
 let next=base;
 for(const edition of manifest.editions) next=await appendEdition(next,edition);
 const before=base.domain, after=next.domain;
 if(M.canonical(before.assertions)!==M.canonical(after.assertions)) throw Error('UNEXPECTED_ASSERTION');
 const delta={format:'atlas-plan-edition-suffix-1',baseDigest:await M.objectDigest(base),datasetDigest:await M.objectDigest(next),
  sources:suffix(before.sourceCatalogue.sources,after.sourceCatalogue.sources),sourceEvents:suffix(before.sourceCatalogue.events,after.sourceCatalogue.events),
  revisions:suffix(before.revisions,after.revisions),events:suffix(before.events,after.events)};
 const heads=delta.revisions.map(r=>({...r.record,revisionId:r.id}));
 if(M.canonical(heads)!==M.canonical(suffix(before.entities,after.entities))) throw Error('EDITION_HEAD_MISMATCH');
 return delta;
}
if(require.main===module) build().then(delta=>{
 const file=path.join(__dirname,'../sources/plan-edition-suffix.js');
 const content='(function(root){const data='+JSON.stringify(delta)+';root.AtlasPlanEditionSuffix=data;if(typeof module!=="undefined")module.exports=data;})(typeof window!=="undefined"?window:globalThis);\n';
 if(process.argv.includes('--check')) {if(fs.readFileSync(file,'utf8')!==content) throw Error('EDITION_CACHE_MISMATCH');}
 else fs.writeFileSync(file,content);
 console.log('PASS',delta.baseDigest,'->',delta.datasetDigest,delta.revisions.length,'append-only domain records');
}).catch(e=>{console.error(e);process.exitCode=1;});
module.exports={definitions,appendEdition,build};
