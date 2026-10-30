const assert=require('node:assert/strict'),R=require('./csoi-router.js');
for(const route of R.ROUTES){const path=route.pattern.replace(':id','csp:content').replace(':domain','food'),parsed=R.parse(R.href(path,{q:'water & flow',year:'2026'}));assert.equal(parsed.name,route.name);assert.equal(parsed.query.q,'water & flow');assert.equal(parsed.query.year,'2026');}
assert.equal(R.parse('').path,'/atlas');assert.equal(R.parse('/').name,'atlas');assert.equal(R.parse('#/knowledge/a%3Ab').params.id,'a:b');
for(const value of ['https://evil.invalid/atlas','//evil.invalid/atlas','/knowledge/../atlas','/knowledge/%2F','/knowledge/%','/knowledge/%00','/atlas?x?y','/unknown','/atlas\\evil','/knowledge/'])assert.equal(R.parse(value).valid,false,value);
assert.deepEqual(R.queryState('q=first&q=second&token=SECRET&year=bad&page=-1&companion=yes'),{q:'first'});
assert.equal(R.href('/atlas',{q:'<img src=x>',password:'secret',year:'2026'}),'#/atlas?q=%3Cimg+src%3Dx%3E&year=2026');
assert.equal(R.companionUrl('https://example.invalid/index.html?token=secret#/audit','/knowledge/csp:content',{q:'carbon',token:'secret'}),'https://example.invalid/index.html#/knowledge/csp%3Acontent?companion=1&q=carbon');
for(const url of ['javascript:alert(1)','data:text/html,hello','https://user:password@example.invalid/'])assert.throws(()=>R.companionUrl(url,'/atlas'),/UNSAFE/);
assert.throws(()=>R.href('/unknown'),/INVALID/);assert.equal(R.parse('#/atlas?region=Snowy+Monaro').query.region,'Snowy Monaro');
const P=require('./csoi-pages.js');assert.equal(P.publicOnly([{id:'safe',status:'SYNTHETIC'},{id:'private',data:{security:'COUNCIL_PROTECTED'}},{id:'release',security:'APPROVED_RELEASE'}]).length,1);assert.equal(P.displayAllowed({data:{csoiRecord:{format:'csoi-record-1',security:'PUBLIC',data:{governmentApproval:true}}}}),false);
console.log('PASS: CSOI functional route manifest, deep links, bounded public query, hostile path and companion URL guards');
