# GitHub双向交接协议 v1

GitHub存储证据，Founder短句触发另一个对话；没有证据证明ChatGPT订阅本仓库。本轮没有新机器人、轮询器、Webhook、后台任务或权限变化。

## 精确版本，避免自引用SHA
提交内不能写入它自身Git SHA（会改变SHA）。采用两阶段：
1. R = 完整研究内容提交，固定代码/报告/测试/manifest。HANDOFF_STATUS和REVIEW_REQUEST此时是PREPARING快照。
2. D = 仅交付元数据更新提交：填入新PR、working_head_sha=R、review_target_content_sha=R。R是状态快照对应的内容HEAD，不冒充含该状态文件的最终运输HEAD。
3. 最后单一GitHub评审评论固定完整D与R、README和REVIEW_REQUEST入口、实际CI和未复核范围。Founder短句指定**D**；审查者应读D的全树，核对R..D仅两份交接JSON变化并验证manifest。精确交付HEAD以不可自引用的该评论及PR元数据为锚。任何实质变化需新R、新D与重审。

## 状态和消息回执
SENT=有真实发送/写入的链接；QUEUED=接收系统明确排队；ACKNOWLEDGED=接收者返回绑定SHA的回执；EXECUTING=实际执行声明及证据；REVIEW_READY=包已准备；REVIEWED=有独立审查结果、reviewed_head_sha及review_receipt_commit_sha。GitHub Draft PR创建仅GITHUB_POSTED，response_delivery_state仍NOT_SENT_TO_CHATGPT；不自动推导后四种状态。

所有JSON有 source_pr, scientific_baseline_sha, taskbook_sha, working_head_sha, reviewed_head_sha, review_receipt_commit_sha, status, stage, evidence_uri, blockers, owner, next_action, authorized_scope, no_run_flags, review_actor, response_delivery_state。未发生的回执用null加原因；不填写假的SHA。

GitHub→Codex：核对任务书blob、分支/基线、最新reviewedSHA与许可；发现不同先写差异，不覆盖；执行完写测试与精确版本。ChatGPT→GitHub：评审者只读原文，在对话返回结论/范围/精确D；Founder转交实际回执，Codex按授权归档为后续提交并记录被审查D及归档commit。审阅不得默许新的数值实验、数据授权或上线。

短句模板（各不超过220字，最终PR/HEAD在最终评论中提供）：
- Codex：请读取 PR #N 的精确HEAD D，按 docs/tasks/climateos_client_ai_science_integration_001/NEXT_SESSION.md 核对评审回执，只执行已授权修复；回报PR与HEAD，不合并部署。
- ChatGPT：请只读审阅 PR #N 精确HEAD D，按 docs/tasks/climateos_client_ai_science_integration_001/README.md 和 REVIEW_REQUEST.json 核查证据、许可、QA及科学边界，返回绑定HEAD的评审。

没有生产访问/回执运行证据的接口一律UNKNOWN。仓库已有CI是测试，不是科学审查或ChatGPT消息投递；Pages workflow仅main push/手动，本任务不触发部署。
