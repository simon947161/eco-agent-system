const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const d=require('./atlas-data.js'),r=require('./atlas-route-layout.js'),m=require('./atlas-model.js');
const original=JSON.stringify(d),all=new Set(d.nodes.map(n=>n.id));
const layout=r.project(d,all);assert.equal(layout.nodes.length,15);assert.equal(layout.edges.length,16);
for(const n of layout.nodes){assert.deepEqual([n.x,n.y],r.positions[n.id]);assert(d.contentItems.some(c=>c.ownerNodeId===n.id));}
assert.equal(new Set(layout.nodes.map(n=>n.x+','+n.y)).size,15);
for(const e of layout.edges){assert(d.assertions.some(a=>a.id===e.id&&a.from===e.from&&a.to===e.to));const a=layout.nodes.find(n=>n.id===e.from),b=layout.nodes.find(n=>n.id===e.to);assert(r.path(a,b,e.candidate).startsWith(`M ${a.x} ${a.y}`));assert(r.path(a,b,e.candidate).endsWith(`${b.x} ${b.y}`));}
const partial=r.project(d,new Set(['csp','csp6','csp8']));assert.equal(partial.edges.length,2);for(const n of partial.nodes)assert.deepEqual([n.x,n.y],r.positions[n.id]);
assert(r.corridor(d,'csp').has('audit'));assert(!r.corridor(d,'csp').has('candidate'));assert(!r.corridor(d,'csp').has('lsps'));
assert.equal(m.paths(d,'csp','op').length,2);assert.equal(m.paths(d,'lsps','scope').length,2);assert.equal(m.findCrossPaths(d)[0].status,'HYPOTHESIS_ONLY');
assert.equal(JSON.stringify(d),original);
const html=fs.readFileSync(path.join(__dirname,'index.html'),'utf8'),js=fs.readFileSync(path.join(__dirname,'atlas.js'),'utf8');
assert.match(html,/<aside[^>]*id="inspector"[^>]*hidden/);assert(!html.includes('class="sidebar"'));assert.match(html,/atlas-route-layout.js/);assert.match(html,/id="textRoutesBtn"/);assert.match(html,/id="workspaceBtn"/);assert.match(html,/id="admissionBtn"/);assert.match(js,/root:'all'/);assert.match(js,/class:'stop-ring'/);assert.match(js,/returnToRoute/);assert.match(js,/HYPOTHESIS_ONLY/);
console.log('PASS: production route projection, model-backed continuous endpoints, stable partial expansion, distinct corridors/candidate exclusion, 127-item data unchanged, default map/hidden panel/utility entry contracts. Browser acceptance is separate.');
