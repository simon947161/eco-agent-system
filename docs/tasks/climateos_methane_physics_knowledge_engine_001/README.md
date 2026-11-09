# 甲烷物理知识网络与受限计算链

唯一任务：CLIMATEOS-METHANE-PHYSICS-KNOWLEDGE-ENGINE-001，2026-11-09。授权见[TASKBOOK_ZH.md](TASKBOOK_ZH.md)。状态 **IMPLEMENTED_SYNTHETIC_TESTED / REVIEW_READY**，科学准入不变。本目录是本任务统一索引；旧PR和核心不修改。

1. [中文创始人报告与路线图](FOUNDER_REPORT_ZH.md)
2. [科学基础现状](SCIENCE_FOUNDATION_REALITY.md)、[广覆盖因子表](FACTOR_UNIVERSE.md)、[四种排序](FACTOR_PRIORITY_AND_CAUSAL_ORDER.md)
3. [机制图](MECHANISM_MAP.md)、[机器图谱](MECHANISM_GRAPH.json)、[14节点公式登记](EQUATION_REGISTRY.json)、[来源登记](SOURCE_REGISTER.md)
4. [路由契约](MODEL_ROUTER_CONTRACT.md)、[已运行链A/阻塞链B](EXECUTABLE_CHAIN_RESULTS.md)、[机器结果](evidence/chain-a.json)
5. [测试与哈希](EVIDENCE_AND_TESTS.md)、[评审请求](REVIEW_REQUEST.json)、[交接状态](HANDOFF_STATUS.json)、[下一轮](NEXT_SESSION.md)、[Conversation Radar](CRP_HANDOFF.md)

从仓库根目录执行，无新增依赖或网络：
```powershell
python docs/tasks/climateos_methane_physics_knowledge_engine_001/run_chain.py
python -m unittest tests.test_methane_knowledge_engine tests.test_physics_validation.GasTests tests.test_client_ai_evidence -v
python docs/tasks/climateos_methane_physics_knowledge_engine_001/verify_package.py
```
第一条覆盖本任务evidence中的派生JSON（runtime含变动计时）；不改input或原始物理核心。stdout可重定向到本任务。固定输入、步进方程、单位、参数来源、残差、误差及拒绝理由均归档。当前没有REAL_DATA计算路径，更没有科学气候验证通过。

R研究提交、D仅交付元数据提交及最终精确HEAD评论沿用PR142协议，见[父协议](../climateos_client_ai_science_integration_001/HANDOFF_PROTOCOL.md)。GitHub发布不等于ChatGPT收到请求。
