# Codex 接着做：SMRC 政策资源 → ClimateOS Council Console

父任务#128；本工作包 `CLIMATEOS-SMRC-POLICY-CONSOLE-001`。沿用原KITTY–Codex协作#126。不要创建新OS、重复任务或用文档替代可运行实现。

## 无需Founder再找文件

1. 读取根目录AGENTS、README、父任务TASKBOOK、EXECUTION_STATE和本目录CONSOLE_INTEGRATION。
2. 核实remote为 `simon947161/eco-agent-system`，读取 `codex/regional-public-os-001-taskbook` 最新内容及PR129；确认PR127依然是否Draft。不要改动未提交文件，不自动合并旧Draft。
3. 使用既有工作副本；没有时在当前获准workspace建立独立checkout。先列明实际位置与分支，再实现；不用Founder手工选文件或复制研究稿。
4. 已知源文件名、哈希与官方链接在 `config/regional-public-os/smrc-policy-sources.json`。本机路径从既有聊天交接取得，写入被忽略的 `.local/smrc-source-locations.json`（`source_dirs`数组），或使用环境变量。不得把绝对路径、原件、内部文件或私人交流提交公共仓库。
5. 运行 `python tools/smrc_policy_console.py`；三份原件应匹配已登记哈希，新版DP/OP缺失时仍继续政策元数据功能，不把缺失标为通过。
6. 运行 `python -B -m unittest discover -s tests -p test_smrc_policy_console.py -v`。读测试报告，随后按实际代码复用原月度Console、EEO/Receipt/Passport和PR127最小能力，加入政策卡、来源版本与三主线研究卡。
7. 获取官方当前DP/OP，核对发布日期、版本、差异与许可；2025版作为历史，旧人员署名不作为现任责任人。无需为人事变化阻塞框架开发。
8. 完成现有Console中的贯通交互和父任务P02；持续维护执行状态、commit、测试与实际阻碍。若当前分支用于任务书而已有实现分支，则在既有父任务分支安排中最小移植；不强制新建重复实现分支。

## 本次已验证的具体内容

- LSPS118页、DP v1.6 94页、CSP36页原件SHA256核对；LSPS关键行动已读。
- 新增脚本可定位、核验、生成公开安全政策数据包；缺失、错版本和未准入分别显示。
- 5项针对性测试通过；三份真实公开原件端到端定位和哈希匹配成功；两份当前执行文档候选保持缺失/待核验。
- 尚未完成UI接入、全仓库回归、网站部署或真实KITTY调度。不要将本页视为这些能力的验收通过。

## 自主推进范围

用户已明确要求把本工作包保存到ClimateOS GitHub并加入原队伍继续推进。常规读取、分支实现、测试、状态保存和仓库任务交接在本次范围内。真实Council系统、内部客户数据、正式政府决定、对外商业联系和新增现金支出不在范围内。需要现实人工判断时先完成其他可执行工作，并给出具体结果与所需决定。
