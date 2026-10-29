/* English public/synthetic Atlas. No Council business data or external runtime services. */
(() => {
'use strict';
const m=AtlasModel,fixtureSize=Number(new URLSearchParams(location.search).get('fixture'));
const d=[60,200].includes(fixtureSize)?m.densityFixture(AtlasData,fixtureSize):AtlasData,NS='http://www.w3.org/2000/svg';
const $=id=>document.getElementById(id),graph=$('atlasGraph'),details=$('details'),empty=details.innerHTML;
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const byId=new Map(d.nodes.map(n=>[n.id,n])),contentById=new Map(d.contentItems.map(c=>[c.id,c]));
const state={view:'relationships',root:'csp',selected:null,contentRoot:'csp:content',contentSelected:null,mode:'coverage',candidates:false,neighbours:true,incremental:false,expanded:new Set(['csp','lsps']),contentExpanded:new Set(['csp:content']),search:'',zoom:1};
let request=0,lastGraphFocus=null;
const svg=(tag,attrs={})=>{const e=document.createElementNS(NS,tag);for(const [k,v]of Object.entries(attrs))e.setAttribute(k,v);return e;};
function button(label,action){const b=document.createElement('button');b.type='button';b.textContent=label;b.addEventListener('click',action);return b;}
function sourceLink(url,label='Open public source ↗'){return '<a href="'+esc(url)+'" target="_blank" rel="noopener noreferrer">'+esc(label)+'</a>';}
function rootContent(owner){return d.contentItems.find(c=>c.ownerNodeId===owner&&c.parentId===null);}
function visibleRelationshipIds(){
 if(!state.incremental)return new Set(d.nodes.filter(n=>n.type!=='candidate'||state.candidates).map(n=>n.id));
 const ids=new Set(['csp','lsps']);let changed=true;
 while(changed){changed=false;for(const e of d.edges)if(ids.has(e.from)&&state.expanded.has(e.from)&&(!e.candidate||state.candidates)&&!ids.has(e.to)){ids.add(e.to);changed=true;}}
 return ids;
}
function relationshipLayout(){const ids=visibleRelationshipIds();return {nodes:d.nodes.filter(n=>ids.has(n.id)).map(n=>({...n,title:n.label,subtitle:n.sub})),edges:d.edges.filter(e=>ids.has(e.from)&&ids.has(e.to)),truncated:false};}
function contentLayout(){const expanded=state.incremental?state.contentExpanded:new Set(d.contentItems.map(c=>c.id));return m.layoutContent(d,state.contentRoot,{expanded,limit:200});}
function isBranch(n){return state.root==='all'||n.type===state.root;}
function focusSet(){if(!state.selected)return new Set();return new Set([state.selected,...d.edges.filter(e=>e.from===state.selected||e.to===state.selected).flatMap(e=>[e.from,e.to])]);}
function render(){
 const active=document.activeElement?.getAttribute('data-node-id');
 graph.querySelectorAll('[data-drawn]').forEach(e=>e.remove());const base=svg('g',{'data-drawn':'true'});graph.append(base);
 const layout=state.view==='content'?contentLayout():relationshipLayout(),map=new Map(layout.nodes.map(n=>[n.id,n])),focus=focusSet();
 const maxX=Math.max(1500,...layout.nodes.map(n=>n.x+250)),maxY=Math.max(760,...layout.nodes.map(n=>n.y+100));graph.setAttribute('viewBox',`0 0 ${maxX} ${maxY}`);graph.style.width=(maxX*state.zoom)+'px';graph.style.minWidth=(maxX*state.zoom)+'px';graph.style.height=(maxY*state.zoom)+'px';
 for(const e of layout.edges){
  const a=map.get(e.from),b=map.get(e.to);const span=Math.max(30,(b.x-a.x-170)*.46);const path=`M ${a.x+170} ${a.y+28} C ${a.x+170+span} ${a.y+28} ${b.x-span} ${b.y+28} ${b.x} ${b.y+28}`;
  const dim=state.view==='relationships'&&(state.selected&&state.neighbours&&!(focus.has(a.id)&&focus.has(b.id))||!state.selected&&!isBranch(a)&&!isBranch(b));
  const p=svg('path',{d:path,tabindex:0,role:'button','data-edge-id':e.id||e.from+'->'+e.to,'aria-label':'Inspect link from '+(a.title||a.label)+' to '+(b.title||b.label),class:'atlas-edge'+(e.candidate?' candidate':'')+(dim?' faded':'')});base.append(p);p.addEventListener('click',()=>inspectLink(e));p.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();inspectLink(e);}});
  if(state.view==='relationships'&&!e.candidate&&state.mode!=='kpi'){base.append(svg('path',{d:path,'pointer-events':'none',class:'atlas-edge colour'+(dim?' faded':''),style:'stroke:'+(a.type==='lsps'?'#477fad':'#238e86'),pathLength:100,'stroke-dasharray':`${(state.mode==='coverage'?e.coverage:e.time)*100} 100`}));}
 }
 for(const n of layout.nodes){
  const selected=state.view==='content'?state.contentSelected===n.id:state.selected===n.id;
  const dim=state.view==='relationships'&&(state.selected&&state.neighbours&&!focus.has(n.id)||!state.selected&&!isBranch(n));
  const g=svg('g',{class:'atlas-node '+(n.type||'csp')+(selected?' selected':'')+(dim?' faded':''),transform:`translate(${n.x} ${n.y})`,tabindex:0,role:'button','aria-pressed':String(selected),'data-node-id':n.id,'aria-label':'Inspect '+(n.title||n.label)});
  g.append(svg('rect',{width:170,height:62,rx:12}));
  const full=n.title||n.label,title=svg('title');title.textContent=full+' · '+(n.status||'SYNTHETIC');g.append(title);
  const t=svg('text',{x:12,y:24});t.textContent=full.length>21?full.slice(0,20)+'…':full;g.append(t);
  const sub=svg('text',{x:12,y:44,class:'sub'});sub.textContent=n.kind||n.subtitle;g.append(sub);
  const choose=()=>state.view==='content'?inspectContent(n.id):inspectNode(n.id);
  g.addEventListener('click',choose);g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose();}});base.append(g);
 }
 if(active)graph.querySelector(`[data-node-id="${CSS.escape(active)}"]`)?.focus({preventScroll:true});
 $('nodeCount').textContent=layout.nodes.length;$('edgeCount').textContent=layout.edges.length;$('contentCount').textContent=d.contentItems.length;
 $('modeExplanation').textContent=state.view==='content'?'Containment tree: structure only, with no progress fill.':state.mode==='coverage'?'Synthetic verification coverage: a visual demonstration, not actual Council review coverage.':state.mode==='time'?'Synthetic elapsed-time proportion. This is not action completion.':'Actual KPI: UNKNOWN. No verified outcome or denominator; all paths remain grey.';
 $('viewContext').textContent=state.view==='content'?'Inside: '+contentById.get(state.contentRoot).title:'Cross-document relationships · synthetic';
 $('relationshipsView').setAttribute('aria-pressed',state.view==='relationships');$('contentView').setAttribute('aria-pressed',state.view==='content');
 $('expansionStatus').textContent=layout.truncated?'View capped at 200 items. Open a narrower content scope.':state.incremental?'Progressive expansion is on.':'All items in this scope are visible.';
 renderBreadcrumbs();
}
function openInspector(){if(matchMedia('(max-width:960px)').matches)$('inspector').scrollIntoView({block:'start',behavior:'instant'});}
function panel(html){request++;state.selected=null;state.contentSelected=null;details.innerHTML=html;render();openInspector();return request;}
function renderBreadcrumbs(){
 const target=$('breadcrumbs');target.replaceChildren();if(state.view!=='content')return;
 target.append(button('Relationship atlas',()=>{state.view='relationships';render();}));
 const id=state.contentSelected||state.contentRoot;
 for(const c of m.contentTrail(d,id)){target.append(document.createTextNode(' / '),button(c.title,()=>openContent(c.id)));}
}
function treeHTML(id,depth=0){
 const c=contentById.get(id),children=m.contentChildren(d,id);if(!c||depth>20)return '';
 const select='<button type="button" data-content="'+esc(c.id)+'">'+esc(c.title)+'</button>';
 return children.length?'<details class="content-tree"'+(depth===0?' open':'')+'><summary>'+esc(c.kind+' · '+c.title)+' <span>'+children.length+' items</span></summary>'+select+children.map(child=>treeHTML(child.id,depth+1)).join('')+'</details>':'<div class="content-leaf"><span class="key">'+esc(c.kind)+'</span>'+select+'</div>';
}
function wireContent(){details.querySelectorAll('[data-content]').forEach(b=>b.addEventListener('click',()=>openContent(b.dataset.content)));}
function revealRelationship(id){if(!state.incremental)return;for(const root of ['csp','lsps'])for(const path of m.paths(d,root,id,{includeCandidates:state.candidates}))for(const edgeId of path)state.expanded.add(d.edges.find(e=>e.id===edgeId).from);}
function inspectNode(id){
 const n=byId.get(id);if(!n)return;if(n.type==='candidate'){state.candidates=true;$('showCandidates').checked=true;}state.selected=id;lastGraphFocus=id;revealRelationship(id);const current=++request;
 const connected=d.edges.filter(e=>(e.from===id||e.to===id)&&(!e.candidate||state.candidates)),root=rootContent(id);
 const paths=['csp','lsps'].flatMap(start=>m.paths(d,start,id,{includeCandidates:state.candidates}));
 details.innerHTML='<div class="detail-head"><h3>'+esc(n.label)+'</h3><span class="detail-badge">'+(n.type==='candidate'?'HYPOTHESIS':'SYNTHETIC')+'</span></div><p class="detail-text">'+esc(n.detail)+'</p><div class="detail-list"><div class="detail-item"><span class="key">Logical identity / revision</span><span class="value">'+esc(n.logicalId+' / '+n.versionId)+'</span></div><div class="detail-item"><span class="key">Official clause / applicability / KPI</span><span class="value">UNKNOWN / UNKNOWN / UNKNOWN</span></div><div class="detail-item"><span class="key">Public discovery entry</span><span class="value">'+(n.source?sourceLink(n.source,'Open directory ↗'):'No verified public source')+'</span></div><div class="detail-item"><span class="key">Synthetic paths</span><span class="value">'+esc(paths.map(p=>p.join(' → ')||'Start').join(' / ')||'No path')+'</span></div></div><h3 class="section-title">Inside this topic</h3><p class="detail-text">Open each level. Internal examples remain synthetic.</p>'+treeHTML(root.id)+'<h3 class="section-title">Adjacent relationships</h3><div class="relation-list">'+connected.map(e=>{const a=d.assertions.find(a=>a.id===e.id),other=e.from===id?e.to:e.from;return '<button data-target="'+esc(other)+'">'+(e.to===id?'↑ Upstream: ':'↓ Downstream: ')+esc(byId.get(other).label)+'<small>'+esc(a.id+' · '+a.status)+'</small></button>';}).join('')+'</div><p id="contentDigest" class="detail-text">Computing content digest…</p>';
 wireContent();details.querySelectorAll('[data-target]').forEach(b=>b.addEventListener('click',()=>inspectNode(b.dataset.target)));
 m.objectDigest(n).then(hash=>{if(current===request)$('contentDigest').textContent='Node digest '+hash+'. Integrity only; no official signature.';}).catch(()=>{if(current===request)$('contentDigest').textContent='Digest unavailable.';});render();openInspector();
}
function inspectLink(edge){
 const a=d.assertions.find(a=>a.id===edge.id);
 const from=state.view==='content'?contentById.get(edge.from).title:byId.get(edge.from).label,to=state.view==='content'?contentById.get(edge.to).title:byId.get(edge.to).label;
 panel('<h3>'+esc(from)+' → '+esc(to)+'</h3>'+(a?'<div class="detail-badge">'+esc(a.status)+'</div><p class="detail-text">Predicate: '+esc(a.predicate)+' / Review: '+esc(a.reviewStatus)+'</p><p class="detail-text">Revision '+esc(a.revisionId)+' · Region '+esc(a.region)+' · '+esc(a.validFrom)+' to '+esc(a.validTo)+'</p><p class="detail-text">Supporting references: '+a.evidenceRefs.length+' · Counter-references: '+a.counterevidenceRefs.length+'</p><div class="warn">Synthetic or research relationship. No official source-to-clause mapping has been admitted.</div>':'<div class="detail-badge">CONTAINS</div><p class="detail-text">This is internal content containment. It does not establish statutory effect or a cross-document policy relationship.</p>'));
}
function openContent(id){
 const c=contentById.get(id);if(!c)return;
 const trail=m.contentTrail(d,id);state.view='content';state.contentRoot=trail[0].id;for(const item of trail)state.contentExpanded.add(item.id);inspectContent(id);
}
function inspectContent(id){
 const c=contentById.get(id);if(!c)return;state.contentSelected=id;lastGraphFocus=id;const current=++request,children=m.contentChildren(d,id),o=d.sourceObservations.find(o=>o.id===c.observationId);
 details.innerHTML='<div class="detail-head"><h3>'+esc(c.title)+'</h3><span class="detail-badge">'+esc(c.status)+'</span></div><p class="detail-text">'+esc(c.text)+'</p><div class="detail-list"><div class="detail-item"><span class="key">Content type / logical identity</span><span class="value">'+esc(c.kind+' / '+c.logicalId)+'</span></div><div class="detail-item"><span class="key">Version / official applicability</span><span class="value">'+esc(c.versionId)+' / UNKNOWN</span></div>'+(o?'<div class="detail-item"><span class="key">Observed public anchor</span><span class="value">'+esc(o.locator)+' · '+esc(o.observedOn)+'<br>'+sourceLink(o.url||d.sources.find(s=>s.id===o.sourceId).url)+'</span></div>':'<div class="detail-item"><span class="key">Evidence status</span><span class="value">Authored synthetic breakdown. Not extracted official text.</span></div>')+'</div><div class="relation-list">'+(c.parentId?'<button data-content="'+esc(c.parentId)+'">↑ Parent content</button>':'')+'<button id="scopeContent">Focus this subtree</button>'+(c.ownerNodeId?'<button id="ownerNode">Back to relationship topic</button>':'')+'</div><h3 class="section-title">'+(children.length?'Internal breakdown':'End of admitted content')+'</h3>'+(children.length?treeHTML(id):'<p class="detail-text">No further content has been admitted. This is an explicit leaf, not a missing percentage or an invented clause.</p>')+'<h3 class="section-title">Content-addressed receipt</h3><p id="contentDigest" class="detail-text">Computing item and subtree digests…</p>';
 wireContent();$('scopeContent').addEventListener('click',()=>{state.contentRoot=id;render();});if(c.ownerNodeId)$('ownerNode').addEventListener('click',()=>{state.view='relationships';inspectNode(c.ownerNodeId);});
 m.contentReceipt(d,id).then(receipt=>{if(current===request)$('contentDigest').textContent='Item '+receipt.itemDigest+' · Subtree '+receipt.subtreeDigest+'. Child changes alter the ancestor receipt. No external witness or official signature.';}).catch(()=>{if(current===request)$('contentDigest').textContent='Content receipt failed validation.';});render();openInspector();
}
function closeDetails(){request++;state.selected=null;state.contentSelected=null;details.innerHTML=empty;render();const target=lastGraphFocus&&graph.querySelector(`[data-node-id="${CSS.escape(lastGraphFocus)}"]`);target?.focus({preventScroll:true});target?.scrollIntoView({block:'nearest',inline:'nearest',behavior:'instant'});}
$('closeDetails').addEventListener('click',closeDetails);document.addEventListener('keydown',e=>{if(e.key==='Escape')closeDetails();});
$('zoom').addEventListener('input',e=>{state.zoom=Number(e.target.value)/100;$('zoomValue').textContent=e.target.value+'%';render();});
$('fitScope').addEventListener('click',()=>{const width=graph.viewBox.baseVal.width;state.zoom=Math.max(.35,Math.min(1,graph.parentElement.clientWidth/width));$('zoom').value=String(Math.round(state.zoom*100));$('zoomValue').textContent=Math.round(state.zoom*100)+'%';render();});
$('relationshipsView').addEventListener('click',()=>{state.view='relationships';render();});$('contentView').addEventListener('click',()=>openContent(state.selected?rootContent(state.selected).id:state.contentRoot));
$('incremental').addEventListener('change',e=>{state.incremental=e.target.checked;render();});
$('expandNode').addEventListener('click',()=>{const id=state.view==='content'?state.contentSelected:state.selected;if(!id){$('expansionStatus').textContent='Select a node to expand.';return;}state.incremental=true;$('incremental').checked=true;(state.view==='content'?state.contentExpanded:state.expanded).add(id);render();});
$('resetExpansion').addEventListener('click',()=>{state.expanded=new Set(['csp','lsps']);state.contentExpanded=new Set([state.contentRoot]);state.selected=null;state.contentSelected=null;request++;details.innerHTML=empty;render();});
document.querySelectorAll('[data-root]').forEach(b=>b.addEventListener('click',()=>{state.root=b.dataset.root;state.view='relationships';state.selected=null;request++;details.innerHTML=empty;document.querySelectorAll('[data-root]').forEach(other=>{other.classList.toggle('selected',other===b);other.setAttribute('aria-pressed',other===b);});render();}));
document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{state.mode=b.dataset.mode;document.querySelectorAll('[data-mode]').forEach(other=>other.setAttribute('aria-pressed',other===b));render();}));
$('showCandidates').addEventListener('change',e=>{state.candidates=e.target.checked;if(!state.candidates&&state.selected==='candidate')closeDetails();render();});$('showNeighbours').addEventListener('change',e=>{state.neighbours=e.target.checked;render();});
$('search').addEventListener('input',e=>{
 state.search=e.target.value.trim().toLowerCase();const out=$('searchResults');out.replaceChildren();if(!state.search)return;
 const matches=d.contentItems.filter(c=>(c.title+' '+c.text).toLowerCase().includes(state.search));out.append(document.createTextNode(matches.length+' internal-content matches. Showing up to 12.'));
 for(const c of matches.slice(0,12)){out.append(button(m.contentTrail(d,c.id)[0].title+' / '+c.title+' · '+c.kind,()=>openContent(c.id)));}
 if(!matches.length)out.append(document.createTextNode(' No matching admitted content.'));
});
$('sourcesBtn').addEventListener('click',()=>{panel('<h3>Public-source observations</h3><p class="detail-text">Observed metadata and limited public text. Original-byte, permission and applicability admission remains incomplete. Official graph mappings: 0.</p>'+d.sourceObservations.map(o=>'<div class="warn"><strong>'+esc(o.title)+'</strong><p>'+esc(o.note)+'</p><p>Anchor: '+esc(o.locator)+'</p><p>Observed '+esc(o.observedOn)+' · Adopted '+esc(o.adoptedOn||'UNKNOWN')+'</p>'+sourceLink(o.url||d.sources.find(s=>s.id===o.sourceId).url)+'<p>'+esc(o.status)+' · Raw digest UNKNOWN</p><button data-content="'+esc(o.id+':content')+'">Explore observed content</button></div>').join(''));wireContent();});
$('discoveryBtn').addEventListener('click',()=>panel('<h3>Cross-path hypotheses & counterevidence</h3><h3 class="section-title">Detected structural convergence</h3>'+m.findCrossPaths(d).map(h=>'<div class="warn"><strong>'+esc(h.id+' · '+h.status)+'</strong><p>'+esc(h.explanation)+'</p>'+h.branches.map(b=>'<p>'+esc(b.rootId+': '+b.paths.map(p=>p.join(' → ')).join(' / '))+'</p>').join('')+'<p>Evidence references: '+h.evidenceCount+'</p>'+h.questions.map(q=>'<p>'+esc(q)+'</p>').join('')+'</div>').join('')+'<h3 class="section-title">Authored hypotheses and falsifiers</h3>'+m.discover(d).map(h=>'<div class="warn"><strong>'+esc(h.id+' · '+h.status)+'</strong><p>Rule: '+esc(h.ruleVersion)+'</p><p>'+esc(h.explanation)+'</p>'+h.paths.map(p=>'<p>'+esc(p.from+' → '+p.to+' / '+p.assertionId+' / '+p.status)+'; support references: '+p.evidenceRefs.length+'; counter-references: '+p.counterevidenceRefs.length+'</p>').join('')+'<p>Synthetic counterexample: '+esc(h.counterevidence.map(c=>c.reason).join(' / '))+'</p><p>Requires review. This enumerates authored candidates, not automatic semantic discovery.</p></div>').join('')));
$('auditBtn').addEventListener('click',async()=>{const current=panel('<h3>Audit & version history</h3><p>Recomputing dataset and linked event history…</p>');try{const a=await m.auditSnapshot(d);if(current!==request)return;details.innerHTML='<h3>Audit & version history</h3><p class="detail-text">Snapshot '+esc(a.datasetDigest)+'</p><p>Structure issues: '+a.issues.length+' · Event chain: '+(a.historyValid?'PASS':'FAIL')+'</p>'+d.events.map(e=>'<div class="warn">'+esc(e.sequence+' / '+e.type+' / '+e.objectId)+'<p>'+esc(e.observedAt)+'</p><p>'+esc(e.reason)+'</p><p>'+esc(e.digest)+'</p></div>').join('')+'<p class="detail-text">'+d.contentItems.length+' content items have distinct logical and version identities. Each subtree has a reproducible child-linked receipt. Export the snapshot to retain a checkpoint.</p><div class="warn">History contains synthetic fixture events only. Hashes do not prove truth, completeness, official adoption or protection against whole-history replacement. No independent signature or witness.</div>';}catch{if(current===request)details.textContent='Audit failed. Do not rely on this dataset.';}});
$('exportBtn').addEventListener('click',async()=>{try{const bundle=await m.exportSnapshot(d);const blob=new Blob([JSON.stringify(bundle,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='atlas-public-snapshot.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$('appStatus').textContent='Public/synthetic snapshot exported. Verify its digest independently; it is not an official credential.';}catch{$('appStatus').textContent='Export blocked: dataset verification failed.';}});
$('aboutBtn').addEventListener('click',()=>panel('<h3>About this independent atlas</h3><p class="detail-text">An English, offline-capable research prototype for public strategy and internal content exploration. It runs without paid services or external runtime dependencies. Synthetic containment is kept separate from observed public text and official relationships.</p><div class="warn">No Council internal records. No real case data. No actual KPI. No deployment or official endorsement. Current source-admission and large-graph limits remain documented in NEXT_SESSION.md.</div>'));
if([60,200].includes(fixtureSize)){state.view='content';state.contentRoot='density:0';state.contentExpanded=new Set(['density:0']);$('fixtureSize').value=String(fixtureSize);$('appStatus').textContent='SYNTHETIC '+fixtureSize+'-item density fixture. No official content.';}
$('fixtureSize').addEventListener('change',e=>{const url=new URL(location.href);if(e.target.value==='base')url.searchParams.delete('fixture');else url.searchParams.set('fixture',e.target.value);location.href=url.href;});
const issues=m.validate(d);if(issues.length){details.textContent='DATA_INVALID: '+issues.join('; ');return;}render();
})();
