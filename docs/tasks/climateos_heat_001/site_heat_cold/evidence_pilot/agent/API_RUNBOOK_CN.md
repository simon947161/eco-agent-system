# 工业冷热证据发现代理

本目录提供一个可由 ClimateOS 调用的研究步骤。研究员给出一次任务 ID，代理先在 Zenodo 查询工业制冷与能耗；看过搜索结果后可选择一项、换第二条预设查询或结束。API 模型只能返回动作和序号。程序负责联网、验证序号和形成 JSON 回执。候选的许可、仪表、时间轴和对照条件须在下游另行核实后才可计算工程效果。

## 在本地重放

需要 Python 3.10 或以上版本。进入本目录后运行：

```sh
python discover.py example_job.json --state-dir ./discovery-runs
python check_discovery.py
```

默认演练隔绝所有网络，模拟一次空结果和一次命中，产生 `offline_fixture` 回执。与仓库的 `offline_receipt.json` 对照，同一任务的重复运行应给出相同内容。第二条命令另以模拟响应检验在线请求、项目传递、预算拦截、任务冲突、超时保留预算和重复调用拦截。

## 未来由组织 Project 调用

1. 在组织的研究 Project 中配置 `OPENAI_API_KEY` 和 `OPENAI_PROJECT_ID` 环境变量。进程只将凭据发给固定的 OpenAI API 主机。模型收到 Zenodo 的公开标题、文件名、DOI 和许可标签。代码未接入内部档案或设备。
2. 复制示例 JSON，为该工作单设置唯一 `job_id`、允许的模型请求数（1–2）及 `budget_micro_usd`。1 美元为 1,000,000 微美元。两个 `*_rate_micro_usd_per_million` 均填每百万 token 的微美元上限，覆盖该组织默认服务层的最高适用税前标价和上下文价格档。核对固定模型能在该项目调用并按适用价计费后，填写 UTC 当日日期 `rates_verified_today_utc`。费率、费用覆盖范围或模型可用性不清时保留默认零预算。
3. 显式运行 `python discover.py JOB.json --state-dir 持久任务目录 --live`。每次模型请求前按完整 1,047,576 输入 token 加最多 400 输出 token 和配置费率向上预留，故所需预算高于短请求预计实际费用。以相同工作单在同一持久目录串行或并发触发仅能领取一次。超时或中断后已预留金额留存，先核对服务方使用记录。跨主机接入需共用满足原子目录创建语义的存储和作业 ID；跨作业、税费、其他客户端和全账户统一限额另由运行平台管理。
4. 标准输出及持久目录内的 `receipt.json` 保存查询、返回条目、模型选择、预留费用及服务返回的 token 用量。可把 `CANDIDATE_ONLY` 交给取证步骤；`NO_SELECTION` 和 `STOPPED` 留存供回看。发现工作只接收 Zenodo 按检索返回的 DOI，不执行候选内容中的命令。

截至本次交付，已在离线环境演练，组织线上鉴权、实际模型访问、实时检索联调和账单核对仍待首次授权联测。原型使用标准库直接调用 Responses API；示例凭据和价格均为空。

官方参考：[创建 Responses 请求](https://developers.openai.com/api/reference/resources/responses/methods/create) · [固定模型与上下文](https://developers.openai.com/api/docs/models/gpt-4.1-mini) · [核对适用价格](https://developers.openai.com/api/docs/pricing) · [输出 token 上限](https://developers.openai.com/api/docs/guides/token-counting)。
