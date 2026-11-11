# 从一块正在变干的土地，进入公共知识体系

读取日期：2026-11-11。范围严格为 8 个官方目标：5 个可读，WESR 首页无可提取正文，2 个 wis2box 介绍路径不可访问。没有安装节点或取得观测数据；没有下载报告全文。结构化来源及失败记录见 `un_wmo.json`。本文原创图示是学习解释，不是机构官方图或物理因果图。

## 三个不同职责

**官方事实｜GEDS**：UNEP 把碎片化、来源质量、互操作、可及性与能力建设作为治理问题；这一框架是自愿性的，不新设报告义务和标准。[GEDS：Overview / GEDS framework](https://www.unep.org/en/what-we-do/digital-transformations/global-environmental-data-strategy-geds)

**官方事实｜GEO-7**：官方页面描述综合评估与草稿审阅过程，记载 2025 年 12 月发布。本轮读的是概览与时间线，不是全文；不能声称检验过报告中的经济预测。[GEO-7：Overview / Timeline](https://www.unep.org/geo/global-environment-outlook-7)

**官方事实｜WIS2**：交换网络支撑跨境观测流转；WIS2 于 2025 年 1 月运行，wis2box 降低部署节点的门槛。[WMO WIS](https://wmo.int/activities/wmo-information-system-wis)

## 机制深读：一条通知还不是一份科学证据

```text
目录：这里有什么，在哪里，怎样访问？
                ↓
Broker 通知：有新数据可取
                ↓
Cache / 数据提供者：取得相应记录
                ↓
本地独立准入：权利 → 格式 → 单位 → 时间支撑 → 空间支撑 → 质量
                ↓
能够被研究问题使用？仍需明确适用范围
```

前三步来自 WMO Knowledge Hub 的机制描述：Global Discovery Catalogue 提供发现与访问说明，订阅 Global Broker 接收通知，数据来自 Global Cache 或提供者。第四步是 **ClimateOS 的设计建议**，不能冒称 WMO 已替本项目做完准入。该页面列出的 2026-11-17、2027-02 活动晚于本次日期，只是预告，不计作已开展。[WMO Knowledge Hub：opening technical overview](https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/wmo-information-system-wis)

**可核的差别**：PR155 `Graph.plan` 组织已准入模型的依赖执行；WIS2 组织跨机构数据交换。前者不会自动提供后者的覆盖、时效或源记录。`Field.validate` 与 `State.require` 已有单位、时空和缺失门，可作为未来输入适配的检查点；本轮没有接入 WIS2。

**反例**：一条通知准时到达，但实际记录有缺测；或两条“日雨量”采用不同日界。交换成功仍不足以支持同一科学比较。这里是可测试的风险情形，未声称在真实 WIS2 数据中观测到此故障。

**许可门**：官方软件仓库标注 Apache-2.0，README 说明其发布、发现和访问能力；没有复制软件。许可徽标不授权其传输的所有数据。数据本身的条款要逐项核查。[wis2box README / licence badge](https://github.com/World-Meteorological-Organization/wis2box)

**仍未知**：具体通知字段、消息协议细则、重发去重策略、站点质量标记、数据许可，以及实际延迟。本次没有读 Manual No.1060 或 Guide No.1061 正文，不把记忆中的 MQTT 细节写成已核事实。

## 独立理解与分歧

**AI INTERPRETATION / 待 Founder 确认**：这个学习站最有价值的产物，也许是一张“哪一层尚不能回答”的地图。再多一个执行图，也不能补上缺测的站点历史；机构有权威，也不能把一个全球评估直接变为家乡的措施效果。下一步先选一份合法记录，追完整条证据链，可能比马上运行整套国际节点更有信息价值。

**Founder 声部**：本研究没有新增或伪造 Founder 现场观察。其已表达的探索愿景只由同目录思想导言承载；本文的建议与反例均是 Codex 的判断，不冒充 Founder 原话。

**下一问**：如果我们只能为“土地变干”补充一个证据，应先核雨量日界、站址迁移还是土壤水分？需要以具体地方和误差预算决定，当前没有证据给出通用排序。
