# ClimateOS 生物多样性概念数据模型

概念提案，非官方数据库规范、正式计算工具或交易系统。制度依据：[生命周期](NSW_BIODIVERSITY_CREDIT_LIFECYCLE.md)；来源见[证据登记册](BIODIVERSITY_EVIDENCE_REGISTER.md)。

## 通用记录与追溯

每个对象采用稳定logical ID、不可变revision ID、parent revision、来源ID/修订、获取时间、有效时间、观察时间、空间范围/CRS、方法版本、权利状态、质量标记、复核人/时间与证据定位。哈希针对明确字节表示，不代表语义真实、官方签名或专业认可。原始数据、派生数据和解释分别记录；未知值用null及missing_reason，不补零。

下表字段是建议的最小研究字段，所有真实个人身份、精确敏感物种点位、地块权益和交易条款需要另行授权与访问控制。当前包不含此类实例。

| 对象 | 核心字段 | 来源；空间/时间尺度 | 质量、版本与限制 | 关系 |
|---|---|---|---|---|
| Land Parcel 土地地块 | parcel_id、Lot/DP、geometry_ref、CRS、area_ha、title_date、tenure、interest_constraints、existing_obligations、eligibility_state | 地籍/产权和经核查图层；地块及产权时点 | 坐标与边界来源锁定；不由遥感推产权；资格非自动判断 | 一个parcel可对应部分BSA及多次调查；BSA可跨多个产权 |
| Ecological Survey 生态调查 | survey_id、method/version、team/assessor_ref、dates、effort、weather、season、plot_ids、track_ref、raw_data_ref、QA | 现场记录；样方/路线/调查期 | 原始记录只读；缺测、未调查与未检出分开；认可人员负责正式评估 | 调查包含observations，支持Assessment |
| Vegetation Community 植被群落 | PCT_id/name/version、TEC_association/basis、zone_id、polygon、condition_class、candidate_alternatives、field_justification | BioNet+现场；群落zone及调查/分类日期 | PCT不等同TEC；保留被拒分类和理由；图层不能替代现场 | 关联Survey、Land Parcel、Assessment及Calculation |
| Species Observation 物种观测 | taxon_id/version、scientific_name、event_date、count/unit、detection_state、method/effort、location/precision、evidence_ref、sensitivity | 现场/获准BioNet记录；点/种群/调查期 | 坐标敏感性与探测偏差；旧记录不证明当前存在；去重保留原记录 | 归属Survey；支持species polygon与Assessment |
| Assessment 生物多样性评估 | case_id、purpose（impact/stewardship）、assessor_accreditation_ref、BAM_version、database_versions、zone/species_polygon_refs、baseline_refs、BSSAR/BDAR_ref、review_state | 认证报告与复核；评估边界/报告日期 | 不混淆需求和供给；认证人员、部门复核、最终批准分别存储 | 固定Survey/Community/Observation修订；产出Calculation |
| Credit Calculation 信用计算 | calculation_id、input_revision_refs、BAM_C_version、method_version、credit_class、raw_result/rounding_ref、additionality_adjustment_ref、credit_report_ref、run_time | BAM-C报告；zone/species polygon及运行时间 | 本项目不执行官方计算；教学输入单独synthetic标记；无报告不可称法定结果 | 依赖Assessment；拟议量与Registry发行量分别保留 |
| Stewardship Agreement 保护管理协议 | BSA_id、signed/effective/registered_dates、title_refs、boundary_ref、management_plan_version、actions/schedule、TFD_ref、payment_conditions、variation_refs | 已签协议、产权登记、管理计划；管理zone/长期 | 签署、登记、发行不同；20年计划不代表责任20年终止；约束未来所有者 | 关联Parcels、Assessment、Registry与Monitoring |
| Credit Registry 信用登记 | registry_record_id、credit_serial_or_block_ref、BSA_id、class、quantity、issue_date、holder_ref、status、transfer/retirement_event_refs、snapshot_date | 官方登记/ownership report；信用块及事件时间 | 原始snapshot不可覆盖；issued/held/transferred/retired/suspended不能混同；公开清单有时点限制 | 对应BSA与Calculation；供Transaction引用 |
| Market Transaction 市场交易 | transaction_id、credit_block_refs、quantity/class、buyer/seller_refs、agreement_date、settlement_date、transfer_registration_ref、price_AUD/GST_basis、TFD_payment_ref、auction_id | 获准交易凭证/公开登记；交易时点 | 合同/转让/付款分开；挂牌/批准采购不是成交；空价格不是0 | 引用Registry修订；不直接创建Outcome |
| Monitoring Record 长期监测 | monitoring_id、BSA_id、permanent_plot_refs、baseline_revision、survey_method/version、date、indicators/units、management/events、missingness、review/adaptation_ref | 现场重复调查/报告；永久点/管理zone，年度行动与通常五年生态周期 | 与基线可比；方法改变需桥接说明；因果归因另审；未监测不等于无变化 | 关联BSA、Survey、Community/Species；检验Assessment预测 |

## 关系与约束

1. Assessment引用固定的调查和分类修订。修改物种鉴定不能静默改变历史BAM-C结果。
2. BSA管理范围不是parcel总面积。Species polygon也不是vegetation zone全部面积；保留几何交叠与计算依据。
3. Registry以事件追踪信用状态；Transaction只能引用已核查状态，不能由市场表格推造发行记录。
4. Monitoring可支持或反驳预测，但不能通过“交易完成”自动填充actual_gain。
5. 同地块出现其他项目时，仅存重叠候选，需检查法律、额外性和双计规则后才能确认兼容，不自行假设ACCU/BSA可叠加。
6. 金钱单位AUD、面积ha、VI分数、个体数、类别信用和tCO₂-e必须分开；不能用通用`environmental_value`数字替代。

## 与已检查Atlas架构的映射

目标合同为#130的固定修订 `e3d8f074e0e1ba5e9614c3f4c5a2b973746b2ab7`：`apps/public-strategy-atlas/atlas-domain.js`。现有类型支持Area/SpatialUnit、QuantifiedObservation、Baseline、SourceArtifact、DocumentRevision、EvidenceAnchor、ImplementationMechanism、Activity、Outcome等。新领域对象先作为现有类型的data主题，而不是新增并行类型系统。

本包`atlas-candidate.json`沿用`atlas-domain-1`实体、断言、修订和事件结构；实体挂在现有`area`站点，关系用`RESEARCH_CANDIDATE`，`classification=LOCAL_RESEARCH`、`state=PROPOSED`、`admission=PENDING`。没有新增顶层UI站点，也没有将任何研究节点提升为官方批准。候选顺序位于route station数据中，尚非运行时导航路线。

兼容性检查使用固定修订的原生validate函数，另检查哈希、端点修订和负面变异。不宣称完整运行时verify/import、已有用户工作区迁移、来源catalogue准入或浏览器验收。安全准入需在未来授权的Atlas分支追加并回放历史，在那之前本包仅是可审查候选，不自动进入已部署Council应用。
