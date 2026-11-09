# 长期知识与证据索引（待正式接入）

|知识节点|权威/冻结入口|复用方式与成熟度|
|---|---|---|
|K01 机制与因素|[PR143机制网络](../climateos_methane_physics_knowledge_engine_001/MECHANISM_GRAPH.json)、[公式](../climateos_methane_physics_knowledge_engine_001/EQUATION_REGISTRY.json)|引用70因素/14节点；不重新给普适影响百分比|
|K02 澳洲法源|[PR144七层知识包](../climateos_au_landfill_methane_methods_001/METHOD_KNOWLEDGE_INDEX.md)|继承条款/变量/反例/学习题和来源缺口|
|K03 全球制度差异|[来源](GLOBAL_SOURCE_REGISTER.md)、[crosswalk](JURISDICTION_METHOD_CROSSWALK.md)|9新主题；4法域对照，NZ有限；非全球穷尽|
|K04 统一证据接口|[schema](CLAIM_EVIDENCE_SCHEMA.json)、[规则](REVIEW_RULES.md)|独立提案；语义映射旧Evidence Passport，不覆盖旧schema|
|K05 分层技术审查|[三包与结果](REVIEW_EXAMPLES_AND_RESULTS.md)、[角色](REVIEWER_ROLE_AND_INDEPENDENCE.md)|IMPLEMENTED_SYNTHETIC_TESTED，真实独立人审PENDING|
|K06 真实片段|[开放案例](OPEN_DATA_CASES.md)、[原始数据许可](evidence/open-case-acquisition.json)|真实液相浓度转换可复算；非全场减排准入|
|K07 治理记忆|[审计](EXISTING_ECOCHAIN_AUDIT.md)、[原memo](ECOCHAIN_GOVERNANCE_MEMO_2026-11-09.md)、[待迁移索引](ECOCHAIN_INTEGRATION_STATUS.md)|ECOCHAIN_CANONICAL_NOT_FOUND；Enotebook PENDING_INTEGRATION|

学习顺序：先读Founder报告和三包结果，再读四边界质量账，然后比较法规用途，最后读证据接口/独立审查职责。学习问题：为何C算对仍不能通过？为何L=5不是减排？为何HH-8不能称全场直接实测？为何SHA不能证明数据真实？

后续接口仅登记，不实现求解器：堆肥（好氧/厌氧热点、CH4/N2O通量）、厌氧消化（负荷/产气/泄漏/能源）、畜牧（动物/饲料/粪污边界）、稻田（水分/管理/季节）、污水（溶解/逸散/污泥/气体分配）。各自必须新增版本化方法与独立验证；不能把填埋场schema强行当其科学模型。

版本更新规则：来源改变→新source版本与差异；规则改变→新rules版本与回归；主张改变→新包hash及CORRECTED事件；旧结论保留且可撤回。所有新知识先独立ChatGPT/Founder评审，不改旧学习记录或科学准入。
