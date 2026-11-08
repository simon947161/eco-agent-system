# 空间温室气体假说验证：唯一导航

任务 `CLIMATEOS-SPATIAL-GHG-HYPOTHESIS-VALIDATION-001`，执行日期 2026-11-09（Sydney）。唯一任务依据 [TASKBOOK_ZH.md](TASKBOOK_ZH.md)。基线 PR140 `16f0b59dab966f0b66d91b7c28135e8fce9e4cc1`；本任务书提交 `7a6de0d1ed53c91bfcda529b090631755998d94d`。独立分支，不修改 PR138–140 或已验证核心。

**研究交付已形成；科学准入仍 PENDING。** Stage 1 `WITH_LIMITS`；Stage 2 `BLOCKED / NO_VALID_VERTICAL_PROFILE`；Stage 3 `WITH_LIMITS / METHOD_READY_NOT_VALIDATED`。取得真实 AirCore 数据不等于通过本任务跨高度定量比较门槛。

已提交独立 [Draft PR141](https://github.com/simon947161/eco-agent-system/pull/141)。ChatGPT对研究HEAD `1daa3a15b698c5a9216e7286cf1243ef0cf870dc` 返回 `ACCEPT_WITH_CONDITIONS`；[评审回执](SCIENTIFIC_REVIEW_RECEIPT.md)另行归档，不提升科学准入，下一阶段等待Founder。

| 阅读目的 | 文件 |
|---|---|
| Founder 通俗结论与地区措施 | [FOUNDER_REPORT_ZH.md](FOUNDER_REPORT_ZH.md) |
| 假说、支持与反证 | [HYPOTHESIS_EVIDENCE_MATRIX.md](HYPOTHESIS_EVIDENCE_MATRIX.md) |
| 文献、章节、访问限制 | [SOURCE_REGISTER.md](SOURCE_REGISTER.md) |
| 三候选准入 | [HIGH_ALTITUDE_DATA_FIT.md](HIGH_ALTITUDE_DATA_FIT.md) |
| 真实数据及停止理由 | [NO_VALID_VERTICAL_PROFILE.md](NO_VALID_VERTICAL_PROFILE.md) |
| 同质量受控反事实 | [SAME_MASS_COUNTERFACTUAL_FEASIBILITY.md](SAME_MASS_COUNTERFACTUAL_FEASIBILITY.md) |
| 公式、单位、误差和接口 | [ENGINE_METHOD_CONTRACT.md](ENGINE_METHOD_CONTRACT.md) |
| 实际测试与证据 | [SCIENTIFIC_VALIDATION.md](SCIENTIFIC_VALIDATION.md) |
| ChatGPT 评审包 | [CRP_HANDOFF.md](CRP_HANDOFF.md) |
| 下一轮与 Conversation Radar | [NEXT_SESSION.md](NEXT_SESSION.md) |

## 离线复算（仓库根目录，Python 标准库，无下载）

```powershell
python docs/tasks/climateos_spatial_ghg_hypothesis_validation_001/audit_profile.py --check
python -m unittest discover -s docs/tasks/climateos_spatial_ghg_hypothesis_validation_001 -p test_audit_profile.py -v
python -m unittest tests.test_physics_validation.GasTests -v
```

第一项重验原件 SHA 与结构 QC；第二项验证准入防错；第三项只重跑原有 P1 合成/解析参考测试，不运行观测换算或气候模型。输入 [INPUT_MANIFEST.json](INPUT_MANIFEST.json)、预登记 [PROFILE_PROTOCOL.json](PROFILE_PROTOCOL.json)、人工元数据判定 [METADATA_GATES.json](METADATA_GATES.json)、确定性输出 [PROFILE_QC.json](PROFILE_QC.json)。脚本不能自行解除科学门槛。

原始 75 MB ZIP 留在仓库外；本目录只保留 CC0 下一个剖面的原始成员、来源 README 和下载回执。逐文件 SHA 可离线复验；发布者独立 checksum 未取得。重复下载不是复算前提。全部数据是公开大气观测，非 Council 或设施运行资料。

D3 `DATA_NOT_READY`、P1-A `PENDING`、PR140 `NO_VALID_PAIR`、P2/P4 `HYPOTHETICAL` 不变。没有部署、合并、法定因子变更、排放反演、气候模拟或地区减排率。ChatGPT 评审与 Founder 后续授权是不同门槛。
