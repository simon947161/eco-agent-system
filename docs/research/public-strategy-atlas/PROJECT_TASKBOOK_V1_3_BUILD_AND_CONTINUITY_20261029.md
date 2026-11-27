# ClimateOS Public Strategy Knowledge Atlas — Founder V1.3 开发授权与跨设备持续执行任务书
**生效：** 2026-10-29 Australia/Sydney  
**状态：** FOUNDER AUTHORIZED BOUNDED WEBSITE IMPLEMENTATION / NOT DEPLOYED  
**唯一 GitHub 工程分支：** `feature/public-strategy-atlas-web-mvp-20261029`，从 `research/public-strategy-atlas-20261029` 派生；**不能改变 PR #129、main、生产 Sites 和 WCOS**。  
**网站目录：** `apps/public-strategy-atlas/`。  
**永久接续入口：** `apps/public-strategy-atlas/NEXT_SESSION.md`（唯一当前状态）、本任务书、`apps/public-strategy-atlas/README.md`；每次结束提交 `NEXT_SESSION.md` 并推送，禁止仅保存在本地、Work 或 Council 电脑。  
**授权解释：** Founder 明确要求**立刻开始网站设计/开发，而非只提交研究**，本任务书解除 V1.1/V1.2 中针对公开、合成数据离线原型的 A/B/C 编码冻结；但不授权 Council 系统、真实内部数据、对外分享、收费云部署、生产替换、PR 合并或法定结论。

## 1. 不能丢失的设计成果和来源
- O2 横向有机树为主界面、O1 固定泳道为可选辅助、O3 双窗口为后续选项；原则选型已由 Founder 确认，具体 R0 实物此前在另一个本地工作区恢复并经 14 个哈希检查，**不宣称已经上传当前仓库**。
- CSP→DP→OP 与 LSPS↔LEP/DCP/SEPP 分为不同类型的关系；版本、地域、采用日期、时点及法定效力需要各自证据。
- 线条几何位置/长短稳定，灰底可按经定义的指标填充；**关系核验覆盖率、期限经过、实际 KPI 三者严格分开**；没有真实数据就显示 UNKNOWN。
- 证据抽屉、从上到下/反向追溯、暗线候选和反证、哈希/更正事件/审计状态、内容寻址与知识关系分层。
- 两份 GitHub V1.2 都保留：`PROJECT_TASKBOOK_V1_2_TRUSTED_KNOWLEDGE_GROWTH_20261029.md`、`PROJECT_TASKBOOK_V1_2_VERIFIABLE_KNOWLEDGE_GROWTH_20261029.md`；优先采纳二者共识，差异见 `V12_BASELINE_RECONCILIATION_PROPOSAL_20261029.md`。原 R0-K 本地 commit `5279eedc...` 目前原件不可读，**不得为了恢复它而停掉已授权的合成数据网站工作，也不得假称已阅读六份报告**。
- 原 Council Leadership Forum 非公开材料仅研究缘起，不复制或导入私人网页仓库。Michele 对话/展示和任何正式 Council 关联仍需 G1 身份/利益冲突检查。

## 2. 立即启动的实际网站开发

**M0 首次可运行骨架（此次可立刻执行）：**
- 创建 `apps/public-strategy-atlas/index.html`、`atlas.css`、`atlas.js`。
- 无需外部账号/云/付费依赖，普通浏览器直接打开或 `python -m http.server` 本地访问。
- 15 左右明确标识为**合成演示**的节点，覆盖 CSP、LSPS、LEP、DCP、DP/OP、行动、证据；横向有机弧线、不等长分支、可点击节点、反向高亮、证据抽屉、过滤/视图切换、暗线虚线候选和来源缺失标识。
- 明确标出`synthetic / research candidate / public directory reference`。官方来源索引 URL 与“已经确认具体条款直接关联”是不同状态；所有真实 KPI 为 UNKNOWN。
- 三种线条成长模式：合成核验覆盖率（可显示明确 DEMO 标签）、合成期限（注明不是执行率）、公开真实 KPI（没有则保持灰色 UNKNOWN）。图形语义和法定状态不能混在一个百分比。
- 响应式可读，无障碍的键盘聚焦、颜色+线型+文字标记、适配普通单屏；多屏暂不实现自动同步。

**M1 紧接 M0 的数据与证据骨架：**
- 拆分数据与渲染；定义可序列化 SourceArtifact/ContentBlock/DocumentRevision/RelationshipAssertion/ChangeEvent/DiscoveryHypothesis；稳定 logical ID / version ID / digest 分开。
- 实施最小自检（schema, link target, status, missing evidence, version/geographic mismatch）和 3 个反例；不得把合成证据提升为正式来源。
- 根据许可和可验证性逐个引入最新 applicable 的官方 CSP、LSPS、LEP/DCP、adopted DP/OP 的少量真实条款及出处；来源无法读到就显式 UNKNOWN，不为了数量假造条款。
- 测试从 CSP 向下/行动反向/LSPS 规划法定适用的 3 个垂直路径；证据抽屉可追到官方 URL、发布日期/生效日期、地域、条款和版本。

**M2 UI/可信研究升级（M1 后）：**
- O2 增量布局、密度 15/60/200 节点测试、暗线证据与反证、审计镜头、版本时间轴、内容哈希变更历史（离线可复验）。
- 与 Evidence Passport 对接只通过公开、安全、经过独立审查的类型转换，不复制 Council 内部数据；数字凭证和透明收据需研究结论明确后才增加，本阶段不自动签发凭证或部署链。
- 可选 O1 / O3，多屏同步只有在可维护性测试后追加；所有浏览器体验先支持 1 个普通屏幕。
- 实际浏览器截图/操作验证记录；无环境则诚实标为 NOT_TESTED，不可冒充通过。

## 3. 网站视觉目标与用例

- 桌面 16:9 横屏优先：左侧简洁选择器，中央横向稳定树形 SVG 连线，右侧点击展开的证据抽屉；密集图中仅显示选中路径及近邻。
- 节点默认短标签，点击或键盘聚焦才打开详细信息；线条表示可审查 `RelationshipAssertion`；研究推断与暗线用虚线/标签。
- 用户点击任意关系可以追溯原始来源（无可查来源时清楚显示 `UNVERIFIED`）；用户选择“发现暗线”会得到候选而不是正式结论。
- 类别颜色和完成度填充长度两种视觉通道不得混淆；真实绩效暂无数据则显示 UNKNOWN，不默认 0%。
- 顶部明显提示：独立私人研究 / 合成数据示范 / 非 Council 官方 / 不用于规划或法律裁决。

## 4. 跨设备、Work 与 Codex 接续制度（强制）

**唯一权威 = 远程 GitHub 工程分支的已推送提交。** 本地仓库/Work 临时磁盘/聊天只是工作副本。单一执行写入人；不同设备使用独立 worktree，同步前必须读最新 HEAD，防止覆盖彼此工作。

每个可交付阶段完成时，**必须**：
1. 运行可执行测试并记录真实通过/失败/未运行情况；记录截图或提供不可截图的原因。
2. 对变更做来源/隐私扫描（包括路径、环境变量、内部会议、密钥、内部真实个案）；仅把允许公开的代码、合成数据和合法公开摘录写入 GitHub。
3. Commit + 推送本工程分支（明确无推送权限则状态 `PUSH_BLOCKED`；不得写“远程已保存”）。
4. 更新 `apps/public-strategy-atlas/NEXT_SESSION.md`：日期时区、当前远程 SHA、本次变更、真实运行入口、测试命令/结果、已知缺口、唯一最小下一步、禁止动作。
5. 下一次 Codex/ChatGPT Work 打开这个 GitHub 分支后，**先读 README + NEXT_SESSION + 本任务书，再从远程 HEAD 继续**；不要求依赖上一个聊天线程或原电脑。不得把先前研究当成新任务重新做。
6. 当用户在不同电脑上使用 ChatGPT Work，要求其**操作 connected GitHub**（如可用），从本工程分支继续提交，不要求本地 Codex CLI。ChatGPT Work 的独立会话不会凭一份文档自动接管/自动在额度重置后运行；须显式在新会话发出续接指令。**不承诺自动后台执行**。

若 GitHub 写入失败，先保留临时工作文件并明确 `SYNC_BLOCKED`；下次不能当已同步。跨时区/日期接续时，以远端 UTC commit 与澳洲悉尼工作记录对照。

## 5. 明确的边界

**授权**：独立分支公开安全前端 MVP、合成案例、合法公开文件及其关系核验、离线测试、源码推送，以及新 Draft PR 作评审入口（如适合）。允许正常工程修正、添加文件。  
**未授权**：Council 非公开/真实内部记录、实际 Council 账号/API、雇主版权受限信息、违法爬虫、商业 API 费用、购买、正式部署到公共互联网/Existing Sites、修改 PR #129/主线/其他环境、正式诉讼/行政法律判断、自动合并/生产发布。正式共享网站链接需另行审核许可、G1 和公开披露安全性。

## 6. 测试与 Founder 验收

- **首轮最低完成定义**：可从 GitHub 下载并在本地运行的真实 HTML/JS/CSS，具备 O2 形态、至少 3 条可点击/反查的合成路径、证据抽屉、候选暗线模式、无数据状态、清楚的合成标识；有实际 Git SHA、运行说明及明确尚未覆盖的内容。
- **下一轮验收**：自动测试覆盖断言类型、来源链接、版本/地域/时间冲突、哈希篡改、更正事件、200 节点布局复杂度、键盘和移动端操作；公开正式条款来源逐一校验。
- **完成网站项目≠M0 完成**：直到 M1/M2 证据、真实性、适用性、可视性、设备适配和独立测试达到要求，不能宣布“已建成正式 Atlas”。
- 任何项不可完成需留下截图/日志/限制与替代办法，不再次仅递交一份更大的研究任务书。

## 7. 给跨设备任意 ChatGPT Work / Codex 的唯一开工命令

> 继续 ClimateOS Public Strategy Knowledge Atlas **网站实际开发**，GitHub `simon947161/eco-agent-system` 分支 `feature/public-strategy-atlas-web-mvp-20261029`。先读取 `apps/public-strategy-atlas/NEXT_SESSION.md`、`apps/public-strategy-atlas/README.md`、`docs/research/public-strategy-atlas/PROJECT_TASKBOOK_V1_3_BUILD_AND_CONTINUITY_20261029.md`，查看远程 HEAD 和本地变更，按状态从 M0/M1/M2 中**下一个未完成可验证项**继续编码、测试、提交并推送。不要重做 R0/R0-K，也不要询问原电脑路径。只用公开/合成数据，禁止 Council 内部数据、商业付费、部署、修改 PR #129 或合并 main。每次结束更新 NEXT_SESSION，返回远程 SHA/测试结果/唯一下一步。
