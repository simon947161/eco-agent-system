const fs=require('fs'),path=require('path');
const APP='/tmp/csoi-integrity-audit-20261031/readonly-head/apps/public-strategy-atlas',OUT=__dirname;
const M=require(APP+'/atlas-model.js'),E=require(APP+'/atlas-execution.js'),P=require(APP+'/csoi-paths.js'),W=require(APP+'/csoi-work.js');
const seed=require(APP+'/sources/csoi-default-snapshot.js'),d=seed.snapshot.dataset;
const ids=[
 ['T01','CSP29.9基准观察','csoi:source-note:smrc-csp-full-2025:carbon-p30'],
 ['T02','CSP6.1战略目标','csoi:source-note:smrc-csp-full-2025:goal61'],
 ['T03','Delivery Program PHE公开关系','csoi:source-note:smrc-dp-2026:phe-csp61-p31'],
 ['T04','OP食品服务98%计划指标','csoi:published-plan:food-2026:service-kpi'],
 ['T05','LSPS封面采用日观察','csoi:source-note:smrc-lsps-2020:title-adoption'],
 ['T06','Water AMP版本和网络范围','csoi:source-note:smrc-water-amp-2025:revision-and-network-scope'],
 ['T07','Snowy土壤证据分支','csoi:dcp:snowy2013:C9:3:1:b:soil'],
 ['T08','Snowy历史110L/person/day','csoi:dcp-reference:snowy:potable-accommodation'],
 ['T09','Cooma土壤证据分支','csoi:dcp:cooma2014:7:4:2:2:soil'],
 ['T10','Bombala土壤证据分支','csoi:dcp:bombala2012:3:1:5:A9:soil'],
 ['T11','Council LTW范围网页','csoi:source-note:smrc-ltw:scope'],
 ['T12','Council Backflow年度测试网页','csoi:source-note:smrc-backflow:annual-testing']
];
(async()=>{
 const snapshotIntegrity=await M.verifySnapshot(seed.snapshot),before=await M.objectDigest(d);if(!snapshotIntegrity)throw Error('SNAPSHOT_INVALID');
 const rows=[];for(const [testId,topic,id]of ids){const r=M.domainIndex(d).get(id);if(!r)throw Error('MISSING_REAL_RECORD:'+id);const sourceId=r.data.csoiRecord.data.sourceId,source=d.domain.sourceCatalogue.sources.find(s=>s.id===sourceId),lineage=await P.discover(d,{from:id,to:sourceId,mode:'STRUCTURED'}),reverse=await P.discover(d,{from:sourceId,to:id,mode:'STRUCTURED'}),search=E.searchRecords(d,id,{includeUnknownScope:true,limit:100}),trace=W.reverseTrace(d,id),known=E.shortestPath(d,id,'csp6',{direction:'both',mode:'KNOWN_LINK'});
  const technical={testId,topic,id,sourceId,sourceTitle:source.title,sourceUrl:source.officialUrl,sourceRawDigest:source.rawDigest,sourceRevision:source.revisionId,recordRevision:r.revisionId,locator:r.provenance?.locator,recordCategory:r.data.csoiRecord.data.dcpClause?'AUTHORED_DCP_OBSERVATION':r.id.startsWith('csoi:published-plan')?'PUBLISHED_PLAN_OBSERVATION':r.id.startsWith('csoi:dcp-reference')?'HISTORICAL_REFERENCE_RATE':'AUTHORED_RESEARCH_NOTE',pageAnchor:r.data.csoiRecord.data.dcpClause?.anchor||null,governedInputCount:r.data.csoiRecord.inputs.length,sourceMetadataPinMatches:r.data.csoiRecord.data.sourceDigest===source.rawDigest,lineage:lineage.status,lineageNodeIds:lineage.path?.core.nodePins.map(n=>n.id)||[],reverseLineage:reverse.status,knownOfficialLinkToCsp:known.status,searchTotal:search.total,searchIncludesExactId:search.items.some(i=>i.record.id===id),officialAdmission:r.admission,traceOfficialMapping:trace.officialMapping,recordSummary:r.data.csoiRecord.data.summary,originalContentVerification:'PENDING_ROOT_ORIGINAL_VERIFICATION',semanticCompleteChain:'PARTIAL_NO_ADMITTED_OPERATIONAL_OR_OUTCOME_CHAIN',webRoute:'#/knowledge/'+encodeURIComponent(id),sourceRoute:'#/sources/'+encodeURIComponent(sourceId)};
  if(lineage.path)technical.independentPathVerification=await P.verifyPath(d,lineage.path);rows.push(technical);
 }
 const missingQueries=['Council water operations emissions savings 2026 verified actual','QA_NO_SUCH_OFFICIAL_RELATION_20261031','current parcel consent permitted 29.9','7519'];const negativeQueries=missingQueries.map(q=>({query:q,total:E.searchRecords(d,q,{includeUnknownScope:true,limit:100}).total}));
 const missingSemantic=[['csp6','lsps'],['lsps','lep'],['lep','dcp'],['dcp','wbs:water:program'],['csoi:source-note:smrc-csp-full-2025:carbon-p30','wbs:water:program']].map(([from,to])=>({from,to,mode:'KNOWN_LINK',result:E.shortestPath(d,from,to,{mode:'KNOWN_LINK',direction:'both'})}));
 const allNoteGaps=d.domain.entities.filter(e=>e.id.startsWith('csoi:source-note:')&&e.data.csoiRecord.inputs.length===0).map(e=>e.id);
 const output={sha:'744ab46b2bec2ad601da0c4ae528694a4c982154',generatedAt:new Date().toISOString(),snapshotIntegrity,datasetDigest:before,rows,negativeQueries,missingSemantic,routeDefinitions:require(APP+'/csoi-router.js').ROUTES,sourceNoteCapsulesWithoutGovernedInputs:allNoteGaps,unchangedAfterQueries:before===await M.objectDigest(d),limits:'Original bytes and factual wording must be independently checked by original-document audit; these are source/model/web traces, not12admitted statutory/causal chains.'};
 fs.writeFileSync(OUT+'/model-results.json',JSON.stringify(output,null,2)+'\n');console.log(JSON.stringify({snapshotIntegrity,paths:rows.length,sourceNoteGaps:allNoteGaps.length,governedLineageFound:rows.filter(r=>r.lineage==='FOUND_RESEARCH_ONLY').length,routeDefinitions:output.routeDefinitions.length,unchanged:output.unchangedAfterQueries}));
})().catch(e=>{console.error(e);process.exitCode=1});
