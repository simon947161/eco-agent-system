# 高空观测准入：恰好三个候选

| 项目 | NASA ATom merged/Picarro | NOAA AirCore v20210813 | WDCGG Jungfraujoch CH4 |
|---|---|---|---|
| 来源/证据 | S1/S2，方法PDF完整，数值未取得 | S3原ZIP及一个L2+INI+L1met | S4元数据 |
| 版本 | v1/v2不能混用；Picarro ATom1–4方法 | ZIP20210813，L2文件v20210811 | 2025-07-08-1503 |
| 访问/许可 | NASA索引称开放；具体数值取得/再分发未验证；403停止 | 公开200，CC0，引用DOI；本地SHA验证，发布者checksum未知 | GAW政策及隐私确认未操作；未取得文件，不假设CC0 |
| 仪器 | Picarro G2401m WSCRDS；分析池80torr不是环境P | AirCore BIG002；分析仪CFKBDS2007；INI气象传感器“????” | Picarro G1301/G2401，站点时间分段 |
| 时间 | UTC_Start为起飞日午夜后秒/1s bin起点；原生采样1.2或2s并分箱 | UTC重构采样时刻；非实验室分析时钟；小数秒与整数秒标签分开 | UTC+01:00，不能直接当UTC；小时2005–2024元数据 |
| 干湿/标定 | 干摩尔分数；CO2 X2007、CH4 X2004A、CO X2014A；经验水汽校正 | README CO2 X2019/CH4 X2004；INI瓶X2007/X2004A；转换链未证实，保留差异 | X2004A；数据/气象版本更新可能不同步 |
| 分析误差 | §5约CO2 0.08ppm、CH4 0.7ppb（1σ/1s）；10s CO2约0.07ppm；不代替P/T/e误差 | L2逐行气体err及扩散高度跨度；err覆盖因子和全协方差未齐 | 元数据扩展不确定度U=2√(0.31²+(3.61e−4 c)²)ppb；不是本次重算结果 |
| 地理/垂直 | 任务通常约0.2–12km描述不能代替所选飞行的真实范围；本轮没有飞行 | 本次Alt 721.818–21685.831m；纬36.6004–36.8538N，经−98.2139至−97.7074E；Alt基准未知 | 高山固定站，进气口10mAGL；不把进气高度当站点海拔；非同次垂直剖面 |
| QC/同步 | 采样时滞随环境P/T修正，约2–15s依campaign；未读逐行QC | INI cutoffs30–2166，CO tracer；L2已加工，不重新用cutoff裁L2；RH可能取上升段、T/P下降段 | 2014起每小时≥240个5秒样本的公开规则；未验证实际时序 |
| 代表性 | 飞机移动、气团/航线/高度混杂；未获导航实值 | 单次气球下降，不是同地点多高度干预；无L2风；扩散支持不是独立样本 | 固定站时间变化非释放高度干预 |
| 结果 | METHOD_DOCUMENTED / NUMERICAL_FILE_NOT_OBTAINED | STRUCTURE_VERIFIED / QUANTITATIVE_GATE_BLOCKED | METADATA_ONLY / PROFILE_NOT_APPLICABLE |

## 选择与完整性

原ZIP共1,551成员（含目录/macOS附属文件），133个路径匹配的L2 `.txt`；这不是159 flight days的复核，也不是所有飞行数量。按 [PROFILE_PROTOCOL.json](PROFILE_PROTOCOL.json) 字典序取第一个同时含INI和L1met的L2：`Flight_20120114/launch2/AirCoreBIG002_201201141836_v20210811.txt`，不因结果不利再选更“好看”的剖面。

归档只有一个原始剖面成员及其配套文档，未手改数值；它是提供者加工的Level2发布文件，**不是未处理的传感器电压或所有原始分析记录**。L1实验室pic数据未用于重建；本轮不宣称独立重做提供者校准。完整输入成员名、大小、SHA及ZIP成员CRC见 [INPUT_MANIFEST.json](INPUT_MANIFEST.json)。

所有全球元数据门逐项存于 [METADATA_GATES.json](METADATA_GATES.json)。发现标定瓶尺度与最终产品版本说明不同，可能来自历史瓶标签与再处理，但本轮没有该转换证明，故保留UNRESOLVED，不擅自宣称发布者错误，也不静默选择一个尺度。
