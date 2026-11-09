# 一个真实开放数据候选：局部复算成功，全场准入未通过

**候选数1/最多2，调查停止。** 复用PR139已审来源，不扩展设施采集。Li, Jiuling (2025), *Sewer CH4*, v1，DOI [10.5281/zenodo.17718964](https://zenodo.org/records/17718964)，CC BY4.0。公开记录和ZIP各访问一次，没有重试受阻地址。

取得原始 [SL1.zip](evidence/raw/SL1.zip)，61,969字节，发布者MD5 `111905ec94e77b483048b974c38564e9`，SHA256 `d559b1c81e31090c7563accea4091b215c4a0d533d0a23d79b251dd83b9cb589`。ZIP未改，版权归原作者；归档与派生均按CC BY4.0署名，转换不是作者原始字段。获取时间/HTML哈希/许可链接见[收据](evidence/open-case-acquisition.json)。

实际运行 [check_open_fragment.py](check_open_fragment.py)：stdlib读取ZIP内 `Data for Network SL1/Measured_Methane_Data_SL1.xlsx` 第一工作表，校验标题、23条日期/溶解CH4、选定单元格无缺失、无负值、与PR139原转录23/23一致（容差1e−12 mg/L）。完整Excel文件hash及逐行原值/派生值见[结果](evidence/open-fragment-results.json)。

唯一新数值片段：

```text
1 mg/L = (10^-6 kg)/(10^-3 m³) = 0.001 kg/m³
首条12.57978 mg/L → 0.01257978 kg/m³
```

使用Decimal逐行正反换算；该转换因子精确，观测不确定性仍UNKNOWN。这是液相浓度，不套理想气体式，不乘气象系数。没有积分流量、运行上游模型、拟合参数、推源强或比较治理措施。

|证据维度|本轮真实状态|
|---|---|
|版权/字节/字段|RAW_BYTES_VERIFIED；许可页和发布者MD5核对|
|时间|Excel naive日期保留；时区UNKNOWN，不擅自赋UTC/AEST|
|空间|SL1管网标签；坐标、单点/网络代表性UNKNOWN；不是填埋场|
|方法/QC|工作表观察值；仪器、校准、采样/保存方法和QC旗标未在所选表闭合|
|缺失/不确定性|所选23条A/B单元无缺失；不等于完整观测期无缺失；误差/检出限UNKNOWN|
|流量|继承PR139的1705行/311独立时间戳歧义；本轮不重算积分，不连接为气体排放|
|分层结论|OPEN_FRAGMENT_RECALCULATED_WITH_LIMITS；真实填埋完整包 OPEN_CASE_DATA_NOT_READY|

为何不选第二候选：一个合法片段已验证原始字节→字段→转换→反算→结果链；继续下载不能自动补齐同设施/同时段/校准条件。本任务重点是审查协议，不是新增站点数量。真实片段不进入只支持合成账的reviewer求解路由；其报告记录为真实数据局部算术，而完整设施方法/效果为NOT_ASSESSED。下一次真实申报需气体流量+组分+状态基准+校准+同边界同时间原件，另行授权后再决定。
