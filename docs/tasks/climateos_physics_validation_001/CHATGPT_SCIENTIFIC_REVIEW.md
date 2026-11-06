# 提交ChatGPT科学评审

请评审CLIMATEOS-PHYSICS-VALIDATION-001受限合成/参考计算包。Founder授权原文见FOUNDER_AUTHORIZATION.md。先读12页报告，再从CSV/JSON、源码、测试和哈希独立复算。

希望重点确认：

- P1干/湿摩尔分数与实际/参考体积的质量一致性、单位和声明的理想气体边界。
- P2纯甲烷箱单向阀假设、Euler正性约束、解析斜坡oracle和守恒积分是否足够；不把该构成关系认作真实填埋物性。
- P3 IPCC2006年度公式、下一年年初起算、初始继承库存、cohort、16/12、回收后氧化与Gg/kg是否一致；合成值不得冒充官方算例结果。
- P4两种C1是否与同一C0中性精确重合；年度piecewise常数处理、时序/积分和参数网格是否足以验证实现；对未校准温湿响应的限制是否充分。
- 守恒指标、测试、报告QA与独立观测验证的分层是否清楚。软件通过不应使D3或P1-A科学准入升级。

请求返回ACCEPT_WITH_LIMITS / REVISE / REJECT及具体问题。当前状态REVIEW_PENDING，无评审结论自授权。任何新场址、外部数据、自由参数拟合或扩展物理过程均等待Founder决定。
