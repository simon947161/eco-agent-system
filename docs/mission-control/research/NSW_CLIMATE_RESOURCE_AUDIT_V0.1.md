# ClimateOS NSW Public Climate Resource Audit v0.1

**中文名称：** ClimateOS NSW 政府公开气候资源审计 v0.1  
**调查日期：** 2026-10-14（Australia/Sydney）  
**状态：** `DRAFT_FOR_FOUNDER_REVIEW / RESEARCH_ONLY / NO_INTEGRATION_EXECUTED`  
**调查边界：** 一次有界公开资料调查；未读取、上传或同步任何 Council 内部数据；未安装大型依赖；未部署服务；未批量抓取；未修改生产环境。  
**目标环境：** 复用现有 ClimateOS / Mission Control / KITTY / Simon Memory 治理架构，不新建独立平台。

---

## 1. 执行摘要

本轮结论是：NSW AdaptNSW 和 NARCliM 资源可以纳入现有 ClimateOS 学习与研究环境，但应按三种对象分别接入，并经过来源、版本、授权、证据和人工审阅关口：

1. **静态知识资源**：网页、PDF 指南、区域快照、用户指南；适合进入 Knowledge Registry，作为有版本和适用范围的参考知识。
2. **可填写工具**：DOCX/XLSX 模板、Health Check、Risk Assessment、地方政府 Climate Readiness Tool；适合作为受控模板登记，填写后的组织数据默认不得进入公共学习库。
3. **机器可读取数据**：CSV、GeoTIFF、NetCDF，以及交互地图导出的 Excel；适合经 Source Registry、Evidence Passport、参数和许可核验后，进入隔离的研究输入区。

最小方案不是新建门户，而是：

`官方入口 -> Source Registry -> 对象分类/版本与许可登记 -> 隔离下载或仅登记 -> Evidence Passport -> 有界 Cooma 示例 -> Founder Review -> 经批准的 KITTY 只读摘要`

主要可行性判断：

- **高可行性**：登记 Climate Risk Ready Guide、Toolkit、地方政府指南、NARCliM 区域快照和官方元数据。
- **中高可行性**：登记并人工使用 XLSX/DOCX 工具，但必须隔离填写内容并检查公式、隐藏页和版本。
- **中等可行性**：用 NARCliM 交互地图导出的 Excel/JPG/GeoTIFF 做小范围演示。
- **有条件可行**：从 Climate Data Portal 下载点位 CSV 或小范围 GeoTIFF/NetCDF。需要账户、参数纪律、文件体量控制和气候数据解释能力。
- **本轮未确认公众 API**：官方 Portal 用户指南说明 CKAN 是底层框架，但将“API Tokens”标为仅供 Portal 管理员使用。因此不能因为 CKAN 通常有 API 就推断本门户提供受支持的公众 API。

本报告建议以 **Cooma/Snowy Monaro 的公开资料**开展一个很小的、非运营性示范：先用 South East and Tablelands 区域资料建立背景，再用 NARCliM2.0 的 Cooma 点位 CSV或小范围 GeoTIFF比较选定变量、情景和时期；只报告模型投影及集合范围，不生成 Council 资产风险排名、不作地方政策或工程结论。

---

## 2. 调查方法与证据分级

### 2.1 方法

本轮只进行了以下操作：

- 阅读现有 ClimateOS 架构、Mission Control 研究索引、KITTY/Radar 边界说明和既有 Cooma 来源/证据登记样例；
- 查阅 AdaptNSW 官方落地页、PDF 和下载链接；
- 对关键资源核对用途、文件格式、公开版本、授权声明和更新线索；
- 对 API 可用性作“官方资料是否明确支持”的核查；
- 未执行数据下载批处理、账户注册、数据解析或集成。

### 2.2 术语

| 标签 | 含义 |
|---|---|
| **观察** | 官方页面、文件或仓库文档中可直接核验的事实 |
| **解释** | 基于观察对 ClimateOS 适用方式的判断 |
| **假设** | 尚未用实际下载/样本验证、后续必须测试的条件 |
| **建议** | Founder 审阅后才可进入实施队列的行动 |

### 2.3 适用性边界

- Climate Risk Ready NSW Guide 的主要对象是 NSW 州政府机构；地方政府可参考，但不能自动当作 Council 强制要求。
- 地方政府资源页和 2019 年 NSW Local Government Risk Assessment Guide 更贴近 Council 语境，但较旧材料不得静默覆盖 2026 年新版州政府 Guide。
- NARCliM 是区域气候**投影**，不是逐日天气预报，也不是单一地点的确定性未来。
- 官方发布身份证明来源权威和可追溯性，不等于对所有本地决策均充分。

---

## 3. 与现有 ClimateOS / Mission Control / KITTY 架构的对应

### 3.1 已复用的现有能力

| 现有能力 | 本审计的用法 | 边界 |
|---|---|---|
| Source Registry / 官方来源元数据登记 | 记录官方入口、直接文件、发布者、访问日、版本、格式、许可和替代关系 | 只登记不代表内容已被科学验证 |
| Knowledge Registry | 保存网页/PDF 的对象身份、摘要、适用对象和知识点 | 不将旧指南与新指南合并为一个无版本对象 |
| Evidence Passport | 对后续实际下载的数据记录参数、空间/时间范围、情景、模型集合、处理步骤、校验和及允许用途 | 本轮未创建数据 Passport，因为没有执行数据下载 |
| Claim / contradiction / missing-evidence ledger | 区分官方陈述、模型结果、解释和未证实结论 | 禁止把区域投影提升为 Council 资产级结论 |
| Mission Control | 建立研究任务、权限、审阅关口和完成状态 | Mission Control 负责路由，不替代 ClimateOS 技术真相 |
| KITTY | 仅显示 Founder 批准后的公开摘要、来源和限制 | 不向 KITTY 暴露未审阅工作簿或内部组织信息 |
| Conversation Radar | 将新资源当作外部信号，记录“使用前核验” | Radar 信号不是自动建设要求 |
| Simon Memory / ACTP / Handoff | 记录项目连续性、决策和边界 | 不把草案状态提升为 Founder 决策 |

### 3.2 最小对象模型

建议每个 NSW 资源至少登记：

| 字段 | 说明 |
|---|---|
| `source_id` | 稳定的 ClimateOS 内部 ID |
| `official_title` | 官方标题，不自行改写成另一工具 |
| `publisher` | NSW DCCEEW / AdaptNSW 或明确第三方 |
| `canonical_url` | 官方落地页优先；文件 URL 作为版本证据 |
| `accessed_at` | 本次访问日期和时区 |
| `resource_class` | `STATIC_KNOWLEDGE` / `FILLABLE_TOOL` / `MACHINE_DATA` |
| `format` | HTML、PDF、DOCX、XLSX、JPG、GeoTIFF、CSV、NetCDF 等 |
| `version_state` | 文件内版本、发布日期、更新日、是否替代旧版 |
| `audience_scope` | 州政府、地方政府、一般公众、技术用户等 |
| `licence_state` | 明示许可、一般版权、需逐数据集确认或未知 |
| `update_method` | 官方落地页、文件版本、Portal 通知或代际更新 |
| `admission_state` | 仅元数据、已审阅知识、隔离数据、Founder 已批准等 |
| `prohibited_use` | 例如法律意见、资产级风险结论、确定性预测 |

---

## 4. 资源目录

### 4.1 核心目录

| ID | 资源 | 实际用途 | 类型 | 可下载物与格式 | 版本/更新线索 | 授权状态 | 接入可行性 |
|---|---|---|---|---|---|---|---|
| `NSW-CRR-001` | [Climate Risk Ready NSW Guide](https://www.climatechange.environment.nsw.gov.au/resources-and-research/climate-risk-ready-nsw-guide) | 州政府机构气候风险与机会治理的四步方法；建立范围、评估、行动、监测改进 | 静态知识 | [Guide PDF](https://www.climatechange.environment.nsw.gov.au/media/10366)，约 4.86 MB、91 页 | 2026-06 首发；取代 2021 版；页面/配套资源会更新 | © State of NSW；按文件和 NSW 通用版权/免责声明使用，未见该 PDF 明示 CC BY | 高；作为方法参考，不自动当作地方政府义务 |
| `NSW-CRR-002` | [Climate Risk Ready NSW Toolkit](https://www.climatechange.environment.nsw.gov.au/media/10371) | 把 Guide 四步法转成工作表、清单、表格、行动和跟踪模板 | 静态知识 + 可填写模板 | PDF，29 页；PDF 指向可编辑 Word 用户模板 | First published / This version：2026-06 | © State of NSW；未确认可编辑模板的独立许可 | 高；模板副本须保留来源和版本，填写内容隔离 |
| `NSW-CRR-003` | Climate Risk Maturity Health Check（下载页名：Appendix B Health Check Tool） | 评估州政府机构气候风险成熟度，识别能力缺口 | 可填写工具 | [XLSX](https://www.climatechange.environment.nsw.gov.au/media/10396)，官方页标示约 342.75 KB | 作为 2026 Guide 配套下载；本轮未核验工作簿内部版本号 | 未见下载页明示开放许可；按 NSW 版权和文件内条款处理 | 中高；先做结构、公式、隐藏页和宏安全检查 |
| `NSW-CRR-004` | Appendix C Climate Risk Assessment Tool | 以结构化工作簿记录风险/机会、评价与处理信息 | 可填写工具 | [XLSX](https://www.climatechange.environment.nsw.gov.au/media/10401)，官方页标示约 154.02 KB | 作为 2026 Guide 配套下载；本轮未核验工作簿内部版本号 | 同上；不得把填写后的组织风险登记视为公开资料 | 中高；仅作模板实验，不接入公共知识层 |
| `NSW-LG-001` | [Resources for Local Government](https://www.climatechange.environment.nsw.gov.au/resources-and-research/resources-local-government) | 地方政府气候行动、减排和适应资源入口 | 静态索引 | HTML，链接 PDF/XLSX/DOCX 等工具和模板 | 以落地页当前链接为权威；逐文件登记 | 各文件可能不同；不得从入口页推定统一开放许可 | 高；作为 Local Government 资源集合的 canonical landing page |
| `NSW-LG-002` | LG Climate Action User Guide | 供 Council 系统规划、交付和监测 LGA/组织气候行动的四步指南 | 静态知识 | [PDF](https://www.climatechange.environment.nsw.gov.au/sites/default/files/2024-06/DPIE00~1.PDF)，约 13 MB | 官方路径显示 2024-06 发布批次；文件内版本待后续样本核验 | 未在本轮确认独立开放许可 | 高；作为地方政府语境主入口之一 |
| `NSW-LG-003` | Local Government Climate Readiness Tool（原 Health Check） | Council 自评减排与适应能力，并生成阶段进度图用于周期比较 | 可填写工具 | [XLSX](https://www.climatechange.environment.nsw.gov.au/sites/default/files/2024-06/Local%20Government%20Climate%20Readiness%20Tool_1.xlsx) | 页面称旧名为 Health Check；文件路径为 2024-06；内部版本待核验 | 未确认独立开放许可 | 中高；不要与州政府 Appendix B Health Check 混淆 |
| `NSW-LG-004` | Local Government templates set | 气候政策、数据来源与缺口、监测评估、岗位、委员会 ToR、风险政策条款模板 | 可填写工具 | 多个 DOCX/XLSX；其中 [Climate Data Template XLSX](https://www.climatechange.environment.nsw.gov.au/sites/default/files/2023-09/Local%20Government%20Climate%20data%20template.xlsx) | 各文件独立更新；从落地页重新核验 | 未确认统一开放许可 | 中高；只登记空白模板，禁止采集 Council 已填写内容 |
| `NSW-LG-005` | [Guide to Climate Change Risk Assessment for NSW Local Government](https://www.climatechange.environment.nsw.gov.au/sites/default/files/2021-06/Guide%20to%20climate%20change%20risk%20assessment%20for%20local%20government.pdf) | 为 Council 提供基于本地可用信息的定性风险评估方法；可用于更新既有评估 | 静态知识 | PDF | 2019 Revision；文件建议约每五年或有重大新资料/事件时复核 | © State of NSW/文件条款；本轮未确认 CC BY | 高，但必须标注年代并与 2026 Guide 并列而非覆盖 |
| `NSW-LG-006` | Local Government Climate Adaptation Guides 集合 | 风险评估、适应检查、适应手册、韧性规划和专题指南 | 静态知识集合 | 以 PDF 为主；包括 Local government adaptation checklist、Climate adaptation manual、灾害韧性土地利用、Bushfire-Resilient Homes council guide、2025 coastal technical report | 不是单一版本产品；每份文件独立发布和更新 | 部分为 NSW，部分为外部发布者；逐项核验 | 高；作为“指南族”登记，不创建虚构的单一产品 |
| `NSW-NAR-001` | [NARCliM products and data](https://www.climatechange.environment.nsw.gov.au/narclim/narclim-products-and-data) | 按使用者能力选择网页、区域快照、地图或原始/后处理数据 | 静态索引 | HTML，链接快照、地图、Portal、技术资料 | NARCliM 不同代际变量和模型不同；不可静默混用 | Portal 数据通常 CC BY 4.0，除非另有说明；须同时遵守 NARCliM T&C 和署名要求 | 高；作为 NARCliM canonical source family |
| `NSW-NAR-002` | NARCliM2.0 Interactive Projections Map | 以 4 km 网格快速浏览地区/邻域投影并导出地图或统计 | 交互工具 + 机器数据 | 网页；JPG、GeoTIFF、Excel | 3 个排放情景；时期/频率/变量由界面选择；需记录每次选择 | 使用下载物前核验界面/数据条款和署名 | 高；非常适合有界 Cooma 演示 |
| `NSW-NAR-003` | NARCliM2.0 regional climate snapshots | 以非技术语言呈现 NSW 规划区域的主要投影和影响背景 | 静态知识 | HTML + PDF | 2.0 为当前快照；1.0 快照作为归档保留 | 官方页面说明 Portal 资料通常 CC BY 4.0；快照仍应保留自身版权/署名 | 高；Cooma 使用 South East and Tablelands，不外推为点位结论 |
| `NSW-NAR-004` | [NSW Climate Data Portal](https://www.climatechange.environment.nsw.gov.au/climate-data-portal) | 搜索、筛选并下载 NARCliM 模拟、变量、区域和时间段 | 机器数据门户 | 点位：CSV；面域：NetCDF/GeoTIFF；集合或单模型 Dataset | Portal 用户指南 v1.7，2026-04-15；门户/数据集通知更新 | 除非另有说明，Portal 数据/材料为 CC BY 4.0；须读数据集条款和正式署名 | 中；需账户、技术能力和体量控制 |
| `NSW-NAR-005` | [NSW Climate Data Portal User Guide](https://www.climatechange.environment.nsw.gov.au/sites/default/files/2025-07/Climate-data-portal-user-guide.pdf) | 说明搜索、空间选择、日期、格式、下载、账户和 CKAN 背景 | 静态知识 | PDF，26 页 | v1.7，2026-04-15；首次发布 2025-06，更新 2026-04 | NSW 文件版权/免责声明；本轮未确认独立 CC BY | 高；作为 Portal 操作版本依据 |
| `NSW-REG-001` | [South East and Tablelands](https://www.climatechange.environment.nsw.gov.au/my-region/south-east-and-tablelands) | Cooma/Snowy Monaro 的区域背景、主要投影和地区价值语境 | 静态知识 + 快照入口 | HTML/PDF | 当前网页明确包含 Cooma；快照代际需登记 | 保留 AdaptNSW/NARCliM 署名和文件条款 | 高；只作区域背景，不替代本地证据 |

### 4.2 分类小结

| 分类 | 典型资源 | ClimateOS 处理方式 |
|---|---|---|
| 静态知识 | Guide、Toolkit PDF、Local Government guides、regional snapshots、Portal User Guide | 保存元数据和必要的版本化副本；提炼知识点时保留页码、版本和适用对象 |
| 可填写工具 | Health Check、Risk Assessment、Climate Readiness、政策/数据/监测模板 | 登记空白官方模板；复制到隔离工作区填写；输出默认私有且需人工批准 |
| 机器可读取数据 | Interactive Map Excel/GeoTIFF、Portal CSV/GeoTIFF/NetCDF | 下载前冻结参数；下载后校验格式、尺寸、许可、校验和和模型元数据；不得直接进入运行时 |

---

## 5. 各资源的实际用途与限制

### 5.1 Climate Risk Ready NSW Guide 与 Toolkit

**观察**

- 2026 年版 Guide 取代 2021 年版，并加入气候机会、转型风险、国际标准和 NSW 政策变化。
- Guide 使用四步迭代流程：建立基础；识别/分析/评价；制定并实施行动；监测/评价/报告/改进。
- Toolkit 把四步流程转为 PESTLE 提示、风险治理记录、时间范围、利益相关方、影响记录、行动优先级和进度跟踪等模板。
- Toolkit PDF 明确提到另有可编辑 Word 用户模板。

**解释**

- 适合作为 ClimateOS 的方法和治理参考，不应被编码成自动评分真理。
- 工具中涉及风险偏好、治理负责人、资产、服务或内部风险登记的字段可能包含敏感组织资料；即使空白模板公开，填写内容也不是公共数据。

**验证要求**

- 后续若下载 DOCX/XLSX，需记录文件 SHA-256、内部属性、公式、隐藏页、外部链接、宏状态和文件内许可。
- 明确区分“Guide 版本”和“工作簿内部版本”；不能仅因同页链接就假定完全一致。

### 5.2 NSW Resources for Local Government

**观察**

- 官方资源页提供地方政府 Climate Action User Guide、Climate Readiness Tool 和多种模板。
- Local Government Climate Readiness Tool 是 Excel 自评/基准工具，会生成各阶段进度图；官方页面说明它以前称为 Health Check。
- Local Government Climate Data Template 用于记录数据来源并做 Council/agency functions 的数据缺口分析。

**解释**

- 这是建立 Local Government 学习路径的最佳入口，但不应把外部或较旧指南都归并为一个“NSW 官方当前标准”。
- “Local Government Climate Adaptation Guides”在官网上实际是一个资源集合，而非一个有统一版本号的单一产品。
- 对 ClimateOS，地方政府工具最合适的角色是教学模板和流程示范，而不是采集真实 Council 组织数据。

### 5.3 NARCliM2.0 地图、区域资料与下载

**观察**

- 交互地图以约 4 km 网格展示 NARCliM2.0 投影，可选 3 个排放情景和多个时期/频率。
- 地图变量包括平均/最高/最低温、降雨、≥35°C 热日、<2°C 冷夜和 FFDI>50 严重火险天气日。
- 可下载 JPG、GeoTIFF 和 Excel；Portal 可下载 NetCDF、GeoTIFF 或 CSV。
- Portal 的点位选择只输出 CSV；面域选择可输出 NetCDF 或 GeoTIFF。
- Portal 可用 Collection（多个集合成员）或单一 Dataset；实际研究不应只挑一个“看起来合理”的模型。
- Portal 基于 CKAN，但官方用户指南把 API Token 标为仅供管理员使用。

**解释**

- 交互地图适合低成本学习、沟通和参数试验；Portal 适合可重复分析，但对数据体量、日历、集合和气候不确定性要求更高。
- 4 km 是模型网格，不是 4 km 精度的资产风险答案。
- GeoTIFF 适合 QGIS 视觉检查；CSV 适合小规模时间序列；NetCDF 适合更完整的科学分析，但不应成为 v0.1 最小入口。

**官方 API 结论**

`NO_SUPPORTED_PUBLIC_API_CONFIRMED_IN_THIS_BOUNDED_AUDIT`

- 确认底层为 CKAN，不等于确认其 Action API 对公众开放、稳定或受支持。
- 官方指南未提供公众 API 接入流程，且明确 API Token 只供 Portal 管理员。
- 因此最小方案只使用官方网页/人工下载和文件级元数据。未来只有在 NSW 官方文档明确公开 API、认证、速率限制和许可后，才评估 API adapter。

### 5.4 Climate Risk Assessment Tool 与 Maturity Health Check

**观察**

- 州政府页面提供 Appendix B Health Check Tool（XLSX）和 Appendix C Climate Risk Assessment Tool（XLSX）。
- 地方政府另有 Climate Readiness Tool（原 Health Check），用途和受众不同。

**解释**

- 三个工作簿应分别登记为不同对象；禁止用同一个内部 ID 或用“Health Check”短名覆盖。
- 工作簿输出是组织自评或风险分析结果，不是 NARCliM 数据，也不是客观的独立风险评级。
- 任何自动读取、评分或写回都必须另立任务，先验证公式、字段语义、数据保护和人工批准流程。

---

## 6. 授权、版本与更新管理

### 6.1 授权判断

| 资源族 | 本轮确认 | 不应做的推断 |
|---|---|---|
| NSW Guide/Toolkit/工作簿 | 文件显示 State of NSW 版权及通用版权/免责声明入口 | 不因“公开下载”就推断可任意再许可、修改或再发布 |
| Local Government resources | 入口页公开，文件发布者和条款不完全相同 | 不给整个集合套用单一许可 |
| NARCliM Portal 数据与材料 | 官方页称除非另有说明为 CC BY 4.0；还须遵守 NARCliM Terms and Conditions 并正式署名 | 不忽略数据集级例外、免责声明、隐私或引用要求 |
| 第三方 Local Government guides | 由不同发布者托管 | 不把 NSW 页面链接视作 NSW 拥有版权 |

建议后续每个下载对象设置：

- `LICENCE_CONFIRMED`
- `LICENCE_DATASET_SPECIFIC`
- `COPYRIGHT_ONLY_REUSE_RESTRICTED`
- `LICENCE_REVIEW_REQUIRED`

未确认许可时只保留最小元数据和官方链接，不复制全文或再发布衍生文件。

### 6.2 版本与更新方式

采用低频、人工、有界的更新检查，不部署爬虫或定时服务：

1. 检查 canonical landing page 是否变更标题、版本、发布日期或下载链接。
2. 对已批准下载物比较文件大小、SHA-256、PDF/DOCX/XLSX 内部版本和 `Last-Modified`（若服务端提供）。
3. NARCliM 对每份资料登记 generation、模型集合、情景、变量、频率、空间分辨率、时期和偏差订正状态。
4. 触发重新审阅的事件：新 Guide/Toolkit 版、新工作簿、NARCliM 新代际、Portal User Guide 新版、Terms/许可变化、区域快照替换。
5. 保留 superseded 关系；不覆盖旧记录，不把 NARCliM1.0 与 2.0 数据直接拼接。

建议检查频率：Founder 批准后每 6 个月人工检查一次，或在官方发布通知后按事件检查。当前不创建自动化。

---

## 7. Cooma / Snowy Monaro 公开资料示范研究

### 7.1 研究问题

在不使用 Council 内部数据的前提下，回答一个有限问题：

> “公开 NARCliM2.0 资料显示，Cooma 周边在不同排放情景和未来时期下，温度、降雨、热日、冷夜和严重火险天气日的模型投影如何变化；这些变化的模型集合范围和主要限制是什么？”

这不是：

- Snowy Monaro Regional Council 的正式气候风险评估；
- 对道路、建筑、水务、人员或其他资产的风险排名；
- 未来天气预测；
- 法律、规划、投资或工程建议。

### 7.2 公共输入

1. South East and Tablelands 官方区域页和 NARCliM2.0 区域快照：区域叙事背景。
2. NARCliM2.0 交互地图：Cooma 周边的 JPG/Excel/GeoTIFF 小样本。
3. 若 Founder 后续批准技术 POC：Climate Data Portal 的 Cooma 单点 CSV 或很小研究多边形 GeoTIFF。
4. 仅用于背景交叉核验的公开 BoM 站点元数据；不在本审计中下载或混合观测序列。

### 7.3 参数冻结建议

正式下载前应创建一个参数清单：

| 参数 | 最小示范选择 |
|---|---|
| 地点 | Cooma 公共地理坐标的单点；或明确边界的小范围多边形，不默认整 LGA |
| Generation | NARCliM2.0 |
| 变量 | mean/max/min temperature、rainfall、hot days、cold nights、severe fire weather days（以产品可用性为准） |
| 基准期 | 1990–2009（若对应产品提供） |
| 未来期 | 2040–2059 和 2080–2099，或界面正式提供的标准时期 |
| 情景 | 界面提供的 3 个情景，保留官方名称 |
| 集合 | 尽可能使用全部 10 个集合成员；展示中位数/范围，不只选单模型 |
| 空间 | 先点位 CSV；如需 QGIS，仅选小范围 GeoTIFF |
| 输出 | 数据表、简图、参数清单、Evidence Passport、限制说明 |

上述时期是候选，只有界面/数据集实际提供并核对元数据后才能冻结。

### 7.4 分析与验证规则

- 把 baseline 与未来期比较为“投影变化”，不用“将会”。
- 分别报告情景差异和集合成员差异。
- 记录单位、频率、日历、缺失值、偏差订正和派生阈值定义。
- 对极端指标确认它是模型/产品定义的阈值统计，不与本地灾害概率等同。
- QGIS 只用于人工视觉核验和地图呈现；图层 CRS、网格和值域必须登记。
- 不把单个 Cooma 网格推广为整个 Snowy Monaro LGA。
- 发布前由具备气候投影解释能力的人复核。

### 7.5 预期示范产物

- 1 个公开来源清单；
- 1 个冻结参数文件；
- 每个实际下载物 1 个 Evidence Passport；
- 1 份情景/时期对比表和不确定性说明；
- 1 个 QGIS 小范围可视化（仅在后续批准后）；
- 1 份 Founder Review 摘要；
- KITTY 仅显示获批的公开摘要和来源链接。

---

## 8. 最小接入方案（本轮不执行）

### 阶段 0：Founder Gate

- 审阅本报告并确认资源边界、许可处理和 Cooma 演示问题。
- 明确是否允许下载官方空白模板和小样本 NARCliM 数据。
- 未批准前保持 `RESEARCH_ONLY`。

### 阶段 1：静态资源登记

- 在现有 Source Registry 中新增 NSW 资源对象；
- 将 Guide、Toolkit、地方政府指南、区域快照和 Portal User Guide 注册为 Knowledge Objects；
- 记录版本、受众、替代关系、许可和禁止用途；
- 不建设新 UI、不复制整个官网。

### 阶段 2：可填写工具隔离

- 只下载官方空白 XLSX/DOCX；
- 执行文件安全和结构检查；
- 建立模板对象，不导入真实 Council 答案；
- 用完全虚构的演示字段验证可用性，并明确 `SYNTHETIC_DEMO_ONLY`。

### 阶段 3：Cooma 小样本数据 POC

- 先用 Interactive Map 的 Excel/JPG；
- 需要机器读取时，再选择一个点位 CSV 或小范围 GeoTIFF；
- 每次只下载冻结参数对应的小数据集；
- 生成 Evidence Passport 和不确定性说明；
- 不做全 NSW、整代际、全部变量下载。

### 阶段 4：Mission Control / KITTY 呈现

- Mission Control 显示来源、状态、证据、风险和 Founder gate；
- KITTY 只读展示已批准知识卡、图表和“这是投影而非预测”的限制；
- Simon Memory 只记录批准后的决策和任务连续性，不存放原始大型气候文件。

---

## 9. 工作量估算

以下为后续实施的指示性范围，不是本轮执行承诺：

| 工作包 | 估算 | 产物 | 主要依赖 |
|---|---:|---|---|
| 静态资源登记与知识对象 | 1–2 人日 | Source Registry 条目、版本/许可记录、知识摘要 | Founder 批准；官方文件可访问 |
| XLSX/DOCX 模板安全与结构核验 | 1–2 人日 | 模板清单、公式/隐藏页/宏检查、数据隔离规则 | 可下载文件；Office/OpenXML 检查能力 |
| Interactive Map 小样本演示 | 2–4 人日 | Excel/JPG/GeoTIFF 样本、Passport、QGIS 视觉检查 | 参数冻结；地图服务可用 |
| Portal 点位 CSV 或小范围 GeoTIFF/NetCDF POC | 3–7 人日 | 可重复下载记录、解析、集合/情景比较、验证说明 | Portal 账户；下载队列；领域复核 |
| Founder Review 与文档闭环 | 1–2 人日 | 审阅记录、批准/拒绝项、KITTY 可见摘要 | Founder 决策 |

不含 Portal 注册等待、异常大文件处理、完整科学研究、Council 协作或生产集成。

---

## 10. 风险、控制与剩余不确定性

| 风险 | 后果 | 控制 | 剩余状态 |
|---|---|---|---|
| 把州政府 Guide 当作 Council 强制规则 | 适用范围错误 | 登记 audience/scope；与地方政府指南并列 | 需治理复核 |
| 2019 地方指南与 2026 Guide 静默混用 | 方法和版本冲突 | 保留独立对象、日期和 superseded/related 关系 | 可控 |
| 把投影当预测或观测 | 误导用户 | 强制 projection 标签；分开观测和模型数据 | 需领域复核 |
| 单模型/单网格过度解释 | 伪精确本地结论 | 使用集合、范围、4 km 网格说明；禁止资产级推断 | 中等 |
| NARCliM 代际/情景/变量不一致 | 错误比较 | 冻结 generation、scenario、variable、period 元数据 | 可控 |
| XLSX 公式、隐藏页、链接或宏 | 安全/计算错误 | 隔离、结构检查、禁宏、人工核算样例 | 未实测 |
| 工作簿含 Council 内部资料 | 隐私和治理违规 | 仅空白模板/虚构数据；默认不入库、不上传 | 强制边界 |
| NetCDF/GeoTIFF 体量过大 | 额度、存储、运行风险 | 优先点位 CSV/小范围数据；下载前估算 | 可控 |
| 气候日历和时间聚合 | 时间轴或统计错误 | 读取 calendar/frequency 元数据；建立验证样例 | 需技术验证 |
| 许可被过度概括 | 不当再发布 | 每文件/数据集记录许可；保留署名和 T&C | 中等 |
| CKAN 被误当公共 API 保证 | 建立脆弱集成 | 当前明确 API 未确认；只用官方支持的下载流程 | 已控制 |
| Portal 账户或服务变化 | 自动化不可用 | v0.1 不依赖 API/自动抓取；保留人工路径 | 低至中 |
| 区域资料不足以支持地方决策 | 不当建议 | 明确 `CONTEXT_ONLY`，列出缺失证据和审阅要求 | 高重要性 |

---

## 11. Conversation Radar 摘要

### Knowledge points

- Climate Risk Ready NSW 2026 版提供四步治理框架和可编辑配套模板。
- 地方政府资源形成独立的行动、准备度、数据登记和适应指南集合。
- NARCliM2.0 提供从区域快照、4 km 交互地图到 CSV/GeoTIFF/NetCDF 的分层产品。
- Portal 数据通常为 CC BY 4.0，但必须同时核对数据集级例外和 NARCliM Terms and Conditions。

### Idea points

- 把 NSW 资源做成现有 Registry + Evidence Passport 的一个 source family，而不是新平台。
- 以 Cooma 单点 CSV 和小范围 GeoTIFF作为低成本、可验证的 ClimateOS 教学样例。
- 让 KITTY 只显示 Founder 批准后的“知识卡 + 来源 + 限制”，不暴露工作簿或原始大型数据。

### Decisions in this audit

- `REUSE_EXISTING_CLIMATEOS_ARCHITECTURE`
- `NO_NEW_PLATFORM`
- `NO_PUBLIC_API_ASSUMED`
- `PUBLIC_DATA_ONLY`
- `NO_INTEGRATION_IN_THIS_ROUND`
- `FOUNDER_REVIEW_REQUIRED`

### Risks

- 适用对象混淆、版本漂移、许可差异、投影过度解释、工作簿敏感内容、数据体量和 API 假设。

### Open questions

1. Founder 是否批准下载空白 XLSX/DOCX 并做离线结构检查？
2. Cooma 示范优先使用交互地图 Excel，还是 Portal 单点 CSV？
3. 是否要求气候领域人员对集合统计、偏差订正和极端指标作独立复核？
4. 对 NSW 版权资源，ClimateOS 是只保存元数据/链接，还是在许可复核后保存版本化本地副本？
5. KITTY 可见内容应限制为哪一层：来源目录、区域摘要，还是经审阅图表？

### Next actions

1. Founder 审阅本报告并批准/拒绝阶段 1–3。
2. 若批准，先做静态 Source Registry，不下载机器数据。
3. 单独核验三个工作簿的内部版本、结构和许可。
4. 冻结 Cooma POC 参数，再执行一次小样本下载。
5. 产出 Evidence Passport 和人工科学复核记录后，才考虑 KITTY 展示。

### Related project keywords

`ClimateOS`, `EcoEngine`, `CCZPS`, `Mission Control`, `KITTY`, `Conversation Radar`, `NARCliM2.0`, `AdaptNSW`, `Cooma`, `Snowy Monaro`, `South East and Tablelands`, `Evidence Passport`, `Source Registry`, `Founder Gate`, `public climate projections`

---

## 12. 建议与 Founder Gate

### 推荐

批准一个三段式、可停止的最小接入：

1. **先登记**：静态来源、版本、许可和适用范围；
2. **再隔离验证**：空白工作簿和一个 Cooma 小样本；
3. **最后决定展示**：只有证据、许可和科学解释均过关，才进入 KITTY 的只读层。

### 暂不推荐

- 新建 NSW 独立平台；
- 将 Portal 视为有公众 API 并直接编码；
- 批量下载全 NSW、全部情景、全部变量或日尺度 GeoTIFF；
- 把 Council 自评工作簿接入公共知识库；
- 以区域快照直接生成 Council 或资产级行动结论；
- 在没有领域审阅的情况下自动评分气候风险。

### 当前 Gate 状态

`AUDIT_COMPLETE / INTEGRATION_NOT_STARTED / WAITING_FOR_FOUNDER_REVIEW`

---

## 13. 官方来源清单

访问日期均为 2026-10-14：

1. [Climate Risk Ready NSW Guide landing page](https://www.climatechange.environment.nsw.gov.au/resources-and-research/climate-risk-ready-nsw-guide)
2. [Climate Risk Ready NSW Guide PDF](https://www.climatechange.environment.nsw.gov.au/media/10366)
3. [Climate Risk Ready NSW Toolkit PDF](https://www.climatechange.environment.nsw.gov.au/media/10371)
4. [How state government can adapt — Guide and XLSX downloads](https://www.climatechange.environment.nsw.gov.au/how-adapt/state-government/how-state-government-can-adapt)
5. [Resources for Local Government](https://www.climatechange.environment.nsw.gov.au/resources-and-research/resources-local-government)
6. [How local councils and authorities can adapt](https://www.climatechange.environment.nsw.gov.au/how-adapt/local-councils-and-authorities/how-local-councils-and-authorities-can-adapt)
7. [Guide to Climate Change Risk Assessment for NSW Local Government — 2019 Revision](https://www.climatechange.environment.nsw.gov.au/sites/default/files/2021-06/Guide%20to%20climate%20change%20risk%20assessment%20for%20local%20government.pdf)
8. [NARCliM](https://www.climatechange.environment.nsw.gov.au/narclim)
9. [NARCliM products and data](https://www.climatechange.environment.nsw.gov.au/narclim/narclim-products-and-data)
10. [Planning your climate project or assessment with NARCliM](https://www.climatechange.environment.nsw.gov.au/narclim/using-narclim-data/planning-your-climate-project-or-assessment-narclim)
11. [NSW Climate Data Portal landing page](https://www.climatechange.environment.nsw.gov.au/climate-data-portal)
12. [NSW Climate Data Portal User Guide v1.7](https://www.climatechange.environment.nsw.gov.au/sites/default/files/2025-07/Climate-data-portal-user-guide.pdf)
13. [South East and Tablelands](https://www.climatechange.environment.nsw.gov.au/my-region/south-east-and-tablelands)
14. [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)

---

## 14. 审计结束声明

本轮仅完成公开资源调查和报告。没有执行集成、下载数据批次、修改生产环境、部署服务或处理 Council 内部资料。下一步等待 Founder 审阅和新的明确授权。
