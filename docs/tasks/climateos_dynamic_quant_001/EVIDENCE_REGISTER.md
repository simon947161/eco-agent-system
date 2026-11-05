# 证据登记与边界

核查日期2026-11-05。官方资料只用于明确本轮数据/API/产品边界；内部历史结论不冒充新科学验证。没有绕过403、认证或TLS。天气新候选恰好两个，各文档化端点正常请求一次；后续均离线。

|ID|来源、版本与用途|状态/保存|
|---|---|---|
|E01|[NCEI API官方说明](https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation)：v1、metric与includeAttributes|VERIFIED网页；下载URL见收据|
|E02|[GHCN-Daily README](https://www.ncei.noaa.gov/pub/data/ghcn/daily/readme.txt)，页面版本3.35；数据集DOI [10.7289/V5D21VHZ](https://doi.org/10.7289/V5D21VHZ)，Menne等|VERIFIED；TMAX/AWND及质量标志；API子集未自报数据库版本，不将README版本强加于数据|
|E03|[Central Park官方站点](https://www.ncdc.noaa.gov/cdo-web/datasets/GHCND/stations/GHCND%3AUSW00094728/detail)|站点ID及坐标核对；仅该站，非NSW|
|E04|[NCEI Open Data Policy](https://www.ncei.noaa.gov/sites/default/files/2023-12/NCEI%20PD-10-2-02%20-%20Open%20Data%20Policy%20Signed.pdf)，2022-12-14，4a|NOAA/联邦数据在美国公共领域；不是所有第三方资料自动CC0；本美国站公开子集署名研究使用，无背书|
|E05|[NASA POWER Daily API](https://power.larc.nasa.gov/docs/services/api/temporal/daily/)、[数据FAQ](https://power.larc.nasa.gov/docs/faqs/data/)|VERIFIED；同化网格性质与原生尺度，不是站点|
|E06|[NASA时间FAQ](https://power.larc.nasa.gov/docs/faqs/other/)|VERIFIED；默认LST，需显式UTC。现有函数差异见审计|
|E07|[MatrixOne官方仓库](https://github.com/matrixorigin/matrixone)、[许可](https://github.com/matrixorigin/matrixone/blob/main/LICENSE)|VERIFIED官方声明/Apache2；mutable main核查日，不固定生产版本|
|E08|[MatrixOne GIS官方页](https://docs.matrixorigin.cn/mo/en/latest/MatrixOne/Overview/feature/gis.html)|PARTIALLY_VERIFIED，索引v4.2.5，直接打开失败；功能范围/性能仍待实测|
|E09|main@9eb7577e145e76161f9f1cd8509348b19c2904cc及PR130/132/133/134固定SHA|Git文件/PR快照；能力与研究状态见审计，不等于已合并/部署|

## 下载件与原始证据

1. [noaa-receipt.json](evidence/noaa-receipt.json)记录完整请求、检索完成UTC（本地下载文件mtime，不是服务端签名）、权利和语义。原始[noaa-daily.json](evidence/noaa-daily.json)原字节SHA-256为`0d2d7217aa912df6418c69117b6f1b2bfde6f888ff3a8cf152830f9b630f6bbb`；局部.gitattributes -text避免Git换行改写。三行真实观测，2025-05-01—03，不是当前天气。原始文件保留额外TMIN，但本轮只对TMAX/AWND准入和计算，不宣称审核了未用变量。
2. [nasa-secondary-receipt.json](evidence/nasa-secondary-receipt.json)含另一真实下载哈希、请求与返回版本v2.10.2/UTC/单位/坐标。Batlow网格，2025-05-01—03；只做第二源身份/时制核查，未接入智能体统计。原始JSON留授权本地`DynamicQuant-001-Evidence/nasa-power.json`；具体再分发条款未另存，故不重新发布原件。不将当地网格与NY站点融合，也没有另造气体数据。
3. [actual-run.json](evidence/actual-run.json)为真实字节离线回放；[negative-runs.json](evidence/negative-runs.json)为真实原件加修改请求的拒绝演示，不是真实环境实验。tests中修改行/重算收据的夹具明确为合成软件测试，不能当新观测。

字节哈希与Git版本可追溯，不证明原资料无误或产品有科学适用性。官方网页未全部镜像下载；无文件哈希的网页只能按URL/页面版本/核查日追溯，不虚填哈希。未收集私人地块、敏感物种点位或Council记录。

## Founder复核新增文献（非新增观测候选）

[专业智能体连接复核](PROFESSIONAL_AGENT_SCIENCE_INTEGRATION_ZH.md)末尾S1–S8/P1–P4为本证据登记的新增来源明细：EnergyPlus、BASIX、WRF、PALM模型与Dejvice实地验证、HYSPLIT、NeuralGCM/IPCC分类，以及MOI智能体/运行环境/计费。逐条列URL/DOI、版本、正文或索引核实及403/cache miss差别。没有新增天气或气体下载，原两候选上限不变。论文方法/验证与ClimateOS是否执行分开，不提升任何旧合成合同。
