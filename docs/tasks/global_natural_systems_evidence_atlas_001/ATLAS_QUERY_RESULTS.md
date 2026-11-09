# 离线查询：实际结果与复现

完整机器输出 [query-results.json](evidence/query-results.json)，SHA与双次重放记录见 [validation.json](evidence/validation.json)。所有命令由仓库根目录运行；无需网络。

| 过滤/路径 | 实际含义与预期冻结结果 |
|---|---|
| `query --country ETH --process nile_flow` | BLUE_UPPER/BASIN_NILE定性连接、N1边、NBI文献定位；埃塞俄比亚NDC提交元数据，不提供流量 |
| `query --country AU --process enso` | REGIONAL_RAIN、E2条件关联、NOAA来源；政策只是旁侧语境，不是气候系数 |
| `query --country CHN --evidence-type POLICY_ASSESSMENT` | 中国原站20标签，旧政策有效期UNKNOWN；不能解释为80%未减排 |
| `query --country MYS --evidence-type POLICY_COMMITMENT` | 无Scorecard评分；有NDC3.0登记指针，原始文件缺口保留 |
| `query --country USA --system ATM_BOUNDARY --at 2024-06-01T00:00:00Z --evidence-type PHYSICAL_OBSERVATION` | 仅BRW_EXISTING继承观测索引，不重新拟合数据；NO_VALID_PAIR未改变 |
| `query --at 2025-01-01T00:00:00Z` | 无匹配观测记录。未知时间、报道发布和检索时间均不冒充观测支持 |
| `trace --start BLUE_UPPER --end MAIN_NILE` | N1→N2；反向查询无路径，不根据边显示自动推出水量比例 |
| `trace --start CH4_SOURCE --end CLIMATE_RESPONSE` | M1→M2→M3；M3状态BLOCKED / HYPOTHESIS_ONLY，路径可检索不等于全链可计算 |

每个结果包含：单元、typed关系、claim、source URL/版本/许可、反证及unknown。筛选为AND；自然系统可输入七类英文名或具体单元ID。country支持M49/ISO2/ISO3/英文标准名（深样本的别名不一定等于M49标准名，推荐代码）。未知country返回空集，不能降级成全球结果。

`e2e` 实际调用旧比较器与PR145，结果：A METHOD_ALIGNED；B MATERIAL_CONTRADICTION；C EVIDENCE_INSUFFICIENT；三者算术解释均INTERNAL_FIXTURE_REPLAY_ONLY。四场景均insufficient_evidence_for_comparison与not_ready_for_approval。POLICY对象不进入函数输入；人类审查PENDING，REGULATORY_CERTIFICATION=NOT_PROVIDED。

不具备的查询：全球实时资料、坐标/多边形相交、面积比、事件归因、因果强度、全国/全球总排放、碳信用与最佳国家排名。Atlas没有这些能力，空值不能自动补齐。
