# 甲烷科学模型与法定公式比较矩阵

2026-11-04 · 独立研究模型比较；不执行模拟，不改变AWT2015算法。**空间位置、气候背景、反应层状态、模型参数和观测通量是不同对象。** 下表的简化表达式用于阐明结构；若非原文逐式转写，已明确标为模型族/理想化形式。

| 模型/数学形式 | 依据与数据 | 参数、尺度与已验证范围 | 不确定性 / AWT2015采纳状态 |
|---|---|---|---|
| **IPCC SWDS FOD**：`dC/dt=-kC`为连续单碳库形式；IPCC2006 Eq3.4–3.6实际用逐年沉积/存量递推；Eq3.1 `E=(ΣG−R)(1−OX)` | 可降解碳经验一阶衰减与质量账；废物批次/组成、DOC/DOCf/MCF、k、历史沉积、CH4回收、OX | k [yr⁻¹]、半衰期ln2/k；Table3.3按MAT/雨/蒸散类别及废物给默认范围。年度、填埋区/国家清单，不是逐时观测模型 | 初始历史库存、延迟、k和回收/氧化不确定；2019更新须单列。AWT式4是潜力，不含这个k；不能将FOD替换进去 |
| **污水清单**：`EF=B0×MCF`；路径权重×有机负荷，减相应sludge/CH4回收，按IPCC Eq6.1/6.4区分生活/工业 | 负荷与厌氧转化；Q、COD/BOD、路径占比、sludge、B0、MCF、回收CH4 | kgCH4/kgBOD或kgCOD；年度清单/处理系统。IPCC2019 Table6.3与温度讨论有适用系统边界 | COD/BOD不能互换；默认MCF不预测短期塘分层/曝气。不是AWT mixed-solid-waste法定公式 |
| **水温/HRT/负荷理想反应器族**：名义`θ=V/Q`；理想CSTR一阶去除`η=kθ/(1+kθ)`，plug-flow则`η=1-exp(-kθ)` | 物料守恒+理想混合假设；有效容积/流量、实际水温、负荷及反应校准 | θ [day]，k [day⁻¹]；仅理想化结构示例，本研究没有建立/验证真实污水塘参数 | HRT≠SRT，短流/分层/底泥历史改变行为；去除COD不等于全部变成CH4。**结构示意，不是从某篇论文取得的校准公式或法定式** |
| **Arrhenius温度响应**：`r(T)=r_ref exp[-Ea/R (1/T−1/T_ref)]` | 反应/微生物表观速率的温度近似；同一底物/群落与可比实验 | T [K]，Ea [J/mol]，R [J/(mol·K)]；用eV时须配kB。Yvon-Durocher2014跨尺度分析，不是厂级参数库 | 只在校准温区内；高温抑制、适应、底物限制可破坏单一斜率。未被本次AWT20式采用 |
| **Q10族**：`r(T)=r_ref Q10^((T−T_ref)/10)` | 给定温度窗口内的经验倍率；需独立温度操纵/响应测量 | Q10无量纲，温差°C/K一致；Lam2026分湿度估计；WETMETH有Q10(T)及最适温度结构 | 不是普适常数2；温度范围/水分/群落/底物依赖；不可从海拔/纬度推Q10。未被AWT20式采用 |
| **CLEEN / CLEEN_opt**：FOD结构中以雨温/组成估计k，再作现场scale-up；`G=FOD(L0,k_field,废物历史)`仅为结构示意 | 实验回归+现场气体证据；CLEEN2015仅摘要已读；Kim2026是特定场地RF优化的后续实现 | L0体积CH4/废物质量与标准条件；k time⁻¹；作者样本/韩国相邻两fill区校准 | 原始CLEEN回归系数未取得，不补造；收集/表面通量与OX假设混入generation估计。非AWT气候修正项 |
| **覆盖层氧化-传输族**：如`r_ox=rmax·C_CH4/(K_CH4+C_CH4)·C_O2/(K_O2+C_O2)·f_T·f_water`，配扩散/对流 | 这是双底物Monod型示意，不冒充Lam逐式；需气体剖面、孔隙/水分、O2供给、覆盖层结构、CH4 loading | rmax体积/质量基准必须声明；Ks与浓度同单位。Lam的均质土瓶/反应扩散与UNSW/NSW具体biofilter试验各有范围 | 过干抑制微生物、过湿抑制氧扩散；裂隙热点/压力驱动不可用统一OX解释。AWT的OF/RE规定不能用最佳实验效率替换 |
| **甲烷质量账/测量模型**：填埋层`G=R_col+O_cover+E_surface+X_lateral+ΔS/Δt`（一致边界，无外部输入时）；IDM结构`Q=ΔC/response_per_unit_emission` | 守恒约束；R_col不是destroyed。设施大气排放另含vent、device slip等；Bai的OPL+bLs从浓度/气象反演Q | 全部质量项同一mass/time、时空footprint；观察/推算分别存储；大气模型需风、稳定度、背景与源几何 | 回收与销毁不能重复减；溶解/迁移/存储不能漏；测量反演不等于直接生物产生率。AWT有自己的各项规定，不由此账自动改写 |
| **自然湿地过程模型 WETMETH1.0**：分层碳/温度/深度控制产生，氧化与输运另计；其Q10(T)见AppendixA | 全球/高纬湿地及地球系统模型；水位/土层碳、T、湿地面积、氧化参数 | 原论文多年代/粗网格评估，非污水塘或填埋体校准 | 最适温区、氧化与面积不确定；不能用其参数预测Cooma厂址；非AWT法律算法 |

原始来源： [IPCC2006 Ch3](https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/5_Volume5/V5_3_Ch3_SWDS.pdf)、[2019 Ch3](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/5_Volume5/19R_V5_3_Ch03_SWDS.pdf)、[2019 Ch6](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/5_Volume5/19R_V5_6_Ch06_Wastewater.pdf)、[Yvon-Durocher2014](https://pubmed.ncbi.nlm.nih.gov/24670769/)、[Kim2026](https://acp.copernicus.org/articles/26/7789/2026/)、[Lam2026](https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2026.1960703/full)、[Bai2026](https://amt.copernicus.org/articles/19/5157/2026/)、[WETMETH](https://gmd.copernicus.org/articles/14/6215/2021/)。文献阅读深度与未知字段见文献表，不能因模型名熟悉就填参数。

## 比较时必须锁定的定义

`generation`、`surface flux`、`captured gas`、`destroyed methane`和`tCO2e credited`不等价。CH4本体质量与CO2e分开，GWP时域/版本另存；甲烷燃烧转为生物源CO2也不意味着物理上“没有排放”。浓度单位、gas dry/wet、标准温压、面积/质量归一化和积分时间统一后才能比较。

气温升高可能提高一部分温区中的产生与氧化；雨水既可增加水分/底物，也可改变封闭、氧传输和压力。因此净地表排放方向可能与产甲烷方向不同。此为过程解释框架，不是已建立的区域因果结论。

## 下一阶段可做什么（未运行）

可以提出受限、可复算的**独立科学结构敏感性实验**：无真实厂址/ACCU结果，先固定一个公开且经审查的单过程参数集与合成输入，明确输出为模型响应而非现场预测；使用独立算术核对、单位/边界/极限检查、参数区间与反例。任何实地参数迁移、实际减排量、法定计算或生产部署仍须另行批准。当前不运行这些模型。
