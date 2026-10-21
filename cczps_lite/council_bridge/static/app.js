"use strict";
const $ = id => document.getElementById(id);
const token = location.hash.slice(1);
history.replaceState(null, "", location.pathname);
let state, councils = [], prepared = null, preview = null, activeCouncil = "";
function node(tag, text, cls) { const e = document.createElement(tag); if (text !== undefined) e.textContent = text; if (cls) e.className = cls; return e; }
function message(text, error = false) { $("message").textContent = text; $("message").className = error ? "error" : ""; }
async function api(path, body) {
  const response = await fetch("/api/" + path, {method: body === undefined ? "GET" : "POST", headers: {"Authorization": "Bearer " + token, "X-Council-ID": activeCouncil, "Content-Type": "application/json"}, ...(body === undefined ? {} : {body: JSON.stringify(body)})});
  const data = await response.json(); if (!response.ok) throw new Error(data.error || "请求失败"); return data;
}
function button(text, fn, disabled = false) { const e = node("button", text); e.disabled = disabled; e.onclick = () => run(fn); return e; }
async function run(fn) { try { await fn(); await refresh(); } catch (e) { message(e.message, true); } }
async function act(action, payload) { const result = await api(action, payload); message("本地操作已记录；结果仍为合成演练。"); return result; }
function resetDrafts() { prepared = null; preview = null; $("request").textContent = "尚未准备"; $("preview-body").textContent = "尚未预览"; $("submit").disabled = $("approve").disabled = $("export").disabled = true; }
async function refresh() { state = await api("state"); render(); }
function render() {
  $("title").textContent = state.config.name;
  $("metrics").replaceChildren(...[[state.config.objects.length, "已登记的合成空间对象"], [state.assessments.length, "限时回答／演练"], [state.evidence.length, "合成证据记录"], ["未知", "真实当前环境状态"]].map(([value, label]) => { const e = node("div", undefined, "metric"); e.append(node("strong", value), node("span", label)); return e; }));
  $("boundary").textContent = "边界版本：" + state.config.boundary.version + " · 未加载官方几何。证据截止：" + state.evidence.map(e=>e.observed_at).sort()[0] + "（合成样例时间，不是实时数据）。";
  renderMap();
  $("legacy").replaceChildren(...state.config.legacy_references.map(r => node("p", r.path + " — " + r.use)));
  $("jobs").replaceChildren(...Object.values(state.jobs).map(job => { const c = node("div", undefined, "card"), id = job.request.request_id; c.append(node("h3", id), node("span", job.status, "badge"), node("p", "服务：" + job.provider_id + " · 尝试次数：" + job.attempts)); const controls = node("div", undefined, "controls"); if (job.status === "QUEUED") controls.append(button("接收模拟结果", () => act("progress", {request_id:id})), button("模拟超时", () => act("progress", {request_id:id,mode:"timeout"})), button("取消", () => act("progress", {request_id:id,action:"cancel"}))); if (["FAILED","TIMED_OUT"].includes(job.status)) controls.append(button("重试", () => act("progress", {request_id:id,action:"retry"}),job.attempts >= 3)); if (job.status === "COMPLETED_QUARANTINED" && !state.assessments.some(a => a.run_request_id === id)) controls.append(button("检查地方适用性并生成回答", () => act("assess", {request_id:id}))); c.append(controls); if (job.receipt) { const d = node("details"); d.append(node("summary", "回执与隔离结果"), node("pre", JSON.stringify({receipt:job.receipt,result:job.result},null,2))); c.append(d); } return c; }));
  $("answer-list").replaceChildren(...state.assessments.map(a => { const c = node("div", undefined, "card"); c.append(node("h3", a.answer_id), node("span", a.display_state + " · " + a.conclusion_level + "/" + a.evidence_maturity, "badge"), node("p", a.answer), node("p", "缺口：" + a.missing_critical_evidence.join("；")), node("p", "分歧：" + a.conflicting_evidence.join("；")), node("p", "有效至：" + a.valid_until)); const controls = node("div",undefined,"controls"); if (a.display_state === "PENDING_HUMAN_REVIEW") controls.append(button("接受演练 · 非科学签署", () => act("review",{answer_id:a.answer_id,decision:"ACCEPT_DEMO"})), button("拒绝演练", () => act("review",{answer_id:a.answer_id,decision:"REJECT_DEMO"}))); if (a.display_state === "ACCEPT_DEMO") controls.append(button("记录合成后续结果", () => act("observe",{answer_id:a.answer_id}))); const d=node("details");d.append(node("summary","完整回答与证据护照"),node("pre",JSON.stringify(a,null,2)));c.append(controls,d); return c; }));
  $("evidence-list").replaceChildren(...state.evidence.map(e => { const r=node("tr");r.append(node("td",e.evidence_id+" / "+e.spatial_id),node("td",e.classification+" / "+e.source),node("td",e.observed_at+" / "+e.freshness+" / "+e.status)); const td=node("td");td.append(button("撤回",async()=>{await act("withdraw",{evidence_id:e.evidence_id});resetDrafts();},e.status!=="ACTIVE"));r.append(td);return r; }));
  $("imports").textContent=JSON.stringify(state.imports,null,2);
  $("audit").textContent="本地摘要链一致性："+(state.audit_consistent?"通过":"失败")+"。这不等于独立身份、来源真实性或外部防篡改证明。";
  $("outcomes").replaceChildren(...state.outcomes.map(o=>node("p",o.at+" · "+o.outcome)));
  $("events").replaceChildren(...state.events.slice().reverse().map(e=>node("p",e.at+" · "+e.type)));
}
function renderMap() {
  const svg=$("map"), ns="http://www.w3.org/2000/svg";svg.replaceChildren();
  const objects=new Map(state.config.objects.map(o=>[o.id,o]));
  for(const r of state.config.relations){const a=objects.get(r.from),b=objects.get(r.to),line=document.createElementNS(ns,"line");for(const [k,v] of Object.entries({x1:a.x*7.5+20,y1:a.y*4.6+10,x2:b.x*7.5+20,y2:b.y*4.6+10}))line.setAttribute(k,v);svg.append(line);}
  for(const o of objects.values()){const g=document.createElementNS(ns,"g"),circle=document.createElementNS(ns,"circle"),text=document.createElementNS(ns,"text");g.setAttribute("tabindex","0");g.setAttribute("role","button");g.setAttribute("aria-label",o.name);circle.setAttribute("cx",o.x*7.5+20);circle.setAttribute("cy",o.y*4.6+10);circle.setAttribute("r","10");text.setAttribute("x",Math.min(o.x*7.5,590));text.setAttribute("y",o.y*4.6+37);text.textContent=o.name.slice(0,30);const select=()=>{$("object-detail").replaceChildren(node("h3",o.name),node("p",o.kind),node("p",o.id),node("p","SYNTHETIC_ONLY · 不是正式边界或真实环境证据"),node("p","相关证据："+state.evidence.filter(e=>e.spatial_id===o.id).map(e=>e.evidence_id).join("；")));};g.onclick=select;g.onkeydown=e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();select();}};g.append(circle,text);svg.append(g);}
}
$("council").onchange=()=>run(async()=>{activeCouncil=$("council").value;resetDrafts();$("object-detail").replaceChildren(node("p","请选择当前 Council 的一个对象。"));});
$("prepare").onclick=()=>run(async()=>{prepared=await api("prepare",{});$("request").textContent=JSON.stringify(prepared,null,2);$("submit").disabled=false;});
$("submit").onclick=()=>run(async()=>{await act("submit",{request:prepared,provider:$("provider").value});prepared=null;$("submit").disabled=true;});
$("preview").onclick=()=>run(async()=>{preview=await api("preview");$("preview-body").textContent=JSON.stringify(preview,null,2);$("approve").disabled=false;$("export").disabled=true;});
$("approve").onclick=()=>run(async()=>{await act("approve",{digest:preview.digest});$("release-digest").value=preview.digest;$("export").disabled=false;});
$("export").onclick=()=>run(async()=>{const data=await api("export",{digest:preview.digest}),blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"}),url=URL.createObjectURL(blob),a=node("a");a.href=url;a.download="climateos-synthetic-metadata.json";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
$("import").onclick=()=>run(()=>act("import",{source_council:$("source").value,digest:$("release-digest").value}));
$("sync").onclick=()=>run(()=>act("sync",{}));
(async()=>{try{if(!token)throw new Error("请使用启动程序显示的完整本地链接，包含会话访问码。");councils=await api("councils");for(const c of councils){for(const id of ["council","source"]){const o=node("option",c.name);o.value=c.id;$(id).append(o);}}activeCouncil=councils[0].id;await refresh();}catch(e){message(e.message,true);}})();
