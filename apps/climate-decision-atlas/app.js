'use strict';
const meterDay = [[123.7,208],[110.5,197],[105.4,198],[137.7,206],[112.5,237],[104.5,257],[108.4,247],[115.2,242],[294.7,219],[377.1,224],[404.8,204],[665.9,159],[733.4,75],[765.2,50],[818.3,46],[1140,36],[1246.5,36],[1264.9,29],[1269.1,29],[1334.2,26],[1654.6,25],[1901.2,23],[1864.7,26],[2040.3,24]];
const icons = {
  layers:'<path d="m2 8 10-5 10 5-10 5zM3 12l9 5 9-5M3 16l9 5 9-5"/>',
  book:'<path d="M4 4h14a2 2 0 012 2v14H6a2 2 0 01-2-2zM7 16h13M8 8h8"/>',
  focus:'<path d="M3 9V4h5m8 0h5v5m0 6v5h-5m-8 0H3v-5"/><circle cx="12" cy="12" r="2"/>',
  clock:'<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',
  play:'<path d="m8 5 10 7-10 7z" fill="currentColor" stroke="none"/>',
  pause:'<path d="M8 5v14m8-14v14" stroke-width="4"/>',
  file:'<path d="M6 3h8l4 4v14H6zM14 3v5h4M9 12h6m-6 4h5"/>'
};
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
function glyph(name){return '<svg viewBox="0 0 24 24" aria-hidden="true">'+icons[name]+'</svg>'}
$$('i[data-icon]').forEach(el=>el.innerHTML=glyph(el.dataset.icon));
const english = document.documentElement.lang.startsWith('en');
const facilities = english ? {
 cold:{title:'Cold store',type:'Cooling / Heat source',desc:'To keep food cold, the refrigeration system moves heat out of the store. Pick an hour to see how much electricity it used.',name:'Cooling system power',col:0,bound:'The meter shows electrical power in kilowatts (kW). To work out how much heat we could reuse, we also need temperatures, flow rates and someone who needs that heat.'},
 tank:{title:'Heat storage tank',type:'Storage / Between shifts',desc:'A tank could hold hot water for the next shift. How long would it need to keep that water warm?',name:'Heat in the tank at this hour',col:null,bound:'This dataset contains no tank temperatures, capacity or water-use readings. The amount of energy a tank could save is still an open question.'},
 wash:{title:'Wash room',type:'Hot water / Heat user',desc:'When the cleaning shift starts, the water needs to be hot enough. Look at the boiler meter to find hours worth investigating.',name:'Electric boiler power',col:1,bound:'This meter covers the whole boiler. We still need to find out how much water the wash room used and how hot it was.'}
} : {
 cold:{title:'生产冷库',type:'冷端设施  /  热源',desc:'制冷系统把热从库内搬出。点选一个小时，查看当时的制冷用电。',name:'制冷系统 1 · 电功率',col:0,bound:'可回收热量还取决于冷凝温度、流量和当时的用热需求。'},
 tank:{title:'跨班储热罐',type:'时间调节  /  储热',desc:'白天收集余热，晚班取用。罐的作用取决于供热和用热错开多久。',name:'同一时段的储罐热量',col:null,bound:'这个案例缺少储罐温度、容量与取水记录，实际节能量待验证。'},
 wash:{title:'清洗车间',type:'用热设施  /  热用户',desc:'热水需要在清洗时段达到要求温度。电锅炉读数帮助我们找到值得调查的时段。',name:'电锅炉 · 电功率',col:1,bound:'电表覆盖整台锅炉；清洗线分项热量和同期取水量仍待核实。'}
};
const choices=english ? {
 direct:'Do the cooler and the hot-water tap run at the same time? Check whether the heat is hot enough to warm the incoming water.',
 store:'How far apart are the shifts? Check how much water the tank can hold, how much heat it loses and how much hot water the next shift uses.',
 base:'Measure the energy needed to make the same amount of food, keep it just as cold and supply the same hot water. Use that as the starting point.'
} : {direct:'先核对冷凝热与取水是否同时出现，再查温度是否足以直接预热。',store:'先看两班之间隔了多久，再核对储罐容量、散热损失和晚班取水量。',base:'先建立当前班次的基准，记录相同产量、冷库温度与热水交付所需的能源。'};
let state={mode:'iso',hour:15,selected:'cold',zoom:1},map,timer;
function mark(list,key,value){list.forEach(el=>el.setAttribute('aria-pressed',String(el.dataset[key]===value)))}
function drawPlot(){
 const col=facilities[state.selected].col,c=$('#plot');
 if(col===null || !c.clientWidth)return;
 const d=window.devicePixelRatio||1,w=c.clientWidth,h=c.clientHeight;
 c.width=Math.round(w*d);c.height=Math.round(h*d);
 const ctx=c.getContext('2d');ctx.scale(d,d);
 const max=Math.max(...meterDay.map(r=>r[col])), xx=i=>4+i*(w-8)/23,yy=v=>h-4-v/max*(h-9);
 ctx.strokeStyle='#d4dcca';ctx.lineWidth=1;
 for(const fraction of [.3,.7,1]){ctx.beginPath();ctx.moveTo(0,h*fraction-1);ctx.lineTo(w,h*fraction-1);ctx.stroke()}
 const line=()=>{ctx.beginPath();meterDay.forEach((v,i)=>i?ctx.lineTo(xx(i),yy(v[col])):ctx.moveTo(xx(i),yy(v[col])))};
 line();ctx.lineTo(xx(23),h);ctx.lineTo(xx(0),h);ctx.closePath();ctx.fillStyle='#b2c79855';ctx.fill();
 line();ctx.strokeStyle='#597748';ctx.lineWidth=1.8;ctx.stroke();
 const x=xx(state.hour),y=yy(meterDay[state.hour][col]);ctx.strokeStyle='#a66c38';ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();ctx.fillStyle='#b46230';ctx.beginPath();ctx.arc(x,y,3.4,0,2*Math.PI);ctx.fill()
}
function refresh(){
 const f=facilities[state.selected],t=String(state.hour).padStart(2,'0')+':00';
 $('#time').textContent=t;$('#metricTime').textContent=t;$('#hour').value=state.hour;$('#hour').setAttribute('aria-valuetext',t);
 $('#iso').setAttribute('aria-pressed',state.mode==='iso');$('#plan').setAttribute('aria-pressed',state.mode==='plan');
 mark($$('[data-node]'),'node',state.selected);
 $('#kind').textContent=f.type;$('#nodeTitle').textContent=f.title;$('#desc').textContent=f.desc;$('#boundary').textContent=f.bound;$('#metricName').textContent=f.name;
 $('#metric').textContent=f.col===null?(english ? 'Unknown' : '待测'):meterDay[state.hour][f.col].toLocaleString('en-AU');$('#unit').textContent=f.col===null?'':'kW';
 $('.plotbox').hidden=f.col===null;$('#plotlabel').textContent=(english ? 'Norway · 5 Jan 2021 · Hourly meter readings' : '挪威鱼加工厂 · 2021.01.05 · 逐时实测');drawPlot();
 map?.update(state);updateZoom()
}
function updateZoom(){ $('#plus').disabled=state.zoom>=2.4;$('#minus').disabled=state.zoom<=.72 }
function stop(){clearInterval(timer);timer=null;$('#play').innerHTML=glyph('play');$('#play').setAttribute('aria-label',(english ? 'Play the day' : '播放一天'))}
function setHour(h){state.hour=h;refresh()}
$('#play').onclick=()=>{if(timer){stop();return}$('#play').innerHTML=glyph('pause');$('#play').setAttribute('aria-label',(english ? 'Pause playback' : '暂停回放'));timer=setInterval(()=>setHour((state.hour+1)%24),1100)};
$('#hour').oninput=e=>{stop();setHour(+e.target.value)};
$$('[data-node]').forEach(b=>b.onclick=()=>{state.selected=b.dataset.node;refresh()});
for(const mode of ['iso','plan'])$('#'+mode).onclick=()=>{state.mode=mode;refresh()};
$('#plus').onclick=()=>{state.zoom=Math.min(2.4,state.zoom+.2);refresh()};
$('#minus').onclick=()=>{state.zoom=Math.max(.72,state.zoom-.2);refresh()};
$('#reset').onclick=()=>{map.reset();state.zoom=1;refresh()};
function choose(k){mark($$('[data-choice]'),'choice',k);$('#choiceText').textContent=choices[k]}
$$('[data-choice]').forEach(b=>b.onclick=()=>choose(b.dataset.choice));choose('direct');
function route(){
 let page=location.hash.slice(1);if(!['atlas','records','about'].includes(page))page='atlas';
 $('#lang').hash=page;
 $$('[data-page]').forEach(s=>s.hidden=s.id!==page);
 $$('[data-tab]').forEach(a=>a.dataset.tab===page?a.setAttribute('aria-current','page'):a.removeAttribute('aria-current'));
 if(page!=='atlas')stop();else requestAnimationFrame(()=>{drawPlot();map?.update(state)});
 window.scrollTo(0,0);
}
map=window.ClimateMap.init($('#scene'),{onPick:id=>{if(facilities[id]){state.selected=id;refresh()}},onViewChange:v=>{if(Number.isFinite(v.zoom)){state.zoom=v.zoom;updateZoom()}}});
map.bindMinimap($('#mini'));refresh();route();window.addEventListener('hashchange',route);window.addEventListener('resize',drawPlot);
document.addEventListener('visibilitychange',()=>{if(document.hidden)stop()});
