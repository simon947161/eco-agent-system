# ClimateOS Public Strategy Atlas — 网站工程 M0

**状态：** IMPLEMENTED IN GITHUB / EDGE SMOKE VERIFIED / M1 SKELETON / SYNTHETIC DEMO ONLY
**GitHub 独立开发分支：** `feature/public-strategy-atlas-web-mvp-20261029`
**正式开发任务书：** [V1.3](../../docs/research/public-strategy-atlas/PROJECT_TASKBOOK_V1_3_BUILD_AND_CONTINUITY_20261029.md)
**跨电脑唯一续接入口：** [NEXT_SESSION.md](NEXT_SESSION.md)

## 立即运行

下载/检出这个 GitHub 分支，将此目录的 整个目录保留在一起（包括 atlas-data.js 和 atlas-model.js）。优先使用个人设备/个人研究环境。

可直接双击 `index.html`；若浏览器对本地文件有额外限制，用标准 Python 从目录启动：

```bash
cd apps/public-strategy-atlas
python -m http.server 8877 --bind 127.0.0.1
```

然后打开 `http://127.0.0.1:8877/`。网站为**纯静态前端**，无需 npm、专用图数据库、私钥、Council API 或付费服务；不运行自动同步或把数据传到服务器。

## 已写入源代码的 M0 功能（待真正浏览器复核）

- 单屏横向 O2 有机关系树，分支稳定且长短不一；上下分开表达 CSP→DP/OP 的战略执行与 LSPS→LEP/DCP 的规划支路。
- 节点和连线用**全部合成示例**展示；点击节点打开证据抽屉，查看邻接节点并可追踪反向链接。
- 战略、空间规划和全部视角切换；按节点文本过滤；暗线候选单独开关。
- 三个**绝不混合**的填充视图：合成关系核验、合成期限、真实 KPI（始终 UNKNOWN/不填充）。
- 基础响应式页面、键盘选择 SVG 节点、减少动态效果；较窄屏幕可横向滚动画布。
- 官方公开目录的外链仅供人工核对。**没有加载真实条款、没有签名验证、没有提供正式政策关系或真实绩效。**

## 需要进一步验证和建设

**已进行真实 Edge 浏览器冒烟检查和390px响应式iframe检查，见qa/M0_RESULTS.md与qa/M1_RESULTS.md；真实手机及完整无障碍验收仍未完成。** 文件存在于 GitHub 并不证明“浏览器交互测试通过”。下一阶段须在合法个人或 Work 工程环境运行并检查浏览器控制台、加载/点击/搜索/切换、键盘、手机布局、交叉连线和变更后状态。前端 M0 不是完整 Atlas。

后续按 V1.3 进行：
1. M0 浏览器运行/修错与真实截图、可复现测试；
2. M1 数据模型、官方最新适用版来源核对、少量完整真实证据链和断言验证；
3. M2 内容寻址/可复验历史、暗线反证、200 节点密度、审计/版本视图、双屏可选支持。

**未经明确审核不得：** 将 Council 内部资料/个人案件上传 GitHub；把研究推断变成官方关系；接入或改变 Council/ClimateOS 生产环境；部署公开 Site；宣称已经获得 Council 或第三方数字凭证的签名。

## 设备无关的持续工作方式

所有重要文件必须 **commit + push 至这个远程工程分支**；每次执行后更新 `NEXT_SESSION.md` 并核实远程 SHA。新设备或新的 ChatGPT Work 会话不需要找原桌面路径，也不要用记忆凭空推断状态：从 GitHub 读这个 README + NEXT_SESSION + V1.3，直接在最新远程提交继续。

**注意：** Codex 本地工作会话、ChatGPT Work 云电脑和 GitHub 彼此不会自动实时同步。GitHub 能持久保存已推送文件；额度刷新和不同设备的 Work 会话**不会自动触发开发**，必须从新会话显式发出续接指令。仅在本地提交未推送的工作不能保证异机可用。

M1合约与限制见[DATA_CONTRACT.md](DATA_CONTRACT.md)。运行 `node apps/public-strategy-atlas/model.test.cjs` 校验合成数据、反例与摘要事件。当前真实条款准入仍未完成。

## Work continuation: M1 validation + M2 interaction slice

Added strict reference/scope rejection, public observation register (separate from official graph assertions), O2 incremental expansion, discovery/falsifier panel, and local audit/version panel. See [actual checks and limits](qa/M1_M2_WORK_RESULTS.md).

Offline reproducible receipt: `node apps/public-strategy-atlas/audit-cli.cjs`. Pass an expected `sha256:…` argument to compare against a separately retained checkpoint. This does not provide an independent signature or prevent rewriting the entire chain. Portable SHA-256 supports ordinary HTTP/file contexts without new dependencies. Screenshot evidence and a 390px iframe harness are under `qa/`; these do not certify physical mobile devices.
