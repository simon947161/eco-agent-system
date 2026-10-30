/* Public URL state only. A URL never carries a private workspace or approval. */
(function(root){
'use strict';
const ROUTES=Object.freeze([
 ['atlas','/atlas'],['knowledge','/knowledge/:id'],['strategy','/strategy'],['strategy-detail','/strategy/:id'],
 ['wcos','/domains/wcos'],['wcos-domain','/domains/wcos/:domain'],['phe','/domains/phe'],['phe-domain','/domains/phe/:domain'],
 ['data','/data'],['data-record','/data/:id'],['operations','/operations'],['operation','/operations/:id'],['calendar','/calendar'],['calendar-item','/calendar/:id'],
 ['metrics','/metrics'],['metric','/metrics/:id'],['resources','/resources'],['resource','/resources/:id'],
 ['sources','/sources'],['source','/sources/:id'],['discovery','/discovery'],['audit','/audit'],['coverage','/coverage'],['assistant','/assistant']
].map(([name,pattern])=>Object.freeze({name,pattern})));
const QUERY=new Set(['q','year','yearBasis','date','region','status','unit','source','domain','page','item','companion']);
function allowed(value,max=512){return typeof value==='string'&&value.length<=max&&!/[\x00-\x1f\x7f]/.test(value);}
function queryState(input){
 const result={},params=input instanceof URLSearchParams?input:new URLSearchParams(input||'');
 for(const [key,value]of params){if(!QUERY.has(key)||!allowed(value,key==='q'?200:512)||Object.hasOwn(result,key))continue;
  if(['page','year'].includes(key)&&!/^\d{1,4}$/.test(value))continue;
  if(key==='date'&&!/^\d{4}-\d{2}-\d{2}$/.test(value))continue;
  if(key==='companion'&&value!=='1')continue;
  if(key==='yearBasis'&&!['CALENDAR','AU_FISCAL'].includes(value))continue;
  result[key]=value;
 }
 return result;
}
function failure(){return {name:'not-found',path:'/not-found',params:{},query:{},valid:false};}
function parse(input=''){
 if(typeof input!=='string'||input.length>4096)return failure();
 let raw=input.startsWith('#')?input.slice(1):input;
 if(!raw||raw==='/')raw='/atlas';
 if(!raw.startsWith('/')||raw.startsWith('//')||/[\x00-\x20\x7f\\]/.test(raw))return failure();
 const [rawPath,...queryParts]=raw.split('?');if(queryParts.length>1)return failure();
 const pieces=rawPath.replace(/\/$/,'').split('/').slice(1);let decoded;
 try{decoded=pieces.map(decodeURIComponent);}catch{return failure();}
 if(decoded.some(value=>!allowed(value)||!value||value==='.'||value==='..'||/[\/\\?#]/.test(value)))return failure();
 for(const route of ROUTES){const pattern=route.pattern.split('/').slice(1);if(pattern.length!==decoded.length)continue;
  const params={};if(!pattern.every((part,i)=>part.startsWith(':')?(params[part.slice(1)]=decoded[i],true):part===decoded[i]))continue;
  return {name:route.name,path:'/'+decoded.map(encodeURIComponent).join('/'),params,query:queryState(queryParts[0]),valid:true};
 }
 return failure();
}
function href(path='/atlas',query={}){
 const route=parse(path);if(!route.valid)throw Error('INVALID_PUBLIC_ROUTE');
 const params=new URLSearchParams(queryState(query));params.sort();
 return '#'+route.path+(params.size?'?'+params.toString():'');
}
function companionUrl(current,path,query={}){
 const url=new URL(current);if(!['http:','https:','file:'].includes(url.protocol)||url.username||url.password)throw Error('UNSAFE_COMPANION_URL');
 url.search='';url.hash=href(path,{...queryState(query),companion:'1'}).slice(1);return url.href;
}
function navigate(path,query={},options={}){
 const target=href(path,query);if(!root.location)throw Error('BROWSER_REQUIRED');
 if(options.replace){root.history.replaceState(null,'',target);root.dispatchEvent(new Event('hashchange'));}
 else if(root.location.hash===target)root.dispatchEvent(new Event('hashchange'));
 else root.location.hash=target;
}
function subscribe(listener){if(!root.addEventListener)throw Error('BROWSER_REQUIRED');const handler=()=>listener(parse(root.location.hash));root.addEventListener('hashchange',handler);handler();return()=>root.removeEventListener('hashchange',handler);}
const api={ROUTES,queryState,parse,href,companionUrl,navigate,subscribe};root.CsoiRouter=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
