# ClimateOS / WCOS → Council Strategy & Operations Intelligence
## Founder V1.7 · 80 项连续工程总任务书

**编制日期：**2026-10-30（澳大利亚悉尼时间）  
**授权性质：**公开资料、独立研究、合成数据、网站与软件工程的连续实施计划；不授权 Council 内部数据外传、代替主管审批、费用采购、外部公开部署或合并 PR。  
**主工程：**`simon947161/eco-agent-system`；Draft PR **#130**；`feature/public-strategy-atlas-web-mvp-20261029`。  
**独立私有专业系统：**`simon947161/cooma-water-compliance-workos`（WCOS）。核验其仓库权限为 private，但**不得据此推定有权读取/复制其中受保护数据**。  
**基线：**PR #130 已有 V1.6 E0–E10 的路线图、127 内容项、源登记、递归遍历、分层核算、审核/版本、冲突处理、暗线发现和浏览器测试；最新远端 HEAD 每次启动重新查询，不硬编码。本计划建立新一轮 **COI-001—080** 编号，不与既有 ClimateOS 任务号冲突。  
**第一原则：**不是重新开发一个漂亮网页，而是让战略、工作、专业知识、年度安排、工作量与证据连接成持续生长、可核算、可审核的实际工作系统。

### 一、Founder 的目标与使用者

1. **上层**：CSP、LSPS、DP、OP、Resourcing Strategy、法规、财政与年度报告的真实来源、条款、时间/地域适用性和多路径逻辑。CSP→DP→OP 属于正式 IP&R 执行链；LSPS 侧重土地利用，与 CSP 相关但不是任意条款的自动法定父子关系。
2. **中层**：Council Strategy & Operations Intelligence（CSOI），负责目标→运营计划→年度/季度/月/周/日→任务→执行→证据→资源→工作负荷→报告之间的联系。
3. **底层**：继续复用已有 WCOS（LTW、Backflow、Annual Calendar、Guideline Reader、Decision Navigator、Planning Queue、Field Brief、Execution Log、Annual Report）作为专业工作的基线。PHE 其他领域先由官方公开资料构建知识骨架；创始人目前尚未全面掌握这些领域，不应要求创始人先提供内部 SOP 或真实场所资料。
4. **管理辅助**：帮助 Michele 降低规划、准备、核对、会议和报表负担，但不冒充她、不替她决策、不默认读取其工作邮箱/日历、不自动发送或执行 Council 事务。
5. **产品形态**：以有机线路网络为起点的多页面网站。路线、交汇、暗线及每个站点背后的递归内容是主角；每项信息可继续深入子项，并能逆向追溯。单屏、手机、左右双屏都应可用；非传统三栏 dashboard。

### 二、六级数据层与独立权限边界

- **L0 来源/原始记录**：官方公开文件或保留在 Council 授权环境中的业务原件；记录来源/日期/许可/保密级别。
- **L1 清洗与标准化**：场所、物业、装置、批准、业务活动、地区、时间、工作事件的规范 ID 与去重、质量记录。
- **L2 规则与证据**：法定义务、Council 已公开政策、观察、反证、缺失事实，以及 `RULE / EVIDENCE_INFERENCE / DISCRETION / FORMAL_DECISION` 四类不同判断。
- **L3 可复验核算**：工作量、风险、成本、数量、基准/目标/实际，保留公式、分子分母、单位、期间、地域、计算版本与输入收据。
- **L4 管理汇总**：通过覆盖范围/质量/权限检查后的年度、季度、月度、专项服务及资源负荷分析。
- **L5 战略/可共享输出**：经正式授权的高层指标或论证，用于研究对齐 CSP/DP/OP/LSPS 和受控报告；不等于修改 Council 官方文件。

**权限是另一条正交维度。** `PUBLIC / PERSONAL_PRIVATE / COUNCIL_PROTECTED / APPROVED_RELEASE` 不随 L0→L5 自动降低保密级别。小样本汇总仍可能泄露身份；不能因为“匿名”“高层指标”就直接提交公开 GitHub。默认只允许公开权威资料、授权短摘录、合成样例和个人独立构想进入公开 Atlas。

### 三、产品页面与工程合同

- `/atlas`：全屏路线总览、目标/计划/法规/工作/数据关系、暗线与交汇。
- `/knowledge/:id`：任意深度的章节、条款、表格、研究解释、前后文和证据，保留递归父子/跨枝导航。
- `/strategy`：CSP/LSPS/DP/OP/Resourcing Strategy 与责任、版本、效力、执行关系。
- `/domains/wcos`、`/domains/phe`：专业知识入口；前者为受控抽象桥接，后者先是公开法规知识包。
- `/operations`：项目、工作包、任务依赖、工作卡、风险及审核门槛。
- `/calendar`：Mission → Operational Year → Quarter → Month → Week → Day → Task → Field Brief → Execution → Follow-up → Annual Report。
- `/metrics`、`/resources`：分子/分母、物理量、人力/设备、预算/实际支出、指标证据、场所与地区可比性。
- `/sources`、`/discovery`、`/audit`、`/coverage`：资料准入、候选连接、反证、版本哈希、冲突及覆盖/缺口。
- `/assistant`：Michele 辅助台，仅起草和准备事项，任何 Council 真实动作都需明确授权及人工复核。

这些是功能性导航合同，不要求引入付费后端；可使用现有静态客户端路由和一个源数据模型，但每个 URL/页面必须能打开、分享地址、回退/前进、保存可公开状态，并通过真实浏览器验收。**网站是多个互相关联的工作空间，不是一个首页加几十个虚设菜单。**

### 四、80 项任务：8 Pack × 10 项

#### Pack A / COI-001—010 — 既有资产、边界和架构
**目标：**既利用 V1.6，也保证 WCOS 和 Council 数据不受损。

- **COI-001** 核验最新 PR #130、NEXT_SESSION、V1.6 测试与最新资料访问记录；形成 DONE/PARTIAL/TODO/BLOCKED 基线矩阵，避免重写已有系统。
- **COI-002** 只在有权访问的范围清点 WCOS 已有 Annual Calendar、Guideline Reader、Premises/Task Card、Planning Queue、Execution Log、Annual Report、Decision Navigator；记录接口而不导出受保护内容。
- **COI-003** 明确 Atlas Core、CSOI Operations、WCOS Adapter、PHE Public Pack 的模块所有权、ID 边界和依赖方向。
- **COI-004** 建立公开/个人私有/Council 受保护/获批准发布四层安全分类与跨层默认拒绝策略。
- **COI-005** 确立 Council 工作系统为其业务记录的权威来源，Atlas 是独立研究/工作支持系统，不能自行发出官方结论。
- **COI-006** 建立来源许可、版权、员工/客户 PII、商业机密、小样本反识别、存储/截图/导入/导出检查。
- **COI-007** 完成统一逻辑 ID、版本 ID、时空范围、机构权限、事项、来源、事件、证据的类型契约和迁移计划。
- **COI-008** 提交多页面站点架构和真正可运行的页面骨架，保留路线优先、原 127 项和原快照兼容。
- **COI-009** 制定每一 Pack 的软件能力/公开资料覆盖/人类审核准入三重验收状态与测试矩阵。
- **COI-010** 完成基线、权限、页面导航和回归实际测试；提交 Push + NEXT_SESSION 后**立即继续 Pack B**。

#### Pack B / COI-011—020 — 公开 CSP/规划/PHE 法规来源
**目标：**先依靠权威公开知识构建关系，不要求创始人先提供内部资料。

- **COI-011** 从官方目录独立核验现行 CSP 2035、DP 2025–29（2026 修订）、OP 2026–27、资源战略/财务/资产计划和年度报告的具体版本与日期。
- **COI-012** 收集官方 LSPS 2020 与适用 LEP/DCP/SEPP 的法规、地图、地域和生效版本；不得把战略一致性推为自动法定执行关系。
- **COI-013** 建立可检索 Source Register：URL、标题、出版社、版本、采用/生效/提取时间、地域、复用权、原始文件哈希、页/表/条款定位。
- **COI-014** 运行分阶段 intake：目录→合法获取→字节验证→内容/表格提取→确切锚点→版本范围→人工待审；不能自动升格 ADMITTED。
- **COI-015** 在有确切证据时建立 CSP→DP→OP 类型化关联、工作/资金条目，并显示没有关联的战略目标。
- **COI-016** 将 LSPS→土地使用行动→LEP/DCP 作为独立空间规划路径，检查地方旧 LEP、日期与地域，保留未知。
- **COI-017** 建立 NSW Food Authority、NSW Health Public Health、NSW LTW Guidelines、饮用水/Backflow、OSSM 的公开权威资料登记。
- **COI-018** 把每一法规/指引拆成义务、前提、适用对象、风险、例外、来源与人类裁量点，不编 Council 内部程序。
- **COI-019** 建立可实测公开语料覆盖率和缺口队列，区分目录、字节、提取、条款、复用权、准入和法定审核。
- **COI-020** 交付来源支持的真实知识页、版本/页码追溯与负例测试；即使部分 PDF 未获许可，也继续非受阻研发并进入 Pack C。

#### Pack C / COI-021—030 — 数据分层、质量、来源与权限
**目标：**把逐日累积的数据变成可安全复用的战略证据，不能靠一个“清洗完成”按钮。

- **COI-021** L0：支持授权原件与公开原文的记录身份和版本，敏感原件原地保留，公共 GitHub 仅存合法元数据与短摘录。
- **COI-022** L1：对象与事件 ID 清洗，支持同物业多个业务活动、不同场所/水连接点/装置及历史身份去重。
- **COI-023** L2：证据、规则、观察、研究推断、人为裁量、正式决定分栏保存，含反证与 UNKNOWN。
- **COI-024** L3：计算公式、计量单位、时空口径、分子/分母、输入版本与收据绑定，变动后必须失效重算。
- **COI-025** L4：管理统计有明确定义的分母、抽样覆盖率、数据质量和权限标记；“未检查”不等于“合规”。
- **COI-026** L5：生成审批待办与可分享数据审查流程；研究版 CSP 关联与 Council 正式报送保持不同身份。
- **COI-027** 所有跨层升格要有质量核验、责任角色和撤回/重算事件，权限升格另有独立审查。
- **COI-028** 自动检测缺失、重复、错单位、时间地域不一致、来源冲突、过期法规、错误统计分母及重复计数。
- **COI-029** 将层级数据并入现有 Atlas 内容寻址、事件链、快照、独立复验和可兼容迁移；不可创建第二正式图谱。
- **COI-030** 实测拒绝未授权公布、修订回放、历史兼容和跨层来源追溯；提交并继续 Pack D。

#### Pack D / COI-031—040 — WCOS、LTW、Backflow 与 Annual Calendar 桥接
**目标：**现有专业系统是输入底座；上层借它的结构与经过授权的指标，而非搬运工作场所数据。

- **COI-031** 读取已授权的 WCOS 技术契约，映射 Annual Calendar→Month→Week→Day→Task/Premises→Field Brief→Execution→Follow-up→Annual Report。
- **COI-032** 写只读、默认不传真实资料的 WCOS Adapter，首个示例只处理模拟场所、公开规则、合成工时和已授权的非识别性汇总。
- **COI-033** 接入公开 NSW LTW 2021 Guidelines 的章节、分类 A/B/C/S、排放类型、设施、批准及 concurrence 等规则，保存准确来源和适用条件。
- **COI-034** 建 LTW 实务链：登记/初筛→补件→分类/许可与 concurrence 证据→现场→预处理→监测→整改/复检→关闭/报告；禁止 AI 作正式审批。
- **COI-035** 以 Council 公布的 Backflow 要求建水连接点、风险级别、装置、到期检测、缺陷维修、合规状态、通知和结案模型。
- **COI-036** 将 Backflow 年度检查/准备与日历的排程逻辑结合，按真实装置类型和适用条件计算到期，不对所有物业默认同样义务。
- **COI-037** 将 WCOS Decision Navigator 的 RULE / EVIDENCE_INFERENCE / DISCRETION / FORMAL_DECISION 四层接入治理/审核结构。
- **COI-038** 实现“同一模拟餐饮场所可能涉及 Food/LTW/Backflow”条件化交叉检索，负例确保不是所有场所都默认需三项审批。
- **COI-039** 开发安全只读汇总：合规监管对象、应检数、已检数、复核、工时和风险；必须标来源/分母、抑制小样本数据。
- **COI-040** 运行原 WCOS 和 Outlook Calendar 不破坏性兼容演练；不触碰真实同步、私有正式版本或用户实际排班，然后提交继续 Pack E。

#### Pack E / COI-041—050 — PHE 公共知识包
**目标：**Codex 自己学习公开知识；先建设通用结构，任何本地分工/内部数据都标待核实。

- **COI-041** 列出 Council PHE 的公开职能及 NSW 不同主管机构的责任；分开法定权力、Council 公开政策、研究观点、当前 SMRC 内部分工未知。
- **COI-042** Food Safety：Food Act、Food Regulation Partnership、登记/风险、卫生检查、投诉、复检、培训、处罚/决定审查与来源。
- **COI-043** On-site Sewage：安装/运营批准、系统类型、风险、维护、现场检查、失败整改与地表水/土地联系。
- **COI-044** Public Pools & Spas：场所通知、消毒/水质监测、记录与检查、缺陷/复检、相关公共卫生义务。
- **COI-045** Cooling/ Warm Water Systems：登记、风险管理、维护与检查、主管部门和法定通知范围；职责未确认的地方明示 UNKNOWN。
- **COI-046** Skin Penetration：法规适用场所、卫生检查、通知/整改、年度法定报告统计依据。
- **COI-047** 环境卫生与保护、投诉、噪声/污染等模块：按现行法定机构权限区分 Council、EPA、NSW Health 等职责。
- **COI-048** 建“物业/活动/设施/风险/法定条款/检查活动/整改/结果”通用概念图，跨 PHE/WCOS 查询但不复制真实客户。
- **COI-049** 用公开知识与明确合成的业务对象，创建至少五条有条件判断与反例的多级 PHE 工作链，并核验页码/效期/地域。
- **COI-050** 交付真实可点击的 PHE 目录、领域子站、法定来源、工作流、可学习案例和未验证事项面板；进入 Pack F。

#### Pack F / COI-051—060 — 工作量、资源与战略数据核算
**目标：**把基层数量逐级清洗为可解释、能为年度计划/资源战略提供参考的管理信息。

- **COI-051** 为每项监管服务明确统计分母：注册对象、应审批对象、应检对象、风险组、检测到期装置、检查事件、未关闭问题分别计数。
- **COI-052** 建法定/政策检查需求与风险调整公式，把应该做、计划做、实际做、逾期和不能确认对象分开。
- **COI-053** 核算单项工作准备、现场、行程、文书、复检和行政工时；实测/假设/估计数据单独标记。
- **COI-054** 对年度计划推导人员/技能、日程、车辆、培训和设施资源需求，不将估计小时自动当作实际财政支出。
- **COI-055** 建财务账本：批准预算、修订预算、承诺款、实际支出、费用、资本/运营、财政年度与成本分摊。没有来源不得填 Council 金额。
- **COI-056** 建物理环境账本：面积、人口、装置、物业、供水量/污水量/容量、能耗、碳排放；存量、流量、强度和地区边界严格区分。
- **COI-057** 建结果账本：完成检查不等于消除风险；分别衡量工作量、覆盖、问题关闭、服务/环境结果、独立核验和因果归因限制。
- **COI-058** 仅当文件中有可证实关系时，把监管活动、OP/DP 承诺、CSP 目标及资源战略连接；空间相关的才与 LSPS/LEP/DCP 关联。
- **COI-059** 实现反查：从检查、成本、某一面积、绩效/时间序列回到数据来源、公式、工作包及有证据的战略相关性；显示 UNKNOWN 中断点。
- **COI-060** 以 29.9 t CO₂e/人（非碳价）、水务合成样例、土地合成样例、监管应检覆盖与重复分母反例，运行严苛核算/归因测试；进入 Pack G。

#### Pack G / COI-061—070 — 年度日历、任务系统与 Michele 辅助台
**目标：**让主管少做重复查表、准备会议和复核汇总，保留她的管理责任与决定权。

- **COI-061** 实现 Mission/Project→Operating Year→Quarter→Month→Week→Day→Task→Work Item→Field Brief→Evidence→Follow-up→Report 的可导航对象与父子链接。
- **COI-062** 复用 WCOS Annual Edition 年度总览、月份工作、Planning Queue、Execution Log 与 Annual Report 的概念契约；不能直接覆写现存 Excel/Outlook。
- **COI-063** 给每个任务记录来源类型：法定义务/公开运营目标/经授权分配/本人学习/研究建议；角色与审批证据不可猜测。
- **COI-064** 构建循环事件和风险提示：检查到期、设备检测、复检/整改、季度报告和年终回顾；错误/冲突循环有检测和解释。
- **COI-065** 完整工作卡：依据、适用条件、工作量、预计时长、附件状态、下一步、人为裁量、复核责任、证据和版本历史。
- **COI-066** 年度→季度→月→周→日编制与实际执行/回顾双向导航，实际数据不足时只显示计划或 UNKNOWN，不伪报完成。
- **COI-067** Michele 辅助台草案：本周关注、监管风险、待审批准项、资源瓶颈、材料缺口及建议，所有信息基于合成/公开或另行获准来源。
- **COI-068** 会议准备/回顾功能：议题、准备问题、决策待确认、跟进行动、责任角色、来源、截止时间；未经确认不能标“主管同意”。
- **COI-069** Outlook/日历接入默认只读/模拟；实际读写、提醒、邮件、团队共享、账号授权分别需要明确权限、操作确认和审计日志。
- **COI-070** 在真实网站完成从年度总图进入某月/周/工作卡、下钻资料/法规/证据，再向上追踪 OP/CSP 的端到端桌面/移动测试；继续 Pack H。

#### Pack H / COI-071—080 — 完整多页面站点、双屏、审计和验收
**目标：**形成长期可演化的整套工作网站，不以一张路线图或三条合成案例结束。

- **COI-071** 保持有机网络为首页，路线长度不同、分叉/交汇/隐性候选连接有类型/证据，布局稳定且可聚焦，不回到三栏管理仪表板。
- **COI-072** 建多个真正可工作的专业和计划页面：CSP、LSPS、DP/OP、资源、WCOS、Backflow、LTW、Food、OSSM、其他 PHE、Calendar、Metrics、Sources、Audit。
- **COI-073** 每个合法节点与子项支持多层递归、章节/工作包/成本/证据/版本/缺口的下钻和反向返回，不能限制为固定六级，也不能用虚构文本凑满。
- **COI-074** 统一搜索、按年度/地区/法规/来源/工作/单位过滤、跨路径比较、问题导航和解释性候选暗线；同时具备线性文字替代。
- **COI-075** 双屏模式：主屏线路图、副屏独立查看工作卡、日历、条款、核算和审核；普通单屏与手机有同等功能，不需要双显示器。
- **COI-076** 实测 390px 移动端、16:9、21:9、32:9、键盘/触屏、低动效、可聚焦上下文、长表分页和基本读屏无障碍。
- **COI-077** 建单独覆盖量表：软件能力、公开语料覆盖、关系审核、数据质量、实际结果 KPI 五者不能合并成虚假 100%。
- **COI-078** 运行隐私/权限/恶意来源文本、HTML 注入、JSON 导入、记录反识别、版权、权限越界、虚假官方批准的负例测试。
- **COI-079** 跑全部 Node、真实 Chromium、快照/不可变历史/导出导入、并发编辑、15/127/60/200/1000/10000 合成负载及许可范围内真实资料，保存日志和截图。
- **COI-080** 交付 Founder 验收报告、来源/权限缺口、工作链与定量验证、可用页面清单、软件与真实资料分别计分、下期目标；保留 Draft PR，不部署/合并。

### 五、规定的五条端到端业务演示

1. **LTW / Backflow：**官方规则→模拟监管对象与适用条件→年度/月/周任务→现场准备→证据/人为决定→跟进→工作量/资源分析→经证据支持的 OP/CSP 研究联系。
2. **同一虚构餐饮物业：**通过独立适用条件判断 Food、LTW、Backflow，各自的必要性、负责人角色和法定来源；必须有不适用反例，不能简单把三个监管标签全部打勾。
3. **PHE 专业模块：**OSSM 或 Public Pool 等从公开法定义务一路展开到合成工作卡、资源负荷与管理指标，并列出本地操作信息缺口。
4. **财务/环境：**从一项被允许使用的预算/公开指标反向核验原始表格、期间、单位、计算和声明限制；没正式数据时用合成量并保持 UNKNOWN。
5. **年度 Calendar：**从总目录→年度→月份→一周→一天→一项任务→准备/执行/证据→年度报告，再回到战略目标；进度不能靠时间流逝冒充工作完成。

### 六、连续执行、开发调度与“不要做一口就停”规则

这是**八个连续任务包，不是八份需要用户每次重新授权的独立任务书**。在 Codex 当前可用会话中，每完成一个 Pack 的边界验收：运行真实测试、检查敏感资料/权利、commit+push、更新 `NEXT_SESSION.md` 和机器可读任务登记 `COI_TASK_REGISTRY.json`，**立即启动下一个 Pack**。已有功能核验通过可标 VERIFIED 并继续，不能重复改造浪费额度；未完成/受阻项按 PARTIAL/BLOCKED 追踪，不得因某一个官方 PDF 或 Council 权限未开通就停止所有无关工程。

项目控制单元：`Pack → Task → Evidence → Test → Git SHA → Next action`。任务状态只允许 `TODO / IN_PROGRESS / VERIFIED / PARTIAL / BLOCKED`。每个任务记录依赖、输入、输出文件、实际测试命令、版本、公开/私有分类、阻碍责任和下一动作。**任务不等于模型额度；不能保证云任务跨会话自动执行。** 额度/时间/权限中止时必须先完成安全的 GitHub 交接，下一个 Codex/Work 会话由用户手动启动后自动从清单恢复，无需用户重复贴前文。

**单一写入者**对 PR #130 持续推送；并发执行者先核验最新 SHA，禁止 force push 和覆盖远程新提交。个人私有 WCOS 仓库只可在明确独立授权、权限允许的开发环境做接口/测试变更；不得把 Council 内部材料复制到公开 Atlas、GitHub 问题、截图、日志或 AI 提示。

### 七、验收判据、风险与最终交付

- 软件验收：真实可打开的多页面网站、路线/递归、工作卡、Calendar、计算/证据、版本审计和治理辅助，具备测试、截图与导入导出。
- 专业验收：WCOS 原有工作链与数据结构不被破坏；PHE 先以公开来源为准，不把未知本地职能称为已核实。
- 定量验收：明确分母、统计期间、地域和适用范围；分别核算监管覆盖、工时、风险问题关闭、资金、物理与环境结果，并拒绝无法证明的关联。
- 资料验收：如实报告“目录发现 / 原件验证 / 条款锚定 / 当前版本 / 权利 / 授权审核”的各自比例；代码完成不等于官方资料已经准入。
- 管理验收：Michele 辅助台能草拟工作安排、会议资料和待审问题，但任何正式决定/工作账号操作均不得代替人类授权。
- 治理红线：无新增采购、无主站部署、无主分支或 PR #129 修改、无 Council 非公开材料导出、无自动批准、无虚构 Council KPI/碳价/财务支出。遇到高风险权限事项暂停相关动作，继续其余获准开发。

**完整系统完成标准**不能由代码覆盖率、80 条任务标题、15 个测试文件、漂亮截图或合成数据量证明。系统能力、公开资料覆盖、正式审核准入必须分别给出 PASS/PARTIAL/BLOCKED，真实 Council 集成须另行明确批准；没有批准就保持合成/公开研究版，继续提高软件质量。

### 八、Codex 本次开工指令（可复制的精简版）

> Continue the full Council Strategy & Operations Intelligence programme from the latest remote GitHub PR #130 and `NEXT_SESSION.md`. Read the **entire** Founder V1.7 80-task plan `CSOI_V1_7_80_Task_Master_Plan.md` and the Founder V1.6 Atlas taskbook. Execute COI-001 through COI-080 in 8 sequential engineering packs, skipping only functions proven already implemented and tested. Do not stop after one webpage, one synthetic scenario, or a research document. Preserve existing route-first Atlas, 127 content items, complete V1.6 engineering, and WCOS as a separate private professional system. Build public-first PHE reference modules, a safe WCOS adapter, L0–L5 evidence/data transformation, quantification, an operational-year→month→week→day→task Calendar, and a draft-only Michele assistance workspace. Every pack must ship real code, tests, browser evidence and GitHub commits, update `NEXT_SESSION.md` and `COI_TASK_REGISTRY.json`, and continue to the next pack in the same active session. No nonpublic Council data, paid service, autonomous Council decision, deployment or PR merge. Truthfully report any actual access/security/review blockers; finish other safe work rather than halting the whole programme. Treat the latest `NEXT_SESSION.md` as the source of truth for whether the newly tested official network access is technically available; do not confuse a version-number guard with an observed CONNECT failure.

### 九、公开来源起点（需 Codex 每次核验最新版本）

- NSW Office of Local Government，综合规划与报告：https://www.olg.nsw.gov.au/councils/policy-and-legislation/integrated-planning-and-reporting
- Snowy Monaro Council，综合规划与报告：https://www.snowymonaro.nsw.gov.au/Council/Integrated-Planning-and-Reporting
- NSW Planning，战略规划/LSPS：https://www.planning.nsw.gov.au/the-planning-system/environmental-planning-and-assessment-act-1979/strategic-planning
- NSW Water，液体贸易废水指南：https://www.water.nsw.gov.au/our-work/local-water-utilities/liquid-trade-waste
- Snowy Monaro Council，LTW：https://www.snowymonaro.nsw.gov.au/Environment-Waste-and-Weeds/Environmental-and-Public-Health/Public-Health/Liquid-Trade-Waste
- Snowy Monaro Council，Backflow：https://www.snowymonaro.nsw.gov.au/Water-and-Wastewater/Water-Supply/Backflow-Prevention-Program
- Snowy Monaro Council，公开监管领域：https://www.snowymonaro.nsw.gov.au/Ranger-Services
- NSW Food Authority，Food Regulation Partnership：https://www.foodauthority.nsw.gov.au/retail/food-regulation-partnership
- NSW Health，Public Health legislation：https://www.health.nsw.gov.au/phact/pages/default.aspx
- NSW Health，Council reporting：https://www.health.nsw.gov.au/environment/Pages/local-government-authority-reporting.aspx

