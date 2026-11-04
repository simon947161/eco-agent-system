'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=__dirname,hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=n=>JSON.parse(fs.readFileSync(path.join(root,n),'utf8'));
let count=0;const checks=[];
function check(name,fn){fn();count++;checks.push({name,status:'PASS'});}
(async()=>{
const sources=read('download-manifest.json'),claims=read('claims.json'),candidate=read('atlas-candidate.json'),book=read('workbook-inspection.json');
check('source IDs unique',()=>assert.equal(new Set(sources.map(s=>s.id)).size,sources.length));
check('download success and failure hashes distinguished',()=>{assert.equal(sources.filter(s=>s.status==='DOWNLOADED').length,13);for(const s of sources)assert(s.status==='DOWNLOADED'?/^[a-f0-9]{64}$/.test(s.sha256):s.sha256===null);});
check('all claims traceable including text-only leads',()=>{const ids=new Set([...sources.map(s=>s.id),'S16','S17']);for(const c of claims.claims){assert(ids.has(c.source_id));assert(c.locator&&c.paraphrase);assert(['VERIFIED','PARTIAL','UNVERIFIED','SUPERSEDED'].includes(c.verification));}});
check('November unverified claims not promoted',()=>{for(const id of ['C15','C16'])assert.equal(claims.claims.find(c=>c.id===id).verification,'UNVERIFIED');assert.equal(claims.claims.find(c=>c.id==='C14').verification,'VERIFIED');});
check('no transaction or ecological outcome admission',()=>{for(const id of ['G_TRANSACTIONS','G_OUTCOMES','G_AWTM','G_NOV_TEMPLATE'])assert.equal(claims.gaps.find(g=>g.id===id).state,'UNVERIFIED');});
check('all workbook sheets, headers and embedded instructions reviewed',()=>{assert.equal(book.sheets.length,2);assert.equal(book.sheets[0].cells.filter(c=>/^[A-X]6$/.test(c.cell)).length,24);assert(book.sheets.every(s=>s.state==='visible'&&s.validations.length===0&&s.cells.every(c=>c.formula===null)));assert.equal(book.external_parts.length,0);assert.equal(book.external_relationships.length,0);assert.equal(book.drawing_text.length,1);assert.equal(book.sha256,sources.find(s=>s.id==='S08').sha256);});
check('local Markdown links resolve',()=>{for(const file of fs.readdirSync(root).filter(f=>f.endsWith('.md'))){const text=fs.readFileSync(path.join(root,file),'utf8');for(const match of text.matchAll(/\]\(([^)]+)\)/g)){const ref=match[1].split('#')[0];if(ref&&!ref.startsWith('https://'))assert(fs.existsSync(path.resolve(root,ref)),file+': '+ref);}}});
check('seven requested reports present',()=>{for(const n of ['BIODIVERSITY_CREDITS_FOUNDATION_REPORT_ZH','NSW_BIODIVERSITY_CREDIT_LIFECYCLE','BIODIVERSITY_DATA_MODEL','REVERSE_AUCTION_TEMPLATE_AUDIT','BIODIVERSITY_EVIDENCE_REGISTER','FOUNDER_DECISION_BRIEF','CRP_HANDOFF'])assert(fs.statSync(path.join(root,n+'.md')).size>400);});
const report=fs.readFileSync(path.join(root,'BIODIVERSITY_CREDITS_FOUNDATION_REPORT_ZH.md'),'utf8');
const han=(report.match(/\p{Script=Han}/gu)||[]).length;
check('report teaching and scientific boundaries',()=>{assert(report.includes('虚构输入'));assert(report.includes('未运行官方 BAM-C'));assert(report.includes('ADMITTED WITH GAPS'));assert(!candidate.domain.entities.some(e=>e.data.officialApproval!==false));});
let rawVerification='NOT_RUN_NO_RAW_DIR';
if(process.env.CLIMATEOS_BIO_RAW_DIR){for(const source of sources.filter(s=>s.status==='DOWNLOADED'))assert.equal(hash(fs.readFileSync(path.join(process.env.CLIMATEOS_BIO_RAW_DIR,source.file))),source.sha256);rawVerification='PASS_13_ORIGINAL_FILES';checks.push({name:'13 original byte digests, including unchanged blank workbook',status:'PASS'});count++;}
let contractStatus='NOT_RUN_NO_CONTRACT_DIR';
if(process.env.CLIMATEOS_ATLAS_CONTRACT_DIR){
 const dir=process.env.CLIMATEOS_ATLAS_CONTRACT_DIR;
 for(const r of read('atlas-contract-receipt.json'))assert.equal(hash(fs.readFileSync(path.join(dir,path.basename(r.path)))),r.sha256);
 const d=require(path.join(dir,'atlas-domain.js')),m=require(path.join(dir,'atlas-model.js')),base=require(path.join(dir,'atlas-data.js'));
 const dataset={...structuredClone(base),domain:structuredClone(candidate.domain)};
 check('native pinned AtlasDomain.validate',()=>assert.deepEqual(d.validate(dataset),[]));
 assert.equal(dataset.domain.baseDigest,await m.objectDigest(base));
 assert(await m.verifyEvents(dataset.domain.events));
 for(const r of dataset.domain.revisions){const {id,...payload}=r;assert.equal(id,await m.objectDigest(payload));}
 checks.push({name:'base digest, immutable revisions and event chain',status:'PASS'});count++;
 check('official admission negative rejected',()=>{const x=structuredClone(dataset);x.domain.entities[0].admission='APPROVED';assert(d.validate(x).some(e=>e.startsWith('DOMAIN_OFFICIAL_PROMOTION')));});
 check('dangling endpoint negative rejected',()=>{const x=structuredClone(dataset);x.domain.assertions[0].to='MISSING';assert(d.validate(x).some(e=>e.startsWith('DOMAIN_ASSERTION')));});
 check('wrong endpoint revision negative rejected',()=>{const x=structuredClone(dataset);x.domain.assertions[0].toRevisionId=x.domain.entities[0].revisionId;assert(d.validate(x).some(e=>e.startsWith('DOMAIN_ENDPOINT_REVISION')));});
 const tamper=structuredClone(dataset.domain.revisions[0]);tamper.record.label+='tampered';const {id,...payload}=tamper;assert.notEqual(id,await m.objectDigest(payload));checks.push({name:'revision content tamper detected',status:'PASS'});count++;
 contractStatus='PASS_PINNED_NATIVE_STRUCTURE_AND_INTEGRITY_ONLY';
}
const result={task_id:'CLIMATEOS-BIO-CREDITS-FOUNDATION-002',result:'PASS',checks_passed:count,checks,han_character_count:han,rawVerification,contractStatus,runtime_import:'NOT_RUN',browser:'NOT_APPLICABLE_NO_UI_CHANGES',professional_review:'PENDING',transaction_verification:'NOT_RUN',ecological_outcome_verification:'NOT_RUN'};
fs.writeFileSync(path.join(root,'VALIDATION_RESULTS.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
