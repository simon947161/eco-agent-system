// Lightweight route-preview DOM contract. Real Chrome QA is still mandatory.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const d=require('./atlas-data.js'),html=fs.readFileSync(path.join(__dirname,'route-map-preview.html'),'utf8');
const match=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).filter(Boolean);
assert.equal(match.length,1);
assert.match(html,/src="\.\/atlas-data\.js"/);
assert.match(html,/href="\.\/index\.html"/);
assert.match(html,/SYNTHETIC ROUTES/);
assert.match(html,/HYPOTHESIS ONLY/);
assert.equal(d.nodes.length,15);assert.equal(d.edges.length,16);
class Element {
 constructor(tag){this.tag=tag;this.attrs={};this.children=[];this.handlers={};this.style={};this.textContent='';this.className='';this.classList={add:x=>this.className+=' '+x,remove:x=>this.className=this.className.replace(x,'')};}
 setAttribute(k,v){this.attrs[k]=String(v);if(k==='class')this.className=String(v);}
 append(...children){for(const c of children){c.parent=this;this.children.push(c);}}
 addEventListener(k,f){this.handlers[k]=f;}
 querySelectorAll(sel){return sel==='.drawn'?this.children.filter(c=>c.className.includes('drawn')):[];}
 remove(){this.parent.children=this.parent.children.filter(c=>c!==this);}
 scrollTo(){}
}
const names=['routeSvg','mapShell','selection','allRoutes','strategyOnly','planningOnly','showCandidates','zoomIn','zoomOut','resetView','closeSelection','clearFocus','selectionKind','selectionTitle','selectionStatus','selectionText'];
const e=Object.fromEntries(names.map(n=>[n,new Element(n)]));
const mockDocument={getElementById:k=>e[k],createElementNS:(_,tag)=>new Element(tag),addEventListener(){}};
new Function('window','document',match[0])({AtlasData:d},mockDocument);
const latest=()=>e.routeSvg.children.filter(c=>c.className.includes('drawn')).at(-1);
const count=kind=>latest().children.filter(c=>c.className.startsWith(kind)).length;
assert.equal(count('stop'),14);assert.equal(count('route-segment'),14);
e.showCandidates.handlers.click();assert.equal(count('stop'),15);assert.equal(count('route-segment'),16);
const stop=latest().children.find(c=>c.className.startsWith('stop'));stop.handlers.click();
assert.equal(e.selection.className.includes('hidden'),false);
assert(e.selectionTitle.textContent.length);
e.strategyOnly.handlers.click();assert.equal(e.strategyOnly.attrs['aria-pressed'],'true');
e.zoomIn.handlers.click();assert(e.routeSvg.style.width);
e.clearFocus.handlers.click();assert.equal(e.selection.className.includes('hidden'),true);
console.log('PASS route-preview: 15 existing nodes / 16 edges, station selection, candidate toggle, line filter, zoom and inspector closing.');
console.log('NOTE this is a mock-DOM smoke test, not real browser visual, keyboard or WCAG acceptance.');
