# Matrix / MOI专业智能体平台评估（含数据库候选）

2026-11-05 Founder复核修订：**MOI值得作为定制ClimateOS智能体宿主继续评估；RESEARCH_CANDIDATE / NOT_BENCHMARKED。** Founder愿意支付平台与中国算力成本，免费不是前提。三天JSON是否需要换数据库，只能回答存储问题，不能代替平台适配判断。本轮仍不安装、不迁移、不登录账号、不上传或申请资源。

## 智能体平台证据与下一验收依据

重新读取[AI Studio](https://docs.matrixorigin.cn/moi/en/5.0/introduction/ai-studio.html)与[Agents](https://docs.matrixorigin.cn/moi/en/5.0/guides/ai-studio/agents/index.html)正文，官方描述知识、技能、工具及智能体资源管理。这说明它不只是数据库，值得按专业工作平台研究；不表示Founder现有工作区已开通和验证全部能力。

[托管环境](https://docs.matrixorigin.cn/moi/en/5.0/guides/ai-studio/agents/runtime-environments/managed.html)与[自托管环境](https://docs.matrixorigin.cn/moi/en/5.0/guides/ai-studio/agents/runtime-environments/self-hosted.html)官方说明正文已读。它们支持进一步设计计算接入路径，但不能据此保证WRF/PALM、任意中国GPU或并行集群直接可用。需核查具体架构、CPU/内存、MPI/容器、长作业、磁盘、网络、恢复与账单。语言模型推理算力与物理求解器资源要分别设计。

适配验收应围绕同一专业案例：知识/方法能否正确检索，跨会话经验是否恢复，工具能否受控执行，模型作业是否可观察/取消/恢复，输入和结果能否导出，用户能否看懂地图、任务、误差及证据。多工作视图是Founder的目标，本轮未直接体验验证平台布局。

[计费官方说明](https://docs.matrixorigin.cn/moi/en/5.0/guides/billing/index.html)检索可核实Credit与实例等计费边界，直接打开cache miss；不提供虚构价格。应评价付费后的能力、成本与可迁移性，不把收费作为否决理由。未新增账号操作、试用、充值或采购。

建议平台承载工作区与可用资源，ClimateOS保留方法、案例和科学接口；模型在合适环境执行。具体连接尚未实测，详见[科学与专业智能体连接复核](PROFESSIONAL_AGENT_SCIENCE_INTEGRATION_ZH.md)。下面保留的数据库比较是后端子问题，不再代表全部平台评估。

## 可确认的产品边界

[官方仓库](https://github.com/matrixorigin/matrixone)将产品定位为支持事务/分析、MySQL兼容和向量能力的数据库；这是开发方声明，不是本轮性能测试。[LICENSE](https://github.com/matrixorigin/matrixone/blob/main/LICENSE)为Apache-2.0；不能由此认定MatrixOne Intelligence/AI Studio托管服务免费或具有相同合同。

[官方GIS页面](https://docs.matrixorigin.cn/mo/en/latest/MatrixOne/Overview/feature/gis.html)检索索引标示v4.2.5、几何类型与WKT/WKB；同时提示SRID/函数边界。直接打开工具未成功，故GIS细节仅PARTIALLY_VERIFIED，不把最新索引当可执行兼容性保证。日期与经纬度列可查询不等于完整GIS；索引、坐标转换、经纬度谓词、精度及QGIS互操作仍待固定版本实测。没有以第三方宣传补齐访问缺口。

## 三种方案比较

|维度|现有文件/Git与Python|MatrixOne候选|混合方案（仅设计）|
|---|---|---|---|
|时间序列|少量JSON可复放；大批量扫描与并发弱|SQL筛选/聚合候选；吞吐、查询计划未知|数据库存观测索引，原文件仍独立归档|
|GIS|QGIS保留CRS/栅格/图层工具链|几何声明不能证明PostGIS/QGIS等价|保留专业GIS，数据库只存核实可兼容部分|
|来源与版本|Git版本+原字节SHA；大文件不适合Git|Git-for-Data是产品能力主张，不等于科学来源签名|manifest/不可变原件与查询版本绑定，拒绝丢QA标志|
|计算接口|Python明确允许的方法和预算|数据库可供数据，不承担模型物理有效性|query适配器输出相同信封，run方法独立沙箱|
|智能体API|本轮本地函数无LLM|MySQL兼容可供后端调用；AI品牌不代表安全工具门|只读最小权限账号；控制器权限独立于SQL用户|
|访问隔离|固定公开样本，未实现多租户|需要实测账号/角色/隔离和审计；本轮未核实AI Studio权限继承|数据发布审批、敏感物种脱敏留在数据库外门禁|
|部署与成本|现有运行成本低；人工整理成本可见|实例、备份、升级、运维/许可服务条款成本未知|增加两个系统的运维复杂性，不能先假设节约|
|迁移性|JSON契约和方法代码可移植|SQL兼容范围及扩展有锁定风险|保留通用导出与来源完整性回放测试|

## 后续比较的有限设计

只有数据量/并发实际成为瓶颈才申请新决定：固定开源版本和部署预算，用同一公开非敏感样本比较原JSON扫描与数据库的按区域/时段/变量查询，测冷暖缓存耗时、扫描行数、内存/存储、导出完整性、断电恢复与权限拒绝；每种几何操作验证SRID/边界/精度。源SHA、QA、日界和变量语义必须往返不丢。先证明功能等价，再衡量成本。不使用官方benchmark替代自有基准；本轮没有数值性能、价格或扩展性结论。
