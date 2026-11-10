# CLIMATEOS-MULTISOURCE-DATA-ADMISSION-001
## Codex立即执行｜小型多源环境数据接入、ENSO真实配对与主线计算恢复
日期：2026-11-10 Australia/Sydney
Founder授权：立即执行本轮有界公开数据访问、合法小样本下载、质量核查、离线可复算计算；无需再次征询启动许可。若来源受限、要求注册付费/授权或访问失败，不绕过，记录并转向其他已批准候选。不得以“一个URL404”停止整个任务。
仓库 simon947161/eco-agent-system
工作分支 research/climateos-multisource-data-admission-001
冻结父PR148 D da4d7f21c5fcac920e49f34ac1f0ebf6ef1218f9
先读PR148 Founder报告/获取收据/预登记方案/ChatGPT评审 https://github.com/simon947161/eco-agent-system/pull/148#issuecomment-6763303407，PR147 RONI与物理轨迹，PR146 Atlas，旧EcoEngine/CCZPS/气象/GIS连接器与PR143–145审查。禁止重写旧PR和历史证据；本轮只新增薄适配器/有界数据与验收记录。
**主目标**：不是另建数据门户、收集全球API列表或继续扩文档，而是找到至少一个实际可合法获取、质量可解释的历史澳大利亚降雨序列，将它接入现有EcoEngine→ENSO→CCZPS→ECOChain证据接口，尝试完成一段真实历史条件概率计算。研究问题优先于平台；每个数据来源都必须可替换、可审计。

## 1. 有界多源发现与访问决策
候选按研究适配性排序，而非机构地位：澳大利亚SILO/Long Paddock公开文件或无需新凭据的接口、BoM AGCD可用公开文件、NASA POWER历史日/月点数据、NOAA NCEI GHCN-M v4当前单站CSV、Copernicus/ERA5合法可访问的小区域切片；中国气象数据网/国家气象科学数据中心、中国科学院CASEarth及其他明确开放的中国气象/遥感服务作为**跨区域后备与未来气候/生态数据网关候选**，不得将中国格点或站点资料冒充澳洲同地观测。其他官方开放来源可替代，但须记录选择理由。先做metadata-only URL/目录/许可/时间覆盖/变量/空间分辨率/格式/认证需求检查；同一失败端点不反复重试，不绕过403/499/验证码、镜像限制或私人权限。
预算：最多8个候选平台作只读入口核验；最多3个实际数据产品进行小样本获取，最多6个网络数据文件下载（元数据清单可登记但每个实际下载计数）；最多3个澳大利亚地区、每区原预登记3站；不得下载全球大型归档/ERA5整年全球格点或购买/创建凭据。单文件软上限25MB，总下载软上限75MB；超过需缩小合法查询或停止该来源。优先开放许可/不需登录，若仅免费注册可用也记录USER_ACTION_REQUIRED并跳过，不要求Founder操作。
将每个来源登记：official_url、actual_access_result、data_version、license/reuse constraints、cost/auth、variable、temporal_coverage、time_basis、spatial_support、observation_vs_interpolation_vs_reanalysis、unit、QC、raw_bytes_sha256、data_product_id、fallback_reason。数据的可读性与再分发权不同；中国数据平台同样须逐产品核许可证，不默认全部开放。

## 2. 首个真实配对：保留PR148冻结研究问题
优先固定PR148 Wagga、Rockhampton、Perth三个局地组合，1961–2020、JJA/SON、同期和JJA→SON、1961–1990中位数及20/80百分位、RONI ERSSTv6(1991–2020基准)与阈值±0.5°C；**不按计算结果换站、换地区或改阈值**。若源产品无法覆盖原九站，可以选择同一Wagga中心坐标的格点/区域产品作一个**新数据支持版本**，明确它不等于原九站观测，不把它和旧站点计划混为一项复现；选择发生在读取天气结果前，固定geometry/point/grid、版本、单位、插值/再分析语义及适用性。新来源与原站点口径分别输出，禁止混合平均。
最低门：一套真实合法来源的同时间窗ENSO与区域降雨配对数据；如连续覆盖不足60年，只计算符合事前完整性门的重叠年，并清楚报告覆盖偏差；不可为了产出概率降低科学QC门。若只取得短片段，先完成质量与单位准入，不伪造完整60年概率。
首先运行真实降雨质量/缺失/日月定义/站迁/时间对齐；固定月/季节聚合与QC、可复算原字节哈希。然后计算P(dry|warm/cold/neutral)、P(wet|phase)、与非相位基线的差、每组k/n、Wilson区间、按年块bootstrap和分1961–1990/1991–2020诊断、1992等反例（仅当对应地区雨量确实支持），固定留出年/预设基线敏感性。样本数小/相关性/混杂未控制必须显式标记，统计关联不能写因果。
有温度数据且合法可用才研究高温；否则NOT_ASSESSED。IOD/SAM若没有同窗口准入指数就保留CONFOUNDER_NOT_CONTROLLED，不能用天气新闻代替指数。
至少一个地区可真实配对则可报告有界描述性结果（不是全澳结论），不因未覆盖其他地区而废弃已完成有效结果；但不能悄悄把原三地区目标说成全部完成。

## 3. 适配器设计：Source Registry + Admission Gate + Fallback
优先复用现有气象/EcoEngine、PR148 enso_regional_weather.py与PR147 trajectory，新增最小只读Source Registry和可替换输入解析器（CSV/JSON/NetCDF仅在已有库可用时；不为此装重依赖）。明确失败分层：NOT_FOUND_404、ACCESS_RESTRICTED、AUTH_REQUIRED、LICENCE_UNCLEAR、PAYLOAD_INVALID、TIME_SUPPORT_MISMATCH、QC_INSUFFICIENT、DATA_ADMITTED。只在准入成功后运行概率，不能从旧RONI指数延续率回填。
同一问题下不同来源不得无声切换：每次替代生成新source_id、method_version、data_support、reason、provenance与可比性表；同站观测/插值格点/再分析分别标识。若源A失败自动尝试下一个**已列明且在预算内的合法来源**，停止条件是有一个合格输入且完成一段真实配对，或预算用尽；避免为平台数量而多抓。
科学计算接口：物理机制来自EcoEngine/PR147，条件概率属于统计证据；CCZPS以不确定性比较不同情景，不发布具体未来天气预测；ECOChain/PR145只记录证据、反证、数据许可、版本和技术评审，未定位canonical则继续PENDING_INTEGRATION。保留科学门，不把软件PASS当现场验证。

## 4. 三条主线必须保存，不得被新网关冲掉
继承并回归：PR147 CH4 NOAA公式ERF 0.569344413968403W/m²及其适用边界，PR144甲烷合成物料账，PR147水文三节点残差0与31条E质量阻塞，PR146全球Atlas/PR145 A/B/C，Scorecard AU 2005/2030冲突及英文草稿NOT_SENT。旧PR143–148均Draft/未合并；不改变任何旧文件/HEAD/科学准入状态。新数据网关是复用能力，不是新主线。
如果本轮完成ENSO真实历史概率，Founder报告必须单独说明“回到ClimateOS主线”：下一步如何沿海温→Walker环流→区域降雨→水文/生态的链条逐段验证，而非继续无限接平台。

## 5. 测试、结果与GitHub交接
新增目录 docs/tasks/climateos_multisource_data_admission_001/
TASKBOOK_ZH.md、README.md、FOUNDER_REPORT_ZH.md、SOURCE_REGISTRY.json、ACCESS_AND_LICENCE_MATRIX.md、DOWNLOAD_RECEIPTS.json、ADMISSION_REPORT.md、PAIRED_DATA.json或.csv、PROBABILITY_RESULTS.md、UNCERTAINTY_AND_COUNTEREXAMPLES.md、CROSS_SOURCE_COMPARABILITY.md、ECOENGINE_CCZPS_ECOCHAIN_HANDOFF.md、QA_AND_VALIDATION.md、NEXT_SESSION.md、CRP_HANDOFF.md、REVIEW_REQUEST.json、HANDOFF_STATUS.json，以及必要scripts/tests/evidence。不存在的数值留null，数据无再分发权则只保存可合法分享的派生数据与原字节收据，不上传原始文件。
负例测试：404切换、403不绕过、凭据缺失、许可证未知、非澳洲来源错误地映射澳洲、RONI版本错配、时间/月/季节错位、缺测填0、雨量单位、插值当原始观测、源版本无声替换、合成数据冒充实测、样本太少仍给确定性结论、因果/认证越权。回归PR143–148旧结果与精确SHA，记录本地测试、最终D独立CI、真实网络收据。
建立独立stacked Draft PR，冻结父为PR148 D，先审远程HEAD和可选base，研究R与交付D固定；中文Founder大字/Slides式报告先说是否真实取得雨量、多少有效年、哪地区概率与区间、反例和混杂、各来源失败原因、后续科学主线最小下一步。完成后请求ChatGPT只读独立评审，不合并/部署/购买/外联/法定认证/提升科学准入。
科学成功：至少一个地区真实历史降雨与冻结RONI配对并给出可复算条件概率、限制与反证；工程成功可仅为多源准入/诚实失败，但必须区分两者。达到科学成功即停止扩展来源，将工作返回物理过程验证；否则清晰列出最小阻塞并停止预算。
