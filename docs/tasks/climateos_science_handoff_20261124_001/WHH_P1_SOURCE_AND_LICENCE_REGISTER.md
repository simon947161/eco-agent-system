# WHH P1 数据来源与许可登记

2026-11-24 · READ_ONLY · NO_RAW_DATA_DOWNLOADED

**9 个候选门户/系列，5 个深入审查。没有数据集准入。** 多个同系列目录/帮助/版权页视为一个候选，年报另在14项出版物预算计数。NHMRC/WHO是指导来源，不计成观测数据覆盖。机器字段见 [whh_candidates.json](whh_candidates.json)。公开可读、版权许可、Founder下载许可、科学准入为四个独立判断。

|ID / 深度|权利主体与入口|版本/覆盖/字段与格式|许可判断与限制|实际结果|
|---|---|---|---|---|
|D01 深入|[SMRC Environmental Protection](https://www.snowymonaro.nsw.gov.au/Water-and-Wastewater/Wastewater/Environmental-Protection)|The Glen/EPL6368，目录标示12Jan2026–11Jan2027监测PDF；只读目录，未读逐样本表|未找到该监测文件的明确复制/衍生许可；许可原文URL=null；PUBLICLY_READABLE，不是OPEN_LICENSED|LICENCE_UNVERIFIED。报告覆盖标签不代表截至2026-11-24已完成整个期间|
|D02 深入|[NSW EPA EPL6368](https://www.epa.nsw.gov.au/prpoeoapp/Detail.aspx?id=6368&instid=6368&option=licence&prp=no&range=POEO+licence&searchrange=licence&status=Issued)|SMRC链接指向的公共许可详情；许可有效版本、点位字段及附件格式 UNKNOWN|页面Cache miss不是403，不能由URL中Issued推断当前生效；无可核验对象级许可|ACCESS_UNRESOLVED；未猜替代API/镜像|
|D03 深入|[ACT Waterwatch CHIP目录](https://www.act.waterwatch.org.au/data/chip-reports)|Upper Murrumbidgee年度报告/站点数据门户；相关年报2022–25，原始观测导出未读取|[版权原文](https://www.act.waterwatch.org.au/copyright)：CC BY4.0，排除图片/影音/品牌/第三方/另行标许可内容；署名© Upper Murrumbidgee Waterwatch|WEBSITE_TEXT_LICENCE_VERIFIED；ALA逐条观测及第三方权利仍UNVERIFIED，不继承网页许可|
|D04 深入|[WaterNSW API portal](https://api-portal.waternsw.com.au/)|站点、流量、水质等API类别；未请求数值；具体410081序列期未知|[data-attribution](https://api-portal.waternsw.com.au/data-attribution)要求署名但不是完整开放授予；API需注册/订阅/key，未注册或获取|AUTH_REQUIRED STOP。BOM转发许可不等于API访问授权|
|D05 深入|[BOM WDO](https://www.bom.gov.au/waterdata/)|水位、流量、雨量、EC@25C、浊度、pH、水温；全国平台不证明410081具体可用参数/区间|[对象供应者许可表](https://www.bom.gov.au/waterdata/wiski-web-public/copyright.htm)列Water NSW w00231为CC提供方；文字称Attribution Australia，实际所链deed为[CC BY4.0](https://creativecommons.org/licenses/by/4.0/)。保留这种展示差异，记录后再核对将来文件声明|PROVIDER_GRANT_FOUND / ITEM_UNVERIFIED。指定记录必须先核实provider-code和文件声明，未下载任何时间序列|
|D06 初筛|[NSW DCCEEW水质框架/SWAMP入口](https://www.water.dcceew.nsw.gov.au/our-work/science-data-and-modelling/surface-water-science/water-quality-surface-water-environments/monitoring-framework)|公开框架包含SEED监测目录、字段标准/报告/仪表板链接；具体Cooma覆盖UNKNOWN|未深入到对象级许可、数据字段或质量数据；不能把全NSW框架当当地数据|SCREEN_ONLY / LICENCE_UNVERIFIED|
|D07 初筛|[Riverina Water来源说明](https://rwcc.nsw.gov.au/your-water/water-supply/yourwater/)|确认Wagga用Murrumbidgee地表水及地下水；不是定时浓度/抽水量数据包|公开说明页许可未确认；未打开监测值表、客户或内部运行材料|CONTEXT_ONLY；取水量/比例/处理效果UNKNOWN|
|D08 初筛|[NHMRC ADWG](https://www.nhmrc.gov.au/about-us/publications/australian-drinking-water-guidelines)|v4.0 June2025与章节更新；阈值/方法指导，非观测系列|本轮仅引用链接/转述；未核实全部图表/第三方复制许可|GUIDANCE_ONLY；无样本、流量或疾病数据|
|D09 初筛|[WHO2017入口](https://www.who.int/publications/i/item/9789241512770)|WHO相关水安全指导系列；各出版物逐项版本登记|不能统一把WHO各年代出版物视作同许可；不复制全文/图片|GUIDANCE_ONLY；许可对象化审查留待未来实际复用|

## 五项深入审查的具体范围

- D01：已确认名称/许可号/目录时间标签，**原生列、采样点、样本量、单位、LOD、实验室QA、更新日全部未从原表核实**。只登记原始URL，未打开其PDF数据表。公开列出不等于批准本轮下载。
- D02：政府许可和设施记录的用途是身份/条件，不是原始排放序列。没有从名称和监管文书推出地理点位/实际操作状态。
- D03：年报文本可引用；图像例外故没有拷贝地图/照片入包。项目级[Data confidence](https://www.act.waterwatch.org.au/data/data-confidence)描述质量活动，不能代替COO300某次采样校准。年报记录可研究，但原观测许可、时区和样本QA未闭合。
- D04：API文档可读，实际请求需key；在文档阶段即STOP。许可署名页没有解除访问门槛；未使用现有凭证或替代途径。
- D05：[WDO FAQ](https://www.bom.gov.au/waterdata/wiski-web-public/faq.htm)说明供应者的验证与临时记录可能合并，后续验证值可能覆盖临时值；BOM本身不重做供应者QC。A/B/C/E/F是质量等级，D停用；F在部分汇总中排除，可能隐藏缺口。站点级QC未查看。

## 访问失败和停止清单

详见 [access_log.json](access_log.json)。时间只保存检查日期；没有精确请求时间的项目不造时间戳。

- 本地读取Waterwatch目录HTML返回HTTP403，停止该端点。此前web工具已有目录元数据；后来只阅读已知、独立的版权页和指定年报出版物，未重试被拒目录或换镜像下载。
- 2022/23年报：工具返回content-length-too-large，不是源站403。只保留官方索引摘录，没有下载绕过工具限制。
- 2024地图截图未得到可审图像；p28截图Cache miss。只采用文字，不声称地图已复核。
- EPA详情及Numeralla报告打开Cache miss；没有编造HTTP状态、文件hash或当前许可。
- L02全文500/工具失败；PubMed可用信息不足。L03 PubMed没有可用正文，ACS索引摘要单列阅读深度。
- WaterNSW API须认证；旧D3失败原始文件、ArcGIS499和其他旧受限端点均未重试。

任何远端原始观测文件的 `raw_sha256`、`sample_count` 均为null。Git任务书/代码文件哈希与数据原件哈希严格分开。所有许可判断是研究尽调，不是正式法律意见。
