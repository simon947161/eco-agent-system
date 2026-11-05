# 平台无关工具契约 v0.1

入口实现：`cczps_lite/integration/dynamic_quantification.py`。本轮是离线Python函数适配层；不是HTTP/MCP服务、通用插件系统、LLM或数据库。平台无关指JSON信封及科学边界不依赖MatrixOne，不能理解成已跨平台部署。

## 六工具映射

|接口|本轮行为|现有复用/科学门|
|---|---|---|
|get_environmental_context|实现固定公开站点、日期、变量、单位、CRS准入|拒绝地点和日界替换；不自动解析任意地名或QGIS|
|query_observations|实现一份固定NOAA收据的原字节回放、QA、完整日覆盖|复用meteorology_connector.parse_observation数值映射；保留TMAX语义，不使用其自动时间标签|
|run_verified_model|仅daily_descriptive_mean/1；至少3天|名称是预留契约；本轮只是描述算术，SOFTWARE_TESTED_NOT_SCIENTIFIC_MODEL_VALIDATED|
|compare_scenarios|始终REFUSED/SCENARIO_MODEL_NOT_ADMITTED|没有对照和模型就没有开发前后影响结论|
|check_regulatory_context|返回NOT_ASSESSED、legal_effect NONE|不调用133/134法定计算，不进行法律推断|
|generate_evidence_report|生成固定结构中文报告|报告来源、统计语义、缺口；不让自由文本改变工具权限|

## 实际v0.1请求

完整样例见[evidence/request.json](evidence/request.json)。schema_version、question、source_id、coordinates（经度在前）、crs、start_date/end_date、time_basis、variables、permission、model_id全部必填。仅EPSG:4326、指定站点坐标、public_read_only、两种明确变量和单位获准。日期严格ISO，最多31日，不允许反向区间。这个上限是软件预算，不是科学充分性阈值；3日同样只是演示方法最低覆盖规则。

原数据输入bytes；来源URL、检索完成时刻、权利依据、哈希、单位和日界由受版本控制的收据绑定。禁止把调用者填入的rights_review当独立权利证明；它是本研究已审阅的静态信任根，生产服务必须另外认证收据发布者。SHA只证明与收据字节相同，不证明政府签名或无人篡改。源码和收据共同Git审查；没有远程鉴权，也不声称能抵抗恶意本地主机。

## 扩展合同，而非已实现功能

未来任意地区适配至少补齐：geometry类型与CRS/垂直基准、站点/网格足迹、时区和采样/聚合区间、变量高度与单位、原文件及获取方式、权利/敏感级别、QA标志解释/缺失比例、模型ID/版本/参数/边界/校准域、假设、不确定性、审批主体/范围/到期、来源父子关系。字段不齐应拒绝，不默认有效。当前固定站点没有气体高度参数，也不提供未知模型参数入口。

输出包括status、agent_version、按顺序trace、观测日期/变量/原QA、source_sha256、方法/验证状态、单位、不确定性、法规状态和中文报告。记录按日期排序，缺测不填0，非有限值拒绝；未通过任一门的响应没有result或report_zh。仪器误差和代表性误差明确未量化，不伪造概率区间。

## 科学权限与内部能力等级

L0检索、L1观测解释、L2模型、L3情景、L4法定资格只是内部分类。本轮仅L1与描述统计；L2—L4没有获准科学服务。主控制器依次取上下文→查观测→允许方法→法规状态→中文报告，最多五工具，无自主重试/网络/写库/子智能体。拒绝随时终止；有trace不等于科学验证。JSON原始大小100KB、最多31行，不解析宏和外部链接。MatrixOne未来只是替换query适配器，不能绕过任何门。
