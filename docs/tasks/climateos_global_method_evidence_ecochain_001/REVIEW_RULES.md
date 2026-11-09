# 离线分层技术评审规则 v1（待接入提案）

实现：[reviewer.py](reviewer.py)，契约：[CLAIM_EVIDENCE_SCHEMA.json](CLAIM_EVIDENCE_SCHEMA.json)。**只接收三个作者合成包的封闭语义，不是通用环境申报审计产品。** 法规研究矩阵不等于法规求解器。独立专家仍须审查公式适用、原件与治理权限。

七个接口：CLAIM（claim_id、范围、支撑证据、分接口输入与报告值）；METHOD（ID/法域/版本/报告年/公式）；SOURCE_LICENCE（来源ID、origin、许可、payload与SHA）；DATA（气体/相态/单位/干湿/体积基准、时间/时区、空间/CRS、仪器/校准、缺测与不确定性）；CALCULATION（冻结代码SHA、氧化次数、横向去向）；REVIEW（申报者/审查角色ID与权限）；OUTCOME（请求范围，不作为可信结果）。

JSON Schema只规定封闭结构/类型；所有对象禁止未知字段。Python实现了本schema使用的有限子集，不宣称通用JSON Schema引擎。字符串语义、方法/单位白名单、有限数值、引用和角色由确定性规则检查。未实现任意附件路径/网络抓取/LLM执行入口。

|顺序/规则|实际检查|失败结果|
|---|---|---|
|R01|结构、额外字段、NaN/布尔伪数值、schema版本|MATERIAL_CONTRADICTION，拒绝路由|
|R02|来源在审阅Git树中的冻结registry；payload SHA与registry一致；origin不能将合成改为真实|篡改为MATERIAL_CONTRADICTION；未登记为EVIDENCE_INSUFFICIENT|
|R03|许可一致；claim指向源；原始fixture输入逐字段对上，重复证据/claim拒绝|缺许可/引用不足；原输入矛盾/重复为MATERIAL_CONTRADICTION|
|R04|方法法域/版本/报告期与作者合成方法完全一致；禁止改称NGER/ACCU|MATERIAL_CONTRADICTION；方法维度NOT_ASSESSED|
|R05|CH4总物种质量、同一区间、空间四接口、L未知；单位/相态/干湿/参考态/时区明确|已知错配为矛盾，UNKNOWN为证据不足|
|R06|原始流量证据、校准、仪器和不确定性标识；本轮完整包只能写SYNTHETIC_NOT_FIELD|缺证据不能因为算术正确而通过|
|R07|只读调用PR144四接口/CH4/C守恒；报告值核对；禁止重复氧化与离界假减排；冻结core SHA|质量、输出或代码矛盾拒绝；允许把条件算术单独标RECALCULATED|
|R08|外置fixture角色表；申报人与审查人不同，组织不同、无登记COI；拒绝未知/伪审批|冲突为MATERIAL_CONTRADICTION；未知为EVIDENCE_INSUFFICIENT|
|R09|任何EFFECT_VERIFIED、ISO/法定认证或Founder批准自称|MATERIAL_CONTRADICTION；实际输出始终NOT_PROVIDED/NOT_ASSESSED|
|R10|事件顺序、前向hash、外部head、角色、修订新hash、撤回后不继续评审|拒绝事件；不改旧记录|

每个claim独立输出method/arithmetic/evidence/effect、理由、字段指针、补证动作、适用范围、审查来源。包级status仅便于路由，不是总分或认证标签。一个claim的局部错误不改变其他claim的算术结果；全局单位/许可/治理问题影响所有关联claim。`METHOD_ALIGNED`仅指**作者合成账方法**一致，不是AU/US法定符合；`RECALCULATED`可与`EVIDENCE_INSUFFICIENT`并存。

哈希约定：JSON对象以UTF-8、sort_keys、紧凑分隔符、allow_nan=False规范化后SHA256；原始ZIP按字节；冻结Python源码按LF归一化，兼容Git换行。审查包不能自行提供新的可信registry。registry属于待审Git树，仍必须由人固定commit；它不是外部信任根、签名、认证系统或防管理员重写机制。

事件链支持 SUBMITTED → REVIEWED → OBJECTED → CORRECTED → REREVIEWED → WITHDRAWN；可在允许节点撤回。补正须新包hash，撤回不删除旧证据。`verify_events(events, expected_head)`检查外部锚定头；没有外部锚定时，攻击者可重算整条链，因此**不声称区块链不可篡改性**。事件ID在本轮仅测试夹具，未为真实项目颁发审查意见。

保密设计：未来包要声明公开/授权审阅/不可发布原件；公开索引仅存允许披露字段及hash，受限原件留原授权存储，审查者需授权凭证。此原型只处理自有合成与CC BY公开数据，未实现生产ACL或私有材料存储。遇到受限材料应停下补授权，不把hash视为许可。

迁移映射：旧Evidence Passport的 `passport_id → package_id`、`claim_id/supporting_evidence_ids`保留；`gaps → failures/remedy`、`version_conflicts → method/reporting_year failures`、`human_review_required → human_review=PENDING`。这是语义映射提案，不声称通过Bondo原schema，也不修改旧human_scientific_approval。
