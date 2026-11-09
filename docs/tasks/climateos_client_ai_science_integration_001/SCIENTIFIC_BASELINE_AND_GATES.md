# 冻结基线及科学闸门

远程实际元数据见 evidence/remote-baseline.json。任务书提交 53b836250f02e4a5b346c6e30739c736eccca03f，TASKBOOK blob 7032d3fe1ac779c3f978dbfdaa66272bf6f7b94d。以 PR141 最新评审归档提交 e25ffe3e34829d9146628a7c72a363c35d8ec151 为父基线；原研究提交1daa3a15b698c5a9216e7286cf1243ef0cf870dc。未发现任务书冻结HEAD与实际远程冲突。

|对象|精确版本|事实、证据与保留状态|
|---|---|---|
|PR138 P1–P4|f9016aa4cdc728728a1a5dece0b947b1c2e5e7bc|physics_validation.py；PR评论6680664546称30物理测试、522总测试中的1项跳过；最新评论仍科学审查PENDING。P1参考数学≠独立观测准入；P2容器/P3 FOD/P4假设响应无现场校准。|
|PR139|fc450196d01c9add5edf51f599072b18e6658196|local_case_method_intake_001 README、NEXT_SESSION、validate_intake.py：23水相mg/L观测，1705流量行/311时间戳；不能充气相ppm。当前API返回评论空列表，不编造审查接受。|
|PR140|16f0b59dab966f0b66d91b7c28135e8fce9e4cc1|methane_factor_order_001/SCIENTIFIC_REVIEW_RECEIPT.md：有条件接受研究方法，3340结构匹配，科学配对0，NO_VALID_PAIR。风背景选择存在混杂。|
|PR141|e25ffe3e34829d9146628a7c72a363c35d8ec151|spatial_ghg_hypothesis_validation_001/SCIENTIFIC_REVIEW_RECEIPT.md；评论6726949537：ACCEPT_WITH_CONDITIONS，非定量准入。2137 L2/5457气象；NO_VALID_VERTICAL_PROFILE；Stage3 METHOD_READY_NOT_VALIDATED。审阅者未独立重下载ZIP或跑测试。|
|D3 / P1-A|继承上述分支冻结记录|DATA_NOT_READY / PENDING，不由本轮气象实例升级。|

航空总体气候效应不能用作同质量直接CH4/CO2不同释放高度的通用因子。水相/干空气/湿空气、浓度/通量/排放量不能混用。本轮仅气象描述统计，不运行P2–P4、SeweX、排放/高度/气候响应实验；P1数学回归允许且未导入新观测推断。

仓库旧文档与当前事实的差异：dynamic_quant CAPABILITY_AUDIT 记载旧主机路径不存在；本次路径存在并读取公开天气代码，但未证明采集正在运行。PR130描述与README分别出现v4/v8；视为跨文件版本不一致，未验证线上版本，未修改PR130。这些不是当前任务科学基线HEAD漂移，不覆写旧记录。
