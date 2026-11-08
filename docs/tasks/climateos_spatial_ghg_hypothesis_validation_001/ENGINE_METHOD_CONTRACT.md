# 科学方法契约：复用核心，先准入后计算

这是小型可移植设计，不是新GIS、数据库、智能体或碳计算器。唯一新增可执行程序是本任务的离线结构审计。既有核心 `cczps_lite/integration/physics_validation.py` 未修改。

## 问题→模型→门槛

| question_kind | 模型能力 | 允许输出 | 禁止越级 |
|---|---|---|---|
| STATE_CONVERSION | 已有P1 gas_properties（当前CH4专用） | x_dry、x_wet、质量浓度、参考干体积及误差 | 源强/GWP/辐射强迫 |
| TRANSPORT | 未来成熟输运工具接口，当前不执行 | 指定时空的浓度增强/负荷、守恒 | 没有化学模块就给CH4气候寿命 |
| CHEMISTRY_RADIATION | 未来版本锁定化学/辐射模型，当前不执行 | 按气体拆分RF、指标、结构误差 | 航空总效应改名CO2纯气体高度效应 |
| FACILITY_MITIGATION | 已有过程研究框架，参数缺失保持不可执行 | 条件化测量/治理建议 | 实测减排率、信用、全国总量 |

## 最小输入字段

`task_id, question_kind, gas, process, source_url, source_version, licence, retrieval_utc, original_sha256, method_version, observation_id`；`latitude, longitude, terrain_elevation_m, release_height_agl_m, altitude_m, altitude_datum, pressure_coordinate`；`time_start_utc, time_end_utc, native_time_basis, time_support, measurement_or_proxy`；`instrument_id, calibration_scale, qc_definition, qa_flags, detection_limit, uncertainty_coverage, covariance_reference, spatial_support, air_mass_evidence`。

状态换算另需 `x_dry_mol_mol, ambient_pressure_pa, ambient_temperature_k, vapour_pressure_pa` 及其协方差；释放反事实另需 `released_mass_kg, duration_s, injection_geometry, meteorology_version, chemistry_version, initial_conditions, boundary_conditions, no_pulse_control, conservation_tolerance, validation_holdout`。地面设施与航空共享元数据字段，但process、gas、空间支持和科学结果类型不可混并。

显式区分：直接测量（气体/P/T）、提供者重构（AirCore采样时间/高度分配）、代理（地理气候分类）、混杂（风、季节、气团、源区）、可干预量（源率、捕集、释放高度）；经纬度/海拔本身不是反应速率系数。

## P1公式、单位与误差传播

令x为干摩尔分数mol/mol，P/e为总压/水汽分压Pa，T为K，M为kg/mol：

```
c = x(P-e)M/(RT)                         [kg/m³]
x_wet = x(P-e)/P                         [mol/mol]
V_ref,dry = V_actual,wet(P-e)/P_ref*T_ref/T [m³]
```

CH4的M=0.016043kg/mol，R=8.31446261815324J/(mol·K)，来自现有核心；参考干状态须显式声明P_ref=101325Pa、T_ref=273.15K，而不是默认为现场条件。转换：ppb×10⁻⁹、ppm×10⁻⁶、mb×100→Pa、°C+273.15→K、kg/m³×10⁶→mg/m³。守恒检查c_actual V_actual = c_ref V_ref（同一气体干物质量）；没有来源完整e不能擅自设0。

对z=(x,P,T,e)，一阶雅可比J=(c/x, c/(P−e), −c/T, −c/(P−e))，x=0时用解析∂c/∂x=(P−e)M/(RT)避免0/0。u²(c)=JΣJᵀ，再单列或合理纳入采样代表性和模型误差，不能默认为零。两层差值u²(Δ)=u²(cA)+u²(cB)−2Cov(cA,cB)。共享校准、温湿度相关、扩散与时间自相关会影响区间；不得只把逐行err除√N。

若从RH计算e，还需e=RH/100·e_s(T)，声明水/冰饱和定义、公式适用域及RH/T协方差；这是当前缺口，不运行替代算法。对标准体积也用相应雅可比与共同输入协方差，不把体积和浓度当独立。

`gas_properties`硬编码M_CH4；本轮不能传CO2值后声称算出CO2。CO2需要另经审查的显式气体参数接口和独立解析验证；本任务只写接口要求，不改核心。气压类型错误、K/°C混用、ppb未转换、e≥P、未知湿度参照、无限值、未审查gas均拒绝。

## 输出状态与执行权

输出包含 `input_hashes, method_version, units, time_space_support, global_gate_blockers, row_loss_reasons, effective_sample_size_status, uncertainty_budget, evidence_class, scientific_admission`。原有P1数学回归测试通过≠观测准入通过。未知值用UNKNOWN/null，不用零。全局门缺失时不调用任何物理/气候模型。

本轮 `p1_observation_run_enabled=false`、`same_mass_model_run_enabled=false`；它们不是待用户点击就自动启动的产品开关。审计脚本即使门都人工改为VERIFIED，也只返回REQUIRES_SEPARATE_SCIENTIFIC_REVIEW，不自动运行或提升状态。未来工具适配须显式记录授权、气体/边界、离线输入及版本，无隐式下载或调参。
