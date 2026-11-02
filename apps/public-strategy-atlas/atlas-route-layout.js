/* Display projection only. Every station/connection refers to the existing AtlasData. */
(function(root){
'use strict';
const positions={csp:[110,265],csp6:[330,160],csp8:[340,365],dp:[565,220],op:[790,220],kpi:[1005,135],water:[1005,365],audit:[1240,365],lsps:[115,585],priority:[365,585],lep:[610,500],dcp:[640,640],area:[910,585],scope:[1175,585],candidate:[1240,485]};
function project(dataset,visibleIds){
 return {nodes:dataset.nodes.filter(n=>visibleIds.has(n.id)).map(n=>({...n,title:n.label,subtitle:n.sub,x:positions[n.id]?.[0]??n.x,y:positions[n.id]?.[1]??n.y})),edges:dataset.edges.filter(e=>visibleIds.has(e.from)&&visibleIds.has(e.to)),truncated:false};
}
function path(a,b,candidate=false){const dx=b.x-a.x;return candidate?`M ${a.x} ${a.y} Q ${(a.x+b.x)/2} ${Math.min(a.y,b.y)-70} ${b.x} ${b.y}`:`M ${a.x} ${a.y} C ${a.x+dx*.48} ${a.y} ${b.x-dx*.42} ${b.y} ${b.x} ${b.y}`;}
function corridor(dataset,start){const ids=new Set([start]),queue=[start];while(queue.length){const id=queue.shift();for(const e of dataset.edges)if(!e.candidate&&e.from===id&&!ids.has(e.to)){ids.add(e.to);queue.push(e.to);}}return ids;}
const api={positions,project,path,corridor};root.AtlasRouteLayout=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
