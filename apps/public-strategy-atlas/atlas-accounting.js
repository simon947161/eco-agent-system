/* ClimateOS Atlas quantitative strategy-to-work layer v1.
 * Public observation is source-attributed but NOT an admitted official graph mapping.
 * All work, budgets and land/water quantities below are EXPLICITLY SYNTHETIC.
 * No Council private data, payment, network request or official signature. */
(function(root) {
'use strict';
const UNKNOWN='UNKNOWN', OBSERVED='PUBLIC_TEXT_OBSERVED', SYNTH='SYNTHETIC';
const finite=n=>typeof n==='number'&&Number.isFinite(n);
const norm=s=>typeof s==='string'?s.trim():s;
function requireValid(ok,code){if(!ok)throw new Error(code);}
const cases=[
 {id:'carbon-regional-baseline',domain:'CARBON',entryNodeId:'csp6',mappingStatus:'THEMATIC_CONTEXT_ONLY_NOT_OFFICIAL_MAPPING',
  goal:{label:'Environmental protection and emissions context',status:'RESEARCH_CONTEXT',sourceClaim:'CSP environmental measures table, not a proven Objective 6.1→DP/OP action'},
  work:{id:null,description:UNKNOWN,status:UNKNOWN,effort:UNKNOWN},resources:[],funding:[],outputs:[],outcomes:[],
  metric:{id:'csp2035-carbon-per-capita-baseline',label:'CO2e emissions per capita',unit:'t_CO2e/person',value:29.9,
   period:{from:'2021-07-01',to:'2022-06-30',basis:'Snapshot Climate 2021–22 reference period (financial-year label; exact inventory interval needs review)'},
   area:'Snowy Monaro Regional LGA',boundary:'REGIONAL_COMMUNITY_INVENTORY',denominator:'population',method:'Snapshot Climate Australian Emissions Profiles 2021–22',direction:'DECREASE',
   baseline:true,target:UNKNOWN,actual:UNKNOWN,status:OBSERVED,
   source:{url:'https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/csp/smrc-csp-2035-endorsed-20250501.pdf',locator:'printed page 30; Our environmental, CO2e emissions per capita',publisher:'Snowy Monaro Regional Council',adoptedOn:'2025-05-01',rawDigest:UNKNOWN,revisionConfirmed:false,humanReviewed:false}},
  uncertainties:['No verified Objective 6.1-to-metric linkage','No approved DP/OP implementation mapping','Council operational share UNKNOWN','No population denominator admitted for multiplying to total','No budget, expenditure or outcome claimed']},
 {id:'water-service-work-demo',domain:'WATER',entryNodeId:'water',mappingStatus:'SYNTHETIC_ONLY',
  goal:{label:'Illustrative water-service reliability',status:SYNTH},
  work:{id:'synthetic-water-inspection',description:'Illustrative inspection/service volume; NOT a published Council task',status:SYNTH,effort:{value:12,unit:'ML',period:'FY2026-27',area:'SYNTHETIC_PLACE',boundary:'DEMO_WATER_SERVICE'}},
  resources:[{id:'synthetic-water-output',type:'PHYSICAL_FLOW',value:12,unit:'ML',period:'FY2026-27',area:'SYNTHETIC_PLACE',boundary:'DEMO_WATER_SERVICE',status:SYNTH}],
  funding:[{id:'synthetic-water-spend',type:'ACTUAL_EXPENDITURE',value:24000,unit:'AUD',period:'FY2026-27',area:'SYNTHETIC_PLACE',boundary:'DEMO_WATER_SERVICE',status:SYNTH,allocatedShare:1}],
  outputs:[{description:'Illustrative 12 ML water-service throughput',status:SYNTH}],outcomes:[],
  metric:{id:'synthetic-water-cost-per-ml',label:'Illustrative expenditure per water volume',value:2000,unit:'AUD/ML',period:{from:'2026-07-01',to:'2027-06-30'},area:'SYNTHETIC_PLACE',boundary:'DEMO_WATER_SERVICE',denominator:'12 ML synthetic throughput',status:SYNTH},
  uncertainties:['No actual public water volume or spend is inferred','Volume is not treatment capacity','The work example cannot establish real effectiveness']},
 {id:'land-use-work-demo',domain:'LAND',entryNodeId:'area',mappingStatus:'SYNTHETIC_ONLY',
  goal:{label:'Illustrative place-based land planning inquiry',status:SYNTH},
  work:{id:'synthetic-land-review',description:'Illustrative 50 hectare land-review scenario (not a zoning or consent decision)',status:SYNTH,effort:{value:50,unit:'ha',period:'FY2026-27',area:'SYNTHETIC_PLACE',boundary:'DEMO_LAND_SCOPE'}},
  resources:[{id:'synthetic-land-area',type:'PHYSICAL_STOCK',value:50,unit:'ha',period:'FY2026-27',area:'SYNTHETIC_PLACE',boundary:'DEMO_LAND_SCOPE',status:SYNTH}],
  funding:[],outputs:[],outcomes:[],
  metric:{id:'synthetic-area',label:'Hypothetical land area reviewed',value:50,unit:'ha',period:{from:'2026-07-01',to:'2027-06-30'},area:'SYNTHETIC_PLACE',boundary:'DEMO_LAND_SCOPE',denominator:UNKNOWN,status:SYNTH},
  uncertainties:['Applicable LEP/DCP, parcel boundary and control are UNKNOWN','No real project, rezoning or land-use approval is inferred','Population, budget and economic effects remain UNKNOWN']}
];
const index=Object.freeze(Object.fromEntries(cases.map(c=>[c.entryNodeId,c])));
function caseForNode(id){return index[id]||null;}
function assertMeasurement(m) {
 requireValid(m&&typeof m.id==='string'&&typeof m.unit==='string','METRIC_ID_OR_UNIT_MISSING');
 requireValid(m.value===UNKNOWN||finite(m.value),'METRIC_VALUE_INVALID');
 requireValid(m.status===SYNTH||m.status===OBSERVED||m.status===UNKNOWN,'METRIC_STATUS_INVALID');
 requireValid(typeof m.area==='string'&&m.area.length>0,'METRIC_AREA_MISSING');
 requireValid(typeof m.boundary==='string'&&m.boundary.length>0,'METRIC_BOUNDARY_MISSING');
 requireValid(m.period&&typeof m.period.from==='string'&&typeof m.period.to==='string','METRIC_TIME_MISSING');
 if(m.status===OBSERVED)requireValid(m.source&&/^https:\/\//.test(m.source.url)&&m.source.locator,'METRIC_SOURCE_MISSING');
 return true;
}
function assertComparable(a,b) {
 assertMeasurement(a);assertMeasurement(b);
 requireValid(a.unit===b.unit,'UNIT_MISMATCH');
 requireValid(a.area===b.area,'GEOGRAPHY_MISMATCH');
 requireValid(a.boundary===b.boundary,'BOUNDARY_MISMATCH');
 requireValid(a.period.from===b.period.from&&a.period.to===b.period.to,'PERIOD_MISMATCH');
 requireValid(norm(a.method||UNKNOWN)===norm(b.method||UNKNOWN),'METHOD_MISMATCH');
 requireValid((a.denominator||UNKNOWN)===(b.denominator||UNKNOWN),'DENOMINATOR_MISMATCH');
 return true;
}
function totalFromPerCapita(rate,population) {
 assertMeasurement(rate);requireValid(rate.unit==='t_CO2e/person','NOT_EMISSIONS_PER_CAPITA');
 requireValid(population&&finite(population.value)&&population.value>0,'POPULATION_DENOMINATOR_UNKNOWN');
 requireValid(population.unit==='person','POPULATION_UNIT_MISMATCH');
 requireValid(rate.area===population.area,'GEOGRAPHY_MISMATCH');
 requireValid(rate.boundary===population.boundary,'BOUNDARY_MISMATCH');
 requireValid(rate.period.from===population.period.from&&rate.period.to===population.period.to,'PERIOD_MISMATCH');
 requireValid(population.methodologyCompatible===true,'INVENTORY_METHOD_UNVERIFIED');
 return {value:rate.value*population.value,unit:'t_CO2e',status:rate.status===SYNTH&&population.status===SYNTH?SYNTH:'DERIVED_REVIEW_REQUIRED'};
}
function unitConvert(value,from,to) {
 requireValid(finite(value),'QUANTITY_INVALID');
 if(from===to)return value;
 const factors={'ha>km2':.01,'km2>ha':100,'ML>kL':1000,'kL>ML':.001};
 requireValid(Object.prototype.hasOwnProperty.call(factors,from+'>'+to),'UNIT_CONVERSION_NOT_DEFINED');
 return value*factors[from+'>'+to];
}
function assertFinancial(e) {
 requireValid(e&&['APPROVED_BUDGET','REVISED_BUDGET','COMMITTED','ACTUAL_EXPENDITURE'].includes(e.type),'FINANCIAL_CLASS_INVALID');
 requireValid(e.unit==='AUD'&&finite(e.value)&&e.value>=0,'FINANCIAL_UNIT_OR_AMOUNT_INVALID');
 requireValid(typeof e.period==='string'&&typeof e.area==='string'&&typeof e.boundary==='string','FINANCIAL_SCOPE_MISSING');
 requireValid([SYNTH,OBSERVED,UNKNOWN].includes(e.status),'FINANCIAL_STATUS_INVALID');
 return true;
}
function costPerOutput(finance,output) {
 assertFinancial(finance);
 requireValid(finance.type==='ACTUAL_EXPENDITURE','BUDGET_IS_NOT_EXPENDITURE');
 requireValid(output&&finite(output.value)&&output.value>0&&typeof output.unit==='string','OUTPUT_DENOMINATOR_UNKNOWN');
 requireValid(finance.period===output.period,'PERIOD_MISMATCH');
 requireValid(finance.area===output.area,'GEOGRAPHY_MISMATCH');
 requireValid(finance.boundary===output.boundary,'BOUNDARY_MISMATCH');
 requireValid(finance.status===SYNTH&&output.status===SYNTH,'UNADMITTED_COST_OUTPUT');
 return {value:finance.value/output.value,unit:'AUD/'+output.unit,status:SYNTH};
}
function validateAllocations(entries) {
 requireValid(Array.isArray(entries),'ALLOCATIONS_MISSING');
 const grouped=new Map();
 for(const e of entries){assertFinancial(e);requireValid(typeof e.id==='string','FINANCIAL_ID_MISSING');
  requireValid(finite(e.allocatedShare)&&e.allocatedShare>=0&&e.allocatedShare<=1,'ALLOCATION_SHARE_INVALID');
  grouped.set(e.id,(grouped.get(e.id)||0)+e.allocatedShare);}
 for(const sum of grouped.values())requireValid(Math.abs(sum-1)<1e-9,'DOUBLE_COUNT_OR_UNALLOCATED');
 return true;
}
function derivedCase(id) {
 const c=caseForNode(id);if(!c)return null;
 if(c.domain==='WATER'){return costPerOutput(c.funding[0],c.resources[0]);}
 return null;
}
function escapeHTML(x){return String(x??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));}
function panelHTML(id){
 const c=caseForNode(id);if(!c)return '';
 const m=c.metric;const show=(v)=>v===UNKNOWN?'<strong class="accounting-unknown">UNKNOWN</strong>':escapeHTML(v);
 const facts=[
  ['Why / strategy',c.goal.label+' ['+c.goal.status+']'],
  ['What work?',c.work.description],
  ['Where / boundary',m.area+' / '+m.boundary],
  ['How much?',String(m.value)+' '+m.unit],
  ['Measured period',m.period.from+' — '+m.period.to],
  ['Source status',m.status],
  ['Resource / effort',c.resources.length?c.resources.map(x=>x.value+' '+x.unit+' ['+x.status+']').join('; '):UNKNOWN],
  ['Budget / actual spend',c.funding.length?c.funding.map(x=>x.type+': '+x.value+' '+x.unit+' / '+x.period+' ['+x.status+']').join('; '):UNKNOWN],
  ['Output and outcome',c.outputs.length?c.outputs.map(x=>x.description+' ['+x.status+']').join('; '):UNKNOWN],
  ['Verified progress / target',UNKNOWN],
  ['Official goal-to-work mapping',c.mappingStatus]
 ];
 let s='<section id="accountingFlow" class="accounting-flow" aria-label="Work, quantities and evidence"><h3>Work · quantity · accounting</h3><p class="detail-text">Explore a typed, evidence-bounded work chain. Published observation ≠ approved Council action; synthetic examples ≠ real costs.</p><dl>';
 for(const [label,value]of facts)s+='<div class="accounting-pair"><dt>'+escapeHTML(label)+'</dt><dd>'+show(value)+'</dd></div>';
 s+='</dl>';
 if(m.source)s+='<p class="detail-text">Published source: <a href="'+escapeHTML(m.source.url)+'" rel="noopener noreferrer" target="_blank">CSP 2035, '+escapeHTML(m.source.locator)+'</a>. Source reused as a short attributed observation; original PDF not stored here.</p>';
 if(c.domain==='WATER'){const output=derivedCase(id);s+='<p class="detail-text">Derived SYNTHETIC expenditure intensity: '+escapeHTML(output.value+' '+output.unit)+'. Do not present as actual Council spending.</p>';}
 s+='<h4>Evidence gaps / challenges</h4><ul>'+c.uncertainties.map(t=>'<li>'+escapeHTML(t)+'</li>').join('')+'</ul>';
 s+='<p class="detail-text">No independent attestation, Council authorisation, statutory mapping or actual KPI is implied.</p></section>';return s;
}
for(const c of cases){assertMeasurement(c.metric);for(const f of c.funding)assertFinancial(f);}
const api={UNKNOWN,OBSERVED,SYNTH,cases,caseForNode,assertMeasurement,assertComparable,totalFromPerCapita,unitConvert,assertFinancial,costPerOutput,validateAllocations,derivedCase,panelHTML};
root.AtlasAccounting=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
