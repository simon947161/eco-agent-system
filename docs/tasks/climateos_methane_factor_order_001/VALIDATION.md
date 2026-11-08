# 验证记录

2026-11-08，本地Python标准库执行。

- `python -m unittest discover -s docs/tasks/climateos_methane_factor_order_001 -p test_audit.py -v`：5项PASS（缺失/非有限数、重复时间、UTC小时语义、精度阻塞、真实输入排除守恒与高度）。
- `python -m unittest tests.test_physics_validation.GasTests -v`：既有P1参考测试8项PASS；未运行P2–P4或新观测实验。
- `audit_observations.py --source-dir ...`：原ZIP SHA与发布者SHA一致；气象SHA核实；生成归档子集及质量JSON。
- 不带source-dir的离线执行核验固定输入SHA，重新生成同内容JSON；不访问网络、不插补。
- 原始来源含尾随空格及不同换行。首次暂存检查发现这些上游格式；未修改原件，使用仅本目录的`.gitattributes`保留evidence字节并排除其空白风格检查，研究文档和代码仍正常检查。
- 所有新修改限定本任务目录；旧任务书和P1实现保持不变。任务书第7节精度闸门触发，故不创建REAL_COMPARISON.md，不计算实际差异。

安全审查范围：公开NOAA数据及ICOS/WDCGG元数据、来源HTTP记录；没有账户令牌、Council私人材料、现场控制或部署配置。HTML作为证据快照存储，不作为本地应用运行。记录中的公开科学作者联系字段属于原产品元数据，不用于联系或获取权限。

局限：输入指纹证明字节一致而非测量准确；本地测试不替代独立科学评审，也不代表CI已通过。远程CI与最终精确HEAD以新PR状态及评审提交评论为准。
