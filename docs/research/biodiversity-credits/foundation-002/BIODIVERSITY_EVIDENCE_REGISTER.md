# 官方证据登记册

核查日2026-11-05，Australia/Sydney。原件获取时间、MIME、大小、URL、SHA见`download-manifest.json`；原件不随Git发布。DOWNLOADED仅表示取得字节；VERIFIED仅适用于明确定位的主张，不表示所有文件内容、法律现行性或生态结果均已认证。SHA不是官方签名。

## 来源与版本

| ID | 官方来源/发布者 | 版本/日期与定位 | 核查状态 |
|---|---|---|---|
| S01 | [BAM2020 PDF](https://www.environment.nsw.gov.au/sites/default/files/biodiversity-assessment-method-2020-200438.pdf)，NSW DPIE | EES2020/0438；19Oct2020发布，22Oct2020生效；176PDF页；Ch3–5、10–11，Appendices | DOWNLOADED；调查、信用生成计算规则VERIFIED；特定案件方法适用性PARTIAL |
| S02 | [BSA Application Guide](https://www.environment.nsw.gov.au/sites/default/files/biodiversity-stewardship-agreement-application-guide-240021.pdf)，NSW DCCEEW | EHG2024/0021；January2024；39PDF页；§2、4、5、6 | DOWNLOADED；制度与行政过程VERIFIED；旧BOAMS步骤需以2026Portal信息更新 |
| S03 | [BAM-C User Guide](https://www.environment.nsw.gov.au/sites/default/files/biodiversity-assessment-method-calculator-user-guide-240080.pdf)，NSW DCCEEW | EHG2024/0080；2024；介绍、field import、stewardship计算界面 | DOWNLOADED；工具功能及输入结构VERIFIED；未执行BAM-C，工具内原始模板未下载 |
| S04 | [BC Act2016](https://legislation.nsw.gov.au/view/html/inforce/current/act-2016-063)，NSW Parliamentary Counsel | 现行合并版本请求 | 403；SHA=null；全文与当前条文适用性UNVERIFIED；法律框架另由S01/S02官方实施文件支持 |
| S05 | [BC Regulation2017](https://legislation.nsw.gov.au/view/html/inforce/current/sl-2017-0432)，NSW Parliamentary Counsel | 现行合并版本请求 | 403；SHA=null；全文UNVERIFIED；当前variation变化由S10支持 |
| S06 | [Supply Fund Operating Protocol](https://www.environment.nsw.gov.au/sites/default/files/biodiversity-credits-supply-fund-operating-protocol-220551.pdf)，NSW DPE | EHG2022/0551；October2022；§3–6；17PDF页 | DOWNLOADED；历史设计VERIFIED；原运行期止30June2025，2026采购条款沿用状态PARTIAL，不声称废止或全面现行 |
| S07 | [Supply Fund and credit purchasing](https://www.environment.nsw.gov.au/topics/animals-and-plants/biodiversity-offsets-scheme/about/biodiversity-credits-supply-fund/supply-fund-credit-purchasing)，NSW DCCEEW | Updated04November2026；页面开头与April结果段 | DOWNLOADED；6Nov开拍VERIFIED；其他November日期UNVERIFIED |
| S08 | [Credits Wanted Template](https://www.environment.nsw.gov.au/sites/default/files/2026-05/bos-credits-wanted-credit-demand-template.xlsx)，NSW DCCEEW | core.xml modified13May2026；2表/24字段；见audit | DOWNLOADED/READ_ONLY_INSPECTED；不是November专用表 |
| S09 | [Find credit buyers and sellers](https://www.environment.nsw.gov.au/topics/animals-and-plants/biodiversity-offsets-scheme/biodiversity-credits-market/find-credit-buyers-sellers)，NSW DCCEEW | Updated06October2026；Portal/模板/登记段 | DOWNLOADED；静态和临时列表区别VERIFIED |
| S10 | [Offset rules](https://www.environment.nsw.gov.au/topics/animals-and-plants/biodiversity-offsets-scheme/clear-and-develop-land/offset-rules)，NSW DCCEEW | 页面未明确提取更新时间；7March2025规则说明 | DOWNLOADED；当前行政说明VERIFIED；个案法律适用未判断 |
| S11 | [Ecological monitoring for BSAs](https://www.nsw.gov.au/environment-land-and-water/conservation-on-private-land/resource-library/ecological-monitoring-bsa)，NSW BCT | Publication29July2024；baseline/repeat data collection段 | DOWNLOADED；一般五年周期及旧协议例外VERIFIED |
| S12 | [ACCU Scheme](https://cer.gov.au/schemes/australian-carbon-credit-unit-scheme)，CER | 页面更新时间未单独核定；Legislative framework/How it works | DOWNLOADED；联邦框架及市场路径VERIFIED |
| S13 | [Australian carbon credit units](https://cer.gov.au/schemes/australian-carbon-credit-unit-scheme/australian-carbon-credit-units)，CER | 页面更新时间未单独核定；About ACCUs/attributes | DOWNLOADED；单位及登记属性VERIFIED |
| S14 | [BAM tools and resources](https://www.environment.nsw.gov.au/topics/animals-and-plants/biodiversity-offsets-scheme/accredited-assessors/biodiversity-assessment-method-tools-and-resources)，NSW DCCEEW | 2026-11-05观察；Portal/BAM-C/BioNet段 | DOWNLOADED；认可人员和公开工具权限、数据不同步提示VERIFIED |
| S15 | [Credit Demand EOI](https://www.environment.nsw.gov.au/topics/animals-and-plants/biodiversity-offsets-scheme/about/biodiversity-credits-supply-fund/credit-demand-expression-interest)，NSW DCCEEW | Updated01July2025；FAQs | DOWNLOADED；EOI非购买义务VERIFIED；variation泛化说明须结合S10，不作为现行通用授权 |
| S16 | [PCT classification](https://www.environment.nsw.gov.au/topics/animals-and-plants/biodiversity/nsw-bionet/nsw-plant-community-type-classification)，NSW DCCEEW | web检索正文，2026-11-05观察 | 未下载原字节，SHA=null；PARTIAL（分类更新/编号说明）；现场方法以S01为主 |
| S17 | [ACCU additionality](https://cer.gov.au/schemes/australian-carbon-credit-unit-scheme/how-to-participate-accu-scheme/apply-to-participate-accu-scheme/newness-regulatory-additionality-and-government-program-requirements)，CER | web检索正文，2026-11-05观察 | 未下载原字节，SHA=null；PARTIAL（一般要求），不代替具体method审查 |

## 下载完整性与许可

13项实际下载、2项现行法条请求失败。另S16/S17仅有web检索文本。manifest保留Python客户端403与PowerShell同URL正常TLS成功的区别，失败不伪装为成功；不更改TLS、不绕过认证。日期采用客户端Sydney日期，UTC获取时间可能是11月4日，二者不矛盾。

S01/S02版权页允许有条件教育/非商业转载并排除照片；S06有CC BY4.0及例外。S03及网页/Excel的完整许可范围未逐项法律审定，记RIGHTS_NOT_CLEARED_FOR_REDISTRIBUTION。所有官方原件均未提交。原创报告依据仓库许可；引用、字段标签和来源归属不转移官方文件权利。

## 主张登记与证据分类

机器可读记录在`claims.json`，包含source、locator、paraphrase、verification和evidence_class。这里概括关键边界：

| 主张 | 状态 | 证据分类与定位 |
|---|---|---|
| 样方/PCT/VI调查进入正式BAM评估 | VERIFIED | Regulatory design verified；S01 Ch3–5 |
| 正式BAM-C评估由认可人员承担 | VERIFIED | Administrative process verified；S03 Introduction，S14 Calculator |
| 供给生态系统信用Equation4及物种Equation5/6 | VERIFIED（BAM2020文本范围） | Regulatory design verified；S01 §11.6–11.7，printed59–60 |
| 签署、产权登记与发行分别发生 | VERIFIED | Administrative process verified；S02 §5.7–5.8 |
| TFD与信用数/市场价不同 | VERIFIED | Administrative process verified；S02 §5.4、§6.3 |
| 一般五年生态重复监测 | VERIFIED且有协议条件 | Administrative process verified；S11 Repeat data collection |
| 本次Nov6开拍 | VERIFIED | Administrative schedule verified；S07开头 |
| Nov20买方优先日 | UNVERIFIED | Evidence insufficient；未取得该轮原始材料 |
| lateJan2027销售及该轮随后六个月匹配 | UNVERIFIED | Evidence insufficient；S07的六个月对应April，不挪用 |
| 某笔交易完成或已retire | UNVERIFIED/未调查 | Transaction evidence NOT VERIFIED |
| 某地生态恢复或offset净收益实现 | UNVERIFIED/未调查 | Ecological outcome evidence NOT VERIFIED |
| AWTM实际所指与方法 | UNVERIFIED | 代码/docs有界检索无定义，不猜测 |

## 冲突和历史修订

上轮报告保留原样，本包记为新的来源观察：旧May页面不足以支持November；新Nov4版本支持开拍日，其他旧缺口逐项保持。S06旧期限和当前S07活动形成版本张力，不推定存在未取得的延期文件。S15旧variation说明与S10新规则一并保留；S09一处以19May离线、另一处以1JunePortal为列表时点描述，不将其合并成精确统一截断日。模板说明表将CW写成supply register，与主表用途不符，保留原件缺陷。

原始观察/下载哈希、科学规则、研究解释、建议和个案事实分别标记。本轮没有已核验的真实交易和生态结果，不能将这些栏位填为零或成功。
