# CarbonOS × ClimateOS 复用计划

P1-A只读审查/研究展示。P0的 `p1_authorized=false` 是11月3日历史状态；11月4日Founder新任务授权本轮研究/HTML，不等于授权正式计算器。保留P0原始执行状态，另建本任务状态。

| 复用资产与精确版本 | 已有能力 | 本阶段怎样使用 / 不怎样使用 |
|---|---|---|
| CarbonOS Task143–147，`e30d34b588783d76bc479268bc7efcdee89ca08a:docs/tasks/task141_150_carbonos_comparative_accounting_validation/` | 来源协议、公式/因子概念登记、Passport、主张/边界与验证问题 | 用作来源/版本/不确定性结构；文档不是法定执行器；不修改冻结成果 |
| P0 `CLIMATEOS-CARBON-RECOVERY-001` 原始官方snapshot/hash | AWT2015、2026咨询、IPCC2006等 | 复核原字节并引用；纠正§17/Eq1引用等在新审计单列，不重写旧报告 |
| `c51d7935285e0d7c7c45428edaa003fc9fcaba1d:apps/public-strategy-atlas/csoi-layers.js`与`atlas-accounting.js` | 有限通用公式、单位/范围约束、不可变历史输入与独立复算 | 复用其治理思想和已有测试证据；本轮HTML是静态研究展示，不接入真实record/任意公式执行 |
| `9eb7577e145e76161f9f1cd8509348b19c2904cc:cczps_lite/integration/environmental_coupling.py`及schema | 离线静态关系契约，无network/modelrunner | 用作关系分类/假设与准入的设计参照；不把它称为已运行碳水物理耦合模型 |
| 同main `cczps_lite/scientist_runtime/contracts.py`、`runtime.py`、`store.py` | 合成受控Run Receipt/人审状态 | 以后若有实验先复用此审批/隔离边界；本轮不建新agent/MCP/数据库/调度 |
| PR129 `987cc1dc7170204e5eab3d1750590ba463ea9d08:cczps_lite/environmental_question_runtime/streamflow.py`与`evidence_links.py` | HRS历史、原QC与只读月度引用；Receipt/Passport | 用作时序质量/源绑定方法，未接入新甲烷计算。HRS流量不等于污水流量 |
| 同PR `tools/verify_p04_spatial_admission.py`、`tools/verify_p04_semantics.py`、保存catchment及AWRA证据 | 几何/metadata/部分语义核对；有限单格soil结果 | 保留日界/DST、流域版本、全域mask与rainfall lineage阻塞；不重试ArcGIS499、不换来源 |
| `[LOCAL_ONLY_PATH]`等；SHA见P0 `evidence/ecoengine_replay.json` | 情景/时间序列模型与报告；P0合成4PASS/1WARN | 历史情景架构可参考；不是自动准入的实测历史气象库，soil_memory不是土壤碳/CH4动力学 |
| BOM既有公开数据及现有时间/空间工具 | 候选站点背景和取证方式 | 只捕获两个小型气候统计页面/目录；无新完整GIS或气象采集服务。匹配日序列与设施数据仍未建立 |

原路径/版本及既有测试证据由 P0能力地图（原始本地证据，未随公开归档提供）、P0测试receipt（原始本地证据，未随公开归档提供）与本轮 reuse_receipts.json（原始本地证据，未随公开归档提供）追溯。本轮对保存的复用测试证据做字节核对，不重复宣称运行了P0的测试；此前3个CSOI测试文件、12个静态coupling测试、9个HRS测试属于P0。HTML验收另有本轮证据。

## 不应重新创建的能力

不新建GIS引擎、weather API服务、研究数据库、Evidence Passport基础设施、Agent编排或网站后端。新增仅为本任务的来源/公式/变量登记、研究文档、只读HTML与验收脚本。研究展示JS只导航、展示来源和标注证据状态，不计算排放或调用模型。

## 时空与单位复用之前的门槛

先明确station、facility、process layer、catchment四种身份；分别保存坐标/CRS/高程基准/period。HRS source标签09:00 local previous24h、BOM day/window与厂内日志时区不能未经复核直接join。月均或modelled moisture是proxy，实际塘温/覆盖水分是site measurement；derived/calibrated参数不得伪装为直接观测。

输入hash与软件版本只证明可追溯，不证明数值真实或科学可比。对unknown/missing/out-of-scope数据继续阻塞，原始证据不因展示界面产生而变成scientifically admitted。

## 后续受限实验的最小建议（未执行）

经ChatGPT/Founder审阅后，可选一个单过程、单一已审参数集、公开/合成输入、明确温区/水分/边界的独立科学敏感性实验，保留手工或第二实现复算、极限/单位/异常检查和失败receipt。若拟用两地真实设施值，需先补过程温度/负荷/水分/控制状态及许可。不得把实验结果自动用于AWT或当前ACCU主张；任何正式计算器、部署、外部联系仍单独批准。
