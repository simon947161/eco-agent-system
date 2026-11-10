# 主线复用与治理交接

新增薄入口 `cczps_lite/integration/enso_regional_weather.py`，PROCESS_ID=`ENSO_REGION_WEATHER`。只读取冻结任务包，执行准入拒绝和元数据/QC检查；默认无网络、无副作用。真实配对门没有通过，返回DATA_NOT_READY、numerical_output=null、probabilities=[]，不得回退到RONI持续率。

| 原能力 | 本轮实际调用/检查 | 没有声称完成的内容 |
|---|---|---|
| PR147 `physical_process_trajectory` | `trace('ENSO')`及原始RONI哈希；验证旧47文件和旧数值归档 | 未改旧ENSO统计、甲烷、水文或Scorecard |
| PR146 Atlas | 原query/trace与50文件哈希，经PR147接口复用 | 无新空间覆盖或全球模型 |
| EcoEngine `meteorology_evidence_record` | 缺测reading转换为low、indicators=[] | 没有生产气象更新，不把月记录假装UTC瞬时站数据 |
| CCZPS `build_scenario_comparison` | 显式空traceability输入，四旧场景返回证据不足 | 这四场景不是本轮Wagga/Rockhampton/Perth；没有注入地域不匹配概率 |
| PR145分层审查 | 原47测试回归，原内部fixture留存 | 未发真人签名、法定认证或科学批准 |

协议字段复用source/version/temporal_support/spatial_support/unit/uncertainty/counterevidence/model_validation语义。本轮携带源URL、SHA、许可限制、错误收据和缺失原因，交给ECOChain的仅是研究提案；`ECOCHAIN_CANONICAL_NOT_FOUND`不变，Enotebook `PENDING_INTEGRATION`。

下一科学治理任务：由ChatGPT独立核验固定地区选择、预算计数、404来源定位、产品许可及缺数据出口；Founder决定是否新批准有界获取批次。只有真实雨量与固定RONI成功配对后，才可使用OPEN_DATA_RECALCULATED，仍不得自动将模型/因果/未来预测升级。

保留旧闸门：D3 DATA_NOT_READY；P1-A PENDING；PR140 NO_VALID_PAIR；PR141 NO_VALID_VERTICAL_PROFILE；PR143 ChainB BLOCKED；PR144真实场址 DATA_NOT_READY；Stage3 METHOD_READY_NOT_VALIDATED。合并/部署/认证全部未执行。
