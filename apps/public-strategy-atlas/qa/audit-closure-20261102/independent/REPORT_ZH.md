# COI023 / 074 软件闭合读回及076验收边界

本次实际读取原任务子条件并运行精确测试；没有修改运行时、冻结作者基线或登记表。执行者同时是原80项闭合基线作者，因此这是第二次源码与实测读回，不能称为另一位独立代理审查。最终状态由父任务复核。

- COI023：建议 **VERIFIED**。五种研究类型、反证和UNKNOWN实际保留；正式决定被清楚分离/拒绝；缺源规则字段逐项拒绝。没有把正式业务权限加入软件验收前提。
- COI074：建议 **VERIFIED**。按搜索、六类过滤、跨路径比较、问题/候选、线性替代逐项检查；完整法规语料不是其软件新增前提。
- COI076：建议 **保留PARTIAL**。基本读屏实际体验仍未验证；Chromium可访问树、键盘和触摸模拟只能证明对应有限行为，不是读屏听读或专业认证。

精确8个既有原生测试和额外audit-only分类/过滤断言实际通过。父任务同步接入OP导致首次整体文件manifest变化，该回执已保留并标明；另做了模块加载时散列固定的governance/layers和补充断言，不冒充最终全量测试。

浏览器：四个既有套件及五视口线性/可访问树补充检查均在稳定运行时通过。

| 原任务子条件 | 实际观察 | 状态 |
| --- | --- | --- |
| COI-023 RULE | 带来源版本/定位/角色/适用字段的规则研究陈述；缺任一字段拒绝。 | PASS_ACTUALLY_TESTED |
| COI-023 OBSERVATION | 独立观察类型；不会因观察存在成为正式判断。 | PASS_ACTUALLY_TESTED |
| COI-023 EVIDENCE_INFERENCE | 证据推论类型保留，不与观察或规则混同。 | PASS_ACTUALLY_TESTED |
| COI-023 DISCRETION | 人类裁量研究类型保留，不变成授权决定。 | PASS_ACTUALLY_TESTED |
| COI-023 UNKNOWN | 未知类型与未知内容列表保留，不转换成确定结论。 | PASS_ACTUALLY_TESTED |
| COI-023 正式决定与研究分类分离 | L2拒绝FORMAL_DECISION；治理正式决定不获授权；WCOS judgment呈BLOCKED且governmentApproval=false。这是原要求的分类边界，不要求接入真实正式决定。 | PASS_ACTUALLY_TESTED |
| COI-023 反证、未知与来源版本 | 五种研究类型均经新增audit-only断言确认counterevidence/unknowns逐字保留、source revision绑定、officialDecision=false；坏规则的5个必要字段分别拒绝。 | PASS_ACTUALLY_TESTED |
| COI-023 证据输入与陈述分栏 | L2输入证据以inputs中的id/revisionId保存，陈述保存在data.text/judgment，规则依据在data.rule，反证与未知为独立数组；L1继续保留L0源输入。分栏保留证据链不等于证明陈述为真。 | PASS_ACTUALLY_TESTED |
| COI-074 统一搜索 | 数值/单位/源/工作搜索有真实原生断言；既有integration浏览器检验搜索结果进入实际记录。 | PASS_ACTUALLY_TESTED |
| COI-074 年度/地区/法规/来源/工作/单位过滤 | 七维（含搜索词）分别做正例/反例及组合过滤；未知范围排除。法规过滤只搜索记录引用，不承诺现行法律适用。 | PASS_ACTUALLY_TESTED |
| COI-074 跨路径比较 | 保留revision的两记录比较和独立pins路径集比较均有原生断言；实际浏览器含来源记录、冲突、未知、导出验证。 初次移动端超时被保留；父任务将重复整库验证合并为同一私有完整验证事务，既有proof语义保留，并在原限时下重跑。 | PASS_ACTUALLY_TESTED |
| COI-074 问题导航和解释性候选暗线 | 从搜索结果进入记录，发现候选展示原因、替代解释、反证和可证伪条件；错地域候选不能升为已知关系，问题/复核可记录为研究意见。 | PASS_ACTUALLY_TESTED |
| COI-074 线性文字替代 | Text route guide沿当前可见真实边给出起点和终点按钮；补充浏览器逐视口点击实际起点，检查可访问名称/角色。 | PASS_ACTUALLY_TESTED |
| COI-074 真实来源数量的单位过滤 | 直接检查635实体actual cache中38条明确单位的非合成QuantifiedObservation，含33条CSP指标；全部按同一单位保留。注册/修订时measurement展平到data，模型同时校验两层一致。 | PASS_ACTUAL_SOURCE_RECORDS |
| COI-076 390px/16:9/21:9/32:9 | 既有integration脚本在390、1440、1920、2560、3840视口运行；补充线性/AX脚本在390、1440、1600、2560、3840运行。视口模拟不是物理显示器认证。 | PASS_BOUNDED_BROWSER_CHECK |
| COI-076 键盘/触屏/低动效 | 补充脚本使用真实Chromium键盘Enter、390宽has_touch下tap事件和prefers-reduced-motion；不宣称真实物理触屏。 | PASS_BOUNDED_BROWSER_CHECK |
| COI-076 可聚焦上下文 | 源路由h1获得焦点且在视口内，线性按钮可用键盘/触摸模拟打开对应记录。 | PASS_BOUNDED_BROWSER_CHECK |
| COI-076 长表分页 | 原integration脚本加载1000条合成fixture，20行一页，点击Next table rows并断言下一页与无溢出。 | PASS_BOUNDED_BROWSER_CHECK |
| COI-076 基本可访问树/名称 | 读取真实Chromium Accessibility.getFullAXTree，检查heading/button/textbox的名称和非ignored状态，保存逐视口AX记录。 | PASS_BOUNDED_BROWSER_CHECK |
| COI-076 基本读屏实际体验 | 当前Linux环境未发现Orca或speech-dispatcher；AX树不是实际读屏会话，未听读/核对朗读顺序与交互反馈。未安装新工具、未要求购买硬件或专业认证。 | PENDING_TOOL_OR_HUMAN_ACCEPTANCE |

完整原要求、代码行号/散列、每个命令与证据路径见 [readback.json](readback.json)；逐项可筛选表见 [subcriteria.csv](subcriteria.csv)。

屏幕阅读器工具探查：{"orca": null, "speech-dispatcher": null, "espeak": null, "espeak-ng": null, "chromium": "/usr/bin/chromium"}。实际基本读屏验收是 pending，不是执行被拒绝；没有尝试安装、变更权限或绕过限制。可先使用已产生的可访问树和交互脚本，待可用工具或合适人工环境再补听读。

研究语料仍PARTIAL、官方准入仍PENDING、真实Council执行仍UNKNOWN；软件子任务闭合不改变这三者。

5份共113,733,238字节的可再生公开/合成大快照，在浏览器完成后移至 `/tmp/csoi-closure-exports-20261102`，不提交Git；没有删除证据。[逐文件回执](large-export-receipts.json)保留原路径、字节、SHA256、已实际执行的离线验证结果和新位置。proof、小JSON、日志、截图仍在QA。
