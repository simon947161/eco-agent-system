/* Attributed public knowledge projections and conditional research templates. */
(function(root){
'use strict';
const S=typeof module!=='undefined'?require('./sources/csoi-source-observations.json'):root.CsoiSourceObservations,G=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;
const SPECS=[
 ['food','Food safety',['smrc-food'],'Food handling and registration research; statutory exemptions/current Food Act and Food Regulation Partnership remain unverified.',['activity and food handling','notification and registration facts','risk and inspection preparation','complaint or inspection evidence','proposed follow-up and training','human decision review']],
 ['ossm','On-site sewage',['smrc-ossm'],'Installation and operation approvals are distinct; reticulated sewer is not automatically an on-site case.',['system and sewer-service facts','installation versus operation approval evidence','risk and maintenance requirements','field inspection preparation','failure and land/water impact evidence','rectification and human closure review']],
 ['pools','Public pools and spas',['smrc-pools','nsw-health-act','nsw-health-reporting'],'Council notification guidance and NSW Health legislation summaries cite different Regulation editions; current duties are UNKNOWN.',['public-access and facility facts','notification and applicable regulation review','water-quality and disinfectant records','inspection and defect evidence','recheck proposal','human reporting review']],
 ['cooling','Cooling and warm water systems',['nsw-health-legionella','nsw-health-reporting'],'Published NSW Health information identifies regulated systems and independent-auditor roles; local allocation/current legal version UNKNOWN.',['system type and location facts','registration and authority review','risk-management and maintenance evidence','independent-auditor applicability review','inspection or defect follow-up','human notification/report review']],
 ['skin','Skin penetration',['nsw-health-skin','nsw-health-reporting'],'A procedure, its health-service context and published exclusions matter; not every beauty business follows this route.',['procedure and exclusion facts','notification and hygiene source review','inspection preparation','observations and improvement evidence','recheck and human decision review','annual reporting basis']],
 ['environment','Environmental health and complaints',['smrc-pollution','smrc-noise'],'Council, EPA and other authority roles require matter-specific review; a complaint is not proof of a breach.',['complaint and place facts','competent-authority review','current provision and jurisdiction review','observations and counterevidence','proposed referral or follow-up','human conclusion review']],
 ['ltw','Liquid trade waste',['smrc-ltw','nsw-ltw-guidelines'],'Discharge, sewer connection and exact guideline conditions are separate from a business label.',['discharge facts','missing information','guideline category and concurrence evidence','field and pretreatment review','monitoring and rectification','human closure/report review']],
 ['backflow','Backflow prevention',['smrc-backflow'],'Installed testable devices, hazard assessment and the applicable interval matter; no blanket annual obligation applies to every property.',['connection and device identity','testable-device and hazard evidence','applicable interval/current-rule review','test and defect evidence','repair and retest proposal','human notice/closure review']]
];
const bySource=new Map(S.observations.map(o=>[o.id,o]));
const domains=SPECS.map(([id,title,ids,summary,steps])=>({id,title,summary,localCouncilAssignment:'UNKNOWN',currentLegalVersion:'UNKNOWN',officialAdmission:'PENDING',sources:ids,workflowSteps:steps,children:ids.flatMap(sourceId=>{const source=bySource.get(sourceId);return (source?.knowledgeAnchors||[]).map(anchor=>({id:sourceId+':'+anchor.id,title:anchor.title,text:anchor.text,judgmentType:'EVIDENCE_INFERENCE',sourceId:source.intakeRecord.id,sourceUrl:source.url,sourceRevision:source.rawDigest,contentId:'csoi:source-note:'+source.id+':'+anchor.id,locator:anchor.locator,conditions:'Establish domain-specific facts and current legal applicability; this is a research summary.',exceptions:'Published exclusions, historical editions and unknown local responsibility require review.',reviewState:'PENDING',rights:'UNDERLYING_SOURCE_UNKNOWN_AUTHOR_RESEARCH_SUMMARY_ONLY'}));})}));
function applicable(domain,activity){
 if(activity.region&&!['NSW','Snowy Monaro, NSW, Australia','SYNTHETIC_PLACE'].includes(activity.region))return 'REJECTED_REGION';
 const yes=k=>activity[k]===true,no=k=>activity[k]===false;
 if(domain==='food')return yes('handlesFood')?'APPLICABLE_FOR_RESEARCH':no('handlesFood')?'NOT_APPLICABLE':'UNKNOWN';
 if(domain==='ossm')return no('onSiteSewage')?'NOT_APPLICABLE':yes('onSiteSewage')&&yes('reticulatedSewer')?'UNKNOWN_CONFLICTING_SYSTEMS':yes('onSiteSewage')&&no('reticulatedSewer')?'APPLICABLE_FOR_RESEARCH':'UNKNOWN';
 if(domain==='pools')return yes('publicPool')?'APPLICABLE_FOR_RESEARCH':no('publicPool')?'NOT_APPLICABLE':'UNKNOWN';
 if(domain==='cooling')return yes('coolingWaterSystem')||yes('warmWaterSystem')?'APPLICABLE_FOR_RESEARCH':no('coolingWaterSystem')&&no('warmWaterSystem')?'NOT_APPLICABLE':'UNKNOWN';
 if(domain==='skin')return yes('laserHairRemovalOnly')||yes('registeredPractitionerInHealthService')||no('deliberateSkinPenetration')?'NOT_APPLICABLE':yes('deliberateSkinPenetration')&&no('registeredPractitionerInHealthService')&&no('laserHairRemovalOnly')?'APPLICABLE_FOR_RESEARCH':'UNKNOWN';
 if(domain==='environment')return yes('pollutionComplaint')||yes('noiseComplaint')?'APPLICABLE_FOR_RESEARCH':no('pollutionComplaint')&&no('noiseComplaint')?'NOT_APPLICABLE':'UNKNOWN';
 if(domain==='ltw')return no('dischargesLiquidTradeWaste')||no('sewerConnection')?'NOT_APPLICABLE':yes('dischargesLiquidTradeWaste')&&yes('sewerConnection')?'APPLICABLE_FOR_RESEARCH':'UNKNOWN';
 if(domain==='backflow')return no('testableBackflowDevice')||no('waterConnection')?'NOT_APPLICABLE':yes('testableBackflowDevice')&&yes('waterConnection')?'APPLICABLE_FOR_RESEARCH':'UNKNOWN';
 return 'UNKNOWN';
}
function workflow(id,activity={}){
 if(G.inspectPayload(activity).length)throw Error('PHE_PUBLIC_INPUT_DENIED');
 const domain=domains.find(d=>d.id===id);if(!domain)throw Error('PHE_DOMAIN_REQUIRED');
 return {format:'csoi-phe-research-workflow-1',domain:id,classification:'SYNTHETIC_SCENARIO',applicability:applicable(id,activity),officialDecision:'BLOCKED',currentLegalVersion:'UNKNOWN',localResponsibleRole:'UNKNOWN',plannedOnly:true,steps:domain.workflowSteps.map((title,i)=>({id:'phe-template:'+id+':'+i,title,state:'PROPOSED',judgment:i===1?'RULE':i===domain.workflowSteps.length-1?'DISCRETION':'EVIDENCE_INFERENCE',sourceContentIds:domain.children.map(c=>c.contentId),evidence:'UNKNOWN',actualHours:'UNKNOWN',formalDecision:'NOT_ISSUED'})),counterexamples:'The negative condition means this research route is not automatically applicable; it is not a compliance clearance.'};
}
function backflowRule(){const source=bySource.get('smrc-backflow');return {classification:'PUBLIC',sourceId:source.intakeRecord.id,revisionId:source.rawDigest,url:source.url,locator:source.knowledgeAnchors[0].locator,intervalMonths:12,applicability:'TESTABLE_DEVICE',region:'Snowy Monaro, NSW, Australia',anchorVerified:false,currentVersionChecked:false,rights:'UNKNOWN',admission:'PENDING',limitation:'Observed public summary supports research; current legal applicability and formal source admission have not been approved.'};}
const examples={food:{handlesFood:true},ossm:{onSiteSewage:true,reticulatedSewer:false},pools:{publicPool:true},cooling:{coolingWaterSystem:true,warmWaterSystem:false},skin:{deliberateSkinPenetration:true,registeredPractitionerInHealthService:false,laserHairRemovalOnly:false},environment:{pollutionComplaint:true,noiseComplaint:false},ltw:{dischargesLiquidTradeWaste:true,sewerConnection:true},backflow:{testableBackflowDevice:true,waterConnection:true}};
// Explicit reading selections, not inferred regulatory or operational relationships.
// Resolve records in the existing registry; never seed a second graph or a work plan.
const OSSM_READING=[
 ['csoi:dcp:snowy2013:C9:3','snowy','On-site disposal and sewer-connection scope'],
 ['csoi:dcp:snowy2013:C9:3:1:b','snowy','Unavailable sewer connection and land suitability'],
 ['csoi:dcp:snowy2013:C9:3:1:b:soil','snowy','Soil evidence to review'],
 ['csoi:dcp:cooma2014:7:4:2:1','cooma','Historical installation approval references'],
 ['csoi:dcp:cooma2014:7:4:2:2:soil','cooma','Land, soil and terrain evidence to review'],
 ['csoi:dcp:cooma2014:7:4:inspections','cooma','Inspection-strategy reference remains a gap']
];
function readingDomains(clauseId){return OSSM_READING.some(([id])=>id===clauseId)?['ossm']:[];}
async function historicalContexts(dataset,domain){
 if(!domains.some(d=>d.id===domain))throw Error('PHE_DOMAIN_REQUIRED');
 const result={domain,relationship:'CURATED_READING_SELECTION',statutoryLinkage:'UNKNOWN',operationalLinkage:'UNKNOWN',officialAdmission:'PENDING',cards:[]};
 if(domain!=='ossm')return result;
 const M=typeof module!=='undefined'?require('./atlas-model.js'):root.AtlasModel,C=typeof module!=='undefined'?require('./csoi-clauses.js'):root.AtlasCSOIClauses;
 const outlines=typeof module!=='undefined'?{snowy:require('./sources/snowy-dcp-outline.json'),cooma:require('./sources/cooma-dcp-outline.json')}:{snowy:root.CsoiDcpOutline,cooma:root.CsoiCoomaDcpOutline};
 for(const [id,family,purpose]of OSSM_READING){
  const outline=outlines[family],expected=outline?.nodes.find(n=>n.id===id),entity=M.domainIndex(dataset).get(id),data=entity?.data?.csoiRecord?.data,clause=data?.dcpClause;
  const selected=!!expected&&!!clause&&data.sourceId===outline.sourceId&&data.sourceDigest===outline.sourceRevision&&clause.section===expected.section&&M.canonical(clause.anchor)===M.canonical(expected.anchor);
  const status=selected?await C.status(dataset,id):{current:false,status:'CURATED_CONTEXT_UNAVAILABLE',reasons:['SELECTED_SOURCE_OR_PAGE_MISSING_OR_CHANGED']};
  result.cards.push({id,purpose,family,label:expected?.label||id,sourceId:outline?.sourceId||'UNKNOWN',sourceRevision:outline?.sourceRevision||'UNKNOWN',clauseRevision:entity?.revisionId||'UNKNOWN',locator:selected?data.locator:expected?.locator||'UNKNOWN',anchor:expected?.anchor||null,summary:selected?data.summary:'The selected historical evidence is unavailable in this snapshot.',conditions:selected?clause.conditions:[],exceptions:selected?clause.exceptions:[],region:selected?entity.scope.region:'UNKNOWN',current:status.current,status:status.status,reasons:status.reasons,reviewPlans:(dataset.domain?.entities||[]).filter(e=>e.data?.csoiRecord?.data?.reviewPlan?.clauseId===id).map(e=>({id:e.id,date:e.data.csoiRecord.data.reviewPlan.date,clauseRevision:e.data.csoiRecord.data.reviewPlan.clauseRevisionId}))});
 }
 return result;
}
const api={domains,workflow,applicable,backflowRule,examples,historicalContexts,readingDomains,authority:{statutoryPowers:'UNKNOWN_PENDING_CURRENT_LEGISLATION',publicReferences:['NSW Health','NSW Food Authority — retrieval unavailable','NSW Water','Council published service pages','NSW EPA referral named in Council guidance'],localInternalAllocation:'UNKNOWN',formalDecisions:'NOT_DELEGATED'}};
root.CsoiPhe=api;root.AtlasCSOIPhe=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
