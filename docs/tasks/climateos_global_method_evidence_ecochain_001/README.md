# CLIMATEOS-GLOBAL-METHOD-EVIDENCE-ECOCHAIN-001

2026-11-09；唯一[任务书](TASKBOOK_ZH.md)；冻结基线PR144 `77a35e2723372a290579e4549a86781e2be65c04`。**LOCAL_VERIFIED / REVIEW_READY_WITH_GAPS**。本轮独立科学评审PENDING；不合并、不部署、不提供法定认证或真实减排认可。

先读[中文Founder报告](FOUNDER_REPORT_ZH.md)。

1. [既有ECOChain审计](EXISTING_ECOCHAIN_AUDIT.md) → [原战略memo](ECOCHAIN_GOVERNANCE_MEMO_2026-11-09.md) → [接入状态/待迁移索引](ECOCHAIN_INTEGRATION_STATUS.md)。canonical未找到，不能称正式接入。
2. [全球来源](GLOBAL_SOURCE_REGISTER.md) → [四法域对照](JURISDICTION_METHOD_CROSSWALK.md) → [八类冲突](PHYSICAL_AND_ADMINISTRATIVE_CONFLICTS.md)。9新主题；NZ有限摘录/403；其他地区仅扩展索引。
3. [证据契约](CLAIM_EVIDENCE_SCHEMA.json) → [规则](REVIEW_RULES.md) → [角色提案](REVIEWER_ROLE_AND_INDEPENDENCE.md) → [三包实际结果](REVIEW_EXAMPLES_AND_RESULTS.md)。
4. [一个真实开放片段](OPEN_DATA_CASES.md) → [QA与日志](QA_AND_VALIDATION.md) → [长期知识索引](KNOWLEDGE_INDEX.md)。
5. [NEXT_SESSION](NEXT_SESSION.md)、[Conversation Radar/交接](CRP_HANDOFF.md)、[REVIEW_REQUEST](REVIEW_REQUEST.json)、[HANDOFF_STATUS](HANDOFF_STATUS.json)。

从仓库根目录离线复现（标准Python，无新增依赖/网络）：

```powershell
python docs/tasks/climateos_global_method_evidence_ecochain_001/reviewer.py
python docs/tasks/climateos_global_method_evidence_ecochain_001/check_open_fragment.py
python docs/tasks/climateos_global_method_evidence_ecochain_001/run_validation.py
python docs/tasks/climateos_global_method_evidence_ecochain_001/verify_package.py
```

普通run_validation将新运行日志写入git-ignored的runtime_data/global_method_review_validation，不覆盖归档日志，并核对冻结结果；作者归档用过显式--record。不要常规重跑acquire_open_case.py：已取到原始包，脚本也会阻止重复尝试。build_fixtures.py是作者夹具生成器，不是把任意申报注册为可信数据的准入工具；正常评审只读取冻结examples/registry。

状态分开：软件LOCAL_VERIFIED；真实小片段OPEN_FRAGMENT_RECALCULATED_WITH_LIMITS；真实填埋包OPEN_CASE_DATA_NOT_READY；科学准入PENDING；ECOChain ECOCHAIN_CANONICAL_NOT_FOUND；Enotebook PENDING_INTEGRATION；REGULATORY_CERTIFICATION NOT_PROVIDED；DEPLOYED=false。D3/P1-A/PR140/PR141/ChainB/Stage3旧门均未提升。
