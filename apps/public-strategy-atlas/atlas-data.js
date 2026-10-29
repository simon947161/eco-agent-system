/* Public directory references and explicitly synthetic graph. */
(function(root){
  const IP = "https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting";
  const DEV = "https://www.snowymonaro.nsw.gov.au/Building-and-Planning/Development";
  const nodes = [
    {id:"csp",label:"CSP",sub:"Strategy overview · demo",type:"csp",x:58,y:147,source:IP,detail:"A synthetic strategy-tree root. CSP is a public document family; this graph does not establish official clause mappings."},
    {id:"csp6",label:"Objective 6.1",sub:"Environment · demo",type:"csp",x:287,y:66,source:IP,detail:"An environmental theme for the synthetic graph. Wording, revision and DP/OP mappings remain unverified."},
    {id:"csp8",label:"Objective 8.2",sub:"Infrastructure · demo",type:"csp",x:287,y:231,source:IP,detail:"Demonstrates multiple downstream paths. No official one-to-one mapping to these illustrative actions is claimed."},
    {id:"dp",label:"Delivery program",sub:"DP · structure demo",type:"csp",x:553,y:92,source:IP,detail:"Illustrates a delivery-program layer. Approved document clauses have not been admitted."},
    {id:"op",label:"Operational plan",sub:"OP · structure demo",type:"csp",x:791,y:120,source:IP,detail:"Illustrates annual actions. Connections are synthetic modelling examples."},
    {id:"kpi",label:"Indicator definition",sub:"Definition unverified",type:"csp",x:1074,y:65,source:IP,detail:"A KPI needs an approved target, denominator, reporting period and quality evidence. Actual results remain UNKNOWN."},
    {id:"water",label:"Water action",sub:"Synthetic activity",type:"csp",x:1052,y:249,source:IP,detail:"A fictional water activity. It represents no Council case, inspection or completed work count."},
    {id:"audit",label:"Evidence record",sub:"Synthetic review",type:"csp",x:1300,y:237,source:IP,detail:"A synthetic evidence location. No official credential, third-party receipt or real review conclusion exists."},
    {id:"lsps",label:"LSPS",sub:"Land-use planning",type:"lsps",x:58,y:496,source:DEV,detail:"An LSPS document-family entry. It is not automatically a subordinate CSP or LEP task."},
    {id:"priority",label:"Planning priority",sub:"Illustrative priority",type:"lsps",x:304,y:540,source:DEV,detail:"A fictional planning priority. Official clause numbering, original wording and geographic scope remain unverified."},
    {id:"lep",label:"LEP provision",sub:"Scope unverified",type:"lsps",x:568,y:447,source:DEV,detail:"LEP scope, revision and effective dates require evidence. This synthetic node does not identify an actual provision."},
    {id:"dcp",label:"DCP control",sub:"Guidance unverified",type:"lsps",x:813,y:536,source:DEV,detail:"DCP guidance and LEP statutory effect must be distinguished. Clauses and jurisdictions are unverified here."},
    {id:"area",label:"Geographic scope",sub:"Berridale · demo",type:"lsps",x:1074,y:494,source:DEV,detail:"Berridale illustrates geographic context only. No parcel-level LEP or DCP applicability is established."},
    {id:"scope",label:"Effective period",sub:"Official version needed",type:"lsps",x:1291,y:496,source:DEV,detail:"Applicability at a particular date and region requires separate evidence. Without it, the result remains UNKNOWN."},
    {id:"candidate",label:"Hidden-link candidate",sub:"Hypothesis · not fact",type:"candidate",x:1324,y:644,source:null,detail:"An authored cross-document hypothesis. Thematic similarity alone does not establish legal, administrative or scientific validity."}
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

  const sources=[{id:"smrc-ipr-directory",url:IP,classification:"PUBLIC_DIRECTORY_REFERENCE",revisionId:null,rawDigest:null,observedAt:null,licence:"UNKNOWN",verification:"UNKNOWN"},{id:"smrc-planning-directory",url:DEV,classification:"PUBLIC_DIRECTORY_REFERENCE",revisionId:null,rawDigest:null,observedAt:null,licence:"UNKNOWN",verification:"UNKNOWN"}];
  const revisions=[{id:"synthetic-v1",logicalId:"atlas-demo",classification:"SYNTHETIC",validFrom:"2026-01-01",validTo:"2026-12-31",region:"SYNTHETIC_REGION",rawDigest:null,sourceId:null}];
  nodes.forEach(n=>{n.logicalId=n.id;n.versionId="synthetic-v1:"+n.id;n.revisionId="synthetic-v1";n.status="SYNTHETIC";n.sourceId=n.source===IP?sources[0].id:n.source===DEV?sources[1].id:null;});
  const assertions=edges.map(e=>({id:e.id,from:e.from,to:e.to,predicate:e.kind,status:e.candidate?"HYPOTHESIS_ONLY":"SYNTHETIC",revisionId:"synthetic-v1",assertedBy:"synthetic-fixture-author",reviewedBy:null,evidenceRefs:[],counterevidenceRefs:[],validFrom:"2026-01-01",validTo:"2026-12-31",region:"SYNTHETIC_REGION",reviewStatus:"UNREVIEWED",algorithmVersion:"manual-fixture-v1"}));
  const hypotheses=[{id:"h1",status:"HYPOTHESIS_ONLY",assertionIds:["e15","e16"],ruleVersion:"manual-fixture-v1",explanation:"Shared topic alone cannot establish applicability",counterevidence:[{id:"f1",status:"SYNTHETIC",reason:"A hypothetical 2025-only outside-region revision cannot support a 2026 SYNTHETIC_REGION conclusion"}],reviewStatus:"UNREVIEWED"}];
  sources.push({id:"synthetic-source",url:"./qa/synthetic-source.txt",classification:"SYNTHETIC",revisionId:"synthetic-v1",rawDigest:"sha256:52b668dd9d583951d8cb9db04e27618d236293b7aa22db217c2b8cf1edfac408",verification:"SYNTHETIC_ONLY",licence:"MIT"});
  revisions[0].rawDigest=sources.find(s=>s.id==="synthetic-source").rawDigest;revisions[0].sourceId="synthetic-source";
  const dataset={schemaVersion:"atlas-1",sources,revisions,nodes,edges,assertions,hypotheses,contentBlocks:[{id:"block-demo",sourceId:"synthetic-source",offset:0,length:44,digest:"sha256:52b668dd9d583951d8cb9db04e27618d236293b7aa22db217c2b8cf1edfac408",algorithm:"SHA-256",chunking:"whole-file-v1"}],events:[]};
  // Reviewed public metadata observations; never used as official graph assertions.
  dataset.sourceObservations=[
    {id:'obs-csp-2035',title:'CSP 2035',sourceId:'smrc-ipr-directory',locator:'Snowy Monaro 2035 Community Strategic Plan / adoption paragraph',observedOn:'2026-10-29',adoptedOn:'2025-05-01',status:'METADATA_OBSERVED',note:'The directory records adoption on 1 May 2025. Full text and reuse permission have not been verified.',rawDigest:null},
    {id:'obs-dp-2026',title:'DP 2025–2029, 2026 revision',sourceId:'smrc-ipr-directory',locator:'Delivery Program and Operational Plan / 2026 Revision',observedOn:'2026-10-29',adoptedOn:'2026-06-26',status:'METADATA_OBSERVED',note:'The directory lists a 2026 revision. An older revision must not automatically be treated as current.',rawDigest:null},
    {id:'obs-op-2026',title:'OP 2026–2027',sourceId:'smrc-ipr-directory',locator:'Delivery Program and Operational Plan / 2026–2027 adoption paragraph',observedOn:'2026-10-29',adoptedOn:'2026-06-26',status:'METADATA_OBSERVED',note:'The directory lists 2026–2027 adoption but retains older annual-plan prose. Verify the individual document.',rawDigest:null},
    {id:'obs-planning-scope',title:'LEP / DCP scope counterexample',sourceId:'smrc-planning-directory',locator:'How is the region planned by Council? / Snowy Mountains SAP catalyst precinct (exception)',observedOn:'2026-10-29',adoptedOn:null,status:'METADATA_OBSERVED',note:'The directory distinguishes former shire instruments and a special-activation-precinct exception. Region-wide uniform applicability cannot be inferred.',rawDigest:null},
    {id:'obs-csp-summary-61',title:'CSP one-page summary · 6.1',sourceId:'smrc-ipr-directory',url:'https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/csp/csp-2035-plan-on-a-page.pdf',locator:'PDF page 1 / Strategic Objective 6 / 6.1',observedOn:'2026-10-29',adoptedOn:null,status:'PUBLIC_TEXT_OBSERVED',note:'Paraphrase: monitor environmental assets, including air, land and waterways, to protect them. This observation establishes no DP/OP mapping. Original PDF bytes, reuse permission and current applicability remain unverified.',rawDigest:null}
  ];
  dataset.events=[{"id":"fixture-created","type":"ADD","objectId":"synthetic-v1","actor":"synthetic-fixture-author","reason":"Public synthetic fixture only","observedAt":"2026-10-29T00:00:00Z","sequence":0,"previousDigest":null,"digest":"sha256:db8c07372567b6b273240f67a3825ed560a89708128e329cb06f4733be8860ea"}];
  // Recursive content decomposition is separate from cross-document assertions.
  // These authored children are synthetic examples, not extracted Council clauses.
  dataset.contentItems=[];
  const addContent=(owner,parent,suffix,kind,title,text,status='SYNTHETIC',observationId=null)=>{
    const id=owner+':'+suffix;
    dataset.contentItems.push({id,logicalId:id,versionId:id+':v1',revisionId:status==='SYNTHETIC'?'synthetic-v1':null,ownerNodeId:status==='SYNTHETIC'?owner:null,parentId:parent,kind,title,text,status,observationId});return id;
  };
  for(const n of nodes){
    const base=addContent(n.id,null,'content','TOPIC',n.label,n.detail);
    const context=addContent(n.id,base,'context','SECTION','Purpose and context','Illustrative internal structure for '+n.label+'. These are authored demonstration items, not official document text.');
    const clause=addContent(n.id,context,'basis','CLAUSE','Illustrative requirement','State the intended outcome and the conditions that would need to be checked. Official wording and applicability: UNKNOWN.');
    const action=addContent(n.id,clause,'action','ACTION','Illustrative follow-through','Identify an activity, accountable role and review period. No real officer, work order or completed Council activity is recorded.');
    const indicator=addContent(n.id,action,'indicator','INDICATOR','Measurement definition','Target: UNKNOWN. Denominator: UNKNOWN. Reporting period: UNKNOWN. Actual result: UNKNOWN.');
    addContent(n.id,indicator,'evidence','EVIDENCE','Evidence required','Obtain a public source, exact locator, revision, geographic scope, effective date, byte digest and independent review before relying on a claim.');
    const review=addContent(n.id,base,'review','SECTION','Evidence and challenge','A source directory is a discovery entry, not proof of a specific policy relationship.');
    addContent(n.id,review,'falsifier','QUESTION','What could disprove this?','A different revision, region, effective period or explicit exception may invalidate the proposed relationship.');
  }
  for(const o of dataset.sourceObservations){
    const base=addContent(o.id,null,'content','DOCUMENT',o.title,o.note,o.status,o.id);
    if(o.id==='obs-csp-summary-61'){
      const section=addContent(o.id,base,'objective-6','SECTION','Strategic Objective 6','Location observed in the one-page summary; no full-document applicability decision.',o.status,o.id);
      addContent(o.id,section,'clause-61','CLAUSE','6.1 — environmental asset monitoring',o.note,o.status,o.id);
    }
  }
  dataset.events.push({"id":"english-content-v1-added","type":"ADD","objectId":"csp:content","actor":"atlas-public-research-build","reason":"Added 127 English internal-content items and child-linked receipts. Synthetic breakdowns remain separate from observed public text.","observedAt":"2026-10-29T08:11:32.949Z","sequence":1,"previousDigest":"sha256:db8c07372567b6b273240f67a3825ed560a89708128e329cb06f4733be8860ea","digest":"sha256:963d8d32f0807a40a90db8c255cba4da5cac53a2491b94589139e96d3b372126"});
  root.AtlasData=dataset;if(typeof module!=="undefined")module.exports=dataset;
})(typeof window!=="undefined"?window:globalThis);
