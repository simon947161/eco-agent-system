# 开工只读核查与复用决定

核查日期：2026-11-26，Australia/Sydney。最新远程 main：`9eb7577e145e76161f9f1cd8509348b19c2904cc`；交付前再次核对未变化。29个指定源 PR 的真实 HEAD、开放、Draft、未合并状态见 [快照](REMOTE_PR_SNAPSHOT.json) 与 [复核](REMOTE_RECHECK.json)。没有把未合并研究核心拼接到主线。

## 现有网站与接口

| 所在版本 / 模块 | 实际情况 | 本次决定 |
| --- | --- | --- |
| main `cczps_lite/dashboard/` | 已有原生 HTML/CSS/JavaScript 静态站，含人话解释层与既有 forest/paper 设计变量 | 在其 `science/` 下增加中文入口；直接引入 `../styles.css`，局部样式覆盖；旧导航新增一个链接 |
| main `environmental_question_runtime/static`、`scientist_runtime/static` | 与服务端运行、审批流程相关 | 不把只读解释变成新的研究执行入口 |
| #129 `apps/regional-public-os` | Worker 与地方证据/Owner 流程，历史交接有私有发布与未发布模块之分 | 读取公开交接与架构；不复制服务、私有配置或数据 |
| #130 `apps/public-strategy-atlas` | 独立地方政策模块，另有自己的基线与访问边界；当前 HEAD 不等于旧说明提及的历史版本 | 仅登记元数据与边界；不把其受限工作流嵌入科学网页 |
| #157 `apps/earth-science-expedition` | 未合并分支已有独立学习网站，与 `docs/research/world-science-expedition/INDEX.md` 配套 | 借鉴故事、证据折叠的阅读方式；引用原索引，不复制成第二套平台 |
| 各物理 / 耦合研究分支 | 原代码、测试与输出分布于不同 Draft PR | 网页以固定 SHA 链接它们；没有移植求解器、计算接口或研究运行时 |

本次静态页只使用随页面打包的解释内容、状态元数据及归档展示值。无自动外网请求、登录、数据库、后台代理、私有 API、外部字体或分析追踪。内容安全策略 `connect-src 'none'` 限制脚本网络连接；外部证据由读者主动点击打开。

## 现有索引与交接

读取了主线治理文档（AGENTS、README、ROADMAP、CONTRIBUTING、project-principles）。主线未找到覆盖本轮所有研究的统一 `INDEX.md` / `NEXT_SESSION.md`，因此只新建本任务交付索引，继续把研究维护权留在原分支。

- CarbonOS：#132 的 `docs/research/carbonos/INDEX.md`、`NEXT_SESSION.md` 与 D3/P1-A 入口；D3 未准入，P1-A 待评审。
- 甲烷与自然过程：#135–#155 各任务的 README、交接/限制文件及公开评审记录；#138 另读输入、公式实现、四组归档输出、数值与守恒对照。
- 学习网站：#157 的 `INDEX.md`、NEXT_SESSION 与现有界面文件。
- AWT：#163、#165 的四情景、资料目录、交接与独立回执。
- 最新统一科学交接：#168 任务书与 #169 `UNIFIED_TASK_INDEX.md`、NEXT_SESSION、拓扑冲突及独立回执。
- 建筑能源韧性：已读取本地唯一索引 v0.3，未复制附件或完整索引；在本次 main 与29个已抓取研究树中检索未发现对应远程版本，标为 `NOT_FOUND_REMOTE`。这不是对所有未查分支的断言。

精确源路径、固定 SHA 和页面对应见 [SOURCE_MAP.md](SOURCE_MAP.md)。研究说明和公开评审均可与该索引相互追踪。网页“索引标签”中有补充阅读分类；原始停止条件保持原文，分类不是批准或新的科学结论。

## CI 与发布边界

既有 `cczps-lite-tests.yml` 会为 `cczps_lite/**` 自动生成场景和运行核心测试。为避免纯解释站改动触发本轮不授权的科学运行，增加只读变更分类：只有核心/测试目录变化或明确手动触发才执行原核心作业；展示、文档、工作流本身的变化不会自动运行场景。保留原核心命令及手动触发行为。新增独立展示与来源检查流程，不执行研究代码。

现有 GitHub Pages 部署流程仅在 main 推送或手动触发时运行，本次未修改、触发或部署。**后续合并会触及既有部署触发条件，因此本次只交付 Draft PR，合并和部署仍须单独审批。**
