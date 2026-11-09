# 最小契约 v1：证据服务，不是通用科学代理

实现链：request.json → client_ai_evidence.execute → 固定来源与哈希 → dynamic_quantification.run_agent → audit.json + station.geojson + 中文报告。闭集中文问题匹配，未知问题拒绝；没有LLM理解、网络API、数据库或客户门户。principal来自可信本地调用者，不能冒充真实身份认证。部署前必须替换为独立验证的身份系统，本轮不开发。

## 逻辑实体（设计合同，不声称全部已实现）
|实体|键及关系|必填语义|
|---|---|---|
|Project|project_id, tenant_id|owner、合法目的、角色、授权/保留日期|
|Site|site_id→Project|几何、CRS/datum、空间代表性、位置来源|
|Asset|asset_id→Site|物理设施与处理单元区分、运营有效期|
|Monitoring Point|point_id→Site/Asset|测量位置、方法、坐标精度；不得将点当设施|
|Observation|observation_id→point/source|变量、相态、单位/基准、起止日/时区、值或缺失原因、QC、不确定性|
|Sample|sample_id→point|采样起止、介质、保存条件、监管链|
|Laboratory Result|result_id→Sample|分析方法、校准、LOD/LOQ、检出/未检出、单位；未检出非0|
|Geo Layer|layer_id→SourceReceipt|几何、CRS/datum、分辨率、范围、版本|
|Source Receipt|receipt_id|URI、获取时间及依据、原始SHA、版本、归属、Licence链接|
|Licence|licence_id|权利人、用途/地域/再分发限制、核验来源及日期|
|QA Status|qa_id→输入|规则版本、通过/拒绝及行号、未知、不可恢复缺口|
|Model Run|run_id→输入+方法|代码版本/哈希、模型许可/准入、授权、单位、结果、holds|
|Review Decision|review_id→精确commit|审查人、范围、判定、回执URI、后续权限，不自动继承批准|

实际实例只实现单站Observation、来源receipt、固定许可、QA、描述方法与GeoJSON输出。Project/Asset/Sample/LabResult及生产审计存储为DESIGN_ONLY；不把设计实体数当工程完成数。

## 主题与权限
meteorology/station_daily仅允许登记描述统计。PFAS水/土、CH4大气干/湿、CH4溶解态、填埋生成/逸散、水文/地下水分别有独立schema及模型登记；当前全部拒绝计算。mg/L≠ppm；没有相态、温压、基准与方法不能自动转换。

PUBLIC_OPEN_DATA_ADAPTER = IMPLEMENTED_LOCAL。本例公开数据属NOAA，public-demo是用途命名空间，不占有原始数据。角色仅local public-demo-reader、目的research_descriptive；其他principal/tenant拒绝。CUSTOMER_AUTHORISED_ADAPTER、CONDITIONAL_PARTNER_ADAPTER = DESIGN_ONLY，需数据所有者书面授权、用途最小化及合同后才能实现。无Council内部材料。

原始文件只读，固定大小/路径/哈希；禁止任意上传、UNC、目录跳转、链接、可执行文件、替换许可和擅自改模型。哈希证明字节一致，不证明来源真伪或科学真实性。更换输入/许可必须人工更新信任根并重审，不能由请求自报批准。QA失败没有数值结果；缺失不填0。外部CSV/GeoPackage/Lab CSV均未实现导入。

## 生产前合同（本轮不实施）
需分别授权reader/analyst/reviewer/admin，服务器端身份映射租户、最小权限、用途限制及逐对象隔离；不得仅信请求tenant_id。敏感/商业秘密默认拒绝入公开Git。客户原始数据加密不可变存储、授权派生物、撤销与删除执行证据；保留期限须合同明确，不能无限保存。Git历史无法保证彻底删除，因此本例仅公开数据；生产删除应保存不含原文的最小审计墓碑并依合同处理备份。

输出audit保留hash、schema、方法、计算状态、证据等级、holds、reviewer、拒绝原因、来源及结果文件。当前成功拒绝行数0；任一数据错误会拒绝整个批次，错误不产生部分成功值。生产日志完整性、并发、撤销、审计留存和恶意仓库维护者威胁尚未验证。只读证据链接可供未来Evidence Reader/Kitty适配，但当前分支没有已证实的自动ChatGPT投递接口。
