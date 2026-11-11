(function(root){
 'use strict';
 const KEY='climateos-earth-expedition-v1',LIMIT=1000;
 function validate(doc){
  if(!doc||doc.format!=='expedition-notebook/1'||!Array.isArray(doc.events)||doc.events.length>LIMIT)throw Error('笔记格式或数量不支持');
  if(new TextEncoder().encode(JSON.stringify(doc)).length>1048576)throw Error('笔记超过1MiB，请保留已有备份');
  const ids=new Set();
  for(const e of doc.events){
   if(!e||typeof e.id!=='string'||e.id.length>100||ids.has(e.id)||!['note','progress','bookmark'].includes(e.kind)||typeof e.station!=='string'||e.station.length>50||typeof e.text!=='string'||e.text.length>5000||typeof e.at!=='string'||!Number.isFinite(Date.parse(e.at)))throw Error('笔记事件无效或ID重复');
   ids.add(e.id);
  }
  return doc;
 }
 function merge(a,b){validate(a);validate(b);const map=new Map(a.events.map(e=>[e.id,e]));
  for(const e of b.events){if(map.has(e.id)&&JSON.stringify(map.get(e.id))!==JSON.stringify(e))throw Error('同ID不同内容：拒绝覆盖原笔记');map.set(e.id,e);}
  return validate({format:'expedition-notebook/1',events:[...map.values()]});
 }
 function empty(){return {format:'expedition-notebook/1',events:[]};}
 const api={KEY,validate,merge,empty};
 if(typeof module!=='undefined')module.exports=api;else root.ExpeditionNotebook=api;
})(typeof window==='undefined'?globalThis:window);
