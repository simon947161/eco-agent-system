# CLIMATEOS-GLOBAL-METHOD-EVIDENCE-ECOCHAIN-001
## 唯一总任务书：全球公开科学方法论证、选择性复算、标准证据接口与 ECOChain 治理增量
日期：2026-11-09 Australia/Sydney
Founder已批准：开展有界的全球公开来源研究、合法开放数据选择性复算、科学/行政/工程方法交叉对照、可运行的技术评审原型，并将本轮战略备忘录接入既有ECOChain研究。不是授权法定认证、对外发证、全球实时监控、商业化、联系机构、付费、私有数据或部署。
仓库：simon947161/eco-agent-system
任务分支：research/climateos-global-method-evidence-ecochain-001
冻结父提交：PR #144 HEAD 77a35e2723372a290579e4549a86781e2be65c04
先审计最新远程分支/PR #138–144及已存在的 ECOChain/EcoChain/Eco-Chain/E4、CCZPS、ClimateOS Knowledge Garden、NatureHash、Evidence Passport、Enotebook/Method Library、ECOChain 审批/评审者机制。不得凭任务书臆造已有功能。审计旧目录、历史commit、分支、Issue/PR、README与架构，识别权威主入口与 owner；找不到则写 ECOCHAIN_CANONICAL_NOT_FOUND，并将备忘录留在本任务目录，不能伪称已写入原有ECOChain。若原有ECOChain位于另一仓库或受保护分支，只在有权限且不覆盖旧研究时追加链接/备忘录，否则生成可执行的跨仓库接入清单。**禁止另建竞争ECOChain架构。**

## 1. Founder真正目标和边界
ClimateOS的长期目的：利用AI把现有全球自然科学知识、公开数据、物理模型、工程测量、法规和治理方法组织成可检索、可排序、可复算、可质疑、可持续修正的科学知识与技术评审体系，降低专业环境治理门槛。
CCZPS是科学机制/公式/单位/适用范围/计算基础；ECOChain在其已有定位上增加可追溯的申报材料接收、证据检查、方法版本复核、结论分层、异议/复审、公开透明治理记录。ECOChain不等于政府法定认证机构；本轮不授予任何外部主体官方认证、碳信用、合规或减排真实性结论。
**不**构建全球持续性设施流量采集平台，不要求Founder自己取得企业监测数据。开放数据只做少量合法、能复算的验证样本；真实申报材料由未来项目方提供、授权、承担来源与校准责任。可以对缺证据的材料输出INSUFFICIENT_EVIDENCE，而不是推断真实排放。
把“技术方法审查”和“实际环境效果验证”明确分开：方法符合≠数据真实≠效果已证实≠法定合规≠授权认证。

## 2. 全球公开科学/治理方法研究：按问题组织，不是无限搜索
以**甲烷填埋场生成—捕集—氧化—排放**为完整首个评审对象，建立跨地区方法对照；适度记录堆肥/厌氧消化/畜牧/稻田/污水的后续接口，**不**本轮实现其完整科学求解器。
优先国家/国际源：
- Australia: NGER Measurement Determination 2026 C21, CER ACCU landfill 2025, NSW EPA, IPCC 2006/2019（继承PR144精确版本、收据与限制）；
- International: IPCC/WMO/UNFCCC inventories and verification, ISO 14064-1/-2/-3、ISO 14065、ISO 14066、ISO 14067 及 ISO 14040/44（仅核范围与可合法阅读的章节，不暗示取得付费全文）；
- GHG Protocol Project Protocol / Corporate Standard, landfill/methane methods; US EPA GHGRP Subpart HH、US EPA landfill guidance, EU landfill/methane reporting and MRV, UK/Canada/NZ selected official guidance; independent verification/accreditation roles where applicable；
- 数据/测量与空间：OGC/GeoJSON/CF conventions, public environmental measurements and provenance, NOAA/NASA/ICOS/EDGAR/Carbon Mapper 等只作适用性筛查，注意 satellite plume estimate ≠ facility gas flow meter, inventory ≠ observation, model ≠ measurement。
目标**最多12个主要外部新来源主题，最多4个法域深度比较**，每个写官方来源、版本、生效时间、适用对象、公式/参数/数据要求、法律地位、独立验证要求、开放许可、访问级别、不能推断的结论。其他全球地区做可扩展索引/差异地图，不声称全球穷尽。
对每条重要主张至少保留 source locator（条款/页码/公式/表格/原文链接）和 SOURCE_VERIFIED / LIMITED_EXCERPT / METADATA_ONLY / BLOCKED。不得绕过403、付费墙或认证，版权原件未经许可不入Git。

## 3. 全球方法对照与评审规则：允许差异，禁止强制同一公式
构建 METHOD_CROSSWALK：
jurisdiction, version, reporting_year, activity, purpose, system_boundary, CH4/C/CO2e basis, wet/dry, actual/reference m3, temporal/spatial support, formula_id, parameter provenance, uncertainty, instrument QC, calibration, independent verification, permissible defaults, missing-data rules, evidence requirements, recognition authority。
至少分析6类真实冲突：版本/报告年；IPCC与NGER FOD/1.336 vs16/12；收集效率与燃烧破坏效率；气相ppm与源通量kg/h；氧化/管漏/横向离界双计；项目反事实减排与实测排放；可以再加卫星足迹与设施边界。
提供“为什么不可以直接比较”的清楚解释与允许的转换条件；地理坐标/海拔/气压/温度/湿度/风/气象站/仪器位置作为上下文和合理性检查，不将它们未经验证地变成新的全球GWP修正系数。优先复用PR143因素/公式图谱、PR144法规交叉表和P1物理换算。

## 4. ECOChain统一证据申报与审查契约（最小可运行）
设计版本化的独立审查包：
CLAIM（申报了什么、范围/报告期/目标）；
METHOD（法域、版本、公式、可替代规则）；
SOURCE/LICENCE（原始数据或授权引用、SHA、许可、审计权限）；
DATA（气体/相态/单位/干湿/时间/坐标/设备/测量/校准/缺失/不确定性）；
CALCULATION（输入、公式版本、参数、输出、代码/表格哈希、复算记录）；
REVIEW（评审者、利益冲突、规则版本、检查范围、异议、修正、撤回、复审）；
OUTCOME（每项主张的状态及理由，不是单一认证标签）。
评审结果至少独立区分：METHOD_ALIGNED、RECALCULATED、EVIDENCE_INSUFFICIENT、MATERIAL_CONTRADICTION、NOT_ASSESSED；另有 EFFECT_VERIFIED 仅在独立实证支持时可使用，本轮不得发出；REGULATORY_CERTIFICATION=NOT_PROVIDED。
不要把方法符合与计算可复算混为一个总分。对每条claim给出证据指针、失败条件、可补材料、适用范围和审查人。建立版本冻结、可追加复核/异议、审查者独立性/利益冲突、不可变证据哈希、保密权限、撤销机制的设计，若现有ECOChain已有对应概念优先复用其原名/schema。
代码仅限离线可复算小型审查器，不做全球服务/多租户生产认证。检查数据/单位/相态/方法版本/时间/边界/物料守恒/双计/缺许可/无校准/报告期不符。使用确定性规则，LLM只能建议需要检查什么，不可越过确定性科学闸门。

## 5. 必须真正运行的验证，而不是再写战略文件
构建最少三个自有合成申报包：
(A) 方法与算术自洽、证据标注为合成，得到METHOD_ALIGNED+RECALCULATED但不输出EFFECT_VERIFIED；
(B) 故意错误的单位/相态、双重氧化或跨界漏排，必须MATERIAL_CONTRADICTION；
(C) 算术正确但缺原始流量/校准/许可，必须EVIDENCE_INSUFFICIENT。
复用PR144三组质量账与PR143链A的合成物理数值，勿改其冻结核心。独立手算、负例、模型/许可/版本失败保护，保存机器可读结果与Founder通俗解释。
另选择**最多两个**明确合法开放且有可用原始数据/计算说明的真实案例候选；至少尽力完成一个小型可复算片段（如公开核算表或公开数据中的单位/公式/物料账局部验证）。若只有摘要或无许可/完整原始资料，输出 OPEN_CASE_DATA_NOT_READY，不伪造实际减排认证。研究目的为验证评审协议可用性，而非取得全球设施的实时数据或实现全场真实排放。
对来源差异与不确定性给出可检验的解释，不用AI主观评分取代物理量、实测结果或专业独立审核。

## 6. ECOChain既有研究的正式增量（必做）
首先执行 EXISTING_ECOCHAIN_AUDIT：记录发现的仓库、canonical path、历史目的、现有审批者/审查者角色、证据链、E4/NatureHash相关接口、现有Issue/PR、可复用/冲突/未知。保留既有研究和原术语。
将同分支提供的 ECOCHAIN_GOVERNANCE_MEMO_2026-11-09.md 作为今天的正式战略备忘录，**优先追加到已确认的ECOChain canonical目录中**（若该目录不存在或受保护，不擅建同名目录；在本任务目录保留备忘录并给出接入计划与BLOCKED原因）。备忘录必须保留：不做实时全球采集、不自称权威、不发法定认证、以科学/行政/文明方法统一证据接口、全球公开知识研究、有限合法复算、分层评审、申报方负数据责任、未来大机构合作才讨论规模化、与CCZPS/ClimateOS关系。
如果已有ECOChain审核人/审批人规范，新增**技术审查者角色**和检查清单/决策矩阵，区分审核人、独立核验者、方法维护者、Founder批准者，避免单一AI自审自批；但只能以非破坏性增量/提案形式改动。无权威目录就生成待迁移patch/索引，不能宣称已正式接入。
将 PR144 方法知识包和PR143图谱通过引用接入，不复制大量内容；Enotebook canonical仍未核实则保持PENDING_INTEGRATION。

## 7. 科学和工程治理
旧状态不变：D3 DATA_NOT_READY、P1-A PENDING、PR140 NO_VALID_PAIR、PR141 NO_VALID_VERTICAL_PROFILE、PR143 ChainB BLOCKED、PR144真实设施 DATA_NOT_READY、Stage3 METHOD_READY_NOT_VALIDATED。
PR144已通过ChatGPT有条件审查评论 https://github.com/simon947161/eco-agent-system/pull/144#issuecomment-6735839200；读取原文，不自动升级科学门。
绝不把合成审查器的通过作为真实项目减排认可；不能伪造开放数据许可、客户授权、第三方认可、官方ISO认证资格、碳信用。成本上限：最多12主要新来源、4法域、2开放案例候选、3合成申报包、1个小型离线审查器；无新大型依赖、无部署、无私有Council数据、无购买或联系第三方。若遇源无法访问，记录而不无限扩展。
测试至少覆盖正例、负例、缺证据、单位/相态/时区/空间错配、法域版本、重复计量、许可、校准、合成数据伪称真实、越权认证、独立审查角色冲突、哈希篡改和未知字段；输出完整日志、输入/输出SHA、来源许可、回归结果和实际CI状态。禁止未核对就说CI PASS。

## 8. GitHub双向交接
先读取仓库最新 HEAD、NEXT_SESSION 和既有R/D协议。工作仅在独立分支，完成后提交**新的独立 Draft PR**（stacked在PR144当前冻结基线），不得合并/部署/修改旧PR或生产系统。
结果必须进GitHub：README、Founder报告、source receipts、全球对照、评审规则、ECOChain memo、代码/测试、真实/合成证据区分、NEXT_SESSION、CRP、HANDOFF_STATUS、REVIEW_REQUEST。最终评论固定精确D、R..D差异、CI状态、科学限制、Enotebook/ECOChain接入真实状态。ChatGPT只有在Founder发来PR+HEAD后才会实际读取；GitHub发布不等于自动投递。
Codex回报Founder只需：新Draft PR、精确HEAD、中文报告入口、ECOChain备忘录是否已进canonical目录、真实案例是否准入、下一句ChatGPT评审短句。

## 9. 必交目录与成功判据
docs/tasks/climateos_global_method_evidence_ecochain_001/
TASKBOOK_ZH.md; README.md; FOUNDER_REPORT_ZH.md; EXISTING_ECOCHAIN_AUDIT.md; ECOCHAIN_GOVERNANCE_MEMO_2026-11-09.md; GLOBAL_SOURCE_REGISTER.md; JURISDICTION_METHOD_CROSSWALK.md; PHYSICAL_AND_ADMINISTRATIVE_CONFLICTS.md; CLAIM_EVIDENCE_SCHEMA.json; REVIEW_RULES.md; REVIEWER_ROLE_AND_INDEPENDENCE.md; REVIEW_EXAMPLES_AND_RESULTS.md; OPEN_DATA_CASES.md; ECOCHAIN_INTEGRATION_STATUS.md; QA_AND_VALIDATION.md; NEXT_SESSION.md; CRP_HANDOFF.md; REVIEW_REQUEST.json; HANDOFF_STATUS.json; evidence/、tests/及必要的最小脚本。
成功定义：(1)全球官方方法研究有版本与出处；(2)现有CCZPS/PR143/PR144科学能力可复用；(3)三类模拟申报得到合理且可复算的分层评审；(4)真实开放案例至少完成有界尝试，失败诚实阻塞；(5) ECOChain既有目录审计与备忘录接入状态真实；(6)Founder能用简单中文理解做到了什么和下一步缺什么。
