# 机制研究与世界方法对照

检索日2026-11-10。来源/版本/权利见 SOURCE_REGISTER.json。只读官方文档与原论文；未安装外部求解器、未下载新环境数据。本轮发现的可复用机制是：带语义的共享状态，依赖边准入，时钟与空间中介，同一交换通量的双边记账，固定旧库存的迭代，失败回滚，随后比较情景及反证。

| 方法 | 决定 | 采纳内容与边界 |
|---|---|---|
| [CF Conventions 1.12 (2024)](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html) | ADOPT语义 | §3单位/standard_name、§4.4日历、§7边界/cell_methods。这里只实现JSON语义子集，不声称CF/NetCDF合规。固定1.12，避免动态首页草稿版本混用。文档CC0 |
| [CSDMS BMI 2.0](https://github.com/csdms/bmi) | ADOPT接口概念 | init/update、变量/网格/单位/时钟查询，MIT。ModelPort提供统一step(dt)，不是完整BMI实现；物理kernel只返回提案，由耦合器统一提交 |
| [NUOPC](https://earthsystemmodeling.org/nuopc/) | ADOPT概念／DEFER库 | field dictionary、连接器、时钟、运行序列；本轮不引入MPI或声称NUOPC兼容。具体代码发行版与许可待接入前固定 |
| [ESMF regridding](https://earthsystemmodeling.org/regrid/) | ADOPT面积思想／DEFER库 | 一阶保守映射按重叠面积，局部矩形限定。点到面需观测代表性依据；球面/非结构网格留待成熟库。面积守恒不等于信息守恒或真实空间精度 |
| [FAO56 ch3 eq11](https://www.fao.org/4/x0490e/x0490e07.htm) | WRAP已发表公式 | 温度到饱和水汽压；本轮并非完整作物ET模型。[ch2 Penman–Monteith](https://www.fao.org/4/x0490e/x0490e06.htm)含表面/空气阻力等，是后续对照，不把简化bulk公式称为其替代 |
| [Guillod et al. 2015, Nature Communications 6:6443](https://www.nature.com/articles/ncomms7443) | ADOPT反证 | 时间上的正相关可与空间上的负相关并存；大气持续性等会混杂土壤水分—降雨联系。不能推导“湿度反馈一律增雨”，本轮不建降雨反馈方程。论文CC-BY4，未搬运图表 |
| [ERA5官方数据说明](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels) | DEFER实接入 | 再分析结合模型与观测，不等于独立原始观测。使用同化过目标站的产品验证同一目标可产生依赖；须留出独立站点、时段及版本，小时值也不能补造缺测现场土壤/通量 |
| [SciPy 1.14.1 solve_ivp](https://docs.scipy.org/doc/scipy-1.14.1/reference/generated/scipy.integrate.solve_ivp.html) | DEFER替换求解器 | RK/Radau/BDF可作独立时间积分对照；自适应误差控制不消除参数误差或跨组件守恒问题。本次仅stdlib，未安装库；后续接入前核发行许可 |
| 过程参数校准／同化 | DEFER现实校准 | 已运行Ce×U不可辨识反例。未来先测风、温湿、水库存和边界通量，再分训练/验证时窗，保留传感器误差协方差。状态同化不能静默改变观测或使参数获得权威 |
| 有限体积／ODE工具与agentic管理 | ADOPT有限账；REJECT自治提升 | 本轮面积/通量与有限差分透明实现，解析余弦解独立校验。固定seed/模型hash/失败账代替常驻智能体；不自动修改科学公式、自动授予科学准入或法定认证 |

推断与反证分开：合成双向反馈使某些配置蒸发较单向少；这只是模型内部湿度梯度减弱。正/负反馈方向依边界、库存、时滞、尺度而变，迭代失败也是结果。没有观测误差对照时，不能宣布新耦合“比独立模型更准确”。
