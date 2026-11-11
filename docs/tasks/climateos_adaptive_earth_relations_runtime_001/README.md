# Typed Earth Relations Runtime · Issue154

状态：IMPLEMENTED_LOCAL_VERIFIED / SYNTHETIC_PHYSICAL_SANDBOX / SCIENCE_PENDING。

- [中文Founder报告](FOUNDER_REPORT_ZH.md) · [离线10页展示](slides.html)
- [唯一任务书](TASKBOOK_ZH.md) · [冻结协议](EXPERIMENT_PROTOCOL.json)
- [源码复用](SOURCE_REUSE.md) · [图契约](GRAPH_SCHEMA.md) · [实际对照](RUNTIME_EXPERIMENTS.md)
- [反例](COUNTEREXAMPLES.md) · [科学边界](PHYSICAL_SCIENCE_LIMITS.md) · [QA](QA.md)
- [下一轮](NEXT_SESSION.md) · [科学评审](CRP_HANDOFF.md)

仓库根目录直接运行，无新增Python依赖：
```shell
python -m cczps_lite.integration.earth_relations run-graph
python -m cczps_lite.integration.earth_relations compare-scenarios
python -m cczps_lite.integration.earth_relations inspect-relations
python -m cczps_lite.integration.earth_relations plan-subgraph --targets question
python -m cczps_lite.integration.earth_relations trace-influences --diamonds 30 --targets diamond_29_a
python -m cczps_lite.integration.earth_relations audit-failures
python -m unittest tests.test_earth_relations
python -m cczps_lite.integration.earth_relations benchmark --output runtime_data/earth_relations/replay
```

浏览器直接打开slides.html，无服务器、网络请求或生产部署。图内数字是已执行CLI结果的回放，不是在浏览器中新算的预测。
