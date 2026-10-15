# CA-DEMO-001 — KITTY Taskbook

## 1. 唯一 KITTY 与任务去重

本工作只使用现有 KITTY / Mission Control 入口，没有创建第二个 KITTY、代理、账户或任务平台。

主机核查发现：#124 已于 2026-10-15 12:31:55（Australia/Sydney）进入现有 KITTY 线程，唯一脑任务为 `BR-mv8v5hc4-5vcpd`。任务在 12:34:19 以 `SUCCESS / DELIVERED` 结束，完整 2302 字符、未截断；因此本轮没有重发同一启动提示。

远程桥的 `remote-state.json` 仍绑定 2026-10-01 的无关旧任务 `BR-muq6mqbr-1aogk`，桥进程未运行；3543 canonical KITTY 服务本身在监听。旧桥状态不能证明 #124 已运行或已完成，也不应清除或重写来制造成功。

## 2. KITTY 的证据读取边界

- KITTY 已实际读到 #124 Issue 正文与既有评论，并能复述第 4 节固定案例和公式边界。
- 首次结果明确承认 Issue 正文读取到 4000 字符截断，尚未读取官方来源包；故定级为 `CASE_STRUCTURE_ONLY`，不是证据版简报。
- KITTY 尚未因此自动读到本分支文件；Issue 读取不等于仓库 blob 读取。
- 来源包必须先推送成可读取远程文件，再以一个明确的后续提示交给现有 KITTY。
- 后续提示是“读取已发布证据包并补全简报”，不是重复启动 #124。

## 3. 期望交付

一页中文简报（600–900 中文字为目标）应覆盖：

1. 热、降雨可靠性与火险天气怎样经过饲草、牲畜、水源、储量、输配、人员安全和设施连续性影响经营；
2. 哪些是官方区域/行业证据，哪些是虚构输入，哪些仍未知；
3. 维持规模、改善资源管理、分阶段改变生产的好处、代价和验证条件；
4. 可检查的水量账公式，但不填造 Cooma 需水数字；
5. 管理者最先核实的三个问题。

## 4. 状态字段

- `CASE_STRUCTURE_ONLY`：KITTY 只读取任务书、未读取本证据包时可用。
- `EVIDENCE_BASED_DEMO`：KITTY 实际读取固定版本 `SOURCE_PACK.md`，并返回与来源边界一致的简报后才可用。
- `NOT_DELIVERED`：只有 pending/timeout/failed 而无完整回执。

归档时的最终状态、实际 run id、回执时间和是否采用 KITTY 文本，见 `DEMO_RESULT.md` 与 `REVIEW_AND_CRP.md`。Host Codex 文字始终单独署名。首次 KITTY 输出包含与本任务无关的 WCOS 排序意见，归档只记录其农场案例内容和边界，不将该意见扩展为 ClimateOS 前置条件。
