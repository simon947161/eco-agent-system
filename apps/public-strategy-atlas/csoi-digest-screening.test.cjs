const assert=require('node:assert/strict'),G=require('./csoi-governance.js');
const digest='sha256:0423820741d95aec85b743f1bea95c8924cf4456210fcc99ebb0254b6f52ce15';
assert.deepEqual(G.inspectPayload({normalizedTextDigest:digest}),[]);
for(const value of ['0412 345 678','+61 4 1234 5678','qa@example.invalid',digest+' 0412 345 678','sha256:0412 345 678',digest.slice(0,-1)])assert(G.inspectPayload({note:value}).includes('POSSIBLE_PERSONAL_DATA'));
assert(G.inspectPayload({phoneNumber:digest}).includes('SENSITIVE_FIELD'));
console.log('PASS: exact SHA256 values are not phone numbers; ordinary/embedded contact data, malformed digests and sensitive keys remain blocked.');
