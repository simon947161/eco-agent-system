# ChatGPT只读科学评审任务包

请评审本分支唯一[TASKBOOK_ZH](TASKBOOK_ZH.md)的完成度；基线PR140 `16f0b59dab966f0b66d91b7c28135e8fce9e4cc1`。入口[README](README.md)，通俗报告[FOUNDER_REPORT_ZH](FOUNDER_REPORT_ZH.md)。提交时在PR评论固定精确研究HEAD，评审回执提交需与被评审HEAD分开。

## 请求评审的核心结论

1. NASA ATom方法可核验但数值未获；三候选封顶；实际取得AirCore原件并归档一个公开剖面。
2. 2,137条结构可用记录，不等于2,137条独立误测或独立样本。七项全局元数据阻塞，Stage2 `NO_VALID_VERTICAL_PROFILE`；保留值而不计算层差。
3. S6公开NOx/水汽反事实不是直接CH4高度试验，航空非CO2效应不能赋给纯CO2；CO2充分混合是可检验基线，不是靠假设证明H0。
4. 不用mg/m³压力响应推GWP；H0未设ε不能宣布等效；H2方向和强度未知。
5. 区域治理以工艺/监测/成本条件为准，不给未经验证的减排系数或法定主张。

## 必须挑战的问题

- 数据版本README与INI瓶尺度差异，处理为UNRESOLVED是否适当？不能把历史瓶标签自动判作产品错误，也不能无证据消除差异。
- 原件RH可能采用上升段，P/T下降段，误差、时间重构、扩散高度和气团代表性是否仍有被遗漏的混杂？
- 小数秒无重复而整数秒有138重复增量，是否保留了正确身份语义？独立样本数UNKNOWN是否充分？
- 预定义诊断层和扩散包络统计是否仅用于结构覆盖，报告是否任何地方暗示已验证层差？
- 哪些CO2结论只是模型设定？CH4直接排放与NOx诱发甲烷变化是否彻底分开？是否错误地用未读IPCC全文作权威背书？
- 方法契约的干湿基准、P/T/e单位、协方差、守恒和气体适用域是否正确？核心是CH4专用，CO2是否保持未实现？
- 未来反事实需要哪些独立验证和等效界限？是否有理由停止而不是新增候选/仿真？
- 条件治理建议是否越过设施数据、科学准入或授权边界？

## 可复核证据

[INPUT_MANIFEST](INPUT_MANIFEST.json)、原件`evidence/`、[PROFILE_PROTOCOL](PROFILE_PROTOCOL.json)、[METADATA_GATES](METADATA_GATES.json)、[PROFILE_QC](PROFILE_QC.json)、`audit_profile.py`及5项测试。8项既有P1参考测试另列；测试数量不代表科学发现。

请按文件/段落给严重性与最小修正，区分ACCEPT / ACCEPT_WITH_CONDITIONS / CHANGES_REQUESTED。请明确是全文实读、仅PR摘要、静态代码审查、接受作者测试报告，还是独立复跑。无法读取私有仓库时明确列出限制，不假称取得原件。不要执行模型、修改分支、部署/合并或提升科学准入。Founder批准与本评审结论相互独立。
