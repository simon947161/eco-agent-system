# 验证范围与真实证据

本地软件状态LOCAL_VERIFIED；研究交付REVIEW_READY_WITH_SOURCE_GAPS；科学准入PENDING；DEPLOYED=false。不把单元测试或GitHub检查冒充独立现场科学验证。

|检查|真实证据/命令|解释|
|---|---|---|
|11项本任务测试|[tests.txt](evidence/tests.txt)；`python -m unittest discover -s docs/tasks/climateos_au_landfill_methane_methods_001 -p test_mass_balance.py -v`|3手算场景，接口/CH4/碳闭合，缺测/负/NaN，年度小时/单位，相态/许可/校准/版本，体积干湿/参考温度，运行覆盖与图断链|
|19项冻结参考回归|同日志；`python -m unittest tests.test_physics_validation.GasTests tests.test_methane_knowledge_engine -v`|只跑P1与PR143受限链；不执行P2–P4新模拟，不重跑全仓数值研究|
|确定性重放|[replay.json](evidence/replay.json)|3个输出JSON连续执行逐字节相同；输入/输出在manifest内|
|原件字节核对|[package-validation](evidence/package-validation.json)、[原件收据](SOURCE_REGISTER.md)|8个取得原件SHA/大小匹配；4个403不编造SHA；新克隆缓存缺失单列RAW_NOT_CACHED|
|文件/知识/链接|[manifest](manifest.json)、验证器结果|源笔记七层、8来源、公式有定位/变量、每源3练习；相对本地链接存在；文件SHA用LF规范化|
|旧代码/任务保护|[github-baselines](evidence/github-baselines.json)、`git diff <PR143> --name-only`|仅本任务目录变化；任务书blob固定；旧科学状态JSON逐项检查|
|公式原页核对|[web-observations](source_receipts/web-observations.json)|ACCU PDF38/39/42/45/46页用本地Poppler渲染；Eq10/11/15/17/18目视检查；原图不入库|
|隐私/权利|窄模式凭证扫描、待提交文件清单审查|无私人Council材料、外部联系、凭证或版权原件；窄扫描不宣称全面安全证明|
|远程CI|最终Draft PR交付评论固定D和实际CI查询结果|本轮文件在docs/tasks，既有workflow按cczps_lite/tests路径触发，可能不触发；无run时必须记NOT_TRIGGERED，不能写CI通过|

本任务没有新增依赖、服务、基础设施或部署流程。无需网页/手机验收：唯一任务书本轮要求可读报告和知识包，没有要求新增Slides站点；沿用Markdown与Mermaid图，未修改私人网站。

初次包验证暴露一个自举顺序错误：链接检查先要求尚未生成的manifest/验证结果存在。已限定仅`--write-manifest`自举步骤跳过这两项，普通验证仍必须检查它们；后续普通验证通过才记录最终PASS。没有通过删除内容链接规避失败。

链接检查还发现方程的方括号紧邻括号会被Markdown误当链接；已将表达式正确标为代码，并让扫描器忽略代码段。最终验证保留所有真实相对链接检查。

## 重要的验证局限

通过的是输入约束与算术，不是实测源强、设备DRE或参数可辨识性。账本接口输入由作者指定，闭合不能证明它们是真值。合成输入无统计误差分布，实测不确定性UNKNOWN。来源F正文受阻，E-landfill有限阅读，完整法规适用/审计与NGER site-plan附件未闭合，均不是“通过”。

## Git交付防自引用

R保存研究内容/测试/manifest；D仅补两份交接JSON的R/PR链接/发布状态。manifest排除自身、机器校验结果及这两份D元数据，排除项明示；最终评论固定D，审查人必须核R..D仅两文件。原件receipt精确字节SHA不受LF规范化影响。

复核器检查tracked diff和固定Taskbook，提交前另查看untracked/staged范围，防止将缓存或其他任务加入。提交后核本地HEAD、远程branch HEAD、PR HEAD一致；Draft/open/unmerged。远程CI无法验证的内容明确保留限制。
