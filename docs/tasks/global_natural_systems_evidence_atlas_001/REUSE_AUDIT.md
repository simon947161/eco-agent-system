# 既有架构、资产与评审审计

审计日2026-11-09，完整远程身份与评审文字：[baseline.json](evidence/baseline.json)。本任务只新增一个薄 CCZPS 查询适配器、测试及任务知识包。既有权威文件未改。

| 资产/版本 | 实际可复用 | 本轮边界 |
|---|---|---|
| `docs/00_MASTER_ARCHITECTURE/SYSTEM_RELATIONSHIP_MAP.md`、`ECOENGINE_V2_SYSTEM_DEFINITION.md`、`CCZPS_LITE_V0_4_REVIEW.md`（父3bb7178树） | 模拟、物理解释、可能未来比较、制度翻译、记录与人类决定分层 | 文档角色不等于生产实现；没有新建World Model |
| `cczps_lite/engine/scenario_comparison.py` | 真正可调用的纯比较函数、证据不足与人工审批边界 | 传入显式空证据，四配置场景返回不足；不注入Scorecard、不输出优胜者 |
| `cczps_lite/input/spatial_transects.json` | Batlow、Kunlun、Iraq、Baiyangdian-Xiongan配置 | configured_not_validated；上游/下风角色不是已做GIS或风场推导 |
| `cczps_lite/integration/facility_spatial_evidence.py`、QGIS source_registry | Cooma范围、CRS、许可证及接纳门的设计模式 | Cooma/GDA2020条件不能套用尼罗河；不修改冻结门 |
| PR129 `987cc1dc7170204e5eab3d1750590ba463ea9d08` / `apps/regional-public-os/README.md` | HRS历史/研究页的固定证据清单、缺失/过期保守处理 | 只读代码与README；不声称本轮验收线上权限或重新部署 |
| PR130 `e3d8f074e0e1ba5e9614c3f4c5a2b973746b2ab7` / `apps/public-strategy-atlas/DATA_CONTRACT.md`, `atlas-domain.js` | atlas-domain-1实体/来源/断言/反证/审查语义，既有查询概念 | 当前任务分支没有该app全树；不合入另一PR，不复制整套Atlas；导入状态PENDING |
| PR143 `746825e65b8ddbd0f518709c94d9476df107208b` | 物理知识网、公式表和链A边界 | 对话时间线仅观察到作者交接，无单独ChatGPT回执；Chain B BLOCKED |
| PR144 `77a35e2723372a290579e4549a86781e2be65c04` | 四接口甲烷/碳账、法律方法版本与三合成夹具 | [评审6735839200](https://github.com/simon947161/eco-agent-system/pull/144#issuecomment-6735839200)有条件接受；多于4次测量、条款交叉引用等不得直接代码化法定计算 |
| PR145 `ae1050a621ac794e447f9ac047865d90b2f04b03` | typed claims、来源/单位/角色冲突、A/B/C审查器 | [评审6736737730](https://github.com/simon947161/eco-agent-system/pull/145#issuecomment-6736737730)：B的RECALCULATED仅内部夹具；新接口明确标注，不改旧代码 |
| Knowledge Garden / Enotebook / ECOChain | 复用PR145 `EXISTING_ECOCHAIN_AUDIT.md`与`ECOCHAIN_INTEGRATION_STATUS.md`固定证据索引 | 历史检索未定位权威canonical；无新接纳回执。ECOCHAIN_CANONICAL_NOT_FOUND / PENDING_INTEGRATION |

本轮定向搜索未发现可直接复用的全球M49/HydroBASINS几何库存；这不是对所有历史磁盘的穷尽证明。采用元数据和有界关系，0新GIS下载。

Public Strategy Atlas 对接投影：自然单元→SpatialUnit；来源→SourceArtifact/EvidenceAnchor；机制→RelationshipAssertion；反证→CounterEvidence；研究条件→DiscoveryHypothesis；人工审查→ReviewDecision。旧predicate白名单没有本任务物理边类型，故未来适配只能先用 `RESEARCH_CANDIDATE`/`RELEVANT_TO` 携带 `data.process_type`；不得伪造新谓词已受接纳。`classification=LOCAL_RESEARCH`、`admission=PENDING`，实体revision/station绑定仍需原app核验。

本轮真实运行入口选择 **CCZPS integration**，保持全球字段为任务局部投影。没有新数据库、GIS平台、采集服务、代理架构或正式ECOChain身份系统。
