# Founder V1.6 工程验收与交接

2026 年 11 月 28 日，悉尼。PR #130 维持 Draft。验收对象为 `6776a2f4d89978917ce168320bd93000ae60de7b` 的应用代码。验收提交另存测试结果、截图、运行参数和交接记录。

| 独立结论 | 状态 | 依据 |
|---|---|---|
| SOFTWARE_CAPABILITY | PARTIAL | 已运行真实来源阅读、跨分支引用、工作分解、三本账、研究审阅、撤回、冲突与离线重放。逐站来源深度不均；真机、实际读屏器和 Founder 的 Windows 环境仍待验收。 |
| PUBLIC_CORPUS_COVERAGE | PARTIAL | 来源册有 54 条登记，含 30 个文档条目、7 个目录、17 项需求。28 个文档条目保留字节核验记录。本轮独立复验 12 份 PDF 的全部 1,962 页。正式管线的版本确认、全文提取与文档准入均为 0。独立研究层的逐页指纹和表格梳理另行统计。 |
| OFFICIAL_ADMISSION | PENDING | 正式准入文档 0、正式关系 0。当前 LEP 原文、地块图层、再利用权、正式审阅、项目支出与实际结果各有独立缺口。 |

## 实测结果

55 个原生测试文件全部通过，失败 0。Node 24.22.3 对本次实际加载、符合范围的 JS 文件测得行覆盖率 90.11%、分支覆盖率 85.15%、函数覆盖率 96.09%。Chromium 158.0.8127.0 同次依序运行六套系统回归全部通过；另有六套场景检查通过。手机尺寸属于浏览器视口模拟。最终结果、每文件统计和原机读回在 [acceptance.json](acceptance.json)、[native.json](native.json)、[browser-e10.json](system/browser-e10.json) 和 [追加场景日志](additional-browser.log)。

本地复核证据文件及受测源码摘要可运行 `python qa/continuation-20261128/verify-evidence.py`。默认可移交快照为 25,752,757 字节，其 SHA-256 从原始工程登记数据重建后，与浏览器导出独立核对一致。

## 可以直接复现的三条路径

1. **水务站 → Compare published water plans。** Nimmitabel 项目在 DP v2.5 的 PDF 61 和 OP v1.5 的 PDF 68 均出现，均印有 440/25 和 CSP 8.2。两个规划预算格都为 AUD 150,000，分别属于多年项目与年度计划。对照界面显示两个口径、来源和未知实际支出，并拒绝将两格相加。把地点切换到 Cooma 可见拒绝理由。
2. **OP 站 → Browse OP project rows → 搜索 Murrumbidgee。** 水生杂草治理行可沿印出的 CSP 6.2 跳到目标，再回查 DP 的对应公开行。OP 年度格为 AUD 20,000，DP 多年格为 AUD 60,000，可分别打开原件对应页。共享目标支持继续研究；项目成效、付款和正式实施关系仍待证据。
3. **OP 站 → 项目表中搜索 technology p.23 → row 2。** 四项计划活动分别打开自己的内容、行坐标和历史。项目名在 PDF 第 23 页跨四行。核验父单元格的上下边界、描述列及下一项目起点后，原先三个无名称续行都能归属同一项目。四行分别保留待定预算、内部/外部资源和公开引用。旧快照保留当时的缺口。

另可从水务比较打开资产计划 PDF 8、年度报告 PDF 34 和资源战略 PDF 26。管网里程、水库个数、平均供水量、历史抽样次数与水务资金边界分别有来源。536 是 2024–25 年抽样总数，合格样本数、水厂能力、Nimmitabel 的份额和项目归因仍为 UNKNOWN。

## E0–E10 执行结果

| 工程项 | 已执行与验证 | 尚存边界 |
|---|---|---|
| E0 基线 | 在最新起点重现英语启动文案回归并修复。原有 127 条内容、CSP 6.1 原件、三类核算入口、快照和本地冲突保护均复测。 | 历史失败保存在验收记录。 |
| E1 统一模型 | 在现有注册表内追加文档、项目、活动、资源、数量及来源引用。当前 922 个领域实体、48 条领域断言、1,062 个领域修订及对应事件。另保留 16 条原路网断言。 | 已印出的引用、模型断言和正式批准关系各自计数。 |
| E2 公开语料 | 重新确认 DP、OP 版次及相冲突的版本说明。12 份原件的原始字节及逐页文本、渲染摘要可重算。62 张匹配列结构的项目表含 265 个具名行。 | 全来源清单、当前法定版本及完整语义覆盖尚未确认。29 张 DP 表和 33 张 OP 表之外的其他表型未纳入该分母。 |
| E3 递归阅读 | 站点、旧内容、来源、父子层级、子树查询、分页、历史输入和反向引用连通。测试覆盖 6,000 层内容结构、1,000 层浏览器操作和 10,000 项渐进显示。 | 深度压力测试使用合成数据。来源缺失的真实站点显示具体缺口。 |
| E4 工作分解 | 265 个项目行保留为各版独立 Project，复用两个既有 Nimmitabel ID。已把纵向合并单元格分解为四个独立 Activity。可查看资源、日期、父项及印出的目标代码。依赖查询区分循环和被分页截出的先决项。 | 来源未给出的人员工时、实际进度、实付及官方依赖保持 UNKNOWN。 |
| E5 三本账 | 预算、实际支出、库存、流量、期间、单位、分母和归因分别受约束。75 个 DP 格、44 个 OP 格只含以 $ 标示的金额，币种按原计划记 AUD。限定金额和跨期格保留原义。 | 不能把同一项目的两个计划金额当作新增拨款。真实项目级实际支出与成效证据不足。 |
| E6 适用性 | LEP 站提供实际目录、旧郡范围对照、错区拒绝和有地图例外时的复核提示。时间、草案、空间粒度、版本及法律角色的反例已运行。 | 三个现行 LEP 原文端点均实测 HTTP 403。例外指向的 NSW Planning Portal 目录返回 200。地块、法律效力与生效期间继续 UNKNOWN。 |
| E7 审计 | 独立重建、外部指定摘要、来源撤回、旧版导入、字段修订、三方冲突、双标签页过期保存及离线验证都已执行。原始快照可单独重放。 | 无政府签署或外部见证。摘要证明输入与重算一致。 |
| E8 隐含联系 | 新候选固定起点图谱的事件头并重放信号、路径、反证和裁决。来源撤回后保留旧审阅，阻止新的过期批准。旧格式保留原有证明层级。 | 研究批准不产生正式政策、因果或法定关系。 |
| E9 路线优先界面 | 英语主图直接进入项目、预算、原件逐页阅读及证据历史；保留既有中文来源工作区。已检查桌面、390px、16:9、超宽视口、键盘焦点、减少动画与无障碍树。 | 真机及独立屏幕阅读器 NOT_TESTED。 |
| E10 验收交接 | 原件检查、完整 Node 文件集、真实 Chromium 六套系统回归、补充业务路径、截图和可移交命令均归档。 | 详见本目录的机器记录与 NEXT_SESSION.md。 |

## 按任务书逐项验收

| DoD | 裁决 | 判据 |
|---|---|---|
| A 任意深度站点 | PARTIAL | 遍历、压力测试与多个真实档案通过。没有将来源稀疏的站点标为内容完整。 |
| B 来源册 | PARTIAL | 分母、精确版次、权利状态及缺口可查，全网文档清单与正式版次仍待确认。 |
| C 战略到执行 | PARTIAL | 正反向打印引用、合并活动和拒绝案例通过；获授权的正式实施关系为 0。 |
| D 核算 | PASS，限已声明输入范围 | 真实公开观察和预算可追溯，水、土地、碳、资金计算及不兼容输入反例可重放。真实项目支出、碳归因与结果 UNKNOWN。 |
| E 审计 | PASS，限本地完整性 | 数值重算、来源/记录版本、事件、快照、反向追踪和并发本地保存通过。 |
| F 发现与质疑 | PASS，限研究关系 | 重放、错误地理/时间、撤回来源、保留反证与研究裁决通过。 |
| G 路线与可访问性 | PARTIAL | 已测试浏览器范围通过；用户实际设备及读屏器待验。 |
| H 测试证据 | PASS，限实测环境 | 详见 acceptance.json、native.json、system/browser-e10.json 和补充浏览器结果。 |
| I 交接治理 | PASS | 同一 Draft PR、同一分支，运行代码与证据提交可定位。没有发布或合并。 |

## 重放

在 `apps/public-strategy-atlas` 执行。测试记录给出 Node、Chromium、Playwright 和 PyMuPDF 版本。替换 Chromium 路径。输出目录用于保存截图和回执。

```sh
node --test --test-concurrency=3 --experimental-test-coverage '--test-coverage-include=**/atlas-*.js' '--test-coverage-include=**/csoi-*.js' --test-reporter=spec *.test.cjs
ATLAS_CHROMIUM=/usr/bin/chromium ATLAS_BROWSER_WORKERS=1 ATLAS_SYSTEM_QA_OUT=/tmp/atlas-system ATLAS_QA_OUT=/tmp/atlas-e0-evidence python qa/run-local-browser.py run-browser-suite.py
ATLAS_CHROMIUM=/usr/bin/chromium python qa/project-register-browser.py
ATLAS_CHROMIUM=/usr/bin/chromium python qa/plan-edition-browser.py
ATLAS_CHROMIUM=/usr/bin/chromium python qa/service-context-browser.py
ATLAS_CHROMIUM=/usr/bin/chromium python qa/input-navigation-browser.py
ATLAS_CHROMIUM=/usr/bin/chromium python qa/csoi-navigation-state-browser.py
ATLAS_CHROMIUM=/usr/bin/chromium ATLAS_NAV_OUTPUT=/tmp/atlas-navigation python qa/csoi-navigation-browser.py
node tools/materialize-project-register.cjs /tmp/atlas-verified-release.json
node verify-snapshot.cjs /tmp/atlas-verified-release.json sha256:b948f31d4ccbe9ea7fd2b6891d6afa7db194c5817f3fda4ebf8f11a49428d69e
```

PDF 原件、PDF 页面渲染和用户的本地工作区不随交付打包。将公开 PDF 以原始 SHA-256 十六进制名保存到本地，再运行 `python tools/index-public-pages.py --originals DIRECTORY`。另外用 `tools/verify-project-tables.py --dp DP.pdf --op OP.pdf` 及 `tools/verify-project-activities.py OP.pdf` 检验项目格与合并边界。动态目录若更新会产生新摘要，需按新版本登记。

## 讨论纪要与项目索引

工程上保留旧版收据并追加新版事实。原件指纹、公开计划、执行记录、实付款和正式批准的证据门槛各不相同。当前最能改变验收结论的材料，是能对上项目、期间和财务边界的支出记录，以及有授权的法律文本、地图及人工复核。

| 责任角色 | 未决事项与可执行动作 |
|---|---|
| 公开财务资料研究员 | 以 OP 项目 ID、财政年度和范围比对公开季度预算复核或经审计报表中的行，先记录原始摘要、页码、表头和归属；无法归属的数字维持 UNKNOWN。 |
| 规划及法务审阅人 | 取得可合法读取的对应日期 LEP 原文、修订记录及规划地图。先核验 Snowy River 例外，保存地图版次与地块定位依据。 |
| 文档权利人及获授权审阅人 | 核对使用许可、版次和锚点，逐级推进来源准入；保留审批人与实际批准依据。 |
| Founder / 无障碍测试人员 | 在实际 Windows 浏览器、手机和读屏器走通三条路径，记录焦点、朗读顺序、回退和可见结果。 |

项目索引词：Climate OS、Public Strategy Atlas、IP&R、CSP 6.2 / 8.2、DP v2.5、OP v1.5、Murrumbidgee、Nimmitabel、纵向合并单元格、原始页指纹、研究关系重放、LEP 旧郡范围。
