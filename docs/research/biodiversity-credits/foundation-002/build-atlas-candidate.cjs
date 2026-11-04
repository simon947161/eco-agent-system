// Offline candidate builder. Requires read-only contracts extracted from the pinned PR130 commit.
'use strict';
const fs=require('node:fs'),path=require('node:path');
const contract=process.env.CLIMATEOS_ATLAS_CONTRACT_DIR;
if(!contract)throw Error('Set CLIMATEOS_ATLAS_CONTRACT_DIR to the pinned contract directory');
const m=require(path.join(contract,'atlas-model.js')),base=require(path.join(contract,'atlas-data.js'));
const claims=JSON.parse(fs.readFileSync(path.join(__dirname,'claims.json'),'utf8')).claims;
const receipts=JSON.parse(fs.readFileSync(path.join(__dirname,'download-manifest.json'),'utf8'));
const steps=[
['land','Area','土地与资格','S02','§4 Eligibility','土地界限/权益','可评估范围','所有者、评估人员、主管部门'],
['survey','Activity','现场调查','S01','Chapters3–5','调查设计、空间背景','样方与物种原始数据','生态调查团队、认可评估人员'],
['data','SourceArtifact','生态数据与质控','S01','§4–5','样方/物种/GIS','可追溯输入','调查人员、复核人员'],
['assessment','ImplementationMechanism','BAM正式评估','S03','Introduction','经复核调查','BSSAR、管理计划','认可评估人员'],
['calculation','ImplementationMechanism','预测信用计算','S01','§11.6–11.9','VI gain、面积/个体、方法规则','类别/数量和credit report','认可评估人员、部门审查'],
['agreement','PolicyRequirement','BSA与产权登记','S02','§5.5–5.8','申请、BSSAR、TFD和同意','协议和登记','所有者、部长/代表、LRS'],
['registry','SourceArtifact','信用发行与登记','S02','§5.8; §6.1–6.2','登记完成与法定记录','信用状态/持有/retirement记录','信用管理方、持有人'],
['market','ImplementationMechanism','供需匹配与交易','S10','Offset rules','类别、地域、批准条件','拟议匹配、转让/付款各自证据','买卖双方、Supply Fund或其他渠道'],
['stewardship','Activity','长期管理','S02','§6.3–6.4','BSA、资金、行动计划','行动/合规/年度报告','土地所有者、管理机构'],
['monitoring','Outcome','生态结果验证','S11','Repeat data collection','永久点基线与重复观测','结果评价及反证；本包无真实结果','生态人员、复核人员、土地所有者']
];
(async()=>{
const domain={format:'atlas-domain-1',algorithmVersion:'atlas-domain-sha256-1',baseDigest:await m.objectDigest(base),entities:[],assertions:[],revisions:[],events:[]};
async function revision(record){const payload={logicalId:record.id,parentRevision:null,record};const r={id:await m.objectDigest(payload),...payload};domain.revisions.push(r);domain.events=await m.appendEvent(domain.events,{id:'bio-foundation-event-'+domain.events.length,type:'ADD',objectId:r.id,actor:'climateos-research',reason:'Prepare unadmitted biodiversity foundation candidate',observedAt:'2026-11-05T00:00:00+11:00'});return {...record,revisionId:r.id};}
for(let order=0;order<steps.length;order++){
 const [id,kind,label,sourceId,locator,input,output,actors]=steps[order]; const source=receipts.find(s=>s.id===sourceId);
 const common={stationId:'area',state:'PROPOSED',classification:'LOCAL_RESEARCH',admission:'PENDING',provenance:{url:source.url,locator,sourceId,rawDigest:source.sha256?'sha256:'+source.sha256:null},scope:{region:'NSW',period:{from:null,to:null},boundary:'SCHEME_RESEARCH_NOT_PARCEL_APPLICABILITY'},gaps:['Current consolidated law and individual applicability not fully reviewed','No transaction or ecological outcome admitted','Independent professional review pending']};
 domain.entities.push(await revision({...common,id:'bio-foundation:'+id,kind,label,data:{status:'UNKNOWN',routeOrder:order+1,input,output,actors,authority:'BC Act/Regulation framework as described by official guidance; current legal text review incomplete',description:label+'制度研究节点；非真实项目完成记录',sourceIds:[sourceId],claimIds:claims.filter(c=>c.source_id===sourceId).map(c=>c.id),relatedKnowledgeRoutes:['Environmental markets (research topic)','Public policy (research topic)','Evidence governance (research topic)'],officialApproval:false}}));
}
for(let i=0;i<domain.entities.length-1;i++){
 const a=domain.entities[i],b=domain.entities[i+1];domain.assertions.push(await revision({id:'bio-foundation:link:'+i,stationId:'area',state:'PROPOSED',classification:'LOCAL_RESEARCH',admission:'PENDING',provenance:a.provenance,scope:a.scope,gaps:['Research navigation, not automatic legal causality or an approved transaction workflow'],from:a.id,to:b.id,fromRevisionId:a.revisionId,toRevisionId:b.revisionId,predicate:'RESEARCH_CANDIDATE',method:'biodiversity-foundation-reading-order-1',issuer:'climateos-research',reviewer:null,evidenceRefs:[a.provenance,b.provenance],counterevidenceRefs:[]}));
}
const candidate={purpose:'UNIMPORTED_RESEARCH_CANDIDATE',contractCommit:'e3d8f074e0e1ba5e9614c3f4c5a2b973746b2ab7',baseDataPath:'apps/public-strategy-atlas/atlas-data.js',domain};
fs.writeFileSync(path.join(__dirname,'atlas-candidate.json'),JSON.stringify(candidate,null,2)+'\n');
console.log('Built 10 domain candidates, 9 research links, 19 immutable revisions/events; no runtime import');
})().catch(e=>{console.error(e);process.exitCode=1;});
