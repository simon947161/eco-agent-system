/* Connected workspaces over the existing Atlas records; no second graph or remote calls. */
(function(root){
'use strict';
const R=typeof module!=='undefined'?require('./csoi-router.js'):root.CsoiRouter;
const NAV=[['Route map','/atlas'],['Strategy','/strategy'],['WCOS','/domains/wcos'],['PHE knowledge','/domains/phe'],['Operations','/operations'],['Calendar','/calendar'],['Metrics','/metrics'],['Resources','/resources'],['Sources','/sources'],['Discovery','/discovery'],['Audit','/audit'],['Coverage','/coverage'],['Michele drafts','/assistant']];
const TITLES={atlas:'Knowledge route map',knowledge:'Inside the knowledge',strategy:'Strategy and plans','strategy-detail':'Strategy dossier',wcos:'WCOS — controlled interface','wcos-domain':'WCOS professional knowledge',phe:'Public health and environment','phe-domain':'Public professional knowledge',operations:'Operations and work','operation':'Work card',calendar:'Operational year','calendar-item':'Calendar work item',metrics:'Metrics and evidence',metric:'Metric dossier',resources:'Resource requirements',resource:'Resource dossier',sources:'Source register',source:'Source evidence',discovery:'Discovery and challenge',audit:'History and independent audit',coverage:'Coverage and gaps',assistant:'Michele — draft assistance','not-found':'Page not found'};
function element(tag,text,attrs={}){const e=document.createElement(tag);if(text!==undefined&&text!==null)e.textContent=String(text);for(const [name,value]of Object.entries(attrs))if(value!==null&&value!==undefined)e.setAttribute(name,String(value));return e;}
function link(label,path,query={}){return element('a',label,{href:R.href(path,query)});}
function action(label,callback){const e=element('button',label,{type:'button'});e.addEventListener('click',callback);return e;}
function text(host,value,tag='p'){const e=element(tag,value);host.append(e);return e;}
function values(value){return Array.isArray(value)?value:[];}
function title(record){return record?.title||record?.label||record?.id||'Unknown record';}
function recordId(record){return encodeURIComponent(record.id);}
function details(host,record){if(!displayAllowed(record)){text(host,'Protected or unreviewed release content is unavailable in this public workspace.');return;}const dl=element('dl',null,{class:'csoi-fields'});for(const [key,value]of Object.entries(record||{})){if(value===undefined)continue;dl.append(element('dt',key),element('dd',typeof value==='object'?JSON.stringify(value,null,2):value));}host.append(dl);}
function section(host,heading){const e=element('section',null,{class:'csoi-section'});text(e,heading,'h2');host.append(e);return e;}
function records(host,items,path,empty='No records are available for this scope. UNKNOWN remains distinct from zero.',query={}){
 items=publicOnly(items);if(!items.length){text(host,empty);return;}
 const list=element('ul',null,{class:'csoi-records'});for(const record of items){const li=element('li');li.append(link(title(record),path+'/'+recordId(record),query));text(li,[record.kind||record.type,record.classification||record.status||record.state||'UNKNOWN'].filter(Boolean).join(' · '),'small');list.append(li);}host.append(list);
}
function sourceUrl(host,url,label='Open official public source'){try{const parsed=new URL(url);if(parsed.protocol!=='https:'||parsed.username||parsed.password)return;text(host,'Source URL: '+parsed.hostname,'small');host.append(element('a',label,{href:parsed.href,target:'_blank',rel:'noopener noreferrer'}));}catch{/* Missing/unsafe URL stays unavailable. */}}
function catalogue(dataset){return dataset.domain?.sourceCatalogue||root.AtlasSourceCatalogue||null;}
function allEntities(dataset){return publicOnly([...(dataset.nodes||[]),...(dataset.contentItems||[]),...(dataset.domain?.entities||[])]);}
function queryFilter(items,query){const needle=(query.q||'').toLowerCase();return items.filter(item=>(!needle||JSON.stringify(item).toLowerCase().includes(needle))&&(!query.region||JSON.stringify(item.scope||item.geography||item.data?.area||'').includes(query.region))&&(!query.unit||item.data?.unit===query.unit)&&(!query.status||[item.state,item.status,item.classification,item.admission].includes(query.status)));}
function displayAllowed(record){
 const G=typeof module!=='undefined'?require('./csoi-governance.js'):root.AtlasCSOIGovernance;
 const envelope=record?.data?.csoiRecord||(record?.format==='csoi-record-1'?record:null);
 if(envelope&&(!G||!G.assessPublic(envelope,{operation:'DISPLAY'}).allowed))return false;
 const queue=[record],seen=new Set(),forbidden=new Set(['PERSONAL_PRIVATE','PRIVATE','COUNCIL_PROTECTED','APPROVED_RELEASE']);
 for(let i=0;i<queue.length;i++){if(i>=100000)return false;const row=queue[i];if(!row||typeof row!=='object')continue;if(seen.has(row))continue;seen.add(row);
  for(const [key,value]of Object.entries(row)){if(['security','permission','privacy','classification','confidentiality'].includes(key)&&forbidden.has(value))return false;if(value&&typeof value==='object')queue.push(value);}
 }
 return true;
}
function publicOnly(items){return items.filter(displayAllowed);}
function mount(bridge={}){
 if(!R||typeof bridge.getDataset!=='function')throw Error('CSOI_BRIDGE_REQUIRED');
 const routeMap=document.getElementById('routeMap'),app=document.querySelector('.app');if(!routeMap||!app)throw Error('ATLAS_HOST_REQUIRED');
 let generation=0,currentRoute=R.parse(location.hash),destroyed=false;
 const host=element('main',null,{id:'csoiWorkspace',class:'csoi-workspace',hidden:'',tabindex:'-1'});app.append(host);
 const menu=element('details',null,{class:'csoi-navigation',id:'csoiNavigation'}),summary=element('summary','Pages');menu.append(summary);const nav=element('nav',null,{'aria-label':'CSOI workspaces',class:'csoi-page-links'});for(const [label,path]of NAV)nav.append(link(label,path));menu.append(nav);document.querySelector('.command-bar').append(menu);
 const onNavClick=e=>{if(e.target.closest('a'))menu.open=false;};nav.addEventListener('click',onNavClick);
 function mapContext(method,id){R.navigate('/atlas',{item:id});setTimeout(()=>bridge[method]?.(id),0);}
 function tools(host,entries){const row=element('div',null,{class:'csoi-actions'});for(const [label,method,arg]of entries)if(typeof bridge[method]==='function')row.append(action(label,()=>bridge[method](arg)));host.append(row);}
 function contentPage(main,dataset,route){
  const id=route.params.id,item=allEntities(dataset).find(record=>record.id===id);
  if(!item){text(main,'No object with this identity exists in the loaded dataset.');main.append(link('Return to strategy','/strategy'));return;}
  text(main,title(item),'h2');text(main,item.text||item.detail||item.localNote||'This record has no admitted source text.');
  text(main,'Evidence state: '+(item.classification||item.status||'UNKNOWN')+' · Official applicability: '+(item.admission||'UNKNOWN'));
  const parents=element('nav',null,{'aria-label':'Parent and station context'});if(item.parentId)parents.append(link('↑ Parent','/knowledge/'+encodeURIComponent(item.parentId)));if(item.ownerNodeId||item.stationId)parents.append(link('Strategy station','/strategy/'+encodeURIComponent(item.ownerNodeId||item.stationId)));main.append(parents);
  const children=(dataset.contentItems||[]).filter(record=>record.parentId===id),offset=Math.max(0,(Number(route.query.page)||1)-1)*30;
  const childHost=section(main,'Children and downstream content');records(childHost,children.slice(offset,offset+30),'/knowledge','Source-backed leaves can have no admitted children. Missing content is not a completed investigation.');
  if(children.length>30){const pager=element('nav',null,{'aria-label':'Child pages'});if(offset>0)pager.append(link('Previous children',route.path,{...route.query,page:String(Math.floor(offset/30))}));if(offset+30<children.length)pager.append(link('Next children',route.path,{...route.query,page:String(Math.floor(offset/30)+2)}));childHost.append(pager);}
  const edges=root.AtlasModel?.queryRelationships?.(dataset,id,{direction:'both'})||[];const connected=section(main,'Typed relationships and reverse trace');
  if(!edges.length)text(connected,'No evidence-supported relationship is available. Official strategic linkage remains UNKNOWN.');
  for(const edge of edges.slice(0,50)){const other=edge.from===id?edge.to:edge.from;connected.append(link((edge.predicate||'RELATED')+' → '+other,'/knowledge/'+encodeURIComponent(other)));text(connected,edge.classification||edge.status||'UNKNOWN','small');}
  const metadata=element('details');metadata.append(element('summary','Identity, source, scope and revision'));details(metadata,item);main.append(metadata);
  if(item.provenance?.url)sourceUrl(main,item.provenance.url);
  main.append(action('View this object on the route map',()=>mapContext(item.ownerNodeId?'openContent':'openStation',item.ownerNodeId?id:item.stationId||id)));
 }
 function strategyPage(main,dataset,route){
  text(main,'CSP → DP → OP describes the formal implementation/reporting framework. The displayed sample links remain synthetic unless separately evidenced. LSPS, LEP and DCP retain distinct scope and legal roles.');
  const nodes=dataset.nodes||[];
  if(route.params.id){const n=nodes.find(n=>n.id===route.params.id);if(!n){text(main,'Strategy station not found.');return;}text(main,title(n),'h2');text(main,n.detail);main.append(action('Open route context',()=>mapContext('openStation',n.id)));records(main,(dataset.contentItems||[]).filter(c=>c.ownerNodeId===n.id&&c.parentId===null),'/knowledge');records(section(main,'Work, quantities, resources and evidence'),(dataset.domain?.entities||[]).filter(e=>e.stationId===n.id),'/knowledge');}
  else records(main,queryFilter(nodes,route.query),'/strategy');
 }
 function sourcesPage(main,dataset,route){
  const cat=catalogue(dataset),items=publicOnly(cat?.sources||dataset.sources||[]);
  if(route.params.id){const record=items.find(s=>s.id===route.params.id);if(!record){text(main,'Source not found.');return;}text(main,title(record),'h2');sourceUrl(main,record.officialUrl||record.url);if(cat&&root.AtlasIntake)details(main,root.AtlasIntake.sourceStatus(cat,record.id));details(main,record);}
  else{records(main,queryFilter(items,route.query),'/sources');tools(main,[['Open source intake inspector','openSources']]);}
 }
 function coreRecordsPage(main,dataset,route){
  const kinds=route.name.startsWith('metric')?['MetricDefinition','QuantifiedObservation','Baseline','Target','Output','Outcome','AuditReceipt']:route.name.startsWith('resource')?['ResourceAccount','Asset','Workforce','FinancialEntry','CostAllocation','FundingSource']:['Program','Project','WorkPackage','Activity','Task','Deliverable'];
  const items=(dataset.domain?.entities||[]).filter(e=>kinds.includes(e.kind));
  if(route.params.id){contentPage(main,dataset,route);return;}
  text(main,'Records use the existing Atlas identities and immutable revisions. Synthetic work and costs are research scenarios; no Council completion, spend or official attribution is inferred.');records(main,queryFilter(items,route.query),route.path);
  const work=root.AtlasCSOIWork||root.CsoiWork;if(work?.syntheticFixture){const fixture=work.syntheticFixture();const part=section(main,'Synthetic regulatory workload rehearsal');details(part,route.name==='resources'?work.resources(fixture.tasks,{annualProductiveHoursPerPerson:1200}):route.name==='metrics'?work.coverage(fixture.items,'2026-10-30'):work.workload(fixture.tasks));}
 }
 function professionalPage(main,dataset,route){
  const isPhe=route.name.startsWith('phe'),P=root.CsoiPhe||root.AtlasCSOIPhe,W=root.AtlasCSOIWcos||root.CsoiWcos;
  text(main,isPhe?'Public-source professional knowledge. Council-specific responsibility, current legal applicability and internal procedures require separate review.':'Read-only synthetic interface contracts. Council business records remain in their authorised professional system; no private WCOS data has been imported.');
  const domains=values(P?.domains).filter(d=>isPhe?!['ltw','backflow'].includes(d.id):['ltw','backflow'].includes(d.id));
  const fallback=isPhe?[['food','Food safety'],['ossm','On-site sewage'],['pools','Public pools and spas'],['cooling','Cooling and warm water'],['skin','Skin penetration'],['environment','Environmental health']]:[['ltw','Liquid trade waste'],['backflow','Backflow prevention']];
  const entries=domains.length?domains:fallback.map(([id,title])=>({id,title,summary:'Source and local applicability review pending.'}));
  if(!route.params.domain)records(main,entries,isPhe?'/domains/phe':'/domains/wcos');
  else{const domain=entries.find(d=>d.id===route.params.domain);if(!domain){text(main,'No registered professional domain has this identity.');return;}text(main,title(domain),'h2');text(main,domain.summary);for(const child of values(domain.children)){const s=section(main,title(child));text(s,child.text);details(s,{judgmentType:child.judgmentType,sourceId:child.sourceId,locator:child.locator,conditions:child.conditions,exceptions:child.exceptions,reviewState:child.reviewState});}if(!domain.children?.length)text(main,'Exact source sections and local workflow allocation remain PENDING. No regulatory obligation is inferred from the domain name.');}
  if(!isPhe&&W?.syntheticFixture){const fixture=W.syntheticFixture();const s=section(main,'Controlled synthetic adapter example');details(s,{boundary:'SYNTHETIC_ONLY / READ_ONLY',records:values(fixture.records).length});if(W.conditionalServices){const demo={type:'RESTAURANT',foodHandling:true,tradeWasteDischarge:true,potableWaterConnection:true};try{details(s,W.conditionalServices(demo));}catch{text(s,'Conditional assessment requires the full source-bound activity schema.');}}}
  main.append(link('Browse source evidence','/sources'),link('Open work cards','/operations'),link('Operational calendar','/calendar'));
 }
 function calendarPage(main,dataset,route){
  const C=root.AtlasCSOICalendar;if(!C?.annualEdition){text(main,'Calendar engine is not loaded in this software build. No schedules or completion are inferred.');main.append(link('Explore recorded tasks','/operations'));return;}
  const year=Number(route.query.year)||2026,edition=C.annualEdition({year,missionId:'public-research',yearBasis:'CALENDAR',tasks:C.syntheticTasks(year)});
  if(bridge.renderCalendar){bridge.renderCalendar({host:main,route,dataset,edition,navigate:R.navigate,link,element});return;}
  text(main,'Synthetic calendar rehearsal. Planned dates do not imply actual execution or Council assignment.');
  const yearForm=element('form'),yearLabel=element('label','Operating year'),yearInput=element('input',null,{name:'year',type:'number',min:'2000',max:'2100',value:year});yearLabel.append(yearInput);yearForm.append(yearLabel,element('button','Change year',{type:'submit'}));yearForm.addEventListener('submit',e=>{e.preventDefault();R.navigate('/calendar',{year:yearInput.value});});main.append(yearForm);
  const nodes=Array.isArray(edition.nodes)?edition.nodes:Array.isArray(edition.objects)?edition.objects:Object.values(edition.nodes||edition.objects||{}),id=route.params.id;
  if(id){const node=nodes.find(n=>n.id===id)||values(edition.tasks).find(t=>t.id===id);if(node){text(main,title(node),'h2');text(main,node.kind+' · '+node.from+' to '+node.to);const parentNav=element('nav',null,{'aria-label':'Calendar parents'});for(const parent of C.parents(edition,id))parentNav.append(link('↑ '+title(parent),'/calendar/'+recordId(parent),{year:String(year)}));main.append(parentNav);
    const task=edition.tasks.find(t=>t.id===node.taskId);if(task){const card=section(main,'Synthetic work card');details(card,C.taskCard(task));card.append(link('Trace strategy context','/strategy/'+encodeURIComponent(task.stationId)));if(bridge.registerScenario)card.append(action('Append task to local research model',()=>bridge.registerScenario(C.scenarioPayload(task))));}
    const offset=Math.max(0,(Number(route.query.page)||1)-1)*30,children=C.children(edition,id,{offset,limit:30});records(main,children.items,'/calendar','No child work record is present. Actual execution and evidence remain UNKNOWN.',{year:String(year)});if(children.nextOffset!==null)main.append(link('Next calendar items',route.path,{...route.query,page:String(Math.floor(offset/30)+2)}));
    if(node.kind==='REPORT'){text(main,'This annual report contains planned synthetic task references. No actual service delivery or environmental result is reported.');records(main,edition.tasks,'/calendar',undefined,{year:String(year)});}
   }else text(main,'Calendar object not found in this annual edition.');}
  else if(nodes.length){records(main,nodes.filter(n=>!n.parentId&&!values(n.parentIds).length).slice(0,30),'/calendar',undefined,{year:String(year)});records(section(main,'Planned synthetic tasks'),edition.tasks,'/calendar',undefined,{year:String(year)});}
  else{details(main,{year,missionId:edition.missionId,classification:edition.classification||'SYNTHETIC'});records(main,values(edition.tasks||C.syntheticTasks(year)),'/calendar',undefined,{year:String(year)});}
 }
 async function auxiliaryPage(main,dataset,route){
  if(route.name==='coverage'){const cat=catalogue(dataset);details(main,cat&&root.AtlasIntake?root.AtlasIntake.coverage(cat):{sourceInventory:'UNKNOWN'});details(main,{softwareCapability:'PARTIAL — see tested task registry',relationshipAdmission:'PENDING',dataQuality:'REVIEW_REQUIRED',actualOutcomeKpi:'UNKNOWN'});tools(main,[['Inspect coverage and source gaps','openCoverage']]);return;}
  if(route.name==='audit'){const report=await root.AtlasModel.auditSnapshot(dataset);details(main,report);text(main,'No independent government signature or external witness is present.');const events=[...(dataset.events||[]),...(dataset.domain?.events||[])],page=Math.max(1,Number(route.query.page)||1);for(const event of events.slice((page-1)*20,page*20)){const item=element('details');item.append(element('summary',(event.sequence??'')+' · '+event.type+' · '+event.objectId));details(item,event);main.append(item);}if(page*20<events.length)main.append(link('Next events','/audit',{page:String(page+1)}));tools(main,[['Open audit and receipts','openAudit'],['Research workspace','openWorkspace']]);return;}
  if(route.name==='discovery'){text(main,'Candidate paths are explanations to test, not official strategy links or causal findings.');for(const h of root.AtlasModel.discover(dataset)){const s=section(main,h.id);text(s,h.explanation);details(s,{status:h.status,ruleVersion:h.ruleVersion,counterevidence:h.counterevidence});}tools(main,[['Run discovery and challenge','openDiscovery']]);return;}
  if(route.name==='assistant'){const A=root.AtlasCSOIAssistant,C=root.AtlasCSOICalendar;const s=section(main,'Draft-only management preparation');text(s,'Prepared questions and resource checks do not represent Michele’s approval or a Council instruction. Nothing is emailed or sent to Outlook.');if(A?.compileWeek&&C?.annualEdition){const year=Number(route.query.year)||2026,edition=C.annualEdition({year,missionId:'public-research',yearBasis:'CALENDAR',tasks:C.syntheticTasks(year)}),form=element('form'),dateLabel=element('label','Week containing'),dateInput=element('input',null,{type:'date',value:route.query.date||year+'-11-02'}),capacityLabel=element('label','Synthetic available hours'),capacityInput=element('input',null,{type:'number',value:'8',min:'0',max:'1000'});dateLabel.append(dateInput);capacityLabel.append(capacityInput);form.append(dateLabel,capacityLabel,element('button','Prepare weekly draft',{type:'submit'}));s.append(form);const output=element('div',null,{id:'csoiAssistantDraft'});s.append(output);const compile=()=>{output.replaceChildren();try{const draft=A.compileWeek(edition,{date:dateInput.value,capacityHours:Number(capacityInput.value)});details(output,draft);const meeting=A.meetingDraft(draft);const meetingHost=element('details');meetingHost.append(element('summary','Meeting agenda, questions and follow-up drafts'));details(meetingHost,meeting);output.append(meetingHost);if(bridge.registerScenario)output.append(action('Append draft to local research model',()=>bridge.registerScenario(A.scenarioPayload(draft))));}catch(error){text(output,'Draft rejected: '+error.message);}};form.addEventListener('submit',e=>{e.preventDefault();compile();});compile();}else text(s,'Draft compiler is not loaded in this software build. Explore source gaps and work cards to prepare a research agenda.');main.append(link('Work cards','/operations'),link('Calendar','/calendar'),link('Source gaps','/coverage'));return;}
 }
 async function render(route){
  const token=++generation;currentRoute=route;menu.open=false;const atlas=route.valid&&route.name==='atlas';host.hidden=atlas;routeMap.hidden=!atlas;document.body.classList.toggle('csoi-page-active',!atlas);document.getElementById('inspector').hidden=true;
  for(const a of nav.querySelectorAll('a')){if(R.parse(a.hash).name===route.name)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');}
  if(atlas){if(route.query.item&&bridge.openPublicItem)bridge.openPublicItem(route.query.item);return;}
  host.replaceChildren();const header=element('header',null,{class:'csoi-page-heading'});text(header,'COUNCIL STRATEGY & OPERATIONS INTELLIGENCE','small');const heading=text(header,TITLES[route.name]||'Workspace','h1');heading.tabIndex=-1;host.append(header);
  if(route.valid){const companion=element('a','Open this page in a companion window',{href:R.companionUrl(location.href,route.path,route.query),target:'_blank',rel:'noopener noreferrer','data-csoi-companion':'true'});header.append(companion);}
  if(!route.valid){text(host,'This URL is not a registered public workspace.');host.append(link('Return to the route map','/atlas'));return;}
  text(host,'Independent public/synthetic research · official admission and real Council performance remain separately reviewed.', 'p').className='csoi-boundary';
  if(['strategy','sources','operations','metrics','resources'].includes(route.name)){const form=element('form',null,{class:'csoi-filters','aria-label':'Filter public workspace records'});for(const [name,label]of [['q','Search records'],['region','Region'],['unit','Unit'],['status','Evidence state']]){const field=element('label',label),input=element('input',null,{name,value:route.query[name]||'',maxlength:name==='q'?'200':'512'});field.append(input);form.append(field);}form.append(element('button','Apply filters',{type:'submit'}));form.addEventListener('submit',e=>{e.preventDefault();const query={};for(const [key,value]of new FormData(form))if(String(value).trim())query[key]=String(value).trim();R.navigate(route.path,query);});host.append(form);}
  const content=element('div',null,{class:'csoi-page-content'});host.append(content);
  try{const dataset=await bridge.getDataset();if(destroyed||token!==generation)return;
   if(route.name==='knowledge')contentPage(content,dataset,route);
   else if(route.name.startsWith('strategy'))strategyPage(content,dataset,route);
   else if(['sources','source'].includes(route.name))sourcesPage(content,dataset,route);
   else if(['operations','operation','metrics','metric','resources','resource'].includes(route.name))coreRecordsPage(content,dataset,route);
   else if(route.name.startsWith('phe')||route.name.startsWith('wcos'))professionalPage(content,dataset,route);
   else if(route.name.startsWith('calendar'))calendarPage(content,dataset,route);
   else await auxiliaryPage(content,dataset,route);
   if(token===generation)heading.focus({preventScroll:true});
  }catch(error){if(token===generation){text(content,'Workspace could not be verified: '+error.message);content.append(action('Retry this page',()=>render(currentRoute)));}}
 }
 const unsubscribe=R.subscribe(render);
 return {render:()=>render(currentRoute),navigate:R.navigate,destroy(){destroyed=true;unsubscribe();host.remove();menu.remove();routeMap.hidden=false;document.body.classList.remove('csoi-page-active');}};
}
root.CsoiPages={mount,element,link,queryFilter,displayAllowed,publicOnly};if(typeof module!=='undefined')module.exports=root.CsoiPages;
})(typeof window!=='undefined'?window:globalThis);
