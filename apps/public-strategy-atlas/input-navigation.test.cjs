const assert = require('node:assert/strict');
const {inputNeighbours} = require('./csoi-paths.js');
const data = require('./sources/csoi-default-snapshot.js').snapshot.dataset;
const activity = 'csoi:knowledge:op2026:water:activity:service-requests';
const result = inputNeighbours(data, activity);
const references = result.rows.filter(row => row.direction === 'USES' && row.type === 'EXPLICIT_DOCUMENT_REFERENCE');
assert.equal(references.length, 2);
for (const ref of references) {
 const inbound = inputNeighbours(data, ref.id).rows.find(row => row.id === activity);
 assert.equal(inbound.direction, 'USED_BY');
 assert.equal(inbound.pin, ref.pin);
 assert.equal(inbound.pinStatus, 'HEAD_MATCH');
}
const source = result.rows.find(row => row.type === 'SOURCE_EDITION' && row.direction === 'USES');
assert(source.source);
assert(inputNeighbours(data, source.id).rows.some(row => row.id === activity));
const changed = structuredClone(data);
changed.domain.entities.find(e => e.id === references[0].id).revisionId = 'different-current-head';
assert.equal(inputNeighbours(changed, activity).rows.find(row => row.id === references[0].id).pinStatus, 'HISTORICAL_OR_MISSING');
assert.throws(() => inputNeighbours(data, 'absent'), /UNKNOWN_ID/);
console.log('PASS governed source, containment and printed cross-references traversed in both directions; stale pins stay historical');
