# 实际验证与科学边界

日期2026-11-09。基线PR140远程再次核对：OPEN、DRAFT、未合并，HEAD `16f0b59dab966f0b66d91b7c28135e8fce9e4cc1`。其科学评审回执为有条件接受研究停止判断，非真实因素比较通过。本轮延续“全局阻塞与逐行损失分开”的要求。

## 已实际执行

| 检查 | 结果 | 证据与限制 |
|---|---|---|
| 官方公开AirCore ZIP下载 | HTTP200，75,288,295 bytes | [HTTP回执](evidence/aircore_20210813.zip.receipt.json)，没有发布者独立checksum |
| 原ZIP本地SHA-256 | `48a23cfd87467542b2801ac9443b229a60069c76679f0c27eda4527214384f99` | 标识本次原件，不声称发布者双向验证 |
| 提取一个L2+INI+L1met | 成功，无数值改写；zipfile读取时成员CRC检查 | 逐成员路径/bytes/SHA/CRC见[manifest](INPUT_MANIFEST.json)；不是全ZIP每成员完整性审计 |
| 离线审计重放 | PASS | `audit_profile.py --check`：核SHA和确定性输出 |
| 新准入防错测试 | 5/5 PASS | 缺失非零；全局vs逐行；整数秒重复；字节篡改拒绝；人工全门改VERIFIED仍不运行/不准入 |
| 既有P1 GasTests | 8/8 PASS | 只重跑合成/解析参考测试，明确不是真实观测实验；未跑P2/P4等其他模型 |
| 核心不变 | PASS | `git diff --exit-code 16f0b59... -- cczps_lite/integration/physics_validation.py tests/test_physics_validation.py` |

命令见[README](README.md)，原始终端执行摘录归档[VALIDATION_LOG.txt](evidence/VALIDATION_LOG.txt)。测试证明代码对固定输入的行为，不证明数据质量全通过或科学假说正确。

## 实验门槛与未执行

- Stage1 `WITH_LIMITS`：NASA方法、NOAA原件与S6全文已读；IPCC全文受限、部分论文仅摘要。公开模型结果未独立重现。
- Stage2 `BLOCKED`：七项全局元数据仍未闭合；2,137条结构可用，0条获本任务定量准入。不运行P1真实换算、层差、排名或显著性检验。
- Stage3 `WITH_LIMITS`：反事实边界和守恒/误差协议形成；没有直接CH4/CO2同质量高度受控模型复跑，没有新增模拟、拟合、反演或效应系数。
- D3 `DATA_NOT_READY`、P1-A `PENDING`、PR140 `NO_VALID_PAIR`保持；AirCore成功不能替代Cooma排放/设施数据。
- 没有合并、部署、外部联系、付费、私人Council数据、凭证/权限变更或法定核算修改。

结构QC局限：有限数值sentinel的完整来源清单、供应者全QC、垂直datum、时间重构、标定转换均未独立重做；不把无NaN等于高质量。输出为结构描述而非代表性或因果估计。

## 归档审查

只纳入本任务目录；`.gitattributes`保留原件字节。归档来源为NASA/NOAA/WDCGG公开元数据和CC0 AirCore子集；不复制受限论文全文。最终提交前检查相对链接、敏感凭证模式、暂存blob与manifest SHA，以及工作树范围。软件CI/科学评审分别记录，不把Draft PR创建视为科学通过。
