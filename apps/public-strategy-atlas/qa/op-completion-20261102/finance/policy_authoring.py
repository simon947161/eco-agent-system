"""Authored readings loaded by build_finance.py; no raw full-text redistribution."""

# Two charts on each of 118 and 119: numbers were read from the actual pixels.
chart_specs=[
 (118,0,'income-types','拟议收入类别与双轴显示',
  [('Net gain from disposal of asset','.68 M',None),('Other Revenues','1.13 M',None),('Other Income','1.32 M',None),('Capital Grants and Contributions','2.16 M',None),('Interest and Investment Revenue','4.79 M',None),('User Fees & Charges','20.55 M',None),('Operational Grants & Contributions','24.09 M',None),('Rates & Annual Charges','51.37 M',None)],
  '蓝色柱按收入类型表示金额，橙色折线对应右侧百分比轴；折线没有独立数值标签，本次不据像素推算百分比。',
  ['图表采用 M 标注；美元币种代码未写明，不推断 AUD。','Other Revenues 与 Other Income 在该图分开，不能不经说明就同别处合并分类混用。']),
 (118,1,'income-funds','拟议收入的四基金构成',
  [('General Fund','65.95 M','62%'),('Water Fund','13.15 M','12%'),('Sewer Fund','14.69 M','14%'),('Waste Management Fund','12.30 M','12%')],
  '饼图按 General、Water、Sewer 和 Waste 四个基金标注拟议收入份额；这是预算而非到账收入。',
  ['标签显示的是百万格式和整数百分比；本次不从扇形角度制造更精确值。']),
 (119,0,'expenditure-types','拟议运营支出类别',
  [('Depreciation Amortisation & Impairment','30.35 M',None),('Other expenses','2.19 M',None),('Materials and services','33.69 M',None),('Employee benefits and on-costs','41.84 M',None)],
  '水平条形图列出四类拟议运营支出；横轴标 MILLIONS，保留图中两位小数的显示精度。',
  ['折旧等非现金费用不能当现金流出；不将此图与资本项目表简单相加。']),
 (119,1,'expenditure-funds','拟议支出基金图及组合展开',
  [('General Fund','65.51 M','61%'),('Water Fund','15.62 M','14%'),('Other (Sewer + Waste shown separately)','26.94 M','25%'),('Sewer Fund','14.46 M','13%'),('Waste Management Fund','12.48 M','12%')],
  '左图的 Other 是右侧 Sewer 与 Waste 的组合展示，不是第五个可再相加的基金。',
  ['26.94 M 与 14.46 M、12.48 M 属父子组合，禁止三者重复加总。','预算金额与百分比均按印刷精度保留。'])]
for page,image_index,key,title,series,summary,qq in chart_specs:
    image_blocks=[b for b in DOC[page-1].get_text('dict')['blocks'] if b['type']==1]
    box=list(image_blocks[image_index]['bbox']);aa=pixel_anchor(page,box,'facts.series',f'chart-{page}-{key}')
    facts={'chartType':'BAR_WITH_PERCENT_LINE' if key=='income-types' else ('HORIZONTAL_BAR' if key=='expenditure-types' else 'PIE_COMPOSITION'),'budgetStatus':'PROPOSED_BUDGET_NOT_ACTUAL','period':'2026/27','unitAsPrinted':'M / MILLIONS','currency':'UNKNOWN','series':[{'label':label,'amountDisplay':amount,'amountMillion':float(amount.replace(' M','')),'percentageDisplay':pct,'percentage':float(pct[:-1]) if pct else None,'role':'COMPOSITE_PARENT' if label.startswith('Other (') else ('COMPOSITE_CHILD' if key=='expenditure-funds' and label in ['Sewer Fund','Waste Management Fund'] else 'CATEGORY')} for label,amount,pct in series],'sourceReading':'MANUAL_PIXEL_REVIEW_NATIVE_TEXT_HAS_NO_CHART_VALUES','geometricPrecision':'NO_DIGITISATION_BEYOND_PRINTED_LABELS'}
    u=unit(page,'chart-'+key,'OP_BUDGET_FIGURE','Budget summary',title,summary,box,facts,qualifiers=qq,anchors=[aa]);visuals.append({'unitId':u['id'],'pdfPage':page,'type':'CHART','pixelAnchor':aa})

prose(124,'appendix-introduction',[2],'收入政策附录的用途','本附录说明收入筹措方式及费率安排，用来支持服务和活动；文件同时另行发布以便查阅。',{'scope':'Revenue policy appendix; not whole external fee schedule'})
prose(124,'document-directory',[3],'相关规划与收费文件目录','原页将 Delivery Program、OP、LTFP、Revenue Policy 与收费表引向 Council 的 IPR 页面；这里只记录文件关系，未另取收费表。',{'directoryUrl':'https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting','referencedDocuments':['Delivery Program','Operational Plan','Long Term Financial Plan','Revenue Policy','Schedule of Fees and Charges'],'externalDocumentContents':'NOT_RETRIEVED_IN_THIS_BATCH'},qualifiers=['提到某份文件不证明该文件当前有效或内容已全部纳入。'])
prose(125,'cover',[0],'收入政策封面','封面标明 Revenue Policy 2026–2027；配图作为装饰与地域背景，不算政策地图。',{'period':'2026–2027','pageDisposition':'COVER_WITH_DECORATIVE_PHOTO'},category='OP_DOCUMENT_CONTEXT')
prose(126,'acknowledgement',[0,1,2],'原住民致敬页','本页向 Ngarigo、Walgalu、Southern Ngunnawal、Bidawal Peoples 及历代长者致敬；树叶照片不是空间适用性证据。',{'namedPeoples':['Ngarigo','Walgalu','Southern Ngunnawal','Bidawal'],'pageDisposition':'ACKNOWLEDGEMENT_AND_DECORATIVE_PHOTO'},category='OP_DOCUMENT_CONTEXT')
version_table=DOC[126].find_tables().tables[0]
for ri,raw in enumerate(version_table.extract()[1:],1):
    vals=[norm(v) for v in raw];row=version_table.rows[ri]
    facts=dict(zip(['version','datePublished','amendmentLabel','resolution','documentOwner'],vals));facts['rowStatus']='POPULATED_VERSION_RECORD' if vals[1] else 'EMPTY_PLACEHOLDER_NOT_ADOPTED_VERSION';facts['currentness']='UNKNOWN'
    unit(127,'version-'+vals[0].replace('.','-'),'OP_DOCUMENT_VERSION','Revenue Policy version record','收入政策版本 '+vals[0],f'版本 {vals[0]} '+(f'列示日期 {vals[1]}、{vals[2]}，决议 {vals[3]}。' if vals[1] else '仅有预留版本号，其余格为空，不证明已经发布。'),rowbox(row),facts,anchors=[a_cell(127,row,c,'facts.'+field) for c,field in enumerate(['version','datePublished','amendmentLabel','resolution','documentOwner'])])
prose(127,'version-controls',[1,11],'已采用记录与草稿说明并存','版本表有 1.2 已采用记录，但同页底部仍称 working draft 并指向未来提交采用；打印件被标为非受控件。保留这种版本内张力，不裁定当前有效状态。',{'recordedAdoptionVersion':'1.2','recordedAdoptionDate':'30/06/2026','recordedResolution':'225/26','printedCopyStatus':'UNCONTROLLED','workingDraftWordingPresent':True},qualifiers=['附录收入政策的 1.2 与主 OP 的内部 1.3 属不同版本记录，不混并。'],category='OP_DOCUMENT_VERSION')
diagnostics.append({'type':'SOURCE_VERSION_STATUS_TENSION','pdfPages':[127],'description':'Revenue policy appendix table records version 1.2 adopted 30/06/2026 resolution 225/26 while same-page footer still calls document a working draft. Currentness UNKNOWN.','sourceUnitIds':['csoi:op2026:finance:p127:version-1-2','csoi:op2026:finance:p127:version-controls']})
prose(128,'contents',list(range(0,38)),'收入政策目录','目录定位税率、用地分类、分期付款、逾期利息、垃圾与雨水等年费、OSSM、养老金减免、借款及 GST。目录页码属于附录自身编号，不新增收费义务。',{'printedContentRange':[2,14],'pdfContentRange':[129,141],'disposition':'NAVIGATION_ONLY_ALL_LISTED_SECTIONS_REVIEWED_BELOW'},category='OP_DOCUMENT_CONTEXT')

prose(129,'income-mix',[4],'收入来源与成本分担','政策用税费、补助、使用者费用和投资等收入支持公共服务，并说明使用者付费与普遍分担之间的选择及土地所有者间的成本分担。')
prose(129,'fuel-surcharge',[6],'燃油附加费为待启用选项','政策保留应对异常燃油成本上涨的浮动附加费安排；原文明确当时尚未实施，若需启用以 Council 决定日期开始，并称不再另行公开展览。',{'chargeCurrentlyAppliedAsPrinted':False,'activationDate':'NOT_STATED','legalCitationAsPrinted':'s.608 Local Government Act 1993'},['需有异常燃油成本增加及 Council 启用决定；不能把可能收费写成已收费。'])
prose(129,'rate-peg',[9],'2026–27 税收增幅上限说明','原政策称当年 rate peg 为 4.2%，分为 3.9% 基础部分与 0.3% 人口因子；一般收入增加有授权上限，超限需批准。',{'ratePegPercent':4.2,'corePercent':3.9,'populationFactorPercent':0.3,'period':'2026-27','legalCitationAsPrinted':'s.506'},['此处是政策引用的 IPART 信息，未独立检索当前决定。'])
prose(129,'srv',[10],'四年 SRV 与 rate peg 的包含关系','原政策列明四年 SRV 52.48%；2023–24 为 12.25%，其后三年各 10.75%。rate peg 已包含在 SRV 中，不另加 4.2%。',{'fourYearSRVPercent':52.48,'years':[{'period':'2023-24','percent':12.25},{'period':'2024-25','percent':10.75},{'period':'2025-26','percent':10.75},{'period':'2026-27','percent':10.75}],'ratePegRelationship':'INCLUDED_NOT_ADDITIONAL'},['累计四年比例不能作为某一年度或每户税款增幅。'])
prose(129,'land-values-cycle',[11],'土地估值提供周期','原政策称 Valuer General 至少每三年向 Council 提供土地估值，供税费计算使用。',{'maximumIntervalYearsAsPrinted':3})
prose(129,'land-values-base-date',[12],'估值基准日与收费年度','2026/27 和 2027/28 的税率计算使用 2025 年 7 月 1 日土地估值基准；估值日期不能混为预算年度。',{'valuationBaseDate':'2025-07-01','ratingYears':['2026/2027','2027/2028']})
prose(129,'rating-policy',[15],'基础税额与从价税结构','一般 business、farmland、mining、residential 采用基础税额加从价税；business、farmland、residential 采用相同率。唯一的活动中心子类是 electricity generation，其费率为 business 的 2.5 倍。',{'onlySubcategoryAsPrinted':'Electricity Generation','electricityMultiplier':2.5,'commonRateCategories':['Business','Farmland','Residential']},['Mining 与 electricity generation 的差异税率须单独保留。'])
prose(129,'mining-base-ceiling',[16],'矿业倍数及基础税额收入上限','Mining 采用 business 的 2.5 倍费率。基础税额按不会超过税收收入 50% 的限制确定；这不是每个类别实际恰好收取 50%。',{'miningMultiplier':2.5,'baseRevenueCeilingPercent':50})
prose(130,'rating-policy-continuation',[3],'从价税额与服务成本检视','从价税按允许的最高收入计算；Council 选举后的 delivery plan 编制还要审视各地区服务成本与税率类别结构是否合理对应。',{'reviewContext':'Delivery plan following a Council election'},['这不表示本轮已经完成每个地区的成本归属核验。'])
prose(130,'land-categories',[5],'四种可征税土地类别','政策按 Residential、Business、Farmland、Mining 四类组织 rateable land；本研究不替任何具体地块作分类决定。',{'categories':['Residential','Business','Farmland','Mining'],'legalCitationAsPrinted':'s.514'},['地块事实与当前分类准入 UNKNOWN。'])
prose(130,'residential',[7,8,9],'住宅类别的主用途与排除项','住宅主用途为居住，包含住宅分区空地与 rural residential；酒店、汽车旅馆、guesthouse、nursing home 被排除在该段定义之外。',{'excludedUses':['hotel','motel','guesthouse','nursing home'],'includedCases':['vacant land zoned residential','rural residential']},['以主用途和原定义为前提，不按地图颜色直接判断单个地块。'])
prose(130,'business',[11],'Business 为余项类别','不能归为 farmland、residential 或 mining 的土地归 business，原文以商业及工业为主要使用例子。',{'excludedOtherCategories':['Farmland','Residential','Mining']})
prose(130,'farmland',[13,14],'农业类别与 rural residential 分界','Farmland 要求主用途为商业农业，原文列出畜牧、养殖、林业及盈利作物等例子；rural residential 不因此归入 farmland。',{'ruralResidentialIncluded':False,'dominantUse':'Commercial farming'},['示例不是自动豁免或逐地块判断。'])
prose(130,'mining',[16],'矿业类别','政策将主用途为开采煤或金属的土地列为 mining；不是所有采掘或乡村土地。',{'dominantUse':'Mining coal or metals'})
prose(130,'payments',[19,20,21,22,23,24],'年度缴款或四次分期','年款到期日为 8 月 31 日；也可按 8 月 31 日、11 月 30 日、2 月 28 日、5 月 31 日分四期，通知需提前一个月寄送。',{'annualDue':'31 August','instalments':['31 August','30 November','28 February','31 May'],'noticeLeadTime':'1 month'},['这是原政策日期规则，不创建个人提醒，也不判断某户欠费。'])
prose(130,'overdue-interest',[26],'逾期税费最高利率','原文对未按期支付的每期税费计息，并列出 2026/27 最高年利率 9.5%；利率由部长逐年确定。',{'maximumAnnualInterestPercent':9.5,'period':'2026/2027','legalCitationAsPrinted':'s.566(3)'},['最高年利率不等于本研究已计算任何欠费利息。'])

# Category definitions and rate table with row/column coordinates.
tdef=DOC[130].find_tables().tables[0]
defspec=[([1,2,3],'Business','Business','一般商业土地，排除另列 business 子类。'),([4],'Electricity Generation','Business','发电子类涉及 Eucumbene Dam、Lake Jindabyne、相关水道及用于发电的相关土地。'),([5,6,7],'Farmland','Farming','符合农业类别定义的土地，排除该类另列子类。'),([8],'Mining','Mining','符合矿业类别定义的土地，排除该类另列子类。'),([9,10,11],'Residential','Residential','符合住宅类别定义的土地，排除该类另列子类。')]
for rows,short,category,summary in defspec:
    b=bbox_union([rowbox(tdef.rows[i]) for i in rows]);unit(131,'rating-category-'+slug(short),'OP_REVENUE_CATEGORY','Revenue policy rating categories',short,summary,b,{'shortTitle':short,'categoryAsPrinted':category,'parcelApplicability':'UNKNOWN'},anchors=[anchor(131,b,'summary')])
tr=DOC[130].find_tables().tables[1];rate_headers=[norm(v) for v in tr.extract()[0] if v is not None];meta=table_meta(131,'ordinary-rates','Ordinary rates 2026/2027',rowbox(tr.rows[0]),rate_headers,'MIXED: $ / rate in dollar / %','2026/2027','Revenue policy rates')
rates=[]
for ri,raw in enumerate(tr.extract()[1:],1):
    row=tr.rows[ri];collapsed=[];boxes=[]
    for k in range(7):
        collapsed.append(norm(' '.join(str(x or '') for x in raw[k*3:k*3+3])))
        boxes.append(bbox_union([b for b in row.cells[k*3:k*3+3] if b]))
    label=collapsed[0] or collapsed[1];values=[];aa=[]
    for k,(col,sym) in enumerate([('Base','$'),('Ad Valorem','rate in dollar'),('Yield','$'),('% of yield','%'),('% from base rate','%')],2):
        values.append({'column':col,**cell(collapsed[k],sym,'2026/2027',col)});aa.append(anchor(131,expanded(boxes[k]),f'facts.columnValues[{k-2}]'))
    facts={'tableId':meta['id'],'categoryDisplay':collapsed[0],'subcategoryDisplay':collapsed[1],'columnValues':values,'rateStatus':'POLICY_SCHEDULE_NOT_ACTUAL_LEVY','currency':'UNKNOWN'}
    qq=['Mining 的印刷 Yield 为 $0.00，但 Base 与 Ad Valorem 非零；不能说矿业费率为零。'] if label=='Mining' else []
    u=unit(131,'rate-'+slug(label),'OP_REVENUE_RATE_ROW','Revenue policy rates',label,f'{label} 的基础税额、每美元从价率、预计收益及两种比例分别保留；不根据该表计算未提供估值的地块账单。',rowbox(row),facts,qualifiers=qq,anchors=aa+[meta['headerAnchor'],anchor(131,expanded(bbox_union(boxes[:2])),'facts.categoryDisplay')]);rates.append(u)
unit(131,'general-rates-total','OP_REVENUE_RATE_TOTAL','Revenue policy rates','预计普通税收入与调整限制','印刷预计普通税收入为 $27,779,928；正式征收时允许小幅调整，以免超过 IPART 允许的总收益。',[46.5,509,547,566],{'sourceDeclaredTotal':cell('$27,779,928','$','2026/2027','Estimated General rates')},['最终征收数值可能微调；不是已收现金。'],anchors=[anchor(131,[46.5,509,547,566],'summary')])
unit(131,'rating-differences','OP_REVENUE_POLICY','Revenue policy rates','发电与矿业类别的差别理由','政策希望延续发电类与其他商业土地的缴费差距；原文称当时无现有矿业土地所有者，但矿业有较高支付能力及交通网络服务成本，因此仍保留较高税率。',[46.5,569,547,746],{'miningLandownersAsPrinted':'No current mining landowners stated','currentActualStatus':'UNKNOWN'},qualifiers=['这是文件当时的说明，不外推为今天仍无矿业土地所有者。'],anchors=[anchor(131,[46.5,569,547,746],'summary')])

map_titles=['Business','Business — Electricity Generation','Farmland','Residential']
for idx,b in enumerate([b for b in DOC[131].get_text('dict')['blocks'] if b['type']==1]):
    box=list(b['bbox']);pa=pixel_anchor(132,box,'facts.map',f'rating-map-{idx+1}')
    facts={'mapTitleAsPrinted':map_titles[idx],'highlightMeaning':'原页说明红色表示该税率类别/子类别适用部分','legendObserved':[{'symbol':'red fill','meaning':'category areas per page caption'},{'symbol':'purple outer boundary','meaning':'visible outline; legal/cadastral precision not admitted'},{'symbol':'grey fine linework','meaning':'background parcel-like linework; no parcel data extracted'}],'scale':'NOT_VISIBLE','north':'NOT_VISIBLE','coordinateReferenceSystem':'NOT_VISIBLE','geometryExtracted':False,'parcelApplicability':'UNKNOWN','visibleContextLabels':['Michelago','Bredbo','Adaminaby','Berridale','Jindabyne','Bombala','Delegate'],'mapPurpose':'RATING_CATEGORY_ILLUSTRATION_IN_REGISTERED_POLICY'}
    u=unit(132,'rating-map-'+str(idx+1),'OP_REVENUE_MAP','Revenue policy rating maps',map_titles[idx]+' 评级地图','原页用红色突出 '+map_titles[idx]+' 相关区域；只记录图例和地域背景，不据低分辨率轮廓裁定某个地块应缴税率。',box,facts,['需要地块记录、现行分类及正式审查才能判断具体地块。'],['四个面板没有 Mining 地图；不自行补画。','未见比例尺、北向或 CRS，不能猜测。'],[pa,anchor(132,[46.5,54,523,83],'facts.highlightMeaning')]);visuals.append({'unitId':u['id'],'pdfPage':132,'type':'MAP','pixelAnchor':pa})

prose(133,'annual-charge-principle',[3],'年费与使用者付费原则','政策拟以使用者付费原则安排 2026/27 年费，引用 s.496、s.501、s.502；具体服务是否可用及提供条件仍要逐项查看。',{'legalCitationsAsPrinted':['s.496','s.501','s.502'],'period':'2026/2027'})

# Fee matrix: group labels are retained as context, not treated as zero-price rows.
fee_count=0
for page in [133,134]:
    tab=DOC[page-1].find_tables().tables[0];data=tab.extract();meta=table_meta(page,'waste-fees','Waste charges comparison',rowbox(tab.rows[0]),[norm(x) for x in data[0]],'$','columns 2027 and 2026','Revenue policy annual charges')
    group='Domestic / general waste services' if page==133 else 'Commercial FOGO';locality='AS_STATED_IN_ROW';group_code=''
    for ri,raw in enumerate(data[1:],1):
        vals=[norm(v) for v in raw];row=tab.rows[ri]
        if vals[0] in ['1.9','1.10','1.11','1.12']:
            group=vals[1];group_code=vals[0];locality='AS_STATED_IN_SUBSEQUENT_ROW';continue
        if vals[1].startswith('All Areas'):
            locality=vals[1];continue
        if not vals[3] and not vals[4]:continue
        facts={'tableId':meta['id'],'group':group,'groupCode':group_code,'itemAsPrinted':vals[0],'descriptionAsPrinted':vals[1],'relevantSectionAsPrinted':vals[2],'localityConditionAsPrinted':locality,'columnValues':[{'column':'2027',**cell(vals[3],'$','2027',vals[1])},{'column':'2026',**cell(vals[4],'$','2026',vals[1])}],'comparisonStatus':'POLICY_CHARGE_SCHEDULE_NOT_AMOUNT_COLLECTED'}
        qq=['2026 栏空白表示该格未列值，不替换为 0，也不推断新设或取消收费。'] if vals[4]=='' else []
        conditions=[]
        if 'Fortnightly' in vals[1]:conditions.append('此行明确 Fortnightly；不与另一个 360L 行合并。')
        if page==134 and '240L' in vals[1]:
            qq.append('本表 Weekly / Cooma-Monaro 与 PDF137 条款 fortnightly / Cooma 有源内差异，未裁定。')
        if page==133 and vals[0]=='1.4':qq.append('表中 Cooma-Monaro Region ONLY 与 PDF135 Cooma Township only 范围不同，原样保留。')
        if vals[0]=='1.6':conditions.append('每次/每申请收费，不是年费；Council 主动换桶项目的排除条件见 PDF135–136。')
        title=(vals[0]+' ' if vals[0] else '')+vals[1]
        unit(page,f'waste-fee-r{ri:02d}','OP_REVENUE_CHARGE_ROW','Revenue policy waste charges',title,f'{group} 的“{vals[1]}”在 2027 与 2026 栏分别印为 {vals[3] or "空白"}、{vals[4] or "空白"}；适用条件和服务频率必须结合相应条款。',rowbox(row),facts,conditions,qq,[a_cell(page,row,c,'facts.'+f) for c,f in enumerate(['itemAsPrinted','descriptionAsPrinted','relevantSectionAsPrinted','columnValues[0]','columnValues[1]'])]+[meta['headerAnchor']]);fee_count+=1
assert fee_count==22

# Each numbered condition retains its own qualifier; grouped clauses below only
# combine their continuation/bullet blocks, never an unrelated condition.
clause_specs=[
 (134,'1.1.1',[21],'垃圾管理年费的征收范围','原条款对 rateable assessments 征收年度垃圾管理费，并引用 s.501。',{'legalCitationAsPrinted':'Local Government Act 1933 (NSW), s.501'},[],['原文把 Act 年份印为 1933，与其他段落的 1993 不同；不静默改正文。']),
 (134,'1.1.2',[22,23,24],'住宅与商业垃圾管理费分项','政策把垃圾管理费拆为住宅及 business/commercial 两项；住宅项原文写 all rateable assessments，商业项写 business/commercial assessments。',{},['两段范围措辞存在交叉，不据此替具体地块裁定应收一项或两项。'],[]),
 (134,'1.1.3',[25],'按土地使用类别选费','适用垃圾管理费按土地使用分类确定。',{},['具体土地分类未经本研究确认。'],[]),
 (134,'1.1.4',[26],'垃圾管理费账单与分期','垃圾管理费列在年度 Rates and Charges Notice，可按季度分期。',{'billing':'Annual rates and charges notice','payment':'Quarterly instalments'},[],[]),
 (134,'1.1.5',[27],'优惠须资格与批准','符合条件并获批准者可能按 Waste Management Charge Policy 277 获折扣；原条款没有给出统一折扣金额。',{'referencedPolicy':'Waste Management Charge Policy 277','discountAmount':'NOT_STATED'},['须符合资格并获批准。'],[]),
 (134,'1.2.1',[29],'居民垃圾收集的地域与服务前提','Kerbside Collection Area 内要同时服务可用且实际提供；区域外则须申请并获准。每处住宅可按 Kerbside Collection Policy 申请多个服务。',{},['区域内：服务可用且提供。','区域外：申请并获批准。','额外服务按相关政策申请。'],[]),
 (134,'1.2.2',[30],'居民垃圾每周服务的收费单位','年度垃圾收集费按获服务的 domestic premises 计，服务频率为每周。',{'frequency':'Weekly','chargeBasis':'Per domestic premises per annum'},[],[]),
 (134,'1.2.3',[31],'一宗评税含多住宅','同一 assessment 有多于一个 domestic premises 时适用多个服务费。',{},['触发条件：同一 assessment 内多处住宅。'],[]),
 (134,'1.2.4',[32],'请求额外居民服务','请求额外 domestic services 的 assessment 会有多个服务费。',{},['触发条件：请求额外服务。'],[]),
 (134,'1.2.5',[33],'120L 升 240L 的附加费与旧区例外','申请从 120L 升至 240L 通常加费；former Snowy River Council 区域须等 Council 决议把标准从 240L 改为 120L 后才适用该附加费。',{'fromLitres':120,'toLitres':240,'exceptionRegion':'former Snowy River Council area'},['旧 Snowy River 例外持续到规定的 Council resolution。'],[]),
 (134,'1.2.6',[34],'居民垃圾费账单与分期','该费列入年度税费通知，可季度分期缴付。',{'billing':'Annual rates and charges notice','payment':'Quarterly instalments'},[],[]),
 (135,'1.3.1',[3],'居民回收服务的准入','回收收费要求 Kerbside Collection Area 内服务可用且提供；区域外须申请并获准。可按政策申请额外服务。',{},['区域内服务可用并提供。','区域外申请且批准。'],[]),
 (135,'1.3.2',[4],'居民回收每两周服务','居民回收年费按每处获服务住宅计，收集频率每两周一次。',{'frequency':'Fortnightly','chargeBasis':'Per domestic premises per annum'},[],[]),
 (135,'1.3.3',[5],'回收：多住宅多个服务费','同一 assessment 有多处住宅时，适用多个回收服务费。',{},['多处 domestic premises。'],[]),
 (135,'1.3.4',[6],'回收：请求额外服务','请求额外居民回收服务的 assessment 会产生多个服务费。',{},['请求额外服务。'],[]),
 (135,'1.3.5',[7],'回收费通知与分期','回收费列入年度税费通知，可季度分期。',{'billing':'Annual rates and charges notice','payment':'Quarterly instalments'},[],[]),
 (135,'1.3.6',[8],'回收运输附加成本的延续条件','文件称 2022 年 12 月 ACT Hume 回收设施被火灾毁损，涨费持续支付运往 Sydney 的成本，直到新 Canberra 设施建成且运行；文中预期为 2028。',{'incidentMonth':'2022-12','expectedReplacementYear':2028},['终止条件是新设施建成并运行，不仅到达某日历年份。'],['2028 是源文件预期，不是已验证完工承诺。']),
 (135,'1.4.1',[10],'居民 FOGO 服务范围','FOGO 仅在服务可用且提供的评税物业适用，正文当时限定 Cooma Township；可按政策申请多个服务。',{'locationAsPrinted':'Cooma Township only'},['服务可用且提供。'],['收费表写 Cooma-Monaro Region ONLY，不能无声扩大正文 township 范围。']),
 (135,'1.4.2',[11],'居民 FOGO 收集频率','FOGO 年费按每处获服务住宅计，每两周收集一次。',{'frequency':'Fortnightly','chargeBasis':'Per domestic premises per annum'},[],[]),
 (135,'1.4.3',[12],'多住宅与 strata 的 FOGO 选择','多住宅产生多个服务费；multi-unit dwellings 与 strata 可选择加入，每单元采用与独立住宅相同费率。',{'multiUnitParticipation':'OPT_IN','perUnitRate':'Same as single dwelling houses'},['多单元/strata 须 opt in，不表述为自动纳入。'],[]),
 (135,'1.4.4',[13],'FOGO 账单与分期','居民 FOGO 费用列于年度税费通知，可季度分期。',{'billing':'Annual rates and charges notice','payment':'Quarterly instalments'},[],[]),
 (135,'1.5.1',[15],'空地垃圾年费的服务条件','空置 rateable assessment 在垃圾收集服务可用、但未提供服务时适用该费。',{},['Vacant rateable assessment；服务可用但未提供。'],[]),
 (135,'1.5.2',[16],'空地收费按 assessment 计','无服务情况下按 assessment 收取空地年费，原文说明包括 developed 与 undeveloped land。',{'chargeBasis':'Per assessment per annum','developmentStatusesAsPrinted':['developed','undeveloped']},['不得仅因写 vacant 就删除原文 developed 的说明。'],[]),
 (135,'1.5.3',[17],'空地费账单与分期','空地垃圾年费列入年度税费通知，可季度分期。',{'payment':'Quarterly instalments'},[],[]),
 (135,'1.6.1',[19],'居民换桶申请范围','居民申请改变 Council 发放的 Waste、Recycling 或 FOGO 桶大小时适用换桶费。',{'binServices':['Waste','Recycling','FOGO']},['须居民申请改变桶容量。'],[]),
 (135,'1.6.2',[20],'Council 主动换桶计划的排除项','该费只在居民申请换尺寸时适用；Council 自己开展统一换桶计划时不收此项。',{'councilInitiatedProgramExcluded':True},['居民自行申请与 Council 主动计划区分。'],[]),
 (136,'1.6.3',[3],'换桶费并非年费','申请时收取换桶费，必须在换桶前全额缴清；它不是年度收费。',{'annualCharge':False,'paymentTiming':'Full payment before bin changeover'},[],[]),
 (136,'1.7.1',[5],'Bank of Bins 自愿参与','居民选择参加且当地服务可用时才适用 Bank of Bins。',{},['Elected participation；service available。'],[]),
 (136,'1.7.2',[6],'Bank of Bins 服务范围','Bank of Bins 只收集家庭生活垃圾及回收物。',{'scope':'Domestic household waste and recycling only'},[],[]),
 (136,'1.7.3',[7],'Bank of Bins 需申请批准','该服务是否批准要经过申请决定。',{'approval':'Determined upon application'},[],[]),
 (136,'1.7.4',[8],'Bank of Bins 年费分期','费用计入年度税费通知，可季度分期。',{'payment':'Quarterly instalments'},[],[]),
 (136,'1.8.1',[10],'推桶服务为可用时自愿选择','Wheel Out/Wheel In 只适用于选择参与且服务可用的居民。',{},['选择参与且服务可用。'],[]),
 (136,'1.8.2',[11],'推桶服务申请','服务批准通过申请决定。',{'approval':'Determined upon application'},[],[]),
 (136,'1.8.3',[12],'推桶服务减免资格','符合条件的居民可以申请减免，须满足申请表 250.2016.24.2 中条件；文中未给统一自动豁免。',{'applicationForm':'250.2016.24.2'},['符合资格、申请及表中条件。'],[]),
 (136,'1.8.4',[13],'推桶费用通知','费用计入年度税费通知，可季度分期。',{'payment':'Quarterly instalments'},[],[]),
 (136,'1.9-transition',[15],'商业垃圾改为年度评税账单','使用 Council 商业垃圾服务的物业从月度发票改为年度物业 assessment 账单，可按常规季度分期缴费。',{'previousBilling':'Monthly invoice','newBilling':'Annual property assessment / rates and charges notice'},['适用于使用该商业服务的物业。'],[]),
 (136,'1.9.1',[16],'商业垃圾用户','该费适用于 Commercial Waste Service 使用者。',{'applicability':'Users of Commercial Waste Service'},[],[]),
 (136,'1.9.2',[17,18],'商业垃圾按桶容量与周频率计','有商业路边收集服务的地区，按 240L、360L 桶及 660L、1100L skip bins 每周服务收年费；年度账单可季度分期。',{'binLitres':[240,360,660,1100],'frequency':'Weekly','chargeBasis':'Annual charge per bin/skip'},['仅服务提供地区。'],[]),
 (136,'1.10-transition',[20],'商业回收改为年度账单','商业回收服务使用物业从月度发票改为年度评税账单，可季度分期。',{'previousBilling':'Monthly invoice','newBilling':'Annual property assessment'},['实际使用该回收服务。'],[]),
 (136,'1.10.1',[21],'商业回收用户','该费适用于 Commercial Recycling Service 使用者。',{'applicability':'Users of Commercial Recycling Service'},[],[]),
 (136,'1.10.2',[22,23],'商业回收正文频率与容量','在有商业路边回收服务地区，360L、660L、1100L 桶按每两周收集收取年费，可季度分期。',{'binLitres':[360,660,1100],'frequency':'Fortnightly','chargeBasis':'Annual charge per bin'},['须有商业路边服务。'],['PDF133 另有未写频率的 360L $649 及显式 fortnightly $397 行；两行都保留，不代替作者选择。']),
 (136,'1.10.3',[24],'商业回收运输成本延续','ACT Hume 设施火灾后，原政策把运往 Sydney 的成本继续计入，直到新 Canberra 设施建成运行；2028 仅为文中预期。',{'incidentMonth':'2022-12','expectedReplacementYear':2028},['终止取决于建成且运营。'],[]),
 (137,'1.11-transition',[4],'商业 FOGO 年度账单','使用商业 FOGO 服务的物业由月度发票改为年度评税账单，并可按常规季度分期。',{'previousBilling':'Monthly invoice','newBilling':'Annual property assessment'},['只适用于使用服务的物业。'],[]),
 (137,'1.11.1',[5],'商业 FOGO 用户','本项适用于商业食品及园林有机物收集服务的用户。',{'applicability':'Users of Commercial FOGO Collection Service'},[],[]),
 (137,'1.11.2',[6,7,8],'商业 FOGO 的地区与双周条件','正文称 Bombala、Delegate、Nimmitabel、Bredbo、Michelago 及 former Snowy River 区不提供该服务；Cooma 按 240L 桶每两周收集收年费，可季度分期。',{'unavailableAreas':['Bombala','Delegate','Nimmitabel','Bredbo','Michelago','Former Snowy River Area'],'availableAreaAsPrinted':'Cooma','binLitres':240,'frequency':'Fortnightly'},['只对服务提供并使用的物业。'],['PDF134 价格表写 Cooma-Monaro / Weekly，与本条不同；没有裁定哪个正确。'])]
for page,code,bb,title,summary,facts,conditions,qq in clause_specs:
    facts={'clauseAsPrinted':code,**facts};prose(page,'clause-'+code.replace('.','-'),bb,title,summary,facts,conditions,qq)

prose(137,'reference-documents',[11,12],'垃圾收费定义的外部来源','政策指向 LGA 1993 Dictionary 及 Resource and Waste Management Policy and Procedures 以解释术语和费用；本轮未把外部定义冒充已全文读入。',{'referencedSources':['NSW Consolidated Acts – LGA 1993 Dictionary','Resource and Waste Management Policy and Procedures'],'externalContents':'NOT_EXPANDED_IN_THIS_BATCH'})
prose(137,'short-names',[13,14,15,16,17,18,19,20],'垃圾收费简称','原页为生活垃圾、回收、FOGO、空地服务及 Waste Management、Bank of Bins 列简称；简称映射不是新增收费类别。',{'shortNames':['Domestic Waste Collection Charge','Domestic Recycling Collection Charge','Domestic FOGO Collection Charge','Domestic Waste Vacant Land Charge','Waste Management Charge','Bank of Bins']})
prose(137,'domestic-premises',[22,23],'Domestic premises 定义须同时看废物性质','住宅、flat、strata、附属住宅、公寓、villa、dual occupancy 等均可属于 domestic premises，但要以实际或可居住用途以及通常家庭垃圾种类/数量为前提；例子不穷尽。',{'examples':['House','Flat','Strata Unit','Granny Flat','Attached unit','Detached unit','Apartment','Villa','Dual Occupancy','Multi-Unit Dwellings'],'examplesExhaustive':False},['住宅用途或可供住宅使用。','垃圾种类及数量属于一般家庭产生水平。'])
prose(138,'additional-unusual-waste',[3],'超出普通家庭种类或数量的废物','即使场所用于或可用于居住，若废物种类或数量超出普通家庭水平，政策保留按 s.501 或 s.502 对额外部分加费的权利。',{'legalCitationsAsPrinted':['s.501','s.502']},['仅针对超出普通家庭种类或数量的部分。'])
prose(138,'domestic-waste-definition',[5,6],'一般家庭垃圾示例','住宅产生的家庭垃圾示例包括食物、包装、不可回收物、玻璃陶瓷及绿废；这是示例列表，不声明每项在所有服务中均可混投。',{'examples':['Food waste','Packaging materials','Non-recyclable items','Glass and ceramics','Green waste']},qualifiers=['本段为垃圾类别定义，不能代替投放规则。'])
prose(138,'commercial-landfill-classification',[8],'填埋商业垃圾分类依据','商业填埋垃圾按组成和更重要的来源分类，关键在于来自家庭还是商业场所；不能仅凭外观自动裁定。',{'classificationFactors':['Composition','Source of generation'],'sourceEmphasised':True})
prose(138,'transaction-dockets',[10],'商业处置收据的作用','原文说明商业单位通常取得标记 commercial 的处置收据用于业务记录，工作人员经验和自报信息辅助来源识别；仍可能发生分类争议。',{'receiptRole':'Business records and reporting/claiming context'},qualifiers=['收据或员工经验不是本研究已作出的特定废物法律分类。'])
prose(138,'commercial-waste-definition',[12,13],'一般商业垃圾示例','经济活动产生的商业废物可包括包装、办公纸板、拆除混凝土、大量绿废及混合 skip/truck 垃圾；例子不穷尽。',{'examples':['Packaging materials','Office paper/cardboard','Demolition rubble/concrete','Larger volumes of green waste','Mixed or unsorted skip/truck waste'],'examplesExhaustive':False})
prose(138,'stormwater',[15],'雨水管理费的窄地域条件','原政策按每宗 occupied、rateable 且服务可用的土地每年 $20 收费，仅限 former Bombala/Delegate 区；Cooma-Monaro 与 Snowy River 当时不收此年费。新 stormwater DSP 采用前，其他地区雨水问题随道路资本/养护工程处理。',{'annualCharge':cell('$20','$','2026/2027','Per occupied rateable parcel per annum'),'chargedAreasAsPrinted':['former Bombala/Delegate Council areas'],'notChargedAsPrinted':['Cooma-Monaro','Snowy River'],'legalCitationAsPrinted':'s.496A','DSPStatusAsPrinted':'Being developed'},['Occupied rateable land。','服务可用。','地域限 former Bombala/Delegate。','其他地区临时安排持续到 SMRC stormwater DSP 采用。'])
prose(139,'water-sewer-ltw-fee-reference',[3],'水、污水及液体贸易废水费另见收费表','本附录没有展开水、污水及 liquid trade waste 的费率，而是指向另行 Schedule of Fees and Charges。',{'referencedDocument':'SMRC Schedule of Fees and Charges','ratesInThisSection':'NOT_STATED'},qualifiers=['未取回外部收费表，不能把它说成已完成费率覆盖。'])
prose(139,'ossm-scope',[5,8],'OSSM 年度续期收费与付款','配置 onsite sewage systems 的物业收年度续期费，列于年度 rates notice；正文称适用于 Snowy Monaro 所有 onsite sewage management systems，并可季度分期。',{'systemExamples':['Septic tank','Aerobic system','Worm system'],'billing':'Annual rates notice','payment':'Quarterly instalments','legalCitationsAsPrinted':['s.501','s.107A']},['收费文本不代替特定系统批准、风险评估或当前适用性审查。'])
prose(139,'ossm-subsidy',[6],'OSSM 仍由一般税收补贴','政策认为该项目部分效益惠及广泛社区，因此一般税收仍提供补贴；本段没有给出补贴金额或比例。',{'subsidyAmount':'NOT_STATED','subsidyRate':'NOT_STATED'})
t=DOC[138].find_tables().tables[0];r=t.rows[1];raw=t.extract()[1]
unit(139,'ossm-charge','OP_REVENUE_CHARGE_ROW','Revenue policy OSSM','OSSM 年费比较','OSSM 年费在 2027 栏为 $35.00、2026 栏为 $34.00；不包含后续条款排除的安装、转移、复查等其他收费。',rowbox(r),{'chargeName':'OSSM','columnValues':[{'column':'2027',**cell(raw[1],'$','2027','Annual OSSM renewal charge')},{'column':'2026',**cell(raw[2],'$','2026','Annual OSSM renewal charge')}]},anchors=[a_cell(139,r,0,'facts.chargeName'),a_cell(139,r,1,'facts.columnValues[0]'),a_cell(139,r,2,'facts.columnValues[1]')])
prose(139,'ossm-exclusions',[11],'OSSM 年费不包含的事项','年度金额不覆盖初次安装或运行批准、产权变更后的运行批准转移、系统复查所需的 re-inspection、顾问费用，以及已发通知相关管理费。',{'excludedCharges':['Initial approval to install or operate','Transfer of approval to operate on new ownership','Re-inspection when system review needed','Consulting fees','Administration fees relating to issued notices']},['不能把 $35 解释为这些事项的全部许可费用。'])
prose(139,'ossm-short-name',[12],'OSSM 简称','文件使用 OSSM 作为 onsite effluent disposal 系统收费的简称；这是术语说明，不是系统准许排放的独立证明。',{'shortName':'OSSM'})
prose(139,'rails-pipes',[14,15,16,17],'公共场所设施年费按市场价值','政策可对在公共场所上、下或跨越其上的轨道、管线、杆线、电缆、隧道等结构征年费；2026/27 对地下及地面/上方两类均写 Current Market Value，未给固定金额。',{'legalCitationAsPrinted':'s.611','period':'2026/2027','chargeBasisAsPrinted':{'Under a public place':'Current Market Value','On or over a public place':'Current Market Value'}},['市场价值未在本文件逐项列出，不能编造固定费率。'])
prose(140,'pensioner-eligibility',[4,5],'养老金减免资格与居所限制','持 Pensioner Concession Card 或其他符合资格者，针对唯一或主要居所按 s.575 获减免；表列金额为每年最高额。',{'legalCitationAsPrinted':'s.575','eligibility':'Pensioner Concession Card or otherwise qualifying','residence':'Sole or principal place of residence'},['资格和主要居所条件同时保留。'])
t=DOC[139].find_tables().tables[0]
for ri,raw in enumerate(t.extract()[1:],1):
    row=t.rows[ri];label=norm(raw[0]);val=norm(raw[1]);unit(140,'pensioner-rebate-'+str(ri),'OP_REVENUE_REBATE','Revenue policy pensioner concessions',label,f'{label} 的年度最高减免额为 {val}；须满足养老金资格及唯一/主要居所条件。',rowbox(row),{'scope':label,'maximumRebate':cell(val,'$','Per annum','Maximum rebate'),'combinedScope':ri==1},['普通税与 domestic waste management charge 共用 $250 上限，不是各自 $250。'] if ri==1 else [],anchors=[a_cell(140,row,0,'facts.scope'),a_cell(140,row,1,'facts.maximumRebate')])
prose(140,'credit-cards',[14],'机构信用卡授权上限','批准员工的单卡额度在 $500–$10,000，总上限 $200,000；文件称当时有 39 张卡，其中 3 张用于 Rural Fire Service。额度不是已消费金额。',{'individualMinimum':cell('$500','$','As printed','Card limit'),'individualMaximum':cell('$10,000','$','As printed','Card limit'),'aggregateLimit':cell('$200,000','$','As printed','Total card limit'),'cardCountAsPrinted':39,'ruralFireServiceCardsIncluded':3},qualifiers=['不得当成当前持卡人数或实际债务/支出。'])
prose(140,'borrowing-law-references',[16],'新借款引用的限制','新借款需遵守原文引用的 Clause 230 Local Government (General) Regulations 2005 及 s.624；本轮只记录引用，未作当前法律整合。',{'legalCitationsAsPrinted':['Clause 230 Local Government (General) Regulations 2005','s.624 Local Government Act 1993']})
prose(140,'external-borrowing-considerations',list(range(17,25)),'外借资金需要考虑的因素','新外部贷款要考虑自筹偿付能力、利率、替代融资、法定上限、资产管理、净偿债成本及长期债务降低，不能仅凭某个预算数直接批准借贷。',{'factors':['Self-funding ability','Interest rates','Alternative finance options','Statutory loan borrowing limits','Asset management principles','Net debt service cost','Long term debt reductions']})
prose(140,'overdraft',[25],'无透支安排的当时说明','文件称 Council 当时没有 overdraft facility；本轮未查银行授权或今天是否变化。',{'overdraftFacilityAsPrinted':False,'currentActualStatus':'UNKNOWN'})
prose(140,'restricted-fund-borrowing',[26],'受限用途基金内部借款需先批准','从 Water Fund 等专用收入基金内部借款，要按 s.410 申请，并在资金使用前获得部长批准。',{'legalCitationAsPrinted':'s.410','exampleRestrictedFund':'Water Fund','approvalAuthorityAsPrinted':'Minister'},['申请并获部长批准必须先于资金使用。','不是本系统对内部借款作出的授权。'])
prose(141,'fees-cost-recovery',[3],'收费支持服务成本','政策按 s.608 向所供服务收费以回收或部分回收成本，不声称所有服务都已全成本回收。',{'legalCitationAsPrinted':'s.608','costRecovery':'Full or partial as service context permits'})
prose(141,'fees-cso',[4],'使用者付费中的社区义务例外','收费主要按使用者付费，但识别 Community Service Obligations 时考虑支付能力，并由交叉补贴支持公共利益。',{'principle':'User pays with ability-to-pay/CSO recognition','communityServiceObligations':'Cross subsidised'},['不能把 user pays 简化为所有服务一律完全由个人承担。'])
prose(141,'fee-setting-factors',[5,6],'定价考虑因素','原文引用 s.610D，考虑服务成本、行业/NSW 政府参考价格、社区重要性与法规要求等因素。',{'legalCitationAsPrinted':'s.610D','factors':['Council cost','Relevant industry or NSW published charge guidance','Community importance','Regulation-specified factors']})
prose(141,'fee-schedule-period',[8,9],'收费表年度与配套阅读','完整收费金额见另附 Schedule of Fees and Charges，期间为 2026-07-01 至 2027-06-30，并须结合收入政策阅读。',{'periodStart':'2026-07-01','periodEnd':'2027-06-30','externalFeeScheduleContents':'NOT_RETRIEVED'},['不得把收入政策附录本身当成完整收费表。'])
prose(141,'ceo-fee-authority',[10],'CEO 可调整范围有限','原文授权 CEO 在收到请求后调整 non-legislated fees；并非任意修改法定费用的授权。',{'decisionRole':'CEO','feeScope':'Non-legislated fees','trigger':'Upon request'},['非立法设定费用且有请求。'])
prose(141,'gst',[12],'GST 变化条款','GST 按 ATO 要求征收；若 GST 规则变更，政策保留相应调整费用而不另通知的权利。',{'tax':'GST','authorityReferenced':'Australian Taxation Office'},['仅在 GST 规则变更的条件下适用所述调整条款。'])

diagnostics.extend([
 {'type':'SOURCE_SERVICE_FREQUENCY_AND_GEOGRAPHY_CONFLICT','pdfPages':[134,137],'description':'Commercial FOGO table: Cooma-Monaro Region, 240L, Weekly, $748. Clause 1.11.2: Cooma, 240L, Fortnightly. Both retained; no currentness or correctness ruling.','sourceUnitIds':['csoi:op2026:finance:p134:waste-fee-r02','csoi:op2026:finance:p137:clause-1-11-2']},
 {'type':'SOURCE_GEOGRAPHIC_SCOPE_DIFFERENCE','pdfPages':[133,135],'description':'Domestic FOGO table says Cooma-Monaro Region ONLY; clause 1.4.1 says presently Cooma Township only. No silent geographic expansion.','sourceUnitIds':['csoi:op2026:finance:p133:waste-fee-r06','csoi:op2026:finance:p135:clause-1-4-1']},
 {'type':'SOURCE_FREQUENCY_ROW_AMBIGUITY','pdfPages':[133,136],'description':'Commercial recycling has a 360L row $649 with no frequency and a separate 360L Fortnightly row $397, while clause 1.10.2 states fortnightly collection. Separate rows preserved; no price selected for a customer.','sourceUnitIds':['csoi:op2026:finance:p133:waste-fee-r19','csoi:op2026:finance:p133:waste-fee-r22','csoi:op2026:finance:p136:clause-1-10-2']},
 {'type':'SOURCE_LEGISLATION_YEAR_TYPO_OR_CONFLICT','pdfPages':[134],'description':'Clause 1.1.1 prints Local Government Act 1933, while policy elsewhere identifies 1993. No silent correction or current legal admission.','sourceUnitIds':['csoi:op2026:finance:p134:clause-1-1-1']}])
prose(142,'public-documents',[0,1,2,3,4,5,6,7,8],'结尾的公开文件入口','末页指向 Council 网站上的 Snowy Monaro 2035 CSP、Delivery Program、OP 与 Annual Reports，以及官方社交入口；文档可获取关系不等于已形成具体行动链接。',{'website':'www.snowymonaro.nsw.gov.au','referencedDocuments':['Snowy Monaro 2035 Community Strategic Plan','Delivery Program','Operational Plan','Annual Reports'],'relationScope':'Document availability only'},category='OP_DOCUMENT_CONTEXT')
prose(142,'feedback',list(range(9,18)),'反馈与补充信息渠道','文件欢迎读者就计划提出意见或索取补充资料，并将反馈用于改进服务、计划和报告；本任务没有代用户发送意见。',{'outboundMessageSent':False},category='OP_DOCUMENT_CONTEXT')
prose(142,'public-contact',list(range(18,27)),'公开联系与办公室信息','末页列出公开联系渠道及 Cooma、Berridale、Bombala、Jindabyne 办公室；Council 邮箱在原件末页可查，此处不复写这一非必要联系地址，其余事实只对应原版本。',{'phone':'1300 345 345','post':'PO Box 714, COOMA NSW 2630','emailContactProjection':'PUBLIC_COUNCIL_EMAIL_PRESENT_ON_ORIGINAL_ENDPAGE_NOT_REPLICATED_NONESSENTIAL_CONTACT_DETAIL','offices':[{'place':'Cooma','address':'81 Commissioner Street, Cooma NSW 2630'},{'place':'Berridale','address':'2 Myack Street, Berridale NSW 2628'},{'place':'Bombala','address':'71 Caveat Street, Bombala NSW 2632'},{'place':'Jindabyne','address':'2/1 Gippsland Street, Jindabyne NSW 2627'}],'currentContactValidity':'UNKNOWN'},category='OP_DOCUMENT_CONTEXT')
