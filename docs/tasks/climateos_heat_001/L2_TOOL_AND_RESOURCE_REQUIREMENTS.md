# L2 工具、人员与资源需求（不安装、不运行）

## 1. 工具路线评估

| 方案 | 适配点 | 主要风险/限制 | 进入条件 |
|---|---|---|---|
| Modelica Buildings / IBPSA 热工水力组件 | 动态管网、设备/控制和建筑模型接口；有已维护的 district heating examples | 组件假设、版本兼容、复杂度和验证责任仍在项目；不可直接视为合格模型 | 先核许可证/精确版本、组件适用性和基准覆盖；审批后最小原型 |
| Modelica / OpenModelica 自建一维组件 | 方程显式、可组合热源/罐/管网；支持 FMI 交换 | 实现验证成本高；工具生态/求解器设置需固定 | 设计包冻结，专家审查组件和时间步策略 |
| EnergyPlus PlantLoop + FMI/接口 | 建筑负荷/设备和能耗系统联算；可作为需求端或设备交叉核对 | 长距离动态输送、高差与热波传播能力要逐项证实；不默认替代专用网络模型 | 仅在接口测试与物理能力矩阵通过后考虑 |
| 专用区域供热工具（如许可商业软件） | 可能包含网络设计/泵与负荷流程 | 许可、可重复性、透明度、接口及数据驻留 | 单独采购/安全审查与 Founder 明确批准 |
| QGIS 3D 场景图 | 仅作未来有授权空间数据的概念可视化/坐标检查 | 不是热工水力求解器；当前无场址数据 | 获批空间数据来源和坐标基准后 |
| OpenFOAM/CFD | 局部三维流动、复杂接头或设备几何研究 | 成本高且超出此 L2 一维系统问题 | 不属于本设计阶段；若未来确有必要须新任务书 |

## 2. 公开文档核对点（截至 2026-11-27）

研究设计时参考官方项目文档入口：Modelica Buildings Library 文档/下载页（含版本与支持工具信息）、OpenModelica Windows 下载与 FMI 文档、EnergyPlus 外部接口/FMU 文档、FMI 标准 3.0.2、QGIS 3D Map View 文档。版本可能更新，实际批准运行时须再次核验、固定安装包哈希和许可证；此表不表示已经安装或兼容性已现场测试。

- Modelica Buildings Library 官方入口：https://simulationresearch.lbl.gov/modelica/
- 官方下载/版本与工具支持说明：https://simulationresearch.lbl.gov/modelica/download.html
- OpenModelica Windows 下载：https://openmodelica.org/download/download-windows/
- OpenModelica FMI 工具文档：https://openmodelica.org/doc/OpenModelicaUsersGuide/latest/fmitlm.html
- EnergyPlus 26.2 外部接口指南：https://energyplus.readthedocs.io/en/v26.2.0/guides/external-interfaces-application-guide/index.html
- FMI 3.0.2 规范：https://fmi-standard.org/docs/3.0.2/
- QGIS 3.44 3D Map View 用户手册：https://docs.qgis.org/3.44/en/docs/user_manual/map_views/3d_map_view.html

版本注记：本次查阅到 Buildings Library 14.0.0 发布记录及 OpenModelica 1.27.1 稳定下载页面；EnergyPlus 26.2 文档提供 FMI co-simulation 说明；OpenModelica FMI 页面区分 FMI 2.0.5 支持与 FMI 3.0.2 实验性能力。具体交叉兼容性须用未来批准环境验证。此文没有依赖这些软件运行，也没有安装任何大型软件。

## 3. 专业角色

需要：区域供热/管网水力工程师（压力、泵、气蚀、管径）；热力系统与热泵/储罐工程师；Modelica/数值方法专家；建筑负荷/终端服务专家；科学独立复核者；空间数据治理人员（只在未来获批空间数据时）。Founder/科学负责人冻结输入边界、主指标、容差及阶段门。供应商参数仅在获得许可且单位/运行条件匹配后使用。

## 4. 资源估计框架（当前机器能力未核实）

所需资源依赖节点/段数、时间范围、耦合策略、扫参数和随机试验数，当前没有可审计的 GPU/CPU/RAM/磁盘资源清单。需在获批后先做只读硬件盘点并提交估算，之后才可以申请运行。L2 一维小型网络不应默认要求 GPU；主要瓶颈可能是耦合刚性、参数扫参数或协同软件。最低资源建议由工具试运行和基准实测决定，不能在本 PR 臆造容量或工期。

未来资源申请须分开说明：软件安装包大小/依赖与许可证；CPU 核数、RAM 峰值、磁盘（输入/中间/输出/日志）；单次运行墙钟时间与总批次数；可否容器/离线部署；数据隔离与日志保留。先用解析极限和单情景估算，再申请参数研究。大型软件安装、集群/GPU 采购或外部数据访问都需另行审批。

## 5. 建议顺序

科学验收本文档 → 冻结参数字典/解析基准及独立复核者 → 选一条获批工具链并完成版本/许可证/兼容性评估 → 提交实现与测试计划 → Founder 对合成实现作明确批准 → 独立验证通过后再申请任何真实数据/P2。每一门均需新的明确决定。