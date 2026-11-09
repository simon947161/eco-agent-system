# 全球自然系统证据 Atlas｜研究入口

2026-11-09；执行唯一 [TASKBOOK_ZH](TASKBOOK_ZH.md)。冻结父提交 `3bb71785ad2705823a78748c9ba4cd5003becb41`，研究基线 CCZPS 全球规范 v0.1；不是全球模型或科学准入。

**已实现离线查询、定向路径追踪、验证器及 CCZPS→PR145 合成端到端接口。LOCAL_VERIFIED / REVIEW_READY_WITH_GAPS；科学准入 PENDING；未部署。**

从 [12页中文 Founder 报告](FOUNDER_REPORT_ZH.md) 开始。精确 R/D 见 [交接状态](HANDOFF_STATUS.json) 与新 Draft PR 最终评论；D 不写入自身内容。

| 入口 | 内容 |
|---|---|
| [既有资产与评审审计](REUSE_AUDIT.md) | PR129/130/143–145、原架构、冻结分区与角色 |
| [全球登记](GLOBAL_COVERAGE_REGISTER.json) | 248 M49条目；236仅登记、12深入元数据案例；不等于主权国家数 |
| [分类](NATURAL_SYSTEM_TAXONOMY.md)、[关系图](RELATION_GRAPH.json) | 七系统、25单元、7边、3机制；几何覆盖0% |
| [来源与许可](DATA_SOURCE_AND_LICENSE_REGISTER.md) | 12新增主题，原始网页不入Git，权限阻塞如实保留 |
| [Scorecard](SCORECARD_METHOD_AND_COVERAGE.md)、[国家映射](COUNTRY_NATURE_POLICY_CROSSWALK.md) | 原站评分与承诺/报道/结果分离；12国样本理由 |
| [跨境案例](CROSS_BOUNDARY_CASES.md) | 水文、ENSO、全球甲烷的机制与可证伪边界 |
| [证据](EVIDENCE.json)、[schema](EVIDENCE_SCHEMA.json)、[关系schema](RELATION_SCHEMA.json) | 十类证据；模型和生态结果缺口不是已获得成果 |
| [实际查询结果](ATLAS_QUERY_RESULTS.md)、[完整输出](evidence/query-results.json) | 可运行、可检索、可追溯 |
| [主线交接](CCZPS_ECOCHAIN_HANDOFF.md)、[QA](QA_AND_VALIDATION.md) | 下一科学治理决策与真实测试 |
| [NEXT_SESSION](NEXT_SESSION.md)、[CRP](CRP_HANDOFF.md)、[评审请求](REVIEW_REQUEST.json) | Founder转交，未自动送达ChatGPT |

仓库根目录，标准 Python，零新增依赖/服务/网络：

```powershell
python -m cczps_lite.integration.global_natural_systems_atlas validate
python -m cczps_lite.integration.global_natural_systems_atlas query --country ETH --process nile_flow
python -m cczps_lite.integration.global_natural_systems_atlas query --country AU --process enso
python -m cczps_lite.integration.global_natural_systems_atlas query --country CHN --evidence-type POLICY_ASSESSMENT
python -m cczps_lite.integration.global_natural_systems_atlas query --country MYS --evidence-type POLICY_COMMITMENT
python -m cczps_lite.integration.global_natural_systems_atlas query --country USA --system ATM_BOUNDARY --at 2024-06-01T00:00:00Z --evidence-type PHYSICAL_OBSERVATION
python -m cczps_lite.integration.global_natural_systems_atlas trace --start CH4_SOURCE --end CLIMATE_RESPONSE
python -m cczps_lite.integration.global_natural_systems_atlas e2e
python docs/tasks/global_natural_systems_evidence_atlas_001/run_validation.py
```

`query` 支持自然系统或单元ID、国家名称/M49/ISO、过程、观测时间、证据类型和文字搜索；条件合取。`trace` 是有向图检索，不是影响权重计算。未知时段不会匹配 `--at`；检索日期不是观测日期。

正常验证日志写入 git-ignored `runtime_data/global_atlas_validation`，不覆盖归档。`acquire_metadata.py` 仅作者一次采集，禁止重试已存在收据；`extract_metadata.py` 需要未公开原始缓存；`build_atlas.py` 与 `freeze_package.py` 是显式作者版本生成工具，**不能作为把新来源自行升级为可信的准入流程**。新来源、参数、几何及任何科学实验须独立审查。
