'use strict';
// Inspect a real source-backed default record, not a synthetic fixture.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const APP=path.resolve(__dirname,'../../..'),P=require(path.join(APP,'csoi-pages.js'));
const cachePath=path.join(APP,'sources/csoi-default-snapshot.js'),seed=require(cachePath);
const dataset=seed.snapshot.dataset;
const records=dataset.domain.entities.filter(e=>e.kind==='QuantifiedObservation'&&e.data?.csoiRecord?.data?.sourceId&&e.data.csoiRecord.sourceClass!=='SYNTHETIC'&&typeof e.data.csoiRecord.data.measurement?.unit==='string'&&e.data.csoiRecord.data.measurement.unit!=='UNKNOWN');
if(!records.length)throw Error('NO_KNOWN_UNIT_SOURCE_RECORD_AVAILABLE_FOR_CHECK');
const rows=records.map(e=>{const unit=e.data.csoiRecord.data.measurement.unit;return {id:e.id,kind:e.kind,classification:e.classification,sourceClass:e.data.csoiRecord.sourceClass,sourceId:e.data.csoiRecord.data.sourceId,revisionId:e.revisionId,measurementUnit:unit,topLevelDataUnit:e.data.unit??null,unfilteredVisible:P.queryFilter([e],{}).some(x=>x.id===e.id),unitFilterRetainsRecord:P.queryFilter([e],{unit}).some(x=>x.id===e.id)};});
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const report={at:new Date().toISOString(),format:'actual-source-unit-filter-readback-1',task:'COI-074',sourceCacheSHA256:hash(cachePath),pagesModuleSHA256:hash(path.join(APP,'csoi-pages.js')),datasetEntityCount:dataset.domain.entities.length,knownUnitSourceObservationCount:rows.length,incorrectlyExcluded:rows.filter(r=>r.unfilteredVisible&&!r.unitFilterRetainsRecord).length,status:rows.every(r=>r.unitFilterRetainsRecord)?'PASS_ACTUAL_SOURCE_RECORDS':'FAIL_REAL_SOURCE_UNIT_FILTER',rows,limitation:'Tests recorded-unit filtering only; no legal applicability, metric computability, source completeness or actual outcome is inferred.'};
fs.writeFileSync(path.join(__dirname,'source-unit-filter-readback.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({...report,rows:rows.slice(0,3)},null,2));
