# P4 独立科学与许可评审请求

评估日期：2026-11-24（Australia/Sydney）｜`READ_ONLY`｜`NO_RAW_DATA_DOWNLOADED`

授权：[Issue #164](https://github.com/simon947161/eco-agent-system/issues/164)。本包只做发现与尽调；评审不需要下载原始数据或运行父引擎。精确交付HEAD见本Draft PR最终回执，父HEAD固定9aea387a4261b913163b3be3197597089d9e9414。

请ChatGPT优先审查：

1. [四项候选](CANDIDATE_DATASET_REGISTER.md)及[JSON](candidate_register.json)的候选/深审上限、各闸门和NO_SUITABLE_DATASET停止是否充分；是否错误把未知写成不存在。
2. [许可](LICENCE_AND_PROVENANCE_AUDIT.md)：C04 Dryad政策 [S10](https://datadryad.org/terms) 是否只支持元数据级CC0而未被说成独立权属确认；C01/C03未知和C02 STOP是否保守。
3. [九类映射](FIELD_TIME_QC_MAPPING.md)：浓度/平均/模型率、年报/测量窗/百年cohort是否分开；匿名场址和机场替代气象是否正确保留。
4. [法规缺口](BASELINE_LEGAL_RIGHTS_GAPS.md)：AWT旧新方法、FOGO收集与工艺、数据版权与信用权利是否混同。
5. [Founder最小审批](FOUNDER_P4_DECISION_CN.md)：是否应接受STOP，或仅授权C04明确文件URL补查；不要把本评审解释为下载/计算授权。
6. [实际检查](VALIDATION.md)与[回执](validation_results.json)：是否准确区分本地文档校验、继承CI和新HEAD的CI未触发；父冻结文件有无更改。

当前SCIENCE=PENDING、REAL_DATA=DATA_NOT_READY、CREDIT=NOT_DETERMINED。没有原始包、实际减排、独立现场核证、法定意见或信用签发。请把评审绑定新PR精确HEAD；本请求不代表评审已完成。
