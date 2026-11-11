# 同一问题，不同责任

|层级|官方能力|ClimateOS可对照点|本轮决定与限制|
|---|---|---|---|
|数据治理|UNEP GEDS来源、质量、可及性|Field/Evidence Passport元数据|LEARN；战略不是数据许可|
|综合评估|GEO-7证据与情景评估|CCZPS人类审查|LEARN；未核全文或地方措施效果|
|交换|WIS2目录、通知、取回|输入准入之前的链路|DEFER接入；未运行节点或取得观测|
|状态估计/模拟|ERA5同化；DestinE不同时间尺度|PR152假设场与PR155有限调度|LEARN；不是同等规模/预测能力|
|耦合|NUOPC初始化、时钟、连接职责|Graph.plan / CoupledPorts / advance|LEARN；不宣称实现NUOPC|
|接口|BMI生命周期、变量、时间/网格查询|ModelPort的提案语义|WRAP教学子集；不宣称完整BMI|

真实深读： [WIS2机制](research_parts/un_wmo.md)；[NUOPC/BMI机制](research_parts/interfaces.md)。
这些图都是原创教学关系，不是官方图或因果发现。

## 可复算小研究

`python apps/earth-science-expedition/research/interface_experiment.py`
实际包住已有CoupledPorts事务；三组固定合成输入各4步，对原Runtime逐字段减算差值。
结果、配置、时间序列、单位、水热残差及源码SHA在evidence/interface-results.json。
实验同时调用单独Surface端口，证实时钟前进900s而共享状态hash不变、proposal与库存不同。
这反驳了“把step改名update即可相容”的假说。

不兼容明确保留：本外壳用dict配置与list目标缓冲，官方Python规范用配置文件与ndarray；
局地短变量名未完整映射CSDMS Standard Names；get_value_ptr拒绝；固定时步，只允许整数步目标；
update_until等于当前时刻为本地no-op，不能声称完整符合规范；仅矩形条带的一小部分网格查询；
未装BMI生态组件/ESMF，未与外部模型耦合，未运行真实环境预测。时间单位s不等于已实施通用UDUNITS解析。

公有父模型公式不改，科学PENDING。只有接口行为和既有合成物理的回归得到验证。
