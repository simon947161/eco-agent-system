# P0 只读审计 · 2026-11-23

唯一授权来源：[Issue162](https://github.com/simon947161/eco-agent-system/issues/162)，原文归档 [TASKBOOK](TASKBOOK.md)。Windows / PowerShell / Python3.14；新工作树独立、起始干净。远程 main=`9eb7577e145e76161f9f1cd8509348b19c2904cc`。逐PR实际状态见 [GitHub收据](evidence/github-intake.json)：均OPEN/DRAFT/UNMERGED，不能按main已具备这些能力来描述。

## 基线与单一位置

选定 PR145 `ae1050a621ac794e447f9ac047865d90b2f04b03` 为 stacked 基线；它已包含 PR137–144 的受限计算、物料账、证据接口。新分支 `codex/climateos-awt-001-20261123`。新增实现唯一目录 `docs/tasks/climateos_awt_001/`，测试进入现有 `tests/`，复用既有CI。没有复制CarbonOS归档、引入数据库或搭建AI服务。

|资产|精确版本 / 路径|本次处置与真实限制|
|---|---|---|
|CarbonOS P1-A 与D3|PR132 `2ec66ae41ae2e1d4a0f1aaa92aa98c9f0ff4c5b0`；`docs/research/carbonos/INDEX.md`、`NEXT_SESSION.md`、`batch-d3/DATA_ADMISSION_REPORT.md`|只读引用，独立分支未并入本基线。D3三个候选停止、原始观测文件0；许可/原件字节/时钟/QC/独立通量未形成完整证据，不重试403或重新跑已接受批次。|
|本地P1-A|工作区 `research/CLIMATEOS-CARBON-P1A-001/`；`EXECUTION_STATE.json`、历史公式报告可读|LOCAL_VERIFIED是旧运行记录，非本轮重跑。报告存在、20公式研究已归档PR132；本机额外缓存不上传。独立科学准入PENDING。|
|中文物理解释|PR137 `37c4b093e511bd9b5014c276390ebde114d28eed`；`docs/tasks/climateos_dynamic_quant_001/METHANE_ALTITUDE_PRESSURE_ZH.md`|引用浓度/质量/气候响应分离；不修改原PR。|
|有界物理计算|PR138 `f9016aa4cdc728728a1a5dece0b947b1c2e5e7bc`；`cczps_lite/integration/physics_validation.py`|复用数值域检查及碳→CH4计量，不另写FOD/温度响应模型。|
|真实开放液相片段|PR139 `fc450196d01c9add5edf51f599072b18e6658196`；PR145 `evidence/open-fragment-results.json`|23条溶解浓度仅支持单位复算，不能转作填埋场源强或1000t真实输入。保持OPEN_CASE_DATA_NOT_READY。|
|甲烷物理与守恒|PR143 `746825e65b8ddbd0f518709c94d9476df107208b`；`cczps_lite/integration/methane_knowledge_engine.py`|复用conserve；ChainB仍BLOCKED，不强接不同边界。|
|四接口CH4/C账|PR144 `77a35e2723372a290579e4549a86781e2be65c04`；`docs/tasks/climateos_au_landfill_methane_methods_001/mass_balance.py`|实际调用已存在的evaluate/generation接口。其SYNTHETIC_DAY_001为原内部夹具时间标签；本轮显式适配区间积分量，仅检验代数守恒，绝不把百年量标作日排放。|
|证据接口及ECOChain|PR145基线；`reviewer.py`、`CLAIM_EVIDENCE_SCHEMA.json`、`KNOWLEDGE_INDEX.md`|复用canonical/digest、append_event/verify_events和closed-schema基本类型检查；领域护照是兼容扩展，无并行库。真实独立评审者/信任锚未建立，ECOCHAIN_CANONICAL_NOT_FOUND、Enotebook PENDING_INTEGRATION。|
|Bondo Evidence Passport|本树 `cczps_lite/contracts/bondo_evidence_passport.schema.json`|语义映射来源、claim、冲突、gap、人审；该schema固定Bondo元数据且禁raw/models，不能冒充AWT合格格式。保留原schema。|
|EcoEngine公开适配 / Public Strategy Atlas|公开 `cczps_lite/integration` 适配可读；PR130 metadata HEAD=`e3d8f074e0e1ba5e9614c3f4c5a2b973746b2ab7`、OPEN/DRAFT/UNMERGED，未检查网站/数据库|本试算无需地理数据库或实时站点，不调用私人系统。Atlas正式接入NOT_VERIFIED，不凭名称声称接入成功。|
|PR152/155/157|HEAD见GitHub收据，远程Draft|本轮不需风热耦合器或学习网站计算；不导入多余依赖，不改旧成果。|

## 先验评审限制

已读[PR144评审6735839200](https://github.com/simon947161/eco-agent-system/pull/144#issuecomment-6735839200)及[PR145评审6736737730](https://github.com/simon947161/eco-agent-system/pull/145#issuecomment-6736737730)：有条件接受合成研究，非真实设施/法定认证。内部复算必须命名INTERNAL_FIXTURE_REPLAY_ONLY；hash不是独立真实性证明；NGER条款解释缺口不得直接法定代码化。

## Missing / blocked

- 1000t组成、实际场址、逐期捕集/库存/泄漏/能耗/残渣、独立校准和合法许可包不存在：真实主张DATA_NOT_READY。本轮只做显式作者合成fixture。
- AWT2015外部因子逐报告期版本链、真实项目注册/crediting period/过渡、FOGO豁免及场址法律义务、Safeguard/其他权利登记未完备。
- NSW现行法网页本轮403后停止；可读EPA指引只能支持保守筛查，不冒充完整法条审查。旧NSW/D3受阻下载未重试。
- 未找到独立审批者真实任命及ECOChain权威接纳位置，不创建替代注册表。

P0结论：可推进独立合成P1–P3；真实数据准入与法定主张保持受阻。已接受历史批次不重做。资产文件哈希见后续生成的 `evidence/reuse-hashes.json`，哈希验证是版本核对，不是科学验证。

补充核对：[本地P1-A与公开PR132公式报告](evidence/p1a-local-archive-check.json)的LF SHA相同，确有已公开可复用版本；只读取两份公开研究文档，不访问其私有缓存。[PR130元数据收据](evidence/pr130-metadata-only.json)只证明分支状态，不代表私人Atlas或数据库验收。
