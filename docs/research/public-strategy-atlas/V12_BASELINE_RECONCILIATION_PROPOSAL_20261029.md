# Atlas V1.2 双任务书基线核对与 R0-K 恢复建议（2026-10-29）

**状态：** EVIDENCE-BASED COMPARISON / FOUNDER DECISION PENDING / NO IMPLEMENTATION AUTHORIZATION  
**工作分支：** `research/public-strategy-atlas-20261029`，仅公开研究元数据。  
**禁止：** 不修改两份历史任务书、R0/O2 原件、Council 非公开资料、PR #129、Sites、main；不自动复制在 Council 管理设备或 OneDrive 中的文件。

## 1. 本次远程 GitHub 独立核验

在本分支中实际读取了以下两份不同的 V1.2（**不再把它们误当作同一文件或已经自动合并**）：

| 临时标识 | 精确文件路径 | 当前仓库文件 SHA | 版本性质 |
|---|---|---|---|
| **V1.2-A / TRUSTED** | `docs/research/public-strategy-atlas/PROJECT_TASKBOOK_V1_2_TRUSTED_KNOWLEDGE_GROWTH_20261029.md` | `bf4e6c12e1af3c463af4e3fd669870e7764d59c8` | V1.2 区块链式可信知识生长网络；对应既有远程提交 `19056b86de9aa9099616f948da686ef31550b674`。 |
| **V1.2-B / VERIFIABLE** | `docs/research/public-strategy-atlas/PROJECT_TASKBOOK_V1_2_VERIFIABLE_KNOWLEDGE_GROWTH_20261029.md` | `35b250d01edffc198dadd61bce376a12e2ab5d31` | V1.2 区块链式组织、暗线发现与可审计认知；独立文件，既有远程任务书。 |

注意文件 SHA 是 GitHub 的 blob object ID，不是内容的 SHA-256；不可混称为原始文档 SHA-256。

**共同目标**：Founder 要求把可验证的内容与关系历史、哈希组织、多入口暗线检索、人工核验以及横向 O2 树结合；不强制公链、代币、Council 内部系统或立即实施。两者均冻结 A/B/C/D 开发。

## 2. 实际交叉对应

| 范围 | V1.2-A / TRUSTED | V1.2-B / VERIFIABLE | 裁决 |
|---|---|---|---|
| 研究范围 | R0-K 区块链式知识结构、字节范围/内容块、关系断言和来源 | 同核心范围，进一步明确四层架构：来源 DAG、语义关系图、追加式事件链、智能发现图 | **兼容；B 的四层划分宜纳入后续统一架构** |
| 可信度界限 | 区分来源/签名/证明/法律适用，强调本地日志不能防御有权重写全库者 | 同样强调；给出精细事件类型及隐私删除测试 | **互补** |
| 标准与技术路径 | 四路线：传统哈希日志、Merkle 内容寻址、签名/SCITT、链上锚定 | 调研 W3C VC/JOSE-COSE、RFC9942/9943、Git/IPLD 及现有资产字段适配 | **互补，均保留研究要求** |
| 隐性关系/反证 | 至少三类候选强/弱/拒绝，并规定地域/时点假阳性处理 | 提供 10 个反例/测试设计，明确测试仅设计/实际执行须区分 | **B 测试条目更加可操作** |
| UI | O2 横向树上的证据根系、暗线、时间历史、审计视角 | 原 O2 彩色线条、证据/暗线/撤回状态和交互 | **兼容** |
| 明确交付文件名 | 六份：`R0K_FOUNDER_THESIS_AND_BOUNDARIES.md`、`R0K_STANDARDS_AND_ARCHITECTURE_DECISION.md`、`R0K_CONTENT_ADDRESSING_EVENT_MODEL.md`、`R0K_HIDDEN_LINK_DISCOVERY_AND_FALSIFIERS.md`、`R0K_ORGANIC_ATLAS_UX_EXTENSION.md`、`R0K_ROADMAP_GATES_AND_FOUNDER_DECISION.md` | 六份：`R0K_BLOCKCHAIN_INFORMED_ARCHITECTURE.md`、`R0K_CONTENT_AND_ASSERTION_SCHEMA.md`、`R0K_DARK_LINK_DISCOVERY_PROTOCOL.md`、`R0K_ORGANIC_TREE_TRUST_OVERLAY.md`、`R0K_STANDARDS_AND_ASSET_FIT.md`、`R0K_FOUNDER_DECISION_GATE.md` | **确实存在不可静默忽略的命名差异** |
| 授权边界 | R0-K 研究/静态设计；A/B/C/D 未批准 | 同 | **没有授权冲突** |

## 3. 与已报告 R0-K 本地成果的关系

此前另一工作会话**报告**本地 commit `5279eedc2e8ef8a3dd83643d2be9793f65b72413`、分支 `research/atlas-r0k-evidence-20261029`、来源提交 `19056b86de9aa9099616f948da686ef31550b674`，及 `R0K_FOUNDER_DECISION_GATE.md`。本次**未取得该 commit 原件**。因此：
- 其所报的**父/起始提交指向 V1.2-A 对应的 GitHub 提交**，这有利于今后核历史来源；
- 其所报的**决策文件名与 V1.2-B 的交付清单一致**；
- 二者不构成矛盾的必然证据，但也不能据此断定该本地提交究竟依哪一份执行、六份文件是否完整、是否包含 B 的 10 项反例。需要 read-only `git show` 和实际文件目录印证。
- R0 commit `8be2231272a394efc51423777769e61452c301cc` 经用户转述的恢复审计称 14 项哈希一致；远程本分支仍未持有其全部草图。

## 4. Founder 建议基线（**建议，不是已经批准**）

**优先保留 V1.2-A 作为历史起点 / provenance baseline；以 V1.2-B 作为未来交付格式与更详尽的验收候选；把 A 所有独有的细化技术要求纳入后续单一 V1.3 对照表。**

不得现在把其中一个文件删除或改名，不能为了“统一版本”破坏研究来源与本地 commit 所引用的历史文档。等恢复实际 `5279eed...` 内容后，按真实交付逐项映射 A、B，识别缺项，再由 Founder 批准未来单一 V1.3（不得用重命名伪装完成 R0-K）。如不得不提前选定研究核对表，先用 B 的六文件名对应恢复清单，再核 A 独有约束，状态应标 `PROVISIONAL`。

## 5. 原件恢复受限与合法同步步骤

- 上次另会话**报告** R0-K 位于一个 Council 管理的 OneDrive 下的工作区；这是定位线索，不是已在本环境读取的事实。不要把内部组织账号、用户个人目录和 Office 设备绝对路径写入公开仓库。
- Codex 在可合法使用的原设备/工作环境进行**只读**定位：核对 `5279eed...` commit 和父提交、branch/upstream、六份文档的 SHA-256、内容是否来自公开资料或含公司内部数据/会议/员工信息。
- 先做发布权限和来源分级。仅当所有资料均为个人合法可分享的研究成果且无 Council 非公开信息或未经授权知识产权时，另经 Founder 授权进行隔离分支的受控同步。若权属不清：停在 `RESTRICTED`，只返还非敏感元数据，不能复制到私人 GitHub。
- 找不到本地原件时标 `LOCAL_UNAVAILABLE`，不得重做报告冒充恢复。
- 原件找回以后再出 `R0K_ACTUAL_DELIVERABLE_CROSSWALK.md`，以内容而非文件名断定是否满足 A/B。

## 6. 下一步最小动作（无开发授权）

1. 给可访问原 R0-K Work/原工作区的 Codex 下只读定位指令，只返回目录、Git 提交和文件摘要；未做公开安全审查前不导出全文。
2. 将恢复所得的已批准、非敏感元数据与 A/B 的内容矩阵对齐；记录哪些交付存在/未完成/未知。
3. Founder 确认今后是否采用单一 V1.3 综合基线。A/B/C/D 网站实现、Council 数据接入、采购、部署依旧停止。

**本报告不解决 R0-K 原件的访问缺口，不宣称 R0-K 通过研究验收。**
