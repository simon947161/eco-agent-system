# QA 与验收边界

工程验证和科学成功分开。当前科学结果DATA_NOT_READY；不会以测试绿色宣称已经算出历史概率。

## 可重现命令

仓库根目录，Python标准库，无新增依赖：

```text
python -m cczps_lite.integration.enso_regional_weather
python docs/tasks/climateos_enso_regional_weather_probability_001/scripts/validate.py
```

默认只写忽略目录。`--record`是本轮归档维护选项，不覆盖任何旧任务包；普通复核不得使用它修改证据。线上CI执行本仓库原单元测试workflow；完整CI与本地限定测试的计数和HEAD必须分别记录。

## 本地证据入口

- [validation.json](evidence/validation.json)：实际时间、Python、计数、哈希和状态。
- [新测试日志](evidence/tests-new.txt)：缺数据出口、RONI持续率不能转天气、单位/季节/时区/域/版本/缺测/因果/认证/政策外推拒绝、trace、QC、AS国家码、预登记顺序等。
- [旧验证调用日志](evidence/tests-inherited-run.txt)及[旧120项日志](evidence/tests-inherited.txt)：原47任务文件、50Atlas文件，120限定回归；不修改旧归档。
- [端到端冻结输出](evidence/end-to-end.json)：无概率、无数值、无气温推断，EcoEngine低证据，CCZPS旧四场景均证据不足。
- [manifest](evidence/manifest.json)：本任务文本LF归一化SHA；两份R/D交接元数据、manifest自身、validation自描述除外。原始下载字节SHA另以获取收据为准。

旧结果验证包括CH4 0.569344413968403 W/m²、原三组合成甲烷质量账、三节点合成水文残差0、31条HRS质量E、Scorecard冲突和英文草稿NOT_SENT，以及原RONI结果完全相同。旧端到端结果SHA必须为 `279d823da5ee835a9b3e889a0e4777ff0ee0be9be813c8a992ef62aedcada28a`。

## 科学验收矩阵

| 必要项 | 状态 | 证据 |
|---|---|---|
| PR基线、评审、原科学闸门 | VERIFIED_READ_ONLY | baseline-and-review.json，旧回归 |
| 先定地区/季节/阈值 | LOCAL_VERIFIED | 两收据相同参数SHA、择站早于雨量请求 |
| 合法实际获取 | PARTIAL | 库存HTTP200；雨量HTTP404 |
| 雨量原字节SHA/QC/覆盖 | BLOCKED | 无雨量文件，不能生成SHA或完整性比例 |
| ≥1个区域真实配对 | **FAIL / DATA_NOT_READY** | rows=[] |
| 暖冷中性概率/CI/效应差 | NOT_EXECUTED | 无真实分子分母 |
| 块自助、分期、留出验证 | METHOD_REGISTERED_NOT_EXECUTED | 方案文件；没有声称实现/验证完整引擎 |
| IOD/SAM同步检查 | NOT_EXECUTED | 文档调查，不冒充已控制混杂 |
| ≥1个1961–2020局地反例 | NOT_TESTED | 只有2023外部官方解释，不能代替 |
| 负例/缺测保守出口 | LOCAL_VERIFIED（以日志为准） | 新测试 |
| 科学准入/未来预测 | PENDING | 不升级 |

下载失败和工具读取限制保留原事实；国家码错误及修复完整记录。没有追加下载去凑成功。未进行全国排放、甲烷/水文真实模拟、部署、合并、外联或认证。
