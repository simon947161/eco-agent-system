# CLIMATEOS-ENSO-REGIONAL-WEATHER-PROBABILITY-001
## Codex执行任务书：ENSO历史指数→澳大利亚区域降雨/高温条件概率→CCZPS/EcoEngine证据审查
日期：2026-11-10 Australia/Sydney
Founder授权：立即开展有界真实开放数据研究、历史统计、反证、离线可复算验证。无需再次询问是否启动；不批准生产预测/对外发布预报/新大模型/付费API/私人数据/部署/合并。
仓库 simon947161/eco-agent-system
分支 research/enso-regional-weather-probability-001
冻结父PR147交付HEAD 48d0f576e651cd5072e6319ea1539ffa5ba02936
先核最新远程HEAD、PR143–147状态、原有气象和CCZPS代码；仅在独立分支工作。
**核心问题**：在固定地区、季节、历史期和明确的ENSO定义下，偏干/偏湿/高温事件的条件概率与非ENSO基线相比是多少？变化多大、置信与稳健性如何？哪些物理环流机制支持、哪些反证/混杂可能解释？这不是实时天气预测、确定性归因或ENSO必然导致干旱的声明。

## 0. 复用和冻结
完整阅读PR147 TRAJECTORY_ENSO.md、computed-B.json、RONI.ascii.txt、roni-metadata、OPEN_DATA_AND_SOURCE_REGISTER、反证、Founder报告、ChatGPT评审 https://github.com/simon947161/eco-agent-system/pull/147#issuecomment-6756526286；PR146全球自然关系Atlas，PR143/144甲烷，PR145 ECOChain分层审查。复用现有cczps_lite/integration/physical_process_trajectory.py及EcoEngine气象/气候代码，避免平行数据模型/新门户。PR147 RONI 1961–2020历史指数统计及其SHA冻结不改，所有科学准入PENDING。
**甲烷与水文保护**：复跑PR143–147对应测试，固定原结果0.569344413968403W/m²、甲烷三组合成质量账、三节点合成水文残差0、Cooma 31条E质量不可用、Scorecard澳洲文本冲突及未发送草稿。不得重算/改写/提升科学状态；新ENSO研究不成为CH4或水文准入。

## 1. 区域与研究设计先固定，防止事后挑结果
首选澳大利亚3个有物理差异的区域：NSW内陆/东南部（可包含Snowy Mountains相关格点但不冒充具体城镇）、QLD东部或东北部、WA西南部/西部。若数据产品只支持格点，固定经纬度格点或区域多边形、CRS、海陆掩膜、空间加权方法、面积/站点代表性；不得以一个点代表整个州。若3区资料受阻，可收敛至1–2区并保留缺口。不得因为结果显著临时更换区域。
主要季节JJA与SON，必要时DJF/MAM做预先登记的敏感性；固定1961–2020与PR147 RONI对齐，若降雨数据实际覆盖不齐则明示可用重叠窗口、不可冒充完整60年。ENSO状态：使用冻结RONI ERSSTv6 1991–2020基准、阈值±0.5°C、单季分类；严格区别官方5重叠季事件定义、ONI、SOI。允许单独做RONI替代版本/ONI敏感性，但不能混合定义。预注册一次“季节同期”“JJA→SON滞后”两种分析；不要从大量窗口筛选最好结果。

## 2. 真实开放天气数据准入：先合法取得，再统计
优先BOM AGCD逐日/月降雨格点、BOM区域气候数据/ACORN-SAT高温指标；备选有明确许可、版本和质量标记的官方/研究开放产品（如ERA5、GPCC、CRU、GHCN/NOAA等，视访问与许可），优先一套同质雨量产品；**不能把再分析格点称为原始实测站点**。最多3个数据产品候选、最多2个实际下载、最多3个区域。不要无限换端点绕过403/499或登录限制；若官方页面不提供直接数据，使用明确合法的公开替代并注明产品差异，若无法取得则 DATA_NOT_READY。
每份数据记录URL、正式版本、时间覆盖、许可与再分发权、原始字节SHA、时间/时区、单位、格点/站点定义、缺失/质量码、处理步骤、来源校准和空间代表性。未经许可不提交完整原始大文件到Git；可提交可再分发的小型派生表或哈希与复现脚本。不能用天气预报图片/新闻文字冒充历史降雨序列。
最低成功门：至少一个真实合法开放的ENSO指数与一个同时间窗口、可解释QC的区域降雨序列成功配对；若未达到，保留明确BLOCKED，不生成假概率。

## 3. 概率定义与实际计算
预先固定事件：区域季节总降雨低于该地区1961–1990同季历史中位数定义“偏干”，高于中位数定义“偏湿”；如采用百分位20/80定义“极端偏干/偏湿”，必须事前声明且报告样本数。高温事件若有合格温度产品，则用本地区同季90百分位定义异常高温；无温度数据则明确NOT_ASSESSED，绝不从ENSO指数推温度。
核心表：P(dry|warm)、P(dry|cold)、P(dry|neutral)、P(wet|phase)、P(hot|phase)及与非该相位或基线差值、样本数k/n、时间窗、效应大小、Wilson/适当区间。用1961–1990定基准可能存在气候非平稳与自样本估计偏差，另做后30年、移动基准/替代阈值敏感性，不能将不同基准结果混称一条概率。处理序列自相关、重叠季节、样本小、空间相关；至少一种按年块/分期稳健性和留出年份或交叉验证。不得以p值或显著性筛选结果后才定研究范围。
单独研究IOD/SAM/季风等混杂：有合法同步指数则作分层或受限多变量模型，样本不够则明确混杂未控制，不声称ENSO独立因果效应。保留物理机制：SST梯度→信风/Walker/对流→区域水汽输送与降雨概率，必须有官方/同行来源与反例；不能仅凭相关就量化环流传输系数。

## 4. 反证与比较
至少检查一例ENSO相位与当地降雨不符合常见预期的真实年份；复核BoM有关2023 IOD、SAM、冷锋/气旋等说明，但新闻只是机制背景，不是替代数据。按来源分别记录SOURCE_SUPPORTS / SOURCE_CONTRADICTS / NOT_COMPARABLE。对地区差异、非平稳、站点/格点不一致、样本选择、指数版本、其他模态与因果不可识别提供中文解释。结果必须同时报告反例和零效应/方向相反的区域，不允许只挑成功的地区。

## 5. 可执行交付与主线接口
复用原Atlas query/trace和PR147 trajectory结构，新增最小离线`ENSO_REGION_WEATHER` evidence calculation模块/命令，输出逐年对齐表、样本数、事件标签、概率、效应差、置信/稳健性、来源、反证、质量门和人话解释；真实配对成功才标OPEN_DATA_RECALCULATED，模型/因果门独立PENDING。缺数据时返回DATA_NOT_READY，不可回退到PR147的JJA→SON指数持续率冒充天气概率。
把统计结果作为EcoEngine的条件性证据输入，CCZPS仅进行有界情景/不确定性比较，不自动生成确定性预报或治理批准；ECOChain/PR145记录证据与审查结果、许可/版本/不确定性和反证，不假称canonical正式接入。至少3个负例测试：错季节/时区、指数版本错配、降雨单位/区域支持错配、缺测填零、非因果外推、政策评分混入物理量、越权认证等。回归旧甲烷/水文、保持所有旧闸门。
如果有真实数据，至少两个地区有可复算对照是加分项，但不能为凑数降低来源/QC标准。Founder中文报告要直接回答：哪个区域在厄尔尼诺下偏干概率是多少？样本几次？历史反例是什么？与拉尼娜相比差多少？这种关系能不能推广到未来？若数据未准入则解释确切原因。

## 6. 预算、证据和GitHub交接
限最多3个气象数据产品候选、2个实际下载、3个澳洲区域、2个主季节、1套固定指数、最多3个同步混杂指数；不建全球实时采集、不跑大气GCM、不购买/付费、不联系外部机构、不使用Council私有数据、不扩到甲烷/水文真实模拟。数据超出许可或大小合理限度则只留收据/小型派生表，不提交大文件。真实数据取得失败不循环重试。
必交 docs/tasks/climateos_enso_regional_weather_probability_001/：
TASKBOOK_ZH.md、README.md、FOUNDER_REPORT_ZH.md、PRE_REGISTERED_ANALYSIS_PLAN.md、SOURCE_AND_LICENSE_REGISTER.md、REGION_AND_TIME_DEFINITION.md、PAIRED_ENSO_WEATHER_DATA.(csv/json)、CONDITIONAL_PROBABILITY_RESULTS.md、UNCERTAINTY_AND_SENSITIVITY.md、COUNTEREXAMPLES.md、PHYSICAL_MECHANISM_AND_CONFOUNDERS.md、CCZPS_ECOCHAIN_HANDOFF.md、QA_AND_VALIDATION.md、NEXT_SESSION.md、CRP_HANDOFF.md、REVIEW_REQUEST.json、HANDOFF_STATUS.json、scripts/tests/evidence。若真实天气数据无法准入，PAIRED文件明确为空/阻塞，不伪造数据。
建立独立stacked Draft PR，冻结父HEAD为PR147 D；核对R/D差异和最终PR HEAD、真实CI、测试/原始字节SHA、科学限制；提交中文Founder报告和独立评审请求，Founder转交ChatGPT后再审查。保持PR143–147 Draft不合并、不部署、不发法定认证、不升级既有科学准入。
成功标准不是“概率看起来高”，而是一个或多个可追溯区域的历史真实降雨与ENSO状态正确配对，公开可复算并提供样本数、反例、不确定性与失效条件；以及甲烷/水文成果未受破坏。任何数据阻塞诚实报告，给出最小解锁条件，不以合成概率冒充科学成果。
