# 官方Excel模板只读核查

核查日期2026-11-05。目标November2026专用模板未取得；已检查授权workspace、附件目录及上轮证据目录，未发现目标文件；检索官方页面和精确文件名未找到可核验下载链接。**NOVEMBER_TEMPLATE_NOT_OBTAINED** 不阻断基础研究。

替代：官方 `Credits wanted (credit demand) template`，仅是需求登记同类表格，**不是November反向拍卖表，也不是BAM科学计算工具**。

- 发布者：NSW DCCEEW。
- 来源页：[Find credit buyers and sellers](https://www.environment.nsw.gov.au/topics/animals-and-plants/biodiversity-offsets-scheme/biodiversity-credits-market/find-credit-buyers-sellers)，页面Updated06October2026。
- [实际下载链接](https://www.environment.nsw.gov.au/sites/default/files/2026-05/bos-credits-wanted-credit-demand-template.xlsx)。23801字节。
- SHA-256：`585d06e14c85dfd9ec8b527647db2e742be5888e51469716198dddf7f4b6891a`。
- core.xml：creator DCCEEW；created2026-03-24T01:46:30Z；modified2026-05-13T03:49:21Z。revision为空；路径2026-05不单独作为批准版本号。
- Workbook未发现单独许可声明。公开下载不推定MIT许可；不把官方原件提交到仓库。完整原件保留本地并由manifest定位。
- 方法：Python标准库ZIP/XML解析全部worksheet及包清单；不打开执行宏、不更新外部链接、不重算、不填表、不提交。原始字节前后SHA相同。

## 工作表及结构

两个表均visible：`Credit Wanted Template`、`Lodgement information`。未发现hidden/veryHidden表、隐藏行列、公式、defined names、worksheet数据验证、sheet protection、vbaProject或externalLink部件。没有公式不代表业务规则不存在；必填仅来自星号与说明，Excel没有强制验证。没有自动计算字段。

主表A1标题；A2说明带星号字段必填，联系人姓名及联系信息会公开出现在需求登记册。G5:M5只用于Ecosystem；N5:P5只用于Species；Q5:S5只用于business。正式数据行目前无买方实例。本次未收集姓名或联系方式。

还检查了`xl/drawings/drawing1.xml`的嵌入文本框：它说明公开登记册的法定目的、下载数据的用途限制、姓名/联系方式公开，以及涉及安全或福祉时可请求限制披露的机制。这里是原件说明的概述，未作法律适用认定，也未发起请求。全部关系文件未发现TargetMode=External；customXml中的三组项目是Office/SharePoint元数据、内容类型schema和文档库表单标识，不是隐藏需求表或附加信用计算规则。没有访问schema命名空间URL或执行任何内容。

下表“匹配用途”是研究解释；“必填”依据原件星号及条件分组，不是新增官方验证规则。

| 第6行字段 | 要求与单位/类型 | 填写/验证现状 | 对匹配或决策的作用 |
|---|---|---|---|
| A CWXXX (for dept use only) | 部门专用标识 | 不由申请人生成；非公式 | 后续定位与更新记录 |
| B Date listed | 无星号；日期 | 格式未强制；是否部门填写未明确 | 列表时点与新旧需求 |
| C Ecosystem or Species* | 必填，类别文字 | 无下拉校验 | 选择后续字段路径 |
| D Number of credits* | 必填，信用数量 | 无整数/正数验证；不擅造最小值 | 采购规模及部分满足量 |
| E IBRA Region* | 必填，区域名称 | 无受控词表 | 地理匹配背景 |
| F IBRA Subregion* | 必填，次区域名称 | 无父子区域校验 | 较细地域匹配 |
| G PCT ID* | Ecosystem条件必填，分类ID | 无数据库连接 | 确定植物群落分类 |
| H Plant Community Type Common Name* | Ecosystem条件必填，名称 | 与ID一致性需人工核对 | 避免分类误认 |
| I Offset Trading Group* | Ecosystem条件必填，OTG | 无下拉 | 信用组筛选；不自行确认法定替代 |
| J Threatened Ecological Community (NSW) | Ecosystem，无星号 | 无选项；空白含义未定义 | TEC限制与匹配背景 |
| K Vegetation Formation | Ecosystem，无星号 | 无验证 | 较高层植被分类 |
| L Vegetation Class | Ecosystem，无星号 | 无验证 | 分类及交易组核查 |
| M Hollow Bearing Trees* (Y/N) | Ecosystem条件必填 | 标签指定Y/N，但无数据验证 | 树洞属性匹配 |
| N Species ID* | Species条件必填 | 无分类库验证 | 物种信用识别 |
| O Species Scientific Name* | Species条件必填 | 无ID/名称核对 | 避免俗名歧义 |
| P Species Common Name* | Species条件必填 | 无验证 | 可读物种名称 |
| Q Business Name* | Business条件必填 | 无ABN字段或身份核验 | 需求主体联系背景 |
| R Business Phone* | Business条件必填 | 无号码规则 | 联系，不证明购买权限 |
| S Business Email* | Business条件必填 | 无邮件格式校验 | 联系，不构成合同 |
| T Contact First Name* | 必填，个人信息 | A2说明会公开 | 联系人识别 |
| U Contact Last Name* | 必填，个人信息 | 同上 | 联系人识别 |
| V Contact Email* | 必填，个人信息 | 同上，无格式校验 | 沟通渠道 |
| W Contact Phone* | 必填，个人信息 | 同上 | 沟通渠道 |
| X Contact Mobile* | 必填，个人信息 | 同上；未说明与Phone二选一 | 沟通渠道 |

未发现项目名称、开发批准编号、法定义务证明、预算、单价、采购截止日、优先日、结算、TFD、BAM输入或信用计算公式。不能把这些合理的采购需求反向写成官方表已有字段，也不能从表格登记推导采购决定或法定义务。

## 说明表及原件缺陷

`Lodgement information!A2`说明邮件提交、处理确认、重新提交原表以请求延长/重新登记或终止。它称CW将出现在credit supply register，与主表demand register及官网需求登记用途不一致，按原件措辞错误保留，不能改写成科学结论。它讨论expiry date，但主表没有expiry字段；不能虚构一列，须正式使用时向主管机构澄清。本研究未发送任何邮件。

## 科学输入模板与市场需求模板的区别

BAM-C用户指南描述从工具内取得的plot import模板：包含plot、PCT、area、patchsize、坐标及样方组成/结构/功能输入；指南要求最新模板及特定行结构。该工具内原始模板本轮未取得，故这里只核查指南所描述的数据结构，不声称检查其全部工作表、公式或验证。正式评估另依BSSAR/管理计划要求，不能拿上述24列需求表生成信用。[S03、S14]

## 未解决项

November专用工作簿的字段、隐藏内容、公式、验证、版本和许可均为UNKNOWN，不能从替代版本迁移结论。S08的全部单元格、合并区、元数据及结构扫描在`workbook-inspection.json`，用于复核；它是原件的派生结构记录，不是另一份官方模板。

归档版结构记录保留字段标签及单元格位置，较长说明和文本框采用中文摘要；原始逐字提取仅留本地。复核时按文件SHA重新取得原件即可比对，不将说明全文当作可自由再发布的原创内容。
