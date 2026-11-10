# 条件概率：全部未计算

状态 **DATA_NOT_READY**；[配对文件](PAIRED_ENSO_WEATHER_DATA.json) rows=[]。n=0指没有准入配对，不是地区历史没有降雨事件。k、概率、效应量和区间均 UNKNOWN/null，不能填0或按PR147暖相持续率替代。

| 地区 | JJA同期 | SON同期 | JJA→SON | 暖/冷/中性干湿 | 高温 |
|---|---|---|---|---|---|
| NSW Wagga组合 | DATA_NOT_READY | DATA_NOT_READY | DATA_NOT_READY | 全部UNKNOWN，n=0 | NOT_ASSESSED |
| QLD Rockhampton组合 | DATA_NOT_READY | DATA_NOT_READY | DATA_NOT_READY | 全部UNKNOWN，n=0 | NOT_ASSESSED |
| WA Perth组合 | DATA_NOT_READY | DATA_NOT_READY | DATA_NOT_READY | 全部UNKNOWN，n=0 | NOT_ASSESSED |

## 已登记、未在真实天气上执行的公式

设站月观测值为十分之一毫米x，合格值r=x/10 mm。区域月量为固定N站等权平均 `R_m=Σr_i,m/N`；任何缺站月不计算。季节总量 `R_y,s=Σ_m∈s R_y,m`，只接纳三个完整月份。

`T_r,s=median(R_r,y,s, y=1961…1990)`；`D=1[R<T]`、`W=1[R>T]`；等于阈值为neither。与无条件基线比较时基线也必须使用同一有效年份，不硬设50%（后期变化和ties均可改变比例）。

RONI单季H：暖H≥0.5、冷H≤−0.5、中性其他；阈值单位°C，但RONI不是降雨单位。对相位a和事件E：

`k_a=Σ 1[phase=a]1[event=E]`，`n_a=Σ 1[phase=a]`（仅有效配对），`p_a=k_a/n_a`。
`Δ_nonphase=p_a−k_not_a/n_not_a`；`Δ_base=p_a−k_all/n_all`；`Δ_warm_cold=p_warm−p_cold`。

Wilson区间（z=1.959963984540054）：
`centre=(p+z²/(2n))/(1+z²/n)`，`half=z*sqrt(p(1−p)/n+z²/(4n²))/(1+z²/n)`。n=0必须阻塞；区间不是对未来天气预测。复用PR147函数而非另抄统计库；本轮没有输入天气样本调用该估计。

基准20/80分位数和超阈值计数，以及所有效应的块自助/分期/留出比较，均为 [预登记](PRE_REGISTERED_ANALYSIS_PLAN.md) 中的**待执行方法**，不是已通过的工程或科学结果。
