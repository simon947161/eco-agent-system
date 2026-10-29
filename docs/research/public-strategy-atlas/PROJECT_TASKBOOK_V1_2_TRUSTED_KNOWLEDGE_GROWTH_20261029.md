# ClimateOS Public Strategy Knowledge Atlas
## Founder 工程与研究任务书 V1.2：区块链式可信知识生长网络
**编号：** CLIMATEOS-ATLAS-R0-K-20261029  
**研究截点：** 2026-10-29（Australia/Sydney）  
**状态：** RESEARCH-ONLY / DESIGN HOLD / FOUNDER GATE REQUIRED  
**归属：** ClimateOS Public Strategy Knowledge Atlas；兼顾 WCOS、Evidence Passport、ECOChain 与 Council Strategic–Operational Intelligence 的可复用知识关系思想。  
**仓库/隔离分支：** simon947161/eco-agent-system / research/public-strategy-atlas-20261029  
**前序任务：** [PROJECT_TASKBOOK_V1_20261029.md](PROJECT_TASKBOOK_V1_20261029.md) V1.1；本文件在研究范围、架构目标和 R0 决策门方面优先，V1.1 保留为历史事实，**不可因本任务自动启动 A/B/C/D 编码或部署**。

## 0. Founder 最新战略判断（必须作为研究命题，不要降格成 UI 插件）

Founder 要求：知识关系的生长不是单纯绘制节点连线。每条知识“通路”应能记住自身形成过程、源数据、审核与修订；新资料进入后，允许从时间、地域、主题、条款、制度、组织角色、事件、测量指标和其他线索找出先前未显露的关系（“暗线”）；暗线须能追溯、质疑、审计，帮助人形成认知与判断，而不是让 AI 决定事实。整个系统从最小可信数据单元起采用**区块链式组织思想**：内容寻址、哈希关联、不可静默覆盖的历史、可选择的数字签名与独立核验。研究不预设必须发行代币、部署共识网络或把资料公布到公链。

**修正之前的建议：** 密码学可验证性与知识变更历史不是“不需要考虑的未来插件”，而是从 R0 开始的架构核心要求；但“采用区块链式组织机制”与“立即运行区块链网络”是两个不同的选择。研究必须实证比较，不能教条式禁止或强制上链。

**愿景：** 公开战略文件 → 可寻址条款和证据 → 可信关系断言 → 多路径检索与暗线候选 → 人工复核 → 可重现的认知/决策依据 → 证据与关系持续版本化生长 → 可独立审计的知识体系。

## 1. 必须明确的技术语义

1. **每个字节都可追踪，不等于每字节一个区块。** 保留允许保存的原始二进制字节哈希，按可重复的分块策略形成内容寻址单元；记录 chunk strategy/version、byte-range、encoding、parser version、文本坐标、页码/条号、父对象版本。文件变化需形成新内容标识。给定完整快照应能重算逐块及根哈希；无法取得原始字节时必须标为 METADATA_ONLY，不得假装通过原字节验真。
2. **独立业务身份与内容身份。** 相同的策略目标跨版本保留稳定逻辑 ID；具体文本版本/数字化快照使用不可变内容 ID（digest/codec/version）；两者不能混用。相同内容经不同扫描、OCR、裁切、JSON 序列化可能哈希不同，必须固定规范化规则、输入字节与编码，不承诺语义相同必然同哈希。
3. **关系是可签署/可争议的独立声明。** 不只哈希文件，连 “CSP 6.1 支持 OP 某行动” 这样的关系也有 assertion ID、提出者、证据集合、版本/时间/地域、关系语义、依据、审核状态与反证。更改关系需新断言或 supersede/retract 事件；旧记录仍可审计。
4. **版本图和语义关联图分开。** 哈希链/事件链/Merkle DAG 的节点必须满足密码学可验证结构；政策知识图允许双向、多对多、跨引用及环路。**不能把有环的语义关系网直接称为 Merkle DAG**；应用独立 content objects / events + semantic links/index。
5. **可验证≠真实≠适用≠执行成功。** 文件来源校验、签名完整性、审核资质、条款的法规效力、科学因果与绩效结果各自独立；自签名、私有本地哈希不等于官方签章、可信第三方证明或公开透明登记。
6. **不可篡改是有条件的。** 本地 hash chain 可揭露事后修改，但如果攻击者能同时改全库及根锚点，就不能证明没有改动。必须研究独立锚定、备份、不同主体复核、受信任的签发/透明服务。可校验历史不应妨碍合法更正、撤回、隐私删除与密钥撤销；更正采用新事件，敏感内容不进永久公开账本。

## 2. 可对照的官方技术路径（先研究，再选择）

- **W3C VC Data Model v2.0**（Recommendation 2025-05-15）：https://www.w3.org/TR/vc-data-model/  
  用于研究 issuer、holder、verifier、credential status、evidence 的角色和声明语义。
- **W3C Securing Verifiable Credentials using JOSE and COSE**（2026-10-13 版）：https://www.w3.org/TR/2026/REC-vc-jose-cose-20261013/  
  研究 JWS/COSE 签名、SD-JWT 选择性披露；不能声称已有 Atlas 密钥体系或凭证。
- **IETF RFC 9943 — SCITT**（2026-06，Proposed Standard）：https://www.rfc-editor.org/info/rfc9943/  
  研究签名声明注册、透明服务、可验证收据、独立核验；它并不保证签发声明的语义真实。
- **IETF RFC 9942 — 可验证数据结构和收据**：https://www.rfc-editor.org/info/rfc9942/  
  与 RFC 9943 同时评估，以免将“收据”误定义为任意日志文件。
- **IPFS/IPLD content addressing / Merkle DAG**：https://docs.ipfs.tech/concepts/how-ipfs-works/ 和 https://docs.ipfs.tech/concepts/merkle-dag/  
  研究 content ID、分块策略、哈希引用和离线验证；不默认启用 P2P 网络或把政策全文发布到 IPFS。
- **现有资产**：ClimateOS Evidence Passport、Run Receipt、文件/来源版本、Git 原子提交、WCOS 证据/法条与 R0 有机横向树；必须通过只读检索与真实路径证明，未找到记 UNKNOWN。

**技术比较矩阵必须至少有 4 种候选**：(a) 传统数据库+版本/哈希日志，(b) 内容寻址对象库+Merkle DAG+可复验索引，(c) b + 签名声明/SCITT 风格收据，(d) 权限链/公链上锚定的对照方案。按数据保密、抗篡改信任模型、离线可用、检索延迟、版本纠错、成本、可维护性、第三方审计和迁移难度比较。不能只比较“有没有上链”或把 ECC/哈希算法当作架构收益。

## 3. 数据模型研究：最小可审计对象

数据对象以**概念 schema 草案**交付，不要求当前实现和数据库迁移：

- SourceArtifact：publisher、original_url、rights/licence、retrieved_at、raw_digest?、download_status、content_type、scope、access_level。
- ContentBlock：stable logical ID、content ID、raw_bytes_digest、block offset/length、codec/canonicalization version、parent revision CID、text extraction method、section/page/locator、allowed excerpt、validation status。
- DocumentRevision：document family、adoption/effective/superseded dates、geographic jurisdiction、revision root CID、current_as_of date、revocation/supersession。
- KnowledgeNode：战略目标、LSPS、LEP/DCP 条款、DP/OP 行动、KPI definition、public evidence、synthetic case；区分 semantic ID 和 revision CID。
- RelationshipAssertion：source & target revision references、relation_type、issuer_type/claimant、evidence IDs、counterevidence IDs、confidence method（定性且可解释，非自动认定法律结论）、basis DIRECT_OFFICIAL / INDIRECT_RESEARCH / SYNTHETIC / UNKNOWN、valid_time、observed_time、region、review_status、signature_ref?、receipt_ref?。
- ChangeEvent：event_id、actor、operation ADD/UPDATE/SUPERSEDE/RETRACT/REVIEW/CONTEST、old/new CID、previous_event_hash、event timestamp、reason、authorisation evidence、signature/receipt status、idempotency。
- DiscoveryHypothesis：candidate_id、endpoints/path、algorithm/version、matched features、suggested relation、supporting/counterevidence、falsifier、review_status、created_at；一律 CANDIDATE/NOT_OFFICIAL，不能静默升为 DIRECT_OFFICIAL。
- AuditView：核验对象的链和收据、输入摘要、验证算法与结果、时间/地理有效性、签发者是否可信、证据断点、反证及已撤回关系。

**不将全文公开复刻作为默认目标。** 法规/政策 PDF 的引用要遵守许可、版权及源站限制；需要受限资料时只保存准许的摘要、链接和合法本地快照；缺失原始字节的材料不得标记完整性 VERIFIED_RAW。

## 4. 暗线发现：假设引擎，不是事实制造机

定义“暗线”为**尚无官方明确直接交叉引用，但经可解释的证据路径推测值得审查的候选关系**。示例：LSPS 的某地基础设施容量重点、CSP 的基础设施战略目标、公开 OP 的设施规划行动可能共享地点/时间/主题；这只能产生候选研究路径，不等于官方明确挂接，也不证明已经实施。

建议研究的检索通道：
- 直接文件引用/条款引用（可确证）
- 同一地区或地块的适用性（先校验行政区/有效日期）
- 共同主题/风险/资源/环境指标（受控词典与单位一致性）
- 事件与时间线（规划生效、修订、项目公示、审计发现）
- 不同部门或主体的公开角色定义（勿把人名关联当作利益或过错）
- 证据支持链与反证/冲突链（两个方向搜索）
- 相似条文的语义候选（LLM/embedding 仅用于排序建议，不能作直接条款证明）
- 逆向查询：从结果或疑问返回可能的战略、法律及运营来源。

每条候选须输出：检索入口 → 路径/匹配条件 → 所有证据锚点 → 版本/时点/地域 → 候选推断与明确限度 → 可证伪反例 → 人工审核状态。至少测试一例**语义很相近却因地理/时点失效而必须拒绝的假暗线**，及一例共享主题却没有可证事实的 UNKNOWN。

不得训练/输出无来源的管理者动机、内部责任归因或 Council 真实工作绩效。区分 discoverability（找到可能关系）、evidence relevance（证据相关）与 truth/legal applicability（成立/适用）。

## 5. Atlas UI 研究：原横向有机树延伸为可信知识“生长 + 追踪 + 反证”图

保持 V1.1 R0：双屏/超宽屏优先，普通单屏可用；固定稳定但长短不一的主枝和侧枝；灰色关系基线之上彩色进度填充；文字按需显示、证据抽屉、键盘/移动适配。本轮只做**静态结构草图与交互状态表**，不生成可运行网页。

在横向树上追加三种与进度分离的“可信关系”视觉层：
1. **证据根系**：节点/边下方可逆向打开来源块、文件版次、字节区间/页码、签发和审核链；选中关系后突出其依赖的所有证据块（可多父级）。
2. **生长历史**：时间轴沿可追踪的旧版本→新版本显示，新增/撤回/冲突的边有事件标记；不把线的几何长度变化直接解释为项目绩效。
3. **暗线候选**：未确认的跨枝路径以另一种虚线/微弱连接或“候选层”显示，用户主动打开才展开推荐理由、反证和审查选项。绝不能让新发现闪烁的漂亮连线被误认为 Council 官方决策。
4. **审计镜头**：同一条线点击切换“语义关系解释 / 来源版本 / 哈希完整性 / 第三方签名或透明收据 / 适用性 / 反证”。如果没有密码学证明，显示 NOT_PRESENT 或 SELF_ATTESTED，不显示伪盾牌。
5. **三种成长指标仍分离**：Mapping Coverage（限定审查样本）、Time Elapsed（期限）、KPI Result（具公开同口径结果）；另有“链完整性验证状态”是**核验状态而非进度百分比**。不可混成一个“可信度完成率”。

R0 设计比较必须体现：
- 一屏横向原生树；两显示器双窗口“树 + 证据/审计”；多分支的网状交叉引用；普通手机的列表式路径追溯。
- 固定布局、同内容同参数的确定性位置；仅在显式扩张或源数据改动时增枝；避免 100+ 分支交叉成杂乱神经网。
- 交互可逆：任意暗线一键回溯来源及依据，任何被撤回边能查看此前存在与后来撤回的原因。
- 颜色、线型、符号均有文字解释；不依赖单一色相显示法律效力或数据安全状态。

## 6. R0-K 研究阶段：Codex 本轮唯一工作，不得跳过

**Step K0 — 只读前置核验**：读取 V1.1 任务书、现有 R0 交付是否已经存在、P0/P0.5 可合法访问资产、Evidence Passport/Run Receipt；检查当前分支和 PR #129 状态。若已有同类机制，以复用而非重建为前提；原代码不修改。

**Step K1 — 四路径技术决策研究**：给每个标准列出准确版本/强制性/局限，与目前资产逐字段对比；定义信任威胁模型（自签、本地被篡改、密钥丢失/撤销、冲突元数据、源码源站更换、哈希不一致、历史时间戳伪造、权限访问/版权问题）。尤其说明 Merkle DAG 验证、SCITT 收据、W3C VC、区块链共识的不同作用及组合方式。

**Step K2 — 字节/条款/断言三层结构**：设计 1 份公开文件的受控分块实例与可重复规范化流程，抽取 2 个条款、3 个关系断言及 1 个更正事件的**纯纸面样本**；列明 RAW_VERIFIED 与 OFFICIAL_SOURCE_CONFIRMED 差别。

**Step K3 — 暗线与反证方法**：至少 3 个完全虚构或公开条款候选案例：可支持路径、弱候选、应拒绝的假关系；为每一例保留可重演路径、反证和裁决条件。研究 AI 候选生成的人审阈值、版本偏差/引用幻觉风险。

**Step K4 — UI/交互概念研究**：沿用 V1.1 的 3 套横屏布局对比，增加证据根系、暗线、历史与审计镜头状态图；明确多屏技术条件，单屏必须可独立完成来源审计。

**Step K5 — 后续工程路线和放行门**：判断从纯静态研究走向受控离线概念样件最低需要哪些测试、数据许可、性能预算、真实用户任务和人工审查。仅提出路线，不启动编码。

**本轮交付（6 份 Markdown + 必要图表文本/草图）：**
- R0K_FOUNDER_THESIS_AND_BOUNDARIES.md
- R0K_STANDARDS_AND_ARCHITECTURE_DECISION.md
- R0K_CONTENT_ADDRESSING_EVENT_MODEL.md
- R0K_HIDDEN_LINK_DISCOVERY_AND_FALSIFIERS.md
- R0K_ORGANIC_ATLAS_UX_EXTENSION.md
- R0K_ROADMAP_GATES_AND_FOUNDER_DECISION.md

文档之间要互链，索引到原 V1.1 和现有 R0（如已存在），不覆盖历史研究。若实际资料核查失败，在原位标注 UNKNOWN 与替代官方来源，不为凑满交付制造事实。

## 7. 未来路线图（方向明确，但逐关授权）

- **R0-K（本次）：** 标准研究、数据与事件模型、可证伪暗线设计、横向树可信 UI 草图，Founder 审查。
- **A1（未来另批）：** 完整证据账本，选 1–2 份有合法保存权的公开文件做可重复分块/哈希与变更检测；修订/撤回保留旧证据。先用本地工具，目标新增采购现金 AUD 0。
- **A2（未来另批）：** 完成可复验的关系断言和候选暗线索引；每个证据断点能停；定义不同权限的人工审核记录。比较可追溯性而不是幻想 AI 自行定法。
- **B（未来另批）：** 横向有机树静态/交互 UI，显示生长、来源、暗线、纠错；用户可在 3 步内查看任意样例路径的完整依据，完成移动端与多屏审查。
- **C（未来另批）：** 离线独立验证、故意篡改/源站换版/哈希失效/伪造签名/错误地域/时点的对抗测试。只有明确多主体审计需求才研究试用签名/透明收据；仅符合实际业务与许可时考虑 VC。
- **D/E（未来独立决策）：** 若有真实跨组织的彼此不完全信任、独立时间戳及账本治理需要，才比较许可链/公链锚定或专门透明服务；做正式安全、法务、成本/可维护性审查。公链、代币、个人数据永久存储、Council 内网集成均**不因研究路线而获得授权**。

**预期目标推演**：从“找到战略与业务联系”→“能够证明为什么存在这条联系”→“及时察觉版本与证据变化”→“发现新的待核跨领域联系”→“以清晰反证与责任边界辅助个人/团队判断”→“在正式获得权限后支持跨组织独立审计”。任何一步都不能推定已经具备真实运营绩效或行政授权。

## 8. 明确的验收/停止条件

**R0-K PASS：** 概念 schema 的三层哈希关系没有误把有环语义图写成 DAG；字段有可复算规则；至少三条暗线案例含强/弱/拒绝判定；明确“签名 ≠ 语义真”；至少一张横向树可信关系增层草图；版本/来源可核查；输出四技术路线取舍及相关成本；所有 UI 进度有可解释数据通道；有 Founder Gate 并保留原 A/B/C/D 冻结。

**R0-K PARTIAL：** 有理论但不能核验原文、数据来源或技术适配；允许报告真实缺口，不得假称全部完成。

**立即 STOP：** 需要读取/上传 2026-10-22 Council 内部 Leadership Forum 材料或其他非公开 Council 数据；未经许可复制/再发布全文；需外部商业 API、付费网络、私钥或硬件设备；会改变 PR #129、现有 Owner-Private Sites、主分支或 WCOS/Council 系统；自动推送公开身份声明、部署可访问网站、合并 PR 或执行真实对外签发。

**责任：** Codex 负责可复现研究/技术候选与材料整理；ChatGPT 协助技术审查、反例与任务编排；Founder 负责方向和下一阶段授权；法律/组织授权与法规效力仍需适当专业人员核定。工作成果不得称为 Council 官方意见或 Council 授权项目。

## 9. 可直接给 Codex 的执行口令

> 在独立分支 research/public-strategy-atlas-20261029 上继续 ClimateOS Public Strategy Knowledge Atlas。首先读取本任务书 V1.2 与历史 V1.1，并只读检查已有研究与 Evidence Passport。**本轮只执行 R0-K 区块链式知识组织、字节级可追踪结构、内容寻址、透明收据、暗线发现与可审计有机横向树的研究和静态设计**。完成 6 份 R0K Markdown 交付、来源核验、三种候选暗线及反例、4 种技术路线比较和未来工程授权门；提交到同一隔离分支并返回 Git SHA。不要编程或部署网站，不接 Council 数据，不导入内部会议材料，不使用新付费服务，不发邮件，不改 PR #129/其他分支，不合并 PR。交付后停止，等待 Founder 复核。
