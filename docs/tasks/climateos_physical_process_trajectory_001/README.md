# 三条物理过程轨迹：研究与评审入口

任务 `CLIMATEOS-PHYSICAL-PROCESS-TRAJECTORY-001`。唯一授权范围见 [TASKBOOK_ZH.md](TASKBOOK_ZH.md)。冻结父 PR146：`1e6b13e2b80c50e6d20e05a4e88819eb0de93488`；任务书提交 `947333489f01e5f85cb92084933fa24d766cf334`。本包是现有 Atlas 的薄研究投影，**不是新网站、全球预测模型或科学准入决定**。

## 阅读顺序与研究索引

1. [中文 Founder 报告](FOUNDER_REPORT_ZH.md)：实际结果、停在哪、最少决策。
2. [轨迹方法和字段](TRAJECTORY_METHOD_AND_SCHEMA.md)、[复用审计](REUSE_AUDIT.md)。机器数据：[14 个片段](TRAJECTORIES.json)、[9 个跨过程关系](CROSS_RELATIONS.json)。
3. [甲烷](TRAJECTORY_CH4.md)、[ENSO](TRAJECTORY_ENSO.md)、[水文](TRAJECTORY_HYDROLOGY.md)、[定量结果](QUANTITATIVE_RECALC_RESULTS.md)。
4. [跨过程矩阵](CROSS_PROCESS_CAUSAL_MATRIX.md)、[反证登记](COUNTEREVIDENCE_REGISTER.md)、[来源与准入](OPEN_DATA_AND_SOURCE_REGISTER.md)、[下一输入](MODEL_GAPS_AND_NEXT_INPUTS.md)。
5. [澳洲评分专项](SCORECARD_AU_CORRECTION_BRIEF_ZH.md)、[英文编辑反馈草稿—未发送](EDITOR_NOTE_EN_DRAFT.md)。
6. [测试与核验](QA_AND_VALIDATION.md)、[CCZPS/ECOChain 交接](CCZPS_ECOCHAIN_HANDOFF.md)、[下一次会话](NEXT_SESSION.md)、[对话雷达](CRP_HANDOFF.md)。
7. [REVIEW_REQUEST.json](REVIEW_REQUEST.json)、[HANDOFF_STATUS.json](HANDOFF_STATUS.json) 给出研究提交 R；交付 D 是包含两份交接元数据的外层 Git 提交，精确值在 PR 交接评论中，避免自引用哈希。

## 离线复算

在仓库根目录，Python 标准库即可，无新依赖：

```powershell
python -X utf8 docs/tasks/climateos_physical_process_trajectory_001/run_validation.py
python -X utf8 -m cczps_lite.integration.physical_process_trajectory evaluate CH4
python -X utf8 -m cczps_lite.integration.physical_process_trajectory evaluate ENSO
python -X utf8 -m cczps_lite.integration.physical_process_trajectory evaluate HYDRO
python -X utf8 -m cczps_lite.integration.physical_process_trajectory evaluate CROSS
python -X utf8 -m cczps_lite.integration.physical_process_trajectory evaluate SCORECARD
python -X utf8 -m cczps_lite.integration.physical_process_trajectory trace HYDRO
```

正常验证只写被 Git 忽略的 `runtime_data/physical_trajectory_validation/`。`acquire.py` 是有一次尝试保护的作者取证工具；**复算不需要、也不应重跑下载**。`prepare_evidence.py` 依赖作者本地原网页缓存和 PR129 Git 对象，不是下游离线复算前置条件。原始 RONI 公共领域数值已归档；其他网页只归档事实和收据，不复制受限正文。

最终状态分别表示：LOCAL_VERIFIED=本地限定测试；READY_FOR_REVIEW=可交人工评审；DEPLOYED=false；SCIENTIFICALLY_ADMITTED=false。各旧闸门见交接文件，保持不变。
