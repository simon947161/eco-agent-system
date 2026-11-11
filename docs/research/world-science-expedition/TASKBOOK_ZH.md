# CLIMATEOS-WORLD-SCIENCE-EXPEDITION-001
## 世界地球科学探索站｜Codex 学习、查证、理解并制作互动网站
Founder 授权：2026-11-11（Australia/Sydney）
基线：PR #155 HEAD `256f950685c0eafd3771ff1c1c8fe696de6f5d1d`
工作分支：`research/climateos-world-science-expedition-001`
状态：任务授权与首批工程交付要求；后续研究持续迭代须有新的明确阶段边界。
**主张：带着 ClimateOS 的问题进入联合国、国际科研机构的真实公开资料；一边学、一边质疑、一边用自己的话解释，并逐步把研究路径做成人人能看懂、可追溯、图文并茂的个人地球科学学习网站。**
这是教育/研究/知识基础设施工作，不是另一个物理模型、自称官方合作伙伴或未经验证的科学结论。不要只写新任务书；必须做出真实可运行的网页和首批完成的深度学习成果。

## 1. 执行前先核定边界：不要碰错网站
- 阅读 `AGENTS.md`、ClimateOS架构、PR#155源码/物理限制与审查；**只读**查看PR#130 (`feature/public-strategy-atlas-web-mvp-20261029`) 的路线图式网站交互与证据模式。
- PR#130的 `apps/public-strategy-atlas` 属于**Council owner-only/private trial**，有独立的导航验收/访问控制及用户工作状态。**严禁将其私人Council资料复制到新站，严禁修改或部署原Council站、水文站、个人现有站。** 只借鉴其「Route-first / station / evidence / history / source」体验模式，不依赖其未合并的代码或存储，不把其秘密内容导出。不要同时合并PR130和PR155。
- 在现有ClimateOS仓库新建独立的 **`apps/earth-science-expedition/`**（轻量静态、零重型依赖或按项目现有工具）；将来若要挂到用户的个人 ChatGPT Site/域名，先提交可运行预览与发布方案，**必须经Founder单独审核/批准后才能发布**；不得未经授权创建站点/改变权限/覆盖当前Site。
- 本任务完全无需访问本机私人 `EcoEngine v200`；PR#152,#153,#155 均保持Draft、不合并、不改其原HEAD/科学门。

## 2. 六个带问题的首批研究对象（限定研究规模）
第一批最多 6 个「机构/项目研究站」，源资料初读最多25个官方/原始来源页面。任何需要登录、费用、许可不明或HTTP403的内容，**记录访问限制，不绕过，不假称读完或已合作**。

A. **UNEP WESR / GEDS**：「联合国为什么要建设全球环境数据体系？什么叫来源可信、质量可验证、可负担、互操作？」  
   https://wesr.unep.org/  
   https://www.unep.org/en/what-we-do/digital-transformations/global-environmental-data-strategy-geds
B. **UNEP GEO-7**：「联合国如何从全球证据比较未来？综合评估与可以执行的数值预测有什么差别？」  
   https://www.unep.org/geo/global-environment-outlook-7
C. **WMO WIS2 / wis2box**：「世界气象数据为什么需要全球交换？一个普通开发者可以合法接触哪些公开数据或规范？」  
   https://wmo.int/activities/wmo-information-system-wis
D. **ECMWF / Copernicus ERA5 / Destination Earth**：「再分析、现场观测、数值预测、地球数字孪生究竟如何区别？哪个公开产品允许被我们读取和比较？」  
   https://climate.copernicus.eu/climate-reanalysis  
   https://destine.ecmwf.int/digital-twins/
E. **ESMF / NUOPC**：「真实地球系统模型如何管理时钟、组件、连接器、中介、空间重网格？与 PR#155关系执行器有什么真正差别？」  
   https://earthsystemmodeling.org/nuopc/  
   https://earthsystemmodeling.org/regrid/
F. **CSDMS BMI**：「怎样用共同接口连接不同科研模型？与ClimateOS ModelPort 哪些字段、函数可映射，哪里不兼容？」  
   https://csdms.colorado.edu/wiki/BMI  
   https://github.com/csdms/bmi

**第一批最少完成5个有官方原始来源的研究站，选2个真正深入拆开技术步骤，至少1项真实可运行的“小型可复核学习实验”**（例如只读比较BMI接口与PR152 ModelPort函数，写可执行的兼容性/不兼容性检查；若没有真实接入，不得标成已成功使用BMI；WIS2/ERA5数据接入只在许可、访问、格式确认后做最小合法读取）。不得因为某机构名声大而自动判断可复用。
**保留下一批队列，不一口气研究完：** NSF NCAR CESM、WCRP CMIP7、IIASA MESSAGEix-GLOBIOM、UN SEEA、IPBES Nexus、Jakob Runge Tigramite、NASA Earthdata、其他相关大学/开源机构；每次由Founder选择或Codex根据已发现的缺口给出建议。当前不自动新建十几个PR。

## 3. 每个研究站必须真正回答的“普通人问题”
每家机构/项目都要有同一份可检索的中英双语字段，**中文为主，英语机构名称保留**：
1. 用一句话介绍：这是**机构、报告、模型、软件、数据门户、标准还是评估体系**？不能混为一谈。
2. 为什么创办/推动它？它试图解决什么公共问题？机构责任/资金或治理关系：仅写官网有证据的内容。
3. 它到底怎么运转？资料从哪来、经过什么算法/审核/组件、产生什么输出、谁来使用？绘制原创简化流程图。
4. 普通人现在能访问什么？官方公开网页/数据产品/API/文档/仓库/学习资料，访问权限、许可、费用、账号、更新时间、适用范围按来源核实，不认识就 UNKNOWN。
5. **与ClimateOS直接比较**：数据、时空、物理模型、耦合、因果关联、CCZPS、人类决策中的哪一层对应；哪项可ADOPT / WRAP / LEARN / DEFER / REJECT，以及证据、成本与理由。
6. 一个值得思考的问题：这些成果解决了什么？哪些尚未解决？为什么我们不能把政策分数当物理参数、把再分析当实测、把模型通过测试当预报能力？
7. Founder的“个人理解”与“Codex的推论”分栏：**用户已明确发表的观点可以摘意归纳并标注来源；AI新增思考显著标为`AI INTERPRETATION / 待Founder确认`，不要冒充Founder亲口说过的话**。
8. 每段关键事实能够点开**官方原始出处及准确页面/章节/版本、读取日期**；支持支持证据/相反证据/未查/已过时/修订版本。网页找不到则显示NOT_VERIFIED，不写自信科普。

## 4. 建一个持续成长的学习系统，而不是一次性宣传页
独立设计`Science Expedition Notebook`：每一次学习是一个有稳定ID的**研究路线**，包含「最初的问题→选取的官方来源→读到的关键机制→我和Codex的独立推理→反例/疑点→与ClimateOS关系→下一道问题」。保存问题与认知变化过程，支持后续增补而不覆盖早期错误版本。
- 结构化源登记：`project_id, institution, kind, canonical_url, last_checked, publisher, source_version, exact_section, accessibility, access_date, license/reuse_basis, evidence_status, excerpt_budget, source_hash_if_legally_retained, related_questions, claims, counterclaims, notes, next_step`。
- 状态清晰：`DISCOVERED / SOURCE_READ / OFFICIAL_VERIFIED / INTERPRETATION / CANDIDATE_REUSE / TECHNICALLY_TESTED / BLOCKED`。来源可访问≠软件可安装≠模型已运行≠许可自由再分发≠有正式合作。
- 不把联合国整篇报告、付费材料、受版权保护图表/图片或专有源码直接复制存仓。保留**原文链接、少量可合法引用的片段、原创中文解说、自己画的示意图、可公开的结构化事实**；能确定开放许可并符合署名要求的图片才复用，否则原创SVG和自制图。尊重robots/429和公开服务速率限制，不使用隐蔽抓取或凭证绕过。
- 个人学习笔记：本地可保存/导出/导入（若使用浏览器本地存储，显示本地数据丢失风险和明确备份）；公开发布版不泄露个人私有笔记、旧版EcoEngine或Council数据。若将来需要账户/云同步，另行批准。
- 可扩展的路径索引/断点`NEXT_SESSION.md`，每轮可看见**哪些机构已看过、实际读懂了多少、还有哪些问题**，区分工程功能验收和真实知识阅读深度。

## 5. 网站的用户体验（这是重要验收项）
用户喜欢**深色底、白字、绿色点亮、大字号、Slides式、一屏一个主题、不要长滚动**。这次要形成可探索的**Earth Science Route Map / Knowledge Garden**，不是行政三栏Dashboard：
- 首页：一张读得懂的交互知识路线图：世界观测数据 → 科学模型 → 模型耦合 → 环境关系 → 未来情景/决策。重点是“有哪些机构帮我们完成哪一步”和“我今天最想问什么”。
- 按任务分区的5条学习路线：**观测 / 地球模拟 / 耦合与标准 / 科学证据与评估 / 公共行动**；点击机构或项目站点进**图文说明大卡片**，带入口按钮链接原站、原始来源、简明解释、时间线和“与我的ClimateOS有什么关系”。可用示意图、原创SVG动画或交互关系演示帮助理解，但不得把概念动态图冒称真实模拟或机构官方图。
- 「跟着一条问题学习」：点“我们怎样知道一片土地正在变干？”或“全球模拟怎样进入我家乡？”逐层展示哪个机构/数据/模型能帮我们回答，何处需要科学谨慎。至少一条真正可交互的从问题到来源的完整路径。
- 「学懂了什么」：个人注释、提出疑问、证据对照、复核状态和知识图随学习版本累积。和Council Atlas只**视觉方法相似**，数据/路由/owner权限完全独立。
- 网页手机390px/桌面1440px实测能使用；键盘、焦点、高对比、prefers-reduced-motion、文字替代与链接均可用；不可只展示静态Screenshot或无法点击的卡片。站内图片源可授权，标明来源；不要伪造官方背书。
- 做成**用户确实愿意反复打开的知识工具**：无需云账户的原型、查来源、筛机构、沿路线深读、书签/笔记、学习进度和复盘，主页不堆长报告。

## 6. Codex必须真正完成的第一阶段交付
**工程＋知识内容两个验收门都要通过**：
1. `apps/earth-science-expedition/`：可运行的网站（README启动方式、实际页面/交互/移动端）和独立数据schema；至少5份具原始官方出处、实际阅读内容的中文机构档案；至少2份深度机制解释（含流程图、关键限定、与ClimateOS的具体代码/功能比较）。至少一条用户问题交互路线能从问题进入官方资料/模型，再到“已知/未知/如何试”。
2. 学习研究目录 `docs/research/world-science-expedition/`：`TASKBOOK_ZH.md`、`SOURCE_REGISTER.json`、`CLAIM_LEDGER.json`、`RESEARCH_QUESTIONS.md`、`MECHANISM_COMPARISONS.md`、`FOUNDER_LEARNING_NOTES_ZH.md`（区分Founder事实和AI草稿）、`RIGHTS_AND_ACCESS.md`、`LEARNING_ROUTES.json`、`QA.md`、`NEXT_SESSION.md`、`CRP_HANDOFF.md`；材料要对应实际读到的来源，不写“已经完整读过联合国所有报告”。
3. 一项**真正可复算的技术学习**：优先BMI↔ModelPort接口差异及最小相容适配的独立测试（只对公开模型接口，不改PR152/155物理源码），并明确“接口接通”不等于“物理过程有科学许可”；若研究优先发现其他更有意义的可执行小实验，可提同等证据/成本的替代。
4. 浏览器真实验收：桌面1440×900+手机390×844，逐页打开机构卡、官网链接、关系节点、笔记、回退、直接链接/刷新、来源展开、键盘；导出截图与可复现日志。所有外部链接保留原出处，断链显式BLOCKED；不能用页面存在就称“内容全部已读”。
5. 首批**最多6项目/25个官方原始页面，≤20分钟一批自动下载/测试运行，无付费API/大量模型安装，允许小规模合法公开资料。** 信息不够的项目保留研究问题和访问缺口，不无限扩张。工作不因某个数据API 403而全停。
6. 真实源码、内容证据、截图、自动/浏览器测试、完整版权/隐私检查提交本分支，创建**独立stacked Draft PR**，base为 `research/climateos-adaptive-earth-relations-runtime-001`；附 R/D及GitHub Actions CI与下一轮5个优先问题。PR保持Draft、不得合并或部署到现有用户站点。Founder验收后再决定个人站点发布形式与第二研究批次。

## 7. 反偏航
- 不能只搜集机构Logo、静态链接和AI-generated宣传文案；必须讲清机构层次、为何存在、实际机制与可复用边界。
- 不能仅实现华丽页面而没有真实逐条官方证据；也不能只生成几十份MD文件而没有可操作的网站。
- 不以WHO/UN/科研机构名称做虚假合作或科学背书；不混淆`WESR`数据平台、`GEO-7`报告、`WIS2`交换、`ERA5`再分析、`DestinE`数字孪生、`ESMF`连接器与`BMI`接口。
- 不抓取受限或未许可图文、不开付费账户、不复制原站全部报告。
- 不碰Council owner-only PR#130、私人EcoEngine v200、其他受保护站点，不篡改PR155科学状态，不把学习站误当ClimateOS已获现实科学认证。
- **最重要：每一条路线都留下“我们为什么去看它、今天学懂了什么、还有什么没有懂、明天想追问什么”。**

这轮应让 Founder 感受到真正去“联合国和世界实验室里走了一圈”，而不只是让AI多写一篇总结。先完成首批可运行的网站和深读内容，再申请下一阶段。
