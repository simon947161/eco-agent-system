/* ClimateOS Public Strategy Atlas M0 — SYNTHETIC EXAMPLE GRAPH ONLY.
   No Council business records, no verified statutory relationships, no KPI results.
   Local content digests are not official signatures or truth proofs. */
(() => {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const {nodes,edges,assertions,hypotheses} = AtlasData;
  const map = Object.fromEntries(nodes.map(n => [n.id,n]));
  const state = {root:"csp", selected:null,mode:"coverage",candidates:false,neighbours:true,search:"",incremental:false,expanded:new Set(["csp","lsps"])};
  const graph = document.getElementById("atlasGraph");
  const details = document.getElementById("details");
  const search = document.getElementById("search");
  const emptyDetails = details.innerHTML;
  const explain = document.getElementById("modeExplanation");
  const el = (tag,attrs={}) => {const e=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));return e;};
  const esc = s => String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  function visibleIds(){
    if(!state.incremental)return new Set(nodes.map(n=>n.id));
    const ids=new Set(['csp','lsps']);
    let changed=true;while(changed){changed=false;for(const e of edges)if(ids.has(e.from)&&state.expanded.has(e.from)&&(!e.candidate||state.candidates)&&!ids.has(e.to)){ids.add(e.to);changed=true;}}
    return ids;
  }
  function visibleNode(n) {return (n.id!=="candidate" || state.candidates)&&visibleIds().has(n.id);}
  function inBranch(n) {
    if(state.root==="all")return true;
    return state.root==="csp" ? n.type==="csp" : n.type==="lsps";
  }
  function edgePath(e) {
    const a=map[e.from], b=map[e.to];
    const x1=a.x+155,y1=a.y+28,x2=b.x,y2=b.y+28;
    const span=Math.max(26,(x2-x1)*.46);
    return "M "+x1+" "+y1+" C "+(x1+span)+" "+y1+" "+(x2-span)+" "+y2+" "+x2+" "+y2;
  }
  function makeTitle(node,text){const t=el("title");t.textContent=text;node.append(t);}
  function focusIds() {
    if(!state.selected) return new Set();
    return new Set([state.selected,...edges.filter(e=>e.from===state.selected||e.to===state.selected).flatMap(e=>[e.from,e.to])]);
  }
  function draw() {
    const activeNode = document.activeElement?.getAttribute("data-node-id");
    graph.querySelectorAll("[data-drawn]").forEach(e=>e.remove());
    const base=el("g",{"data-drawn":"yes"}); graph.append(base);
    const caption=el("text",{x:70,y:45,class:"lane-caption"});caption.textContent="STRATEGY / DELIVERY / EVIDENCE";base.append(caption);
    const p=el("text",{x:70,y:424,class:"lane-caption"});p.textContent="SPATIAL PLANNING / STATUTORY CONTEXT";base.append(p);
    const focus=focusIds();
    for(const e of edges) {
      if(e.candidate&&!state.candidates||!visibleNode(map[e.from])||!visibleNode(map[e.to]))continue;
      const a=map[e.from],b=map[e.to],hi=focus.has(e.from)&&focus.has(e.to);
      const dim=state.search&&!([a.label,a.sub,b.label,b.sub].join(" ").toLowerCase().includes(state.search)) ||
        state.selected&&state.neighbours&&!hi ||
        !state.selected&&state.root!=="all"&&!inBranch(a)&&!inBranch(b);
      const d=edgePath(e);
      const path=el("path",{d,class:"atlas-edge"+(e.candidate?" candidate":"")+(dim?" faded":"")});
      makeTitle(path,e.kind+" — 合成示例，未经官方核实");base.append(path);
      if(!e.candidate) {
        const n=state.mode==="coverage"?e.coverage:state.mode==="time"?e.time:null;
        if(n!==null) {
          const fill=el("path",{d,class:"atlas-edge colour"+(dim?" faded":""),
            style:"stroke:"+(a.type==="lsps"?"#477fad":"#238e86")+";",
            "stroke-dasharray":(n*100)+" 100",pathLength:"100"});
          makeTitle(fill,"示例填充 "+Math.round(n*100)+"%；与真实 Council 进度无关");base.append(fill);
        }
      }
    }
    for(const n of nodes) {
      if(!visibleNode(n))continue;
      const dim=state.search&&!((n.label+" "+n.sub+" "+n.detail).toLowerCase().includes(state.search)) ||
        state.selected&&state.neighbours&&!focus.has(n.id) ||
        !state.selected&&state.root!=="all"&&!inBranch(n);
      const g=el("g",{class:"atlas-node "+n.type+(state.selected===n.id?" selected":"")+(dim?" faded":""),transform:"translate("+n.x+" "+n.y+")","data-node-id":n.id,tabindex:"0",role:"button","aria-pressed":String(state.selected===n.id),"aria-label":"查看 "+n.label+" 的证据详情"});
      g.append(el("rect",{width:155,height:56,rx:12}));
      const t=el("text",{x:13,y:23}); t.textContent=n.label;g.append(t);
      const sub=el("text",{x:13,y:41,class:"sub"});sub.textContent=n.sub;g.append(sub);
      makeTitle(g,n.label+" — "+n.sub+"（合成示例）");
      g.addEventListener("click",()=>select(n.id));
      g.addEventListener("keydown",event=>{if(event.key==="Enter"||event.key===" "){event.preventDefault();select(n.id);}});
      base.append(g);
    }
    if(activeNode) graph.querySelector(`[data-node-id="${activeNode}"]`)?.focus({preventScroll:true});
    const note=el("text",{x:1100,y:725,class:"svg-note"});note.textContent="M0 / SYNTHETIC DATA / NO COUNCIL KPI";base.append(note);
    explain.textContent=state.mode==="coverage"?"演示性关系核验填充；尚无真实 Council 核验率。":
      state.mode==="time"?"演示性期限经过比例；绝不代表行动完成或绩效达成。":
      "实际绩效：无经核验的公开结果与分母，所有进度保持 UNKNOWN（灰色）。";
    document.getElementById("nodeCount").textContent=String(nodes.filter(visibleNode).length);
    document.getElementById("edgeCount").textContent=String(edges.filter(e=>(!e.candidate||state.candidates)&&visibleNode(map[e.from])&&visibleNode(map[e.to])).length);
  }
  let panelRequest=0;
  function select(id) {
    state.selected=id;const n=map[id];if(!n)return;const request=++panelRequest;
    if(state.incremental)for(const root of ['csp','lsps'])for(const path of AtlasModel.paths(AtlasData,root,id,{includeCandidates:state.candidates}))for(const edgeId of path)state.expanded.add(edges.find(e=>e.id===edgeId).from);
    const paths=AtlasModel.paths(AtlasData,n.type==="lsps"?"lsps":"csp",id,{includeCandidates:state.candidates});
    const connected=edges.filter(e=>(e.from===id||e.to===id)&&(!e.candidate||state.candidates));
    const relationButtons=connected.map(e=>{
      const other=map[e.from===id?e.to:e.from];
      return '<button type="button" data-target="'+esc(other.id)+'" title="'+esc(e.kind)+'">'+(e.to===id?'↑ 上溯：':'↓ 下游：')+esc(other.label)+' · '+(e.candidate?"暗线候选":"合成路径")+'</button>';
    }).join("");
    const source=n.source?'<a href="'+esc(n.source)+'" target="_blank" rel="noopener noreferrer">查看公开资料目录 ↗</a>':'没有官方来源可验证';
    details.innerHTML='<div class="detail-head"><div><div class="eyebrow">NODE · '+esc(n.id.toUpperCase())+'</div><h3>'+esc(n.label)+'</h3></div><span class="detail-badge">'+(n.type==="candidate"?"HYPOTHESIS":"SYNTHETIC")+'</span></div>'+
      '<p class="detail-text">'+esc(n.detail)+'</p>'+
      '<p class="detail-text">合成多路径：'+esc(paths.map(p=>p.join(' → ')||'起点').join(' / ')||'无可用路径')+'；不证明正式适用。</p>'+
      '<div class="detail-list">'+
      '<div class="detail-item"><span class="key">身份与来源</span><span class="value">合成展示节点；非真实 Council 条款关系</span></div>'+
      '<div class="detail-item"><span class="key">内容哈希 / 数字签名</span><span class="value">合成版本 synthetic-v1；原始资料摘要 UNKNOWN；无官方数字签名</span></div>'+
      '<div class="detail-item"><span class="key">条款、时点与辖区</span><span class="value">UNKNOWN · 尚未进行正式资料核验</span></div>'+
      '<div class="detail-item"><span class="key">可核对入口</span><span class="value">'+source+'</span></div></div>'+
      '<div class="detail-item"><span class="key">关系声明 / 审核</span><span class="value">'+connected.map(e=>{const a=assertions.find(a=>a.id===e.id);return esc(a.id+' · '+a.status+' · '+a.reviewStatus);}).join('<br>')+'</span></div>'+
      '<h3 style="margin-top:20px">邻接关系（演示）</h3><div class="relation-list">'+(relationButtons||'<span class="detail-text">当前未展示邻接关系</span>')+'</div>'+
      '<div class="warn">'+(n.type==="candidate"?"暗线是待证伪的研究候选，不可自动成为官方事实。合成反证：仅适用于2025年、外地区的版本不能支持2026年本地区结论。":"这里只演示追溯交互，没有任何已审核的实际绩效、法规适用或政策映射。")+'</div>';
    details.querySelectorAll("[data-target]").forEach(b=>b.addEventListener("click",()=>select(b.dataset.target)));
    details.insertAdjacentHTML('beforeend','<h3>版本与可审计标识</h3><div id="nodeAudit" class="detail-text">正在计算本地摘要…</div>');
    const revision=AtlasData.revisions.find(r=>r.id===n.revisionId);
    AtlasModel.objectDigest(n).then(hash=>{if(request===panelRequest){const out=document.getElementById('nodeAudit');if(out)out.textContent='逻辑身份 '+n.logicalId+'；版本 '+n.versionId+'；节点内容 '+hash+'；合成原件 '+revision.rawDigest+'。无官方签名。';}}).catch(()=>{if(request===panelRequest){const out=document.getElementById('nodeAudit');if(out)out.textContent='摘要不可用：需要支持 Web Crypto 的浏览器安全上下文。';}});
    draw();
    if(matchMedia('(max-width:960px)').matches)document.getElementById('inspector').scrollIntoView({block:'start',behavior:'instant'});
    else graph.querySelector(`[data-node-id="${id}"]`)?.scrollIntoView({block:"nearest",inline:"nearest",behavior:"instant"});
  }
  document.querySelectorAll("[data-root]").forEach(btn=>btn.addEventListener("click",()=>{
    state.root=btn.dataset.root;state.selected=null;panelRequest++;details.innerHTML=emptyDetails;
    document.querySelectorAll("[data-root]").forEach(b=>(b.classList.toggle("selected",b===btn), b.setAttribute("aria-pressed",String(b===btn))));
    draw();
  }));
  document.querySelectorAll("[data-mode]").forEach(btn=>btn.addEventListener("click",()=>{
    state.mode=btn.dataset.mode;
    document.querySelectorAll("[data-mode]").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));
    draw();
  }));
  document.getElementById("showCandidates").addEventListener("change",e=>{state.candidates=e.target.checked;if(!state.candidates&&state.selected==="candidate"){state.selected=null;panelRequest++;details.innerHTML=emptyDetails;}if(state.selected)select(state.selected);else draw();});
  document.getElementById("showNeighbours").addEventListener("change",e=>{state.neighbours=e.target.checked;draw();});
  search.addEventListener("input",e=>{state.search=e.target.value.trim().toLowerCase();state.selected=null;panelRequest++;details.innerHTML=emptyDetails;state.root="all";document.querySelectorAll("[data-root]").forEach(b=>{b.classList.toggle("selected",b.dataset.root==="all");b.setAttribute("aria-pressed",String(b.dataset.root==="all"));});draw();});
  document.getElementById("aboutBtn").addEventListener("click",()=>{
    openPanel();
    details.innerHTML='<div class="detail-head"><div><div class="eyebrow">RESEARCH NOTICE</div><h3>关于本地原型</h3></div></div><p class="detail-text">本网站是 ClimateOS Public Strategy Atlas 的 M0 工程起点，供独立学习与 UI 验证。图上所有关系、合成进度、节点路径均是人工设计的虚构样本，不可用于官方决策。目录链接并不意味着条款已核准。不会上传任何 Council 内部或个人业务数据。M1 已实现本地合成数据结构、摘要和事件链校验函数；没有官方签名、外部见证或防管理员重写保证。</p><div class="warn">本地演示 ≠ 正式部署；合成关系 ≠ 现行法规；文件完整性 ≠ 语义真实性。</div>';
  });
  document.getElementById("closeDetails").addEventListener("click",()=>{const id=state.selected;state.selected=null;panelRequest++;details.innerHTML=emptyDetails;draw();if(id){const target=graph.querySelector(`[data-node-id="${id}"]`);target?.focus({preventScroll:true});target?.scrollIntoView({block:"nearest",inline:"nearest",behavior:"instant"});}});
  document.addEventListener("keydown",e=>{if(e.key==="Escape")document.getElementById("closeDetails").click();});
  const openPanel=()=>{panelRequest++;state.selected=null;draw();if(matchMedia('(max-width:960px)').matches)document.getElementById('inspector').scrollIntoView({block:'start',behavior:'instant'});};
  document.getElementById('auditBtn').addEventListener('click',async()=>{
    openPanel();const request=panelRequest;details.textContent='正在复验数据与事件链…';
    try {const audit=await AtlasModel.auditSnapshot(AtlasData);if(request!==panelRequest)return;
    details.innerHTML='<h3>本地审计与版本历史</h3><p class="detail-text">'+esc(audit.datasetDigest)+'</p><p>结构问题 '+audit.issues.length+'；事件链 '+(audit.historyValid?'PASS':'FAIL')+'</p><p class="detail-text">链头 '+esc(audit.historyHead)+'</p>'+AtlasData.events.map(e=>'<div class="warn">'+esc(e.sequence+' · '+e.type+' · '+e.objectId+' · '+e.observedAt)+'<br>'+esc(e.reason)+'<br>'+esc(e.digest)+'</div>').join('')+'<div class="warn">摘要证明本次输入一致；不能证明事实、完整历史或防止整链重写。无独立见证、无官方签名。</div>';
    }catch{if(request===panelRequest)details.textContent='摘要不可用：需要支持 Web Crypto 的浏览器安全上下文。';}
  });
  document.getElementById('discoveryBtn').addEventListener('click',()=>{
    openPanel();details.innerHTML='<h3>跨路径暗线与反证</h3>'+AtlasModel.discover(AtlasData).map(h=>'<div class="warn"><strong>'+esc(h.id+' · '+h.status)+'</strong><p>规则 '+esc(h.ruleVersion)+'</p><p>'+esc(h.explanation)+'</p>'+h.paths.map(p=>'<p>'+esc(p.from+' → '+p.to+' · '+p.assertionId+' · '+p.status)+'；支持证据 '+p.evidenceRefs.length+'，引用反证 '+p.counterevidenceRefs.length+'</p>').join('')+'<p>合成反证：'+esc(h.counterevidence.map(c=>c.reason).join(' / '))+'</p><p>结论：待人工审查，不升级为官方事实。</p></div>').join('');
  });
  document.getElementById('sourcesBtn').addEventListener('click',()=>{
    openPanel();details.innerHTML='<h3>公开来源核验登记</h3><p class="detail-text">2026-10-29 人工检视官方网页；以下为目录元数据观察，原始 PDF、条款、许可及适用性未准入。官方图谱关系仍为 0。</p>'+AtlasData.sourceObservations.map(o=>'<div class="warn"><strong>'+esc(o.title)+'</strong><p>'+esc(o.note)+'</p><p>定位 '+esc(o.locator)+'；观察日期 '+esc(o.observedOn)+'；采用日期 '+esc(o.adoptedOn??'UNKNOWN')+'</p><a target="_blank" rel="noopener noreferrer" href="'+esc(o.url??AtlasData.sources.find(s=>s.id===o.sourceId).url)+'">公开原始入口 ↗</a><p>'+esc(o.status)+' / 条款映射 UNKNOWN / 原件哈希 UNKNOWN</p></div>').join('');
  });
  document.getElementById('incremental').addEventListener('change',e=>{state.incremental=e.target.checked;state.selected=null;panelRequest++;details.innerHTML=emptyDetails;draw();document.getElementById('expansionStatus').textContent=state.incremental?'仅显示根与已展开的后代':'显示全部节点';});
  document.getElementById('expandNode').addEventListener('click',()=>{if(!state.incremental||!state.selected){document.getElementById('expansionStatus').textContent='请启用逐层展开并选择节点';return;}state.expanded.add(state.selected);draw();document.getElementById('expansionStatus').textContent='已展开 '+map[state.selected].label+'；节点位置保持稳定';});
  document.getElementById('resetExpansion').addEventListener('click',()=>{state.expanded=new Set(['csp','lsps']);state.selected=null;panelRequest++;details.innerHTML=emptyDetails;draw();document.getElementById('expansionStatus').textContent='展开状态已重置';});
  const issues=AtlasModel.validate(AtlasData);
  if(issues.length){details.textContent="DATA_INVALID: "+issues.join("; ");return;}
  draw();
})();
