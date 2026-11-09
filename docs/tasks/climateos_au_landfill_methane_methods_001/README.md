# 澳大利亚填埋场甲烷工程与核算｜长期研究入口

任务 CLIMATEOS-AU-LANDFILL-METHANE-METHODS-001；2026-11-09。唯一授权见 [TASKBOOK_ZH](TASKBOOK_ZH.md)。科学父基线 PR143 `746825e65b8ddbd0f518709c94d9476df107208b`；本分支只增加本任务包，旧科学核心不变。

**LOCAL_VERIFIED（有界合成账与文件验证）；REVIEW_READY；科学准入 PENDING；未部署。** 实际设施输入 DATA_NOT_READY。Enotebook 正式接入 PENDING_INTEGRATION，不覆盖个人学习进度。

## 按问题阅读

|问题|入口|
|---|---|
|工程师怎么干、现在能算什么？|[中文创始人报告](FOUNDER_REPORT_ZH.md)|
|从哪里学起、每章怎么练？|[中文学习路径](LEARNING_PATH_ZH.md)、[八份知识包索引](METHOD_KNOWLEDGE_INDEX.md)|
|哪份文件、哪个报告年？|[来源](SOURCE_REGISTER.md)、[版本矩阵](REGULATORY_VERSION_MATRIX.md)|
|哪个公式计算哪个量？|[条款与公式](SECTION_AND_EQUATION_CROSSWALK.md)、[四种方法](AU_LANDFILL_METHOD_COMPARISON.md)|
|物理账如何闭合？|[物料账](LANDFILL_PHYSICS_AND_MASS_BALANCE.md)、[合成结果](SYNTHETIC_MASS_BALANCE_RESULTS.md)|
|怎样测量与独立验证？|[测量与校准](MEASUREMENT_AND_MODEL_CALIBRATION.md)、[两案例可行性](OPEN_DATA_FEASIBILITY.md)|
|如何复用旧成果？|[PR143桥接审计](PR143_E06_E07_BRIDGE_AUDIT.md)、[未来模块](FUTURE_MODULES_INDEX.md)|
|如何复跑与评审？|[QA](QA_AND_VALIDATION.md)、[交接](NEXT_SESSION.md)、[评审请求](REVIEW_REQUEST.json)、[Conversation Radar](CRP_HANDOFF.md)|

仓库旧研究入口（只读）：[PR143知识网络](../climateos_methane_physics_knowledge_engine_001/README.md)、[P1–P4物理验证](../climateos_physics_validation_001/README.md)。本任务入口是此次新增项目索引；按任务书冻结要求不改写旧索引/旧任务。GitHub Draft PR 链接本入口，知识包反向链接本页。未另建门户、GIS、数据库或智能体。

## 从仓库根目录复算（Python标准库，无联网）

```powershell
python docs/tasks/climateos_au_landfill_methane_methods_001/run_synthetic.py
python -m unittest discover -s docs/tasks/climateos_au_landfill_methane_methods_001 -p test_mass_balance.py -v
python docs/tasks/climateos_au_landfill_methane_methods_001/verify_package.py
```

源文件精确字节 SHA 在 `source_receipts/`。PDF/HTML原件仅在被Git忽略的 `runtime_data/au_landfill_methods/`，不随PR复制。下载器遇已有收据不再尝试，包括403失败；新克隆按清单自行合法获取后可用验证器检查，不能把未缓存当已校验。学习笔记、自有示例和代码可以独立阅读运行。

验收边界：8主题、2场址候选、3账本场景、3条款算例及1个P1换算；没有法规信用计算器、场址排放反演、全国汇总、回归或气候模拟。D3 DATA_NOT_READY、P1-A PENDING、PR140 NO_VALID_PAIR、PR141 NO_VALID_VERTICAL_PROFILE、PR143 ChainB BLOCKED、Stage3 METHOD_READY_NOT_VALIDATED 全部保留。
