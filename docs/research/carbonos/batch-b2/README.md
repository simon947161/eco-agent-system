# Batch B2：许可、坐标与小样本身份验证

2026-11-04 · [评审输入](https://github.com/simon947161/eco-agent-system/pull/132#issuecomment-6621231758) · Issue131 / Draft PR132。

完成联邦、NSW、QLD重点来源的许可/版本/字段/坐标元数据核查；形成2个QLD污水厂候选（上限10），不是完整身份验证成功。没有固废/填埋场候选入库；联邦与NSW仅元数据审查，抽样覆盖不足明确保留。非随机、可访问性驱动的小样本不能支持任何全国数量、排放或覆盖率。

入口：[10页展示](index.html)、[来源审计](SOURCE_METADATA_AUDIT.json)、[身份JSON](IDENTITY_CANDIDATES.json)、[CSV](IDENTITY_CANDIDATES.csv)、[冲突/失败](CONFLICTS_AND_FAILURES.json)、[协议补充](BATCH_C_PROTOCOL_ADDENDUM.md)、[交接](NEXT_SESSION.md)。

South与West拥有不同名称/地址/旧状态，尽管审批持有人相同仍保持两个候选。RP1仅属于South的排口监测点。63(1e)是活动分类，非许可证编号。审批持有人未自动升级为运营主体。实际厂址ID、处理单元ID、运营主体ID、许可文书ID及坐标均未验证，以null保留。未将任何候选计作填埋场。

## 许可与证据边界

© The State of Queensland (Department of the Environment, Tourism, Science and Innovation)。两页选定事实字段依其[CC BY4默认条款](https://www.detsi.qld.gov.au/help/legal/copyright)署名、改编为实体表；不含图片、标志或第三方地图。原字段摘录见evidence；文件哈希固定本轮摘录，不声称等于原始HTTP正文。联邦默认版权政策不覆盖未经核实的第三方workbook条款；NSW数据库/修改限制未获明确开放许可，因此不发布其记录或几何。

元数据表逐条保留官方URL。NSW图层公开EPSG4283、多边形及字段，但未提供精度；GA ordinal confidence不能换算成米，元数据日期/下载指向也有冲突。QLD页面未公布可核验数值坐标，不推算或地理编码。2019网页状态不是2026实地验证。

## 提交ChatGPT审查

请逐项判断：来源条款是否支持已发布选定字段；元数据版本冲突是否正确处理；持有人/运营商/许可/监测点是否充分分离；保留两个厂址候选的依据是否足够；哪些证据可解锁后续身份验证。不要将工件PASS当成科学通过。P1-A科学准入PENDING；无数值实验、无部署/合并、无私人Council数据。
