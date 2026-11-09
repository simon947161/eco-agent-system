# 三类合成申报及实际结果

输入：[A](examples/A.json)、[B](examples/B.json)、[C](examples/C.json)；实际输出：[review-results.json](evidence/review-results.json)。三包共用PR144三个作者合成情景，不新增真实设施模型。程序不把作者/维护者假装成独立人审者。

|包|构造与实际输出|可解释性|
|---|---|---|
|A|三claim均METHOD_ALIGNED + RECALCULATED；evidence=SYNTHETIC_ONLY|单位、边界、版本、原始fixture、许可与模拟角色匹配。只说明自有合成账能复算|
|B|三个claim均MATERIAL_CONTRADICTION|把总CH4质量改称ambient_air/ppm，氧化两次，把离界当减排；第三claim还删除5kg L，触发原件差异和守恒失败|
|C|三个claim均EVIDENCE_INSUFFICIENT，算术仍RECALCULATED|相同数值但raw_flow_evidence/calibration/licence为UNKNOWN。不是“真实数据不齐却模拟成真实”，是缺证据的作者测试夹具|

独立于调用结果的手算oracle（kgCH4/作者区间）：

```text
未捕集：       110 = 15 + 95
捕集/火炬：    110 = 15 + 32.7 + 62.3
氧化/泄漏：    110 = 15 + 31.08 + 58.92 + 5
C元素输入：    110 × 12/16 = 82.5 kgC
第三情景：     E_inside = 24 + 6 + 1.08 = 31.08 kgCH4
```

第三情景L=5kg只表示离开所设边界，最终去向UNKNOWN。不能拿三情景差值当真实措施效果或全国排放。所有结果effect=NOT_ASSESSED；REGULATORY_CERTIFICATION=NOT_PROVIDED。

PR143链A也实际只读重放：[chain-a-replay.json](evidence/chain-a-replay.json)。2ppm等合成输入的浓度约1.039964673 mg/m³，实际/参考体积质量守恒；沿用原P/e协方差假设和一阶误差，不增做真实排放、辐射或气候模拟。旧代码未改。

47项新增针对性测试覆盖每类结构/单位/气体/相态/干湿/体积基准/时间/时区/空间/法域/版本/报告年/氧化/离界/许可/校准/来源/真假标识/越权/角色/hash/原件链接/重复/撤回等；另30项既有回归。详见[QA](QA_AND_VALIDATION.md)。负例只在测试中变更A副本，没有无限增加候选或创建生产规则。
