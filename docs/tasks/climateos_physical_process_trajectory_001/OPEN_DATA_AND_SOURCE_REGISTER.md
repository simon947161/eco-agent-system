# 来源、数据权利与准入

完整17条来源记录在 [SOURCES.json](SOURCES.json)：10个新增主要主题、7条继承/作者来源。A/B/C数据候选分别1、2、1，C仅一个实测片段；没有新GIS、私人Council数据、付费API或周期采集。论文只用于文献，未作为额外数据候选下载。

| 数据/来源 | 实际取得与版本 | 权利与质量 | 本轮准入 |
|---|---|---|---|
| NOAA GML AGGI | 2025更新网页一次下载；观测段、Table1、Table2 | 官方政府数值公开领域，保留NOAA归属；网页正文不归档 | 全球年度聚合丰度→已发表关系局部复算 |
| CPC RONI | 原ASCII 14752字节，Last-Modified 2026-11-03；ERSSTv6/1991–2020 | NWS公开领域、不得暗示官方背书；无逐行QC/uncertainty | 真实历史指数统计，不称原始温度传感器资料 |
| BoM AGCD雨量 | 说明页可读，参数化产品发现页工具不可访问；未取得payload | 明确允许研究；不把图表CC BY4.0推及原始数值 | DATA_NOT_READY，天气概率null；不声称禁止研究或伪造HTTP403 |
| HRS410033 | PR129固定公共JSON继承；index/分片哈希核验，取2020-01 | ©WaterNSW CC BY3.0 AU；BoM HRS；不重取原CSV；31条E | STRUCTURAL_QC_ONLY；无流量总和或尼罗河映射 |
| NBI站点 | 官方表重新读，Eldeim/Khartoum/Halfaya/Dongola | 只取定位事实，不推定流量开放许可 | 定性拓扑 |
| NOAA/BoM机制说明 | 官方网站，BoM更新2026-09-28 | 作者摘要，无图片复制；预测段不作历史观测 | 机制/反证 |
| Nile研究 | Siam & Eltahir 2015，出版方摘要/CC BY3.0 | 未获取原始资料、未重现原模型 | 区域关联文献 |
| 湿地相反研究 | 2024/2025出版方索引摘录；正文转身份页不可访问 | 只保存书目信息与摘要，未取全文或数据 | 争议登记，全文核验PENDING |
| 澳洲法 | Compilation2/C2025C00153固定HTML下载，latest details核对 | 只保留事实与定位，无整页再发布 | s10基准年独立复核 |
| Scorecard | PR146快照收据+本轮403前网页读取器可见内容 | 原站直接HTTP403已停；短引文，不提交整页 | 当前字节新鲜度PENDING；不能说最新原件完整复核 |

原始下载SHA-256及时间在 [acquisition.json](evidence/acquisition.json)。关键值：

- AGGI HTML `9ffa03d571765dc55d46d57c8e1494e86340d8ddda025c77b3724f48e199dbe1`。
- RONI原始字节 `1297887f581b6190e459cbbf8bdec9a703ff65c1a229e2de4dd94285254f35c8`（Git属性禁用换行转换）。
- 澳洲法HTML `02397536f5043ebfe8d5a3f2e0f6309af6a470e03ed5ff8c516e70e1723680c3`。
- 继承HRS index `bd4728ea129330d5e1abd35dce9b223df87c6801c18ad52e7d9db0eb7e0d45ca`；2020分片与源CSV旧哈希保存在 [子集凭据](evidence/hrs-january-2020.json)。原CSV旧哈希不是本轮重新取得的证据。

读取时间UTC2026-11-09对应悉尼2026-11-10；网页“crawled today”不等于源文件今日修改。HTTP Last-Modified、页面JSON-LD和本轮取得时间分开保存。原Scorecard页面级日期2021-03-29/2025-09-25不能推为AU卡片修改日。

原字节哈希与Git文本LF规范化哈希不同，见 [manifest.json](evidence/manifest.json)。公开来源引用不意味着政府、出版者或Council认可ClimateOS。全部下载失败、不再尝试的端点与预算在 [access-limits.json](evidence/access-limits.json)。
