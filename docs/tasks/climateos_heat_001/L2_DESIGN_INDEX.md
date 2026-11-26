# ClimateOS HEAT–001 L2 文档设计包

状态：Issue #181 已获 Founder 批准 L2 有界设计；本包等待 Founder 科学验收。仅文档设计，无模拟运行、无求解器实现。

## 交付文件

1. [有界科学任务书](L2_BOUNDED_SCIENTIFIC_BRIEF.md)
2. [一维方程与边界](L2_1D_EQUATIONS_AND_BOUNDARIES.md)
3. [空间场景与多物理接口](L2_SPATIAL_SCENE_AND_INTERFACES.md)
4. [未来实验设计与证伪矩阵](L2_EXPERIMENT_DESIGN_AND_FALSIFICATION.md)
5. [验证、确认与阶段门](L2_VERIFICATION_VALIDATION_AND_GATE.md)
6. [工具、人员与资源评估](L2_TOOL_AND_RESOURCE_REQUIREMENTS.md)
7. [中文 Founder 报告（10 页）](L2_FOUNDER_REVIEW_CN.md)
8. [A–C–B 热工水力接口 SVG](figures/l2_thermo_hydraulic_system.svg)
9. [验证阶梯 SVG](figures/l2_verification_ladder.svg)

两张 SVG 为直接编辑的矢量源。#177 的五幅原研究图保持不变并由固定提交引用。

## 来源锁定与依赖

- Issue #181：L2 有界设计正式任务书及 CRP。
- P0 科学审计 Draft PR #174：HEAD de0b951e5644696e956c20cc03ab848e5742be70。
- P0-A 空间实验 Draft PR #177：HEAD 369ee6b9703fedb54ca4da684920e6c23825d6ca；A 为稳定合成余热源，C 为热泵/可选水罐站，B 为一个季节聚合需求；L/T 和五幅图沿用此版本。
- P1 合成能源账本 Draft PR #179：HEAD 5a2039a2753142b2eb17665da2dba6c4a8648b14；Founder 已接受并冻结，仅作为合成会计基线，不修改、不重算。
- ARCH–P0 架构研究 Draft PR #180：HEAD 4c078aefa90ea9206dd789578682b489bf27e29e；复用其稳定 ID、场景语义、provenance/uncertainty passport 和 L0–L4 保真度门。
- main 基线：9eb7577e145e76161f9f1cd8509348b19c2904cc。

本分支只增加本包文档，不修改既有 #174/#177/#179/#180 内容；提交后将以 GitHub 交叉引用评论连回 P0-A/P1/ARCH 讨论，保留它们原 HEAD。

## 固定系统与空间输入

A–C 低温段、C–B 高温段，均为供回水成对管；没有 A–B 第三段或额外需求节点。L 低温/高温概念沟长 80/40m、高程 A/C/B 为 0/+2/+3m；T 为 120/180m，高程 0/+6/+3m。沟长是单程概念输入，不是真实测绘坐标或双管总长。R0 锅炉、R1 本地 ASHP 与联网布局按 P1 冻结的同等逐时服务和期末库存口径比较。

## CRP

- **Knowledge**：P1 L1 能源会计 ≠ 瞬态一维输送/水力 ≠ 3D CFD；已知几何与动态参数不等于现场测量。
- **Idea**：只在遗漏的延迟、压降或热惯性可能跨越预注册决策线时，才需要更高保真度。
- **Wish**：让空间热系统研究可追溯、可证伪、有人类审阅。
- **Reasoning**：先固定边界和方程，再以解析基准、守恒、收敛、独立复核证据判断决策价值。
- **Decision**：P1 已接受且冻结；L2 只文档设计；P2、真实场址、安装和模拟仍冻结。
- **Questions**：管/泵/HP/罐参数来源、独立复核人、工具版本/许可证、GPU01 资源均待未来审批/核验。
- **Next**：Founder 科学验收本包；后续仅在新决定后启动。
- **Keywords**：HEAT–001、MVTEE、A–C–B、L/T、transient 1D、pressure、thermal inertia、falsification、GPU01。

## Founder 决策门

报告最后提供三项未来选项：APPROVE L2 SYNTHETIC IMPLEMENTATION / REQUEST EVIDENCE OR REPAIR / HOLD。当前状态是等待 Founder 科学验收，交付即停止。文档验收不授权实现、数值运行、真实数据访问、P2、部署或合并。
