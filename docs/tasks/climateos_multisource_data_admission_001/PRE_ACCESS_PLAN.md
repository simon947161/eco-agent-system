# 数值读取前固定协议 — multisource/1

授权依据：本目录TASKBOOK_ZH.md，冻结PR148 D da4d7f21c5fcac920e49f34ac1f0ebf6ef1218f9。本文件在本轮任何天气载荷GET前固定；已进行官方元数据浏览和一个NOAA单站HEAD请求，未读天气值。

研究问题、地区、站点、阈值、季节及统计方案完整继承PR148 PRE_REGISTERED_ANALYSIS_PLAN.md和PLAN.json。原失败收据不改。先取得Wagga原三站 ASN00072150、ASN00074104、ASN00072008 的当前官方GHCN-M v4单站CSV；三站等权、任何一站月不合格则组合月缺测；不得换站或退为一站代表原面板。若本面板成功即停止获取其他地区，保留Rockhampton/Perth未覆盖。

访问范围为最多8平台、3产品、6实际文件、单文件25MB/合计75MB；本轮metadata浏览与HEAD分别记录，无原始载荷文件的HTTP HEAD不计文件。所有下载包括元数据文件均计数；不取旧全球tar归档，不重试失败URL。七个平台固定为SILO、BoM AGCD、NOAA NCEI、NASA POWER、Copernicus CDS、CMA、CASEarth。先做只读可用性/许可/支持检查：SILO点API需要有效个人联系邮箱，本轮无已授权联系身份，不填假邮箱；BoM旧受阻图表不重试；NASA1981起资料不能满足原24个基准季门；CDS新身份/令牌不申请；中国区域资料不冒充澳洲；CMA/CASEarth工具不可读则记录UNKNOWN。

主获取源为官方Data.gov产品记录指向的长路径 `/data/global-historical-climatology-network-monthly/v4/precipitation/access/`。Wagga AMO HEAD200，108460字节，Last-Modified 2026-11-05。这是PR148评审指明的当前单站读取方式，不是重试旧404。产品级Data.gov列CC0但同时有non-public/otherRestrictions和异常temporal字段；结合NCEI公开Direct Download与其产品元数据、实际无鉴权访问，允许本次非商业研究；冲突保留，不能扩大为所有NOAA产品/商业法律保证。原始小文件保留署名和原字节；不重许可第三方图片或文献。

如果该三站组合不合格，只可转向已登记且合法支持同Wagga中心的SILO或BoM格点新support版本；要在该载荷GET前另写不可覆盖的support补充记录，明确点/格点/插值而非三站。NASA可作短片段QC但不得降低24/40完整性门；如没有适格替代，则DATA_NOT_READY，不制造概率。不通过增加数值实验来解除权限限制。

冻结分析：1961–2020、基准1961–1990；JJA/SON同期和同年JJA→SON；RONI原SHA、ERSSTv6与±0.5单季阈值不变。QC继承PR148：Q非空、M非空、trace=-1、其他负数、未知标志拒绝；空M日完整性UNKNOWN。毫米转换依据所用产品格式，不猜不同API单位。每季≥24基准季及≥40分析季；相等中位数neither；20/80为Type7；高温NOT_ASSESSED。

统计按旧预登记执行所有三模式和三相位干/湿，k/n、Wilson95%、与非相位/全体差、暖冷差；循环年块3和5、2000次、种子147148；保持60个年槽和缺测，使用共同抽样序列，主区间固定阈值、另重估基准中位数（≥15个有效抽样基准槽）；报告有效重复数和<1800不稳定。前后30年同阈值、1991–2020中位数及20/80敏感性；训练1961–90的Jeffreys平滑概率，1991–2020固定留出Brier与训练无条件基线比较，不调参。相位暖/冷n<5只作LOW_N描述。

IOD/SAM本轮没有获准入的同步原字节；不为填平台扩取指数。记CONFOUNDER_NOT_CONTROLLED，不能解释为独立因果。反例输出全部暖且湿、冷且干年份；1992只在实际值支持时称反例。气象数值和统计关系不能推进旧甲烷/流域/政策科学闸门。

成功停止条件：一个局地面板合法数据与RONI配对、完成预定统计与QC后不再扩源。失败继续在已列候选与预算内按适配性检查，而不是一个URL失败就停止全任务。不可改变旧文件或旧HEAD。本轮新结果须独立评审，scientific_admission=PENDING。
