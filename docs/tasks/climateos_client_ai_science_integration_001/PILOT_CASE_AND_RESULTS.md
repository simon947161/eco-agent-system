# 一个真实站点的端到端验证

选择候选1：既有 NOAA GHCND USW00094728（纽约Central Park）2025-05-01..03归档。未调查候选2，不扩展搜寻。输入不是合成数据，负例测试才使用显式变异。原始路径 docs/tasks/climateos_dynamic_quant_001/evidence/noaa-daily.json；SHA256 0d2d7217aa912df6418c69117b6f1b2bfde6f888ff3a8cf152830f9b630f6bbb。原receipt获取时间是本地下载完成mtime，非服务器证明。本轮离线复用，不谎称重新下载。

[原始API](https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=USW00094728&startDate=2025-05-01&endDate=2025-05-03&dataTypes=TMAX,TMIN,AWND&format=json&units=metric&includeAttributes=true&includeStationName=true&includeStationLocation=true)。[NCEI政策](https://www.ncei.noaa.gov/sites/default/files/2023-12/NCEI%20PD-10-2-02%20-%20Open%20Data%20Policy%20Signed.pdf)2022-12-14 §4a，NOAA美国政府环境资料在美国属公共领域；不推论全部第三方资料或全球均CC0。保留NOAA归属，不暗示背书。[GHCN格式说明](https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt)本轮读取版本3.35；历史归档版本UNKNOWN，以SHA冻结；API units=metric，不把原始.dly缩放规则再次套用。

问题见 request.json。执行后的 trace 在 evidence/audit.json，顺序：闭集问题→本地权限→来源/许可哈希→现有空间时间单位检查→QC→现有描述均值→法规NOT_ASSESSED→中文说明。气温数据21.7、28.9、29.4 °C；风速2.4、1.0、1.3 m/s。均值公式仅 Σx/n；n=3，无回归、排放积分或预测。3/3提供方日覆盖，2变量共6必需值均存在；原文件TMIN不是本例分析变量。

TMAX/AWND原标记实际字串为 `,,W`，中间QFLAG为空。空标记不能保证无误差，未自行去噪或插补。provider日界、校准和仪器不确定性未验证。没有逐小时记录，不将站点代表纽约全域，更不代表Cooma。

空间结果：GeoJSON经度-73.96925、纬度40.77898，边界框[minlon,minlat,maxlon,maxlat]为同一个点。EPSG:4326沿用旧合同，坐标基准未独立测量核实；位置精度UNKNOWN，海拔42.7未用于高度/距离计算。可以重算坐标与边界框；没有地图UI改动或浏览器验收声明。

结果 LOCAL_VERIFIED_PUBLIC_DESCRIPTIVE_SLICE。客户语境只是本地模拟，没有真实客户验收数据或客观效益比较。禁止从三日数值产生趋势、甲烷、污染、健康风险、法律合规或碳信用结论。
