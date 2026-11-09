# 澳洲评分卡基准年核查：供Founder决定是否提醒编辑

**事实与访问边界**：本轮网页读取器在原站URL展示的澳大利亚卡Q2，包含短语“by 2030 compared with the base year of 2030”。该段解释43%的2030目标为何不足以满足题目的50%门槛。随后一次直接下载返回HTTP403，已停止；网页读取器可能使用缓存，不能保证当前服务器字节仍相同。未使用其他身份、镜像或重试绕过。

- 原站：[Climate Scorecard / Australia Q2](https://www.climatescorecard.org/scorecard/)。
- 历史收据：PR146原HTML SHA256 `72dd282073bf130b08379e2b0436599ff6825d00972862e3a4c3f764f6fe0948`，其抽取文件 [scorecard-facts.json](../global_natural_systems_evidence_atlas_001/evidence/scorecard-facts.json)。原件只在旧任务忽略缓存，不重复发布。
- 旧页JSON-LD datePublished=2021-03-29T03:28:18+00:00，dateModified=2025-09-25T03:51:15+00:00；**都是页面级日期，不证明AU卡片日期**。
- 本轮直接尝试时间2026-11-09T20:53:31Z（悉尼11月10日），失败见 [acquisition.json](evidence/acquisition.json)。当前原件SHA不可得，未用旧SHA冒充。

## 独立官方对照

[Federal Register latest details](https://www.legislation.gov.au/C2022A00037/latest/details)指向 `C2025C00153`、Compilation No.2，生效2025-02-20、注册2025-02-27。[固定正文 s10(1)(a)](https://www.legislation.gov.au/C2022A00037/2025-02-20/2025-02-20/text/original/epub/OEBPS/document_1/document_1.html)明确是澳大利亚净温室气体排放到2030年较 **2005年** 减少43%，同时按时点目标和2021–2030预算实施。s10(1)(b)是2050净零。正文已独立下载并记录哈希。

**解释**：在所见段落中，“目标年2030”与“基准年2030”疑似混写；2005是该43%目标的法定基准，不能把2030解释成同一目标的另一个已证实政策基年。编辑原意或页面后来是否修正仍须编辑/Founder确认。此处不否定网站整体工作，也不替编辑作最终裁决。

## 50分能否复算、是否受此影响

页面方法说明五个问题各20分。可见响应为No/No/No/Yes/Yes；历史卡CSS为`fifty`即50。假定每个Yes=20、No=0，计算40；**二元假设不是已经证实的完整评分细则**。可能存在部分得分、文本与分数不同步或其他版本；尚无可逐项重现50的分值表。

因此：`OFFICIAL_SCORE_REPRODUCED=false`，`SCORE_WRONG_PROVEN=false`。纠正基准年后43%仍低于50%，在上述二元规则中Q2仍是No；**未证明该文字问题改变分数**。若其他题存在部分得分或不同规则，需编辑提供明细后另行核对。

待编辑确认的最少问题：①AU卡是否应将该基准年改成2005；②当前卡的逐项得分和部分得分规则是什么，如何得到50；③若已修订，请确认日期及是否影响分值。英文草稿见 [EDITOR_NOTE_EN_DRAFT.md](EDITOR_NOTE_EN_DRAFT.md)，**NOT_SENT**；本轮未联系编辑、发邮件、发网站评论或提出公开纠错请求。
