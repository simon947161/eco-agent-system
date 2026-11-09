# 既有 ECOChain 资产审计

结论：**ECOCHAIN_CANONICAL_NOT_FOUND**。找到历史概念、架构定位和证据契约，不等于找到经批准的 ECOChain 运行主库、审批注册表或签发权限。此结论只覆盖下列有界搜索，不宣称全账户或全部历史不存在。

审计基线：PR144 `77a35e2723372a290579e4549a86781e2be65c04`；任务书 `c4c8b8b61b8d74561688c1110c4b697aee854046`；memo 所在提交 `32c56125e19ffa1f00f7937bcba67729b16e7203`。PR138–144 最新状态见 [远程收据](evidence/remote-baseline.json)，均 open/draft/unmerged；没有改旧分支。PR144 [评论6735839200](https://github.com/simon947161/eco-agent-system/pull/144#issuecomment-6735839200) 为有条件接受，保留全部限制；[完整公开回执](evidence/pr144-review-receipt.json)。

|发现/版本|历史目的与机制|本轮复用/未知|
|---|---|---|
|本仓库 [ECO_CHAIN_AND_ECO_ENGINE_ROLE.md](../../../ECO_CHAIN_AND_ECO_ENGINE_ROLE.md)，最近变更 d554364e518fec8e1c652bdd354cdd3490594ec0|生态贡献、价值、信任记录的概念定位|保留术语；未提供已任命技术审查人名单|
|[SYSTEM_RELATIONSHIP_MAP](../../00_MASTER_ARCHITECTURE/SYSTEM_RELATIONSHIP_MAP.md) §3.5/§4，467ed3d2584d5e7d175cd2bdd87109991ea582ce|EcoChain 为证据/贡献记录层；明确不能当治理权威|本轮审查意见不得变成外部认证权|
|[ECOENGINE_V2_SYSTEM_DEFINITION](../../00_MASTER_ARCHITECTURE/ECOENGINE_V2_SYSTEM_DEFINITION.md) §6|与 EcoEngine 科学工具、ClimateOS 治理目的分工|用既有计算接口，不另建智能体/GIS/数据库|
|[CCZPS_LITE_V0_4_REVIEW](../../00_MASTER_ARCHITECTURE/CCZPS_LITE_V0_4_REVIEW.md) §6|明确当时尚未实现 EcoChain|不能把旧概念图当已运行平台|
|[Bondo Evidence Passport schema](../../../cczps_lite/contracts/bondo_evidence_passport.schema.json)，基线 PR144|schema `climateos.bondo.evidence_passport.v0.1`；证据、claims、version_conflicts、gaps、steward、人审和禁止用途|借用 claim_id/supporting_evidence_ids/gaps 思路；Bondo 的项目限制不适合直接当通用法定申报schema，未修改原件|
|[NatureHash Lab README](https://github.com/simon947161/naturehash-lab/blob/main/README.md)，blob 9eb5bc0a1ee22141f1058a847c13f6dae6b2ce38|v0.1 Concept research；明确不是完成的密码算法；列出 ClimateOS/EcoChain/CCZPS 研究关联|可借鉴 Location/Time/Observation/Evidence/Governance context；没有已验证自然状态、法定审批者或签发接口的证据|
|climateos-knowledge-garden：`02_CRP/2026/2026-06-28_EcoChain_NatureHash_Evidence.md`|历史研究入口：Evidence Chain/Evolution Chain/NatureHash|私有知识库只读审计，未复制正文到公开PR|
|同库 `06_Strategy/Trust_Architecture/ClimateOS_Trust_Architecture_v0.1.md`，blob 754a5949217c6b299949d6b9829f3b594040414a|2026-07-06 draft documentation foundation；审批/核验责任仍有开放问题|owner 账号不等于任命过的科学认可机构；未确认 canonical EcoChain schema|
|[PR143机制图](../climateos_methane_physics_knowledge_engine_001/MECHANISM_MAP.md)、[PR144知识索引](../climateos_au_landfill_methane_methods_001/METHOD_KNOWLEDGE_INDEX.md)|可复用公式/边界/学习路径；Enotebook 尚未正式接入|引用、不复制大量内容；PENDING_INTEGRATION|

搜索范围与限制：本仓库当前树、相关文档历史提交、远程 ECOChain 命名分支、GitHub 仓库/代码/Issue/PR 搜索；`EcoChain / ECOChain / Eco-Chain / E4 / NatureHash / Evidence Passport / Enotebook`。查询默认分支的索引缺失不能证明分支不存在。仓库检索找到 Knowledge Garden 与 NatureHash 研究；未发现另一个已批准 ECOChain 主入口。Simon 的相关 Issue 搜索命中未来计算观察任务，不是审批角色规范。

本地文件名与针对性文本搜索覆盖 `D:/Codex/Simon`、`D:/EcoEngine`、`D:/eco_engine_v200`、`D:/QClawProjects/PRI_Knowledge_Archaeology`、`D:/ClimateOS_Vault/ClimateOS Knowledge Garden`。未摄入私人 Council 或企业内容。Knowledge Garden 部分本地 Git 元数据只读访问被拒，使用已连接 GitHub 的文件 blob 核对；未改变权限。未找到独立 E4 审批实现，E4=UNKNOWN。

角色结论：找到 steward/human_review_required 等旧契约字段，但未找到已批准的 EcoChain Reviewer/Approver/Verifier/Issuer 任命和权限映射。Founder 是本任务决策者，ChatGPT 是待独立评审者，Codex 是作者/执行者；这三者均不能由本程序转换成法定签发者。角色增量仅为[待迁移提案](REVIEWER_ROLE_AND_INDEPENDENCE.md)。
