# CA-DEMO-001 — Review, Validation and CRP

## 1. 四类复核

### 来源复核

- 五项均为 NSW Government / NSW Department 官方入口，检索日为 2026-10-15。
- NARCliM 区域页明确包含 Cooma；Climate Risk Ready Guide 的原始受众为 NSW Government；DPIRD 畜牧评估明确不得解释到单一 holding；Water 页面是一般预算方法；Basic Landholder Rights 页面不是特定地块法律裁定。
- 动态网页可能更新；本包保存访问日期、页面版本线索和适用范围，不把搜索摘要当唯一证据。

### 假设复核

- 100 ha、10 ha 饲草、20 头牛、2 名现有人员、住宅/设备棚/储水设施均明确为 #124 的虚构输入。
- 没有补造水源、许可、储量、作物、土壤、效率、饮水率、工时、工资、成本或收益。
- “热/水压力可能提高管理成本”保留为因果推演，不写成已观察事实。

### 计算与单位复核

- `1 ha·mm = 10 m³ = 0.01 ML`。
- `10 ha × d mm × 0.01 ÷ e = 0.1d/e ML`，且 `0 < e ≤ 1`。
- 若 d 是毛灌溉深度，不重复除以 e；年降雨差不能直接充当净灌溉需水。
- 需求与供给必须使用相同时间窗；年度总量不能证明最干月或热浪期间可供。

### 结论边界复核

- 通过：区域气候压力背景、结构化风险流程、水量账框架、三类经营选项和三项优先核实问题。
- 不通过/未建立：地块投影、实际需水、合法取水量、可靠供水率、缺水概率、载畜率、人员编制、工程设计、法律意见或最优经营方案。
- “未来更热/热日更多”等主张保持为区域投影；不写成天气预报或确定性未来。

## 2. 验证记录

归档前记录以下实际结果：

| 验证 | 预期 | 实际 |
|---|---|---|
| 原审计 SHA-256 | 与 #124 给定值一致 | `PASS` — `999C714302DE6234E295D289E36F902A78830815940E2011D9F328FEF4C9DA87` |
| 官方来源可读性 | 5/5 官方入口可读取 | `PASS` — 2026-10-15 浏览核验；动态页面需后续复核 |
| 目标单元测试 | metadata / environmental question / Cooma site reading | `PASS` — 36 tests, 0.504 s, `OK` |
| 文档链接与固定路径 | README 可到达全部产物 | `PASS` — 8/8 固定文件存在，README 相对链接已核对 |
| Git diff 范围 | 只有本工作文档及必要 README 索引 | `PASS` — README 1 行索引 + 8 份本工作文件；无其他工作区改动 |
| KITTY 案例结构 | 读取 #124 并返回非 ACK 内容 | `PASS` — `BR-mv8v5hc4-5vcpd`, `SUCCESS / DELIVERED`, 2302 字符，未截断 |
| KITTY 证据包交付 | 实际读取固定远程来源包并返回回执 | `PENDING_AFTER_REMOTE_SOURCE_PACK` |

成本：无法从本地 KITTY/网页检索接口读取货币成本，记为 `UNKNOWN`；不得编费用。人工操作：主机只读核查、官方网页读取、文档编辑、测试、Git 推送、Draft PR 与 Issue 回写。

## 3. 风险与剩余缺口

1. 区域模型到地块的尺度落差仍然存在；需点位/小范围气候数据与专业解释。
2. 真实水源与许可完全未知；需当期 licence/approval、Water Sharing Plan、restriction 及地块关系核验。
3. 作物—土壤—灌溉与牲畜参数未建立；不能形成 ML 需求或生产率结论。
4. 工作活动、技能、安全阈值和设施能力未盘点；不能从气候投影推算人员数。
5. 当前河流原始证据与可比性缺口继续保留，本工作没有把旧水文产物升级为当前供水判断。
6. KITTY 只有完整回执才算交付；超时则本轮只保留 Host Codex 明确署名底稿。

## 4. Conversation Radar / CRP

### Knowledge points

- Cooma 位于 South East and Tablelands 官方 NARCliM2.0 区域范围，但区域投影不等于地块预测。
- 农场气候判断需要把需求、合法供给、可靠补给、可达储量和损失按同一时期对齐。
- Domestic and stock right 不能自动授权商业饲草灌溉。

### Idea points

- 先用水量账和季节闸门把“气候故事”变为可检查的经营问题。
- 用分阶段试验、触发阈值和退出条件比较经营选择，不提前选赢家。

### Decisions

- `MAX_FIVE_OFFICIAL_SOURCES`
- `SYNTHETIC_FARM_ONLY`
- `NO_SITE_LEVEL_OR_LEGAL_CONCLUSION`
- `HOST_DRAFT_SEPARATE_FROM_KITTY`
- `NO_NEW_PLATFORM_OR_RUNTIME_CHANGE`

### Risks

尺度误用、法规时效、虚构参数被误当事实、年度水量掩盖季节短缺、储量被误当许可或可靠供给、KITTY pending 被误报为交付。

### Open questions

1. 真实案例使用何种水源、权利/许可与当期限制？
2. 选定饲草、土壤、效率和季节后，净灌溉需水如何由专业方法确定？
3. 哪些经营活动、工时、安全阈值和设施失效模式真正决定人员与资本安排？

### Next actions

1. Founder 审阅本示范是否清楚、省事且守住边界。
2. 如要进入真实场景，先核许可与水量账，不先加数据平台。
3. 只有出现经批准的真实地块/参数和专业复核范围，才开下一证据任务。

### Related project keywords

`ClimateOS`, `CA-DEMO-001`, `KITTY`, `Cooma`, `South East and Tablelands`, `NARCliM2.0`, `farm water budget`, `basic landholder rights`, `Evidence Passport`, `human review`
