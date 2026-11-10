# 一次性获取审计

1. 在任何降雨数值读取前写入PLAN与PRE_REGISTERED_ANALYSIS_PLAN。两份收据记录相同SHA：PLAN `9bb6955f917ef61e77375bca3ae4aa68fb1018d0642dd8b763214324503cf87f`；预登记 `7617b4e04b47c74ef1a6bb92859d0b0fd531a9ab582c9f33175c54a65acb0510`。
2. [inventory-receipt.json](inventory-receipt.json)：2026-11-10T06:46:28Z开始，06:46:57Z完成，HTTP200，12,373,152字节；无凭证。
3. 第一次选择把GHCN FIPS国家码误当ISO，结果为空。保留 [selection-country-code-bug.json](selection-country-code-bug.json)。核查官方countries文件AS=Australia后修正程序，仍是同样三地区和按元数据距离规则；未看降雨、未改变阈值。REGIONS.json包含修正时间和九个库存原始行。
4. [archive-receipt.json](archive-receipt.json)：06:47:26Z开始，06:47:27Z HTTP404结束。收到降雨载荷0字节，未生成归档文件；不能用空文件哈希冒充原始雨量SHA。
5. 该路径来自已见官方目录版本。失败原因只证实HTTP404；“月度归档轮换”只是可能解释，没有验证。后续目录网页也不可读，不据此猜新文件名。没有尝试其他归档、单站替代、镜像或认证。
6. 预算按预登记保守计算，库存1次+归档1次=2次，实际成功1个元数据文件、成功雨量文件0个。不是两次都成功，也不是两种天气产品都取数。网络浏览元数据/论文/政策不属于天气文件获取；DMI网页预览没有成为本地准入数据。
7. 原库存保留在忽略目录 `runtime_data/enso_regional_weather/inventory`，只在本机；复算归档的九站选择可用原文件，Git不传全库存。未来拿到不同库存必须另建版本，不能覆盖本次收据。

停止是本次预登记预算和唯一任务书失败分支要求，不是自动审批拒绝，也不是Founder禁止合法研究。重新获取需要先明确下一有界批次，当前脚本遇已有收据会拒绝重试。
