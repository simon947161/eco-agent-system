/* Public directory references and explicitly synthetic graph. */
(function(root){
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
    {id:'obs-csp-2035',title:'CSP 2035',sourceId:'smrc-ipr-directory',locator:'Snowy Monaro 2035 Community Strategic Plan / adoption paragraph',observedOn:'2026-10-29',adoptedOn:'2025-05-01',status:'METADATA_OBSERVED',note:'官方目录记载采用日期2025-05-01；完整正文和许可未核验。',rawDigest:null},
    {id:'obs-dp-2026',title:'DP 2025–2029，2026修订',sourceId:'smrc-ipr-directory',locator:'Delivery Program and Operational Plan / 2026 Revision',observedOn:'2026-10-29',adoptedOn:'2026-06-26',status:'METADATA_OBSERVED',note:'官方目录列明2026修订；不得把旧版自动视为现行。',rawDigest:null},
    {id:'obs-op-2026',title:'OP 2026–2027',sourceId:'smrc-ipr-directory',locator:'Delivery Program and Operational Plan / 2026–2027 adoption paragraph',observedOn:'2026-10-29',adoptedOn:'2026-06-26',status:'METADATA_OBSERVED',note:'目录列明2026–2027采用日期，但仍保留旧年度介绍，需逐件核验。',rawDigest:null},
    {id:'obs-planning-scope',title:'LEP / DCP 地域反证',sourceId:'smrc-planning-directory',locator:'How is the region planned by Council? / Snowy Mountains SAP catalyst precinct (exception)',observedOn:'2026-10-29',adoptedOn:null,status:'METADATA_OBSERVED',note:'目录区分原辖区规划工具，并列出特殊激活区例外；不能推出全区统一适用。',rawDigest:null},
    {id:'obs-csp-summary-61',title:'CSP一页摘要 · 6.1',sourceId:'smrc-ipr-directory',url:'https://www.snowymonaro.nsw.gov.au/files/assets/public/v/4/council/ipr/csp/csp-2035-plan-on-a-page.pdf',locator:'PDF page 1 / Strategic Objective 6 / 6.1',observedOn:'2026-10-29',adoptedOn:null,status:'PUBLIC_TEXT_OBSERVED',note:'中文释义：监测空气、土地和水道等环境资产，保障其得到保护。此摘要观察没有建立任何DP/OP对应关系；PDF原始字节、许可与现行适用性仍待核验。',rawDigest:null}
  ];
  dataset.events=[{"id":"fixture-created","type":"ADD","objectId":"synthetic-v1","actor":"synthetic-fixture-author","reason":"Public synthetic fixture only","observedAt":"2026-10-29T00:00:00Z","sequence":0,"previousDigest":null,"digest":"sha256:db8c07372567b6b273240f67a3825ed560a89708128e329cb06f4733be8860ea"}];
  root.AtlasData=dataset;if(typeof module!=="undefined")module.exports=dataset;
})(typeof window!=="undefined"?window:globalThis);
