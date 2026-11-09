# 自然系统分类与空间真实性

版本 `atlas-research-1/2026-11-09`。[机器图](RELATION_GRAPH.json)含25单元，七类是ClimateOS研究顶层分类，**不是声称某机构发布了这套统一分类**。跨系统对象可有多种研究关系。

| 系统 | 登记内容 | 权威接口与尚缺内容 |
|---|---|---|
| 大气 | 全球混合库、Walker环流、边界层、气候区、区域降雨、辐射/响应 | NOAA ENSO/GML/AGGI；Köppen-Geiger V3索引、2023论文。无边界层高度面/反演/全球模拟 |
| 海洋 | 太平洋、公海、珊瑚与沿岸 | NOAA过程、IUCN分类；公海法律边界未取得，不划归单国 |
| 水文 | 青尼罗河上下游、干流、跨境流域、全球嵌套流域接口 | NBI站点用途描述；HydroBASINS v1。无下载多边形和流量序列 |
| 陆地生态 | 森林、湿地、泥炭、干旱、农业等分类；亚马孙/北方生态背景 | IUCN GET2.0冻结版本；背景标签为作者选样，不是已验证生态边界 |
| 冰冻圈 | 冰川、海冰、积雪、冻土、极地索引 | 分类接口；范围、年代、季节性与观测产品UNKNOWN |
| 人类系统 | 甲烷源项、土地利用/农业、贸易供应链 | 复用PR143物理边界；无实际设施排放、贸易流或隐含排放 |
| 治理 | 国家、地方、条约、许可、核算与外部评分 | M49统计标识；法律/政策证据各自版本；不归一成生态总分 |

IUCN GET2.0使用realm→functional biome→ecosystem functional group→biogeographic ecotype→global ecosystem type→subglobal type六层分类；本轮只登记接口，不复制其图件或将其等同国家边界。[官方工具](https://iucn.org/resources/conservation-tool/iucn-global-ecosystem-typology)。

HydroBASINS 的12级嵌套关系基于约15角秒父栅格，不代表每条河/坝/地块都具有该测量精度；原产品CRS及边界误差未经本轮文件级确认，仍UNKNOWN。[产品页](https://www.hydrosheds.org/products/hydrobasins)。

M49固定英文表实际248项。独立事实摘录与原网页SHA见 [m49-facts](evidence/m49-facts.json)。包含国家或地区，不是国际承认裁决；缺少的非独立统计实体不能随意补造成M49项目。Antarctica条目与单独POLAR研究索引可同时存在，但不推导主权。

**几何覆盖：国家0/248；自然单元0/25；下载GIS数据集0。** `geometry_ref=null`、`CRS=NOT_APPLICABLE_NO_GEOMETRY`。这并非源产品没有CRS，而是本轮没有接纳几何。逐国科学数据完整率未知，不以248条标识充当全球科学覆盖。

国家—单元关系为多对多的定性context表；`fraction=null`，`relation=RESEARCH_CONTEXT_NOT_GEOMETRIC_OVERLAY`。来源支持的尼罗河/ENSO/BRW连接与作者研究选样分别标注；还没有执行多边形叠加、面积分配或空间归因。
