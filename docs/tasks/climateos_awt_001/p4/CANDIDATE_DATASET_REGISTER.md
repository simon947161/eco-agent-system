# P4 候选登记与停止决定

评估日期：2026-11-24（Australia/Sydney）｜`READ_ONLY`｜`NO_RAW_DATA_DOWNLOADED`

授权：[Issue #164](https://github.com/simon947161/eco-agent-system/issues/164)。全量结构化记录、每个闸门的理由与来源 ID 见 [candidate_register.json](candidate_register.json)；来源阅读层级见 [source_register.json](source_register.json)。

## 真实执行范围

主动选取 4 个发布者数据集合；C01/C03/C04 详细审查，C02 遇阻即停止。Zenodo 两个版本只计同一候选。检索偶然出现的其他结果没有作为额外候选展开；法规/许可网页不计数据集。优先调查澳大利亚联邦及 NSW，再审查国际研究。未重新访问历史 D3 受阻下载、未打开 Council 数据。

|ID / 深度|原始入口与持有方|日期、粒度和预期文件|用途 / 结论|
|---|---|---|---|
|C01 详细|CER [S01](https://cer.gov.au/markets/reports-and-data/safeguard-data) [S02](https://cer.gov.au/markets/reports-and-data/safeguard-data/2024-25-baselines-and-emissions-data)|2024–25 财年，2026-04-15 发布；表最新修订 UNKNOWN。设施年报；CSV 46.93 KB / XLSX 46.87 KB，仅目录标示|可辅助权益重叠线索；不是物料批次基线。许可未核实，BLOCKED|
|C02 初筛|TfNSW [S04](https://www.transport.nsw.gov.au/operations/roads-and-waterways/environment-and-heritage/environmental-compliance/environment) [S05](https://www.transport.nsw.gov.au/system/files/media/documents/2025/SPI-Landfill-Gas-Monitoring-March-2025.pdf)|检索发现 March2025 PDF；版本、大小 UNKNOWN。官方目录403|许可和 QC 未审完，BLOCKED；未转向PDF绕过目录|
|C03 详细|Wechselberger等 / Zenodo [S06](https://zenodo.org/records/14165793) [S07](https://zenodo.org/records/14197882)|v1 2024-11-14；新记录2024-11-21。v1 Data.csv 91.1 kB、Glossary.csv 4.6 kB；不得移用为新版本大小|跨设施甲烷损失方法线索；许可文字未取得，BLOCKED|
|C04 详细|Rodriguez/Hopkins / Dryad [S09](https://datadryad.org/dataset/doi:10.5061/dryad.ht76hdrtc)|2026-02-19版；同一匿名奶牛场多个安装前后campaign；目录全包11.55 MB，不下载|CC0平台政策支持；最值得保留的方法片段，PARTIAL_METHOD_ONLY|

文件大小均是发布者标签，不是本轮测量字节。除 C02 搜索给出的 PDF URL 外，直接文件 URL 未被安全解析，保留 null；不能拼接猜测下载地址。C04 已读取网页内嵌 README，并没有下载 README 文件。

## 七个独立闸门

这里的 SUPPORTED_METADATA 只表示网页支持；NOT_TESTED 不能读作通过。所有原始文件 SHA-256=null。

|候选|G1许可|G2取件|G3来源/版本/时间/单位|G4同设施物料时间|G5残渣/能源|G6校准QC|G7方法/基线|
|---|---|---|---|---|---|---|---|
|C01|UNKNOWN|NOT_TESTED|PARTIAL|FAIL|UNKNOWN|UNKNOWN|PARTIAL|
|C02|UNKNOWN|BLOCKED|UNKNOWN|UNKNOWN|UNKNOWN|UNKNOWN|UNKNOWN|
|C03|UNKNOWN|NOT_TESTED|PARTIAL|FAIL|UNKNOWN|PARTIAL|UNKNOWN|
|C04|SUPPORTED_METADATA|NOT_TESTED|PARTIAL|FAIL|UNKNOWN|PARTIAL|UNKNOWN|

详细理由逐条存于 JSON；FAIL 是对本次完整 1000t cohort 证据链的判断，不否定原研究本身。G5 UNKNOWN 不是证明资料一定不存在，而是已读元数据未建立该链。一个条件失败不能被其他指标高分抵消，因此不加权打分。

## 有限排序与停止

仅就未来**方法核验的资料价值**：C04 → C03（先解决许可）→ C01（监管上下文）；C02 停止，不排序。没有 CANDIDATE_FOR_FOUNDER_APPROVAL 的完整数据链。

**NO_SUITABLE_DATASET。** 所有候选缺关键时间/物料/残渣或权利支持；不为了填满六项而继续搜索。地域和方法选择有偏差，本轮不能推断全国覆盖或全球不存在适合数据。任何下一轮必须有单独授权及具体证据问题。
