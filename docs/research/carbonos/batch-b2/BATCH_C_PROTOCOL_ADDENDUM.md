# Batch C 协议补充 — PROPOSAL_ONLY

继承[Batch C协议](../batch-b/EXTREME_CLIMATE_MULTIGAS_RESEARCH_PROTOCOL.md)，不运行实验。

增加数据合同：climate_index={source,issue_time,valid_time,observed_or_forecast,version}；process_measurement={site_id,process_id,variable,unit,depth,interval_start/end,timezone,QC,method,uncertainty}；gas_observation={gas,biogenic_or_fossil,boundary,flux_or_concentration,unit,method,background,control_state}；factor={formula_id,source_version,valid_reporting_period,GWP_horizon,GWP_version}。

ENSO/IOD/SAM需取得带日期的官方记录后才能形成状态判断，本轮未选择事件或下载指数。气温是proxy，不替代塘温/填埋体温。先注册极端阈值、季节匹配、滞后窗口和操作混杂，再查看气体结果；当前未选数值阈值。CH4生成/氧化/收集/销毁分开；N2O需氮负荷/DO/redox；化石/生物源CO2分开；购电按年份/区域因子，制冷剂按设备工质和质量账。未测量不作0。

三个账本：物料能源、历史方法、环境通量。禁止重复计入回收气体及替代电力。准入要求稳定设施身份、许可允许、时间对齐、测量方法、独立参数审查、可复算测试计划，以及Founder另行实验批准；B2两条候选尚不满足。
