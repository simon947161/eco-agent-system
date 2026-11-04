# 既有气候模型的原文复核疑点
2026-11-04 · REVISE_BEFORE_IMPLEMENTATION

[Kim2026原文§2.3](https://acp.copernicus.org/articles/26/7789/2026/)复核用于设计而非复制实现：
- Eq1展示 log10(k_lab)=a+bR²+cR·FD+dT−eFD+fTX+gY；k为yr⁻¹，T[K]，R按原文为mm/day、组分为百分数。系数未移植；“annual rainfall”措辞与日均单位转换必须审查。
- Eq4 k_adj=F_RF k_lab；Eq5是按废物批次与年龄求和的FOD速率，Q为m³/yr。相同数据反推k再报告拟合不能充当独立验证。
- 网页Eq2把emitted除以“CH₄ oxidized”项，附近文字有氧化假设；其分母含义需核清，不能默认为1−OX。Eq3显示ln(k)+k，而k带yr⁻¹、时间约定未在该式显式呈现。执行前须核对PDF/补充、归一化及推导；本包不替作者纠错，也不将疑点认定为已证实错误。
- Data availability声明数据可能需向作者请求。本轮未联系作者；因此不把该研究列为已取得的开放验证序列。

CALMIM2011手册支持既有过程模型存在，但本包没有完成可执行代码/每项边界条件审计。相关模型均不能直接视为“现成独立真值”。P1-A摘要级CLEEN2015仍保持摘要级，没有因为后续论文引用就升级成全文核验。
