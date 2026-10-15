# CA-DEMO-001 — Codex Taskbook

## 1. 执行边界

- 仓库：`simon947161/eco-agent-system`
- 文档分支：`codex/ca-demo-001-farm-resource-evidence`
- 基线：`origin/main` at `9eb7577e145e76161f9f1cd8509348b19c2904cc`
- 隔离原则：原工作区已有不相关修改；本工作只在独立 worktree 形成文档，不纳入那些修改或运行时状态。
- 对外边界：公开官方材料与虚构案例；不使用 Council、客户、现场、私人 EcoEngine 资产或真实 WCOS 数据。

## 2. C1 原审计核查

观察：主机找回 `NSW_CLIMATE_RESOURCE_AUDIT_V0.1.md` 全文。独立 `SHA-256` 为 `999C714302DE6234E295D289E36F902A78830815940E2011D9F328FEF4C9DA87`，与 #124 给定值一致。

公开安全核查：未发现密钥、令牌、Council 内部材料、客户/个人信息或真实设施身份。文中本地系统名称只用于架构边界说明；公开版未删减，因此没有以删减版冒充原哈希。报告仍标记为研究审计和 `NO_INTEGRATION_EXECUTED`。

## 3. C2 既有能力核查

| 能力 | 当前实现 / 入口 | 本轮验证 | 状态与边界 |
|---|---|---|---|
| 官方来源登记 | `cczps_lite/integration/cooma_official_source_metadata.py`、`cczps_lite/input/cooma_official_source_metadata_pilot.json` | 对应单元测试在归档前执行并记录于 `REVIEW_AND_CRP.md` | `RUNNABLE`；只验证元数据合同，不表示来源内容已获科学采纳 |
| 公共空间来源登记 | `cczps_lite/qgis_local_spatial_foundation/*_source_registry.json` | 文件与既有测试入口存在 | `RUNNABLE / DOMAIN_SCOPED`；不是全项目通用 Knowledge Registry |
| Knowledge Registry | 仅在历史文档中出现 Knowledge Object 候选规则 | 未找到独立可运行注册表或服务 | `DESIGN_ONLY`；本轮来源包是 Markdown 证据包，不宣称已写入知识库 |
| Evidence Passport | `cczps_lite/analysis/mittagang_410033_historical_characterisation.py` 及既有输出；`cczps_lite/site_reading/cooma.py` | 对应站点解读测试在归档前执行 | `RUNNABLE / FIXTURE_AND_ADMITTED_INPUT_BOUND`；本轮没有下载新气候数据，故不伪造新数据 Passport |
| 环境问题研究程序 | `run_environmental_question_runtime.py`、`cczps_lite/environmental_question_runtime/` | 核心单元测试在归档前执行 | `RUNNABLE_LOCAL`；真实地点执行仍由证据闸门阻断 |
| Cooma 场地解读 | `run_cooma_site_reading.py`、`cczps_lite/site_reading/` | `tests/test_cooma_site_reading.py` 在归档前执行 | `RUNNABLE_OFFLINE`；当前水文仍保留 admission/comparability 缺口，不能推出当前流量或趋势 |
| KITTY GitHub Issue 直读 | 主机 Mission Control 的 `github-issues.mjs`；#124 读取证据已落主机审计目录 | KITTY 线程实际复述了 #124 第 4 节；不等于读取未推送仓库文件 | `RUNNABLE_HOST_ONLY`；必须给远程固定文件链接或 Issue 内短证据包 |
| KITTY 脑任务 / 回执 | 现有 3543 KITTY 服务和 `katie-brain-jobs` 持久记录 | 已定位 #124 的唯一任务 `BR-mv8v5hc4-5vcpd`；未重复提交 | 以 `KITTY_TASKBOOK.md` 的最终核查为准；无完成回执不得写“已交付” |

## 4. Codex 产出

1. 归档原审计并保留原哈希。
2. 整理不超过五项官方来源，逐项写明版本、适用范围、可支持与不可支持主张。
3. 固定虚构案例与可检查水量公式。
4. 形成明确署名的 Host Codex 证据示范，保证 KITTY 不可用时任务不整体停住。
5. 对来源、假设、单位和结论边界做独立复核；在远程分支、Draft PR 与 #124 留下可读链接。

## 5. 非产出

没有下载 NetCDF/GeoTIFF、没有调用未核实 API、没有修改运行时、没有把区域投影转为地块结论、没有认定具体 Water Access Licence 或 Basic Landholder Right、没有提出真实用工定额、没有合并旧 PR。
