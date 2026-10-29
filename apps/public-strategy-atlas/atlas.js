/* ClimateOS Public Strategy Atlas M0 — SYNTHETIC EXAMPLE GRAPH ONLY.
   No Council business records, no verified statutory relationships, no KPI results.
   No cryptographic verification has been implemented in this prototype. */
(() => {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const IP = "https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting";
  const DEV = "https://www.snowymonaro.nsw.gov.au/Building-and-Planning/Development";
  const nodes = [
    {id:"csp",label:"CSP",sub:"战略总览 · 示例",type:"csp",x:58,y:147,source:IP,detail:"虚构战略树的根节点。CSP 是真实的公开文件家族，但图中的关系没有进行逐条官方核对。"},
    {id:"csp6",label:"目标 6.1",sub:"环境主题 · 示例",type:"csp",x:287,y:66,source:IP,detail:"以环境主题为演示方向；具体条款文字、正式版本与 DP/OP 对应关系尚待核实。"},
    {id:"csp8",label:"目标 8.2",sub:"基础设施 · 示例",type:"csp",x:287,y:231,source:IP,detail:"用于展示战略目标一对多的路径；不声明本演示的下游行动在正式文件中逐项对应。"},
    {id:"dp",label:"交付计划",sub:"DP · 结构示例",type:"csp",x:553,y:92,source:IP,detail:"用 DP 文件家族展示战略实施层级；未加载已批准版本的具体条款。"},
    {id:"op",label:"年度计划",sub:"OP · 结构示例",type:"csp",x:791,y:120,source:IP,detail:"用 OP 文件家族展示年度行动；这里的连接仅是建模示意。"},
    {id:"kpi",label:"指标定义",sub:"口径待验证",type:"csp",x:1074,y:65,source:IP,detail:"绩效指标必须有正式目标、分母、期间和质量信息。这里没有真实 KPI 结果。"},
    {id:"water",label:"水务行动",sub:"合成活动节点",type:"csp",x:1052,y:249,source:IP,detail:"完全虚构的水务工作节点，不对应真实 Council 个案、检查或完成数量。"},
    {id:"audit",label:"证据记录",sub:"合成审核示例",type:"csp",x:1300,y:237,source:IP,detail:"合成审核位置。未产生官方数字凭证、哈希证明、第三方透明收据或实际审核结论。"},
    {id:"lsps",label:"LSPS",sub:"土地利用规划",type:"lsps",x:58,y:496,source:DEV,detail:"LSPS 文件家族作为规划支路入口；它不自动构成 CSP 或 LEP 的下级任务。"},
    {id:"priority",label:"规划优先项",sub:"示例优先事项",type:"lsps",x:304,y:540,source:DEV,detail:"虚构的规划优先事项节点，正式条款编号、原文与适用区域尚待核实。"},
    {id:"lep",label:"LEP 条款",sub:"辖区待核对",type:"lsps",x:568,y:447,source:DEV,detail:"LEP 是需核对适用范围、版本和生效时间的法定规划工具。此节点没有指向实际条款。"},
    {id:"dcp",label:"DCP 控制",sub:"指导性质待核",type:"lsps",x:813,y:536,source:DEV,detail:"DCP 详细规划指导与 LEP 法定效力不能混同。具体条款和辖区没有在本示例核验。"},
    {id:"area",label:"地区适用性",sub:"Berridale · 演示",type:"lsps",x:1074,y:494,source:DEV,detail:"Berridale 仅作地区维度演示。不能据此断言任何特定地块属于某项 LEP/DCP 条款。"},
    {id:"scope",label:"生效时间",sub:"需官方版本",type:"lsps",x:1291,y:496,source:DEV,detail:"必须另行证明指定条款在指定日期及区域有效；没有凭证时保持 UNKNOWN。"},
    {id:"candidate",label:"潜在暗线",sub:"研究假设 · 非事实",type:"candidate",x:1324,y:644,source:null,detail:"这是人为构造的跨文件候选关系。一个主题相近的连接并不能自动证明它在法规、行政或科学上成立。"}
  ];
  const edges = [
    {id:"e1",from:"csp",to:"csp6",kind:"EXAMPLE_PARENT",coverage:.88,time:.42},
    {id:"e2",from:"csp",to:"csp8",kind:"EXAMPLE_PARENT",coverage:.50,time:.38},
    {id:"e3",from:"csp6",to:"dp",kind:"EXAMPLE_LINK",coverage:.75,time:.42},
    {id:"e4",from:"csp8",to:"dp",kind:"EXAMPLE_LINK",coverage:.40,time:.50},
    {id:"e5",from:"dp",to:"op",kind:"EXAMPLE_LINK",coverage:.61,time:.31},
    {id:"e6",from:"op",to:"kpi",kind:"EXAMPLE_LINK",coverage:.34,time:.22},
    {id:"e7",from:"op",to:"water",kind:"EXAMPLE_LINK",coverage:.52,time:.25},
    {id:"e8",from:"water",to:"audit",kind:"EXAMPLE_EVIDENCE",coverage:.25,time:.17},
    {id:"e9",from:"lsps",to:"priority",kind:"EXAMPLE_PARENT",coverage:.78,time:.45},
    {id:"e10",from:"priority",to:"lep",kind:"EXAMPLE_PLANNING",coverage:.36,time:.54},
    {id:"e11",from:"priority",to:"dcp",kind:"EXAMPLE_PLANNING",coverage:.39,time:.24},
    {id:"e12",from:"lep",to:"area",kind:"EXAMPLE_APPLICABILITY",coverage:.20,time:.15},
    {id:"e13",from:"dcp",to:"area",kind:"EXAMPLE_APPLICABILITY",coverage:.24,time:.29},
    {id:"e14",from:"area",to:"scope",kind:"EXAMPLE_APPLICABILITY",coverage:.12,time:.12},
    {id:"e15",from:"csp8",to:"candidate",kind:"RESEARCH_CANDIDATE",coverage:null,time:null,candidate:true},
    {id:"e16",from:"area",to:"candidate",kind:"RESEARCH_CANDIDATE",coverage:null,time:null,candidate:true}
  ];
  const map = Object.fromEntries(nodes.map(n => [n.id,n]));
  const state = {root:"csp", selected:null,mode:"coverage",candidates:false,neighbours:true,search:""};
  const graph = document.getElementById("atlasGraph");
  const details = document.getElementById("details");
  const search = document.getElementById("search");
  const explain = document.getElementById("modeExplanation");
  const el = (tag,attrs={}) => {const e=document.createElementNS(NS,tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));return e;};
  const esc = s => String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  function visibleNode(n) {return n.id!=="candidate" || state.candidates;}
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
    graph.querySelectorAll("[data-drawn]").forEach(e=>e.remove());
    const base=el("g",{"data-drawn":"yes"}); graph.append(base);
    const caption=el("text",{x:70,y:45,class:"lane-caption"});caption.textContent="STRATEGY / DELIVERY / EVIDENCE";base.append(caption);
    const p=el("text",{x:70,y:424,class:"lane-caption"});p.textContent="SPATIAL PLANNING / STATUTORY CONTEXT";base.append(p);
    const focus=focusIds();
    for(const e of edges) {
      if(e.candidate&&!state.candidates)continue;
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
      const g=el("g",{class:"atlas-node "+n.type+(state.selected===n.id?" selected":"")+(dim?" faded":""),transform:"translate("+n.x+" "+n.y+")",tabindex:"0",role:"button","aria-label":"查看 "+n.label+" 的证据详情"});
      g.append(el("rect",{width:155,height:56,rx:12}));
      const t=el("text",{x:13,y:23}); t.textContent=n.label;g.append(t);
      const sub=el("text",{x:13,y:41,class:"sub"});sub.textContent=n.sub;g.append(sub);
      makeTitle(g,n.label+" — "+n.sub+"（合成示例）");
      g.addEventListener("click",()=>select(n.id));
      g.addEventListener("keydown",event=>{if(event.key==="Enter"||event.key===" "){event.preventDefault();select(n.id);}});
      base.append(g);
    }
    const note=el("text",{x:1100,y:725,class:"svg-note"});note.textContent="M0 / SYNTHETIC DATA / NO COUNCIL KPI";base.append(note);
    explain.textContent=state.mode==="coverage"?"演示性关系核验填充；尚无真实 Council 核验率。":
      state.mode==="time"?"演示性期限经过比例；绝不代表行动完成或绩效达成。":
      "实际绩效：无经核验的公开结果与分母，所有进度保持 UNKNOWN（灰色）。";
    document.getElementById("nodeCount").textContent=String(nodes.filter(visibleNode).length);
    document.getElementById("edgeCount").textContent=String(edges.filter(e=>!e.candidate||state.candidates).length);
  }
  function select(id) {
    state.selected=id;const n=map[id];if(!n)return;
    const connected=edges.filter(e=>(e.from===id||e.to===id)&&(!e.candidate||state.candidates));
    const relationButtons=connected.map(e=>{
      const other=map[e.from===id?e.to:e.from];
      return '<button type="button" data-target="'+esc(other.id)+'" title="'+esc(e.kind)+'">'+esc(other.label)+' · '+(e.candidate?"暗线候选":"合成路径")+'</button>';
    }).join("");
    const source=n.source?'<a href="'+esc(n.source)+'" target="_blank" rel="noopener noreferrer">查看公开资料目录 ↗</a>':'没有官方来源可验证';
    details.innerHTML='<div class="detail-head"><div><div class="eyebrow">NODE · '+esc(n.id.toUpperCase())+'</div><h3>'+esc(n.label)+'</h3></div><span class="detail-badge">'+(n.type==="candidate"?"HYPOTHESIS":"SYNTHETIC")+'</span></div>'+
      '<p class="detail-text">'+esc(n.detail)+'</p>'+
      '<div class="detail-list">'+
      '<div class="detail-item"><span class="key">身份与来源</span><span class="value">合成展示节点；非真实 Council 条款关系</span></div>'+
      '<div class="detail-item"><span class="key">内容哈希 / 数字签名</span><span class="value">NOT IMPLEMENTED · 不存在可验证数字凭证</span></div>'+
      '<div class="detail-item"><span class="key">条款、时点与辖区</span><span class="value">UNKNOWN · 尚未进行正式资料核验</span></div>'+
      '<div class="detail-item"><span class="key">可核对入口</span><span class="value">'+source+'</span></div></div>'+
      '<h3 style="margin-top:20px">邻接关系（演示）</h3><div class="relation-list">'+(relationButtons||'<span class="detail-text">当前未展示邻接关系</span>')+'</div>'+
      '<div class="warn">'+(n.type==="candidate"?"暗线是待证伪的研究候选，不可自动成为官方事实。":"这里只演示追溯交互，没有任何已审核的实际绩效、法规适用或政策映射。")+'</div>';
    details.querySelectorAll("[data-target]").forEach(b=>b.addEventListener("click",()=>select(b.dataset.target)));
    draw();
  }
  document.querySelectorAll("[data-root]").forEach(btn=>btn.addEventListener("click",()=>{
    state.root=btn.dataset.root;state.selected=null;
    document.querySelectorAll("[data-root]").forEach(b=>b.classList.toggle("selected",b===btn));
    draw();
  }));
  document.querySelectorAll("[data-mode]").forEach(btn=>btn.addEventListener("click",()=>{
    state.mode=btn.dataset.mode;
    document.querySelectorAll("[data-mode]").forEach(b=>b.setAttribute("aria-pressed",String(b===btn)));
    draw();
  }));
  document.getElementById("showCandidates").addEventListener("change",e=>{state.candidates=e.target.checked;if(!state.candidates&&state.selected==="candidate")state.selected=null;draw();});
  document.getElementById("showNeighbours").addEventListener("change",e=>{state.neighbours=e.target.checked;draw();});
  search.addEventListener("input",e=>{state.search=e.target.value.trim().toLowerCase();draw();});
  document.getElementById("aboutBtn").addEventListener("click",()=>{
    details.innerHTML='<div class="detail-head"><div><div class="eyebrow">RESEARCH NOTICE</div><h3>关于本地原型</h3></div></div><p class="detail-text">本网站是 ClimateOS Public Strategy Atlas 的 M0 工程起点，供独立学习与 UI 验证。图上所有关系、合成进度、节点路径均是人工设计的虚构样本，不可用于官方决策。目录链接并不意味着条款已核准。不会上传任何 Council 内部或个人业务数据。区块链式内容寻址、数字凭证与审计仅在任务书设计范围中，尚未实装。</p><div class="warn">本地演示 ≠ 正式部署；合成关系 ≠ 现行法规；文件完整性 ≠ 语义真实性。</div>';
  });
  draw();
})();
