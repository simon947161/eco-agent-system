'use strict';
const assert=require('node:assert/strict');
const M=require('./atlas-model.js'),G=require('./csoi-governance.js');
const base=()=>({id:G.logicalId('CSOI_OPERATIONS','test:work'),ownerModule:'CSOI_OPERATIONS',layer:'L0',security:'PUBLIC',sourceClass:'SYNTHETIC',judgment:'OBSERVATION',authority:'INDEPENDENT_RESEARCH',scope:{region:'SYNTHETIC_PLACE',boundary:'DEMO_SERVICE',period:{from:'2026-07-01',to:'2027-06-30'}},inputs:[],data:{title:'Synthetic service work',quantity:12},sensitivity:{personalData:false,confidential:false,reidentifiable:false},provenance:{contentMode:'SYNTHETIC',rights:{mode:'SYNTHETIC_OWNED',basis:'Repository-authored synthetic test fixture'}},observedAt:'2026-10-30T00:00:00.000Z'});
(async()=>{
 const publicRecord=await G.makeRecord(base());assert(await G.verifyRecord(publicRecord));assert(G.assessPublic(publicRecord).allowed);
 assert(G.dependencies('WCOS_ADAPTER',['ATLAS_CORE','CSOI_OPERATIONS']));assert(!G.dependencies('ATLAS_CORE',['WCOS_ADAPTER']));assert.throws(()=>G.logicalId('CSOI_OPERATIONS','../secret?x'),/ID_BOUNDARY/);
 for(const security of ['PERSONAL_PRIVATE','COUNCIL_PROTECTED','APPROVED_RELEASE'])for(const layer of G.LAYERS){const record=await G.makeRecord({...base(),security,layer});for(const operation of ['STORAGE','IMPORT','EXPORT','SCREENSHOT','DISPLAY'])assert(!G.assessPublic(record,{operation}).allowed,security+'/'+layer+'/'+operation);}
 const spoof={...publicRecord,security:'APPROVED_RELEASE',release:{approved:true,reviewerRole:'HUMAN_REVIEWER',signed:true}};assert(G.assessPublic(spoof).reasons.includes('RELEASE_AUTHORITY_NOT_CONFIGURED'));
 await assert.rejects(()=>G.makeRecord({...base(),customerName:'Blocked top-level field'}),/UNKNOWN_RECORD_FIELD/);
 await assert.rejects(()=>G.makeRecord({...base(),councilApproved:true}),/UNKNOWN_RECORD_FIELD/);
 const emailScope=await G.makeRecord({...base(),scope:{...base().scope,region:'private@real-domain.example'}});assert(G.assessPublic(emailScope).reasons.includes('POSSIBLE_PERSONAL_DATA'));
 await assert.rejects(()=>G.makeRecord({...base(),sourceClass:'PUBLIC_AUTHORITY',data:{fullText:'Disguised public document'},provenance:{...base().provenance,url:'https://www.health.nsw.gov.au/phact/pages/default.aspx',locator:'test',sourceRevision:'edition'}}),/SYNTHETIC_RIGHTS_MISMATCH/);
 await assert.rejects(()=>G.makeRecord({...base(),provenance:{...base().provenance,fullText:'Concealed document'}}),/PROVENANCE_UNKNOWN_FIELD/);
 const cyclic={...base()};cyclic.data.self=cyclic;await assert.rejects(()=>G.makeRecord(cyclic),/PAYLOAD_CYCLE/);
 assert.equal(G.authority({...publicRecord,role:'MANAGER',approved:true},{action:'FORMAL_DECISION'}).allowed,false);assert.equal(G.authority(publicRecord,{action:'OUTLOOK_SEND'}).allowed,false);
 await assert.rejects(()=>G.makeRecord({...base(),judgment:'FORMAL_DECISION'}),/FORMAL_DECISION_NOT_AUTHORISED/);
 await assert.rejects(()=>G.makeRecord({...base(),authority:'COUNCIL'}),/COUNCIL_AUTHORITY_NOT_DELEGATED/);
 const cases=[
  [{...base(),data:{nested:{customerName:'Protected example'}}},'SENSITIVE_FIELD'],
  [{...base(),data:{note:'someone@real-domain.example'}},'POSSIBLE_PERSONAL_DATA'],
  [{...base(),data:{note:'04'+ '12345678'}},'POSSIBLE_PERSONAL_DATA'],
  [{...base(),data:{nested:{security:'COUNCIL_PROTECTED'}}},'PROTECTED_CONTENT_MARKER'],
  [{...base(),data:{link:'javascript:alert(1)'}},'UNSAFE_URL_SCHEME'],
  [{...base(),data:{admission:'ADMITTED'}},'UNVERIFIED_OFFICIAL_PROMOTION'],
  [{...base(),data:{governmentApproval:true}},'SENSITIVE_OR_OFFICIAL_FLAG'],
  [{...base(),aggregation:{minimumCell:5,cellCounts:[4,20],reidentificationReviewed:true,complementaryDisclosureChecked:true}},'SMALL_CELL_OR_DISCLOSURE_RISK'],
  [{...base(),aggregation:{minimumCell:1,cellCounts:[20],reidentificationReviewed:true,complementaryDisclosureChecked:true}},'SMALL_CELL_OR_DISCLOSURE_RISK'],
  [{...base(),aggregation:{minimumCell:5,cellCounts:[20],reidentificationReviewed:true}},'SMALL_CELL_OR_DISCLOSURE_RISK']
 ];
 for(const [input,reason]of cases){const assessment=G.assessPublic(await G.makeRecord(input));assert(assessment.reasons.includes(reason),reason);}
 const meta={...base(),id:'csoi:source',sourceClass:'PUBLIC_AUTHORITY',data:{title:'Official source metadata',publisher:'Official publisher',sourceRevision:'observed-edition'},provenance:{url:'https://www.health.nsw.gov.au/phact/pages/default.aspx',locator:'public legislative directory',sourceRevision:'observed-edition',contentMode:'METADATA_ONLY',rights:{mode:'METADATA_ONLY',basis:'URL/title bibliographic metadata only; document reuse UNKNOWN'}}};
 assert(G.assessPublic(await G.makeRecord(meta)).allowed);
 assert(G.assessPublic(await G.makeRecord({...meta,data:{...meta.data,fullText:'A copyrighted full body'}})).reasons.includes('METADATA_FIELD_NOT_PERMITTED'));
 const excerpt={...meta,data:{title:'Permitted short observation',excerpt:'A bounded attributed excerpt.'},provenance:{...meta.provenance,contentMode:'SHORT_EXCERPT',rights:{mode:'PERMITTED_SHORT_EXCERPT',basis:'Synthetic permission test; not a real source licence'}}};
 assert(G.assessPublic(await G.makeRecord(excerpt)).allowed);
 assert(!G.assessPublic(await G.makeRecord({...excerpt,data:{...excerpt.data,excerpt:'x'.repeat(501)}})).allowed);
 assert(!G.assessPublic(await G.makeRecord({...excerpt,data:{...excerpt.data,fullText:'Hidden excess'}})).allowed);
 const bundle=await G.exportPublic([publicRecord]);assert.deepEqual(await G.importPublic(JSON.stringify(bundle)),[publicRecord]);
 const changed=structuredClone(bundle);changed.records[0].data.quantity=13;await assert.rejects(()=>G.importPublic(JSON.stringify(changed)),/BUNDLE_DIGEST/);
 const forged=structuredClone(bundle);forged.records[0].security='COUNCIL_PROTECTED';forged.records[0].revisionId=await M.objectDigest(Object.fromEntries(Object.entries(forged.records[0]).filter(([k])=>k!=='revisionId')));const {digest,...payload}=forged;forged.digest=await M.objectDigest(payload);await assert.rejects(()=>G.importPublic(JSON.stringify(forged)),/PUBLIC_CHANNEL_DENIED/);
 const proto=JSON.parse('{"__proto__":{"polluted":true}}');assert(G.inspectPayload(proto).includes('UNSAFE_OBJECT_KEY'));assert.equal({}.polluted,undefined);
 console.log('PASS: CSOI module boundaries; 90 layer/channel deny checks; rights, nested PII, confidentiality, small-cell, forged release/authority and tampered bundle rejections.');
})().catch(e=>{console.error(e);process.exitCode=1;});
