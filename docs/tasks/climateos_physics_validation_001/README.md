# CLIMATEOS-PHYSICS-VALIDATION-001：受限物理计算验收

2026-11-06（澳大利亚悉尼） · V0.1 · 参考公式/合成输入 · ChatGPT科学评审 PENDING

## 阅读与复算入口

- [12页离线翻页验收报告](index.html)：键盘方向键、Home/End、手机按钮、页码与来源展开；下载整个目录/交付ZIP后本地打开，GitHub源码页不执行HTML。
- [Founder完整授权](FOUNDER_AUTHORIZATION.md)及[原评论](https://github.com/simon947161/eco-agent-system/pull/137#issuecomment-6680117578)。
- [冻结输入](inputs.json)、[公式来源与基线](sources.json)、[字节SHA清单](manifest.json)。
- [P1](p1.json)、[P2](p2.json)、[P3](p3.json)、[P4](p4.json)、[守恒](conservation.json)。CSV与SVG在同目录及charts/。
- [30项独立测试](physics-tests.json)、[完整仓库测试](full-suite.json)、[浏览器24组合检查](browser_qa.json)、[包完整性检查](validation.json)。
- [ChatGPT科学评审请求](CHATGPT_SCIENTIFIC_REVIEW.md)、[下一轮交接](NEXT_SESSION.md)。

本地执行的数值与绘图环境为 Python 3.12.13，第三方绘图依赖精确版本见 [requirements-plot.lock.txt](requirements-plot.lock.txt)。数值核心仅依赖标准库，不依赖NumPy。浏览器QA依赖锁定在 `tools/physics_qa/package-lock.json`，实际Chrome版本另记。它们锁定本轮实际软件版本，不表示已提供完整操作系统容器镜像。

从仓库根目录执行：

```powershell
& D:\apps\Python312\python.exe run_physics_validation.py
& D:\apps\Python312\python.exe run_physics_tests.py
& D:\apps\Python312\python.exe run_physics_tests.py --full
python build_physics_report.py
node tools/physics_qa/report_qa.cjs
python validate_physics_package.py
```

其它机器可在独立环境安装锁定的绘图依赖后用该环境的Python替换本机路径；UI检查复用本机已安装Chrome并记录版本。没有随机抽样，seed不适用；参数扫描是固定网格。SVG固定hash salt、去除日期元数据。测试日志运行时长和浏览器版本属于实际运行记录，不要求字节级相同；数值结果与图表可重复。`--full`沿用既有测试，会生成四个历史输出文件；本轮已还原这些副作用，未作为成果提交。

## 四项实际计算与结果

|模块|运行与核验|边界|
|---|---|---|
|P1|2 ppm、293.15 K、101325/80000 Pa分别得1.333853/1.053129 mg/实际m³；加入e=0/500/1000/2000Pa，验证干湿转换、参考体积、逆变换和质量一致|理想气体近似，实际压力而非海平面订正值；e是给定分压，未引入RH饱和蒸气压经验式|
|P2|24h，三种外压斜率仅改−100/0/+100Pa/h；逸散0.037632/0.024000/0.010368kg；另跑封闭、零生成、初始欠压控制|纯甲烷定容合成箱，单向阀，C完全合成；不是填埋体或实际集气模型|
|P3|IPCC2006年度FOD、12年合成废物史；生成1.183144192GgCH4，逸散0.638897864GgCH4；cohort与独立手算校验|不是官方参考数值结果；所有参数声明合成，未使用默认参数表；无2019混表|
|P4|C0完全同P3；温度中性和水分中性完整结果精确相等；单独温度/水分扰动积分为0.662229328/0.670311180GgCH4|只是假设响应。年度积分变化伴随末期库存变化，未证明更准确或潜力增加|

P2最大守恒残差约8.014×10⁻¹⁵kg，小于1×10⁻¹²kg容差；P3总DDOC守恒残差约9.992×10⁻¹⁶Gg C。P4也保留独立碳库存和甲烷分配残差。全部在float64精度下检查。容差是软件数值容差，不是实际测量准确度。

## 公式、库存和延迟约定

P1：c=x_dry(P−e)M/(RT)，x_wet=x_dry(P−e)/P；参考干体积Vref=Vactual(P−e)/Pref·Tref/T。M_CH4=0.016043kg/mol，M_air=0.028965kg/mol为声明近似。P3另依IPCC原式使用16/12，不能挪用到历史法定AWT的1.336。

P2：Pi=am，a=RT/(MV)，v=C·max(Pi−Pe,0)，m'=g−v。g[kg/h]，C[kg/(h·Pa)]，库存[kg]。显式Euler要求C·a·dt≤1，且边界压力为正、输入非负，以此保证库存非负；不使用截零补救。独立左端通量积分核对库存变化。线性外压斜坡在阀保持开启时有解析解：δ'=ag−s−Caδ，δeq=(ag−s)/(Ca)，δ(t)=δeq+(δ0−δeq)exp(−Cat)。dt=0.5/0.25/0.125/0.0625h误差依次约6.79e−7/3.73e−7/1.95e−7/9.99e−8kg。守恒正确不代表时间误差为零。

P3：依IPCC2006 Vol5 Ch3 Eq3.2、3.4、3.5、3.6、3.1。先衰减上年库存，再添加本年DDOC；新增cohort从次年1月1日起衰减，代表年内均匀处置的平均六个月延迟。初始0.5Gg C是未分年龄的合成继承库存。所有cohort采用同一k，未表达多种废物不同k。1Gg=10⁶kg。回收=生成×合成回收比例，然后仅对未回收部分做氧化。甲烷平衡为生成=回收+氧化+逸散；没有计算氧化产物气体或总废物质量守恒。

P4：温度响应采用归一化Arrhenius数学族，Ea=30000J/mol为合成假设；IUPAC公式依据不意味着此Ea适用于填埋体。水分响应为自定的0–2分段线性曲线，θ为归一化合成指数；NIST线性插值仅支持数学表达，不支持甲烷生物机制。两种C1分别运行，不相乘叠加。年内k固定并用指数精确积分，没有细化到日或小时，也未声称事件级精度。P2储存没有再接到P3/P4，避免重复减收集/氧化/库存。

## 验证层级与尚未满足的科学条件

1. **实现验证通过**：30项独立测试，包括固定PR137数值、逆变换、稳态/封闭解析值、线性斜坡解、cohort闭式解、k=ln2手算、零输入/零衰减/全回收/全氧化、失稳与非法值拒绝和中性精确回归。完整仓库522项，零失败零错误，1项Windows symlink权限跳过。
2. **假设的物理适用性未获准入**：P2箱与阀是合成构成关系；P4参数未校准、水分曲线未经过程验证。参数敏感性为12组k/Ea网格及水分参考值0.4/0.5/0.6，极值范围不是统计置信区间。净排放无法独立辨认生成、回收、氧化和储存。
3. **独立观测验证未执行**：没有真实设施数据输入、拟合、反演、气候归因、ACCU或全国估计。D3仍DATA_NOT_READY，P1-A仍PENDING。沿海/内陆、经纬度、距海距离未转换成排放系数。

## 分支与索引保护

任务基线是PR137 `37c4b093e511bd9b5014c276390ebde114d28eed`，父PR136 `be14a2a`、PR135 `2dea3def`；PR132只读审查 `2ec66ae4`。新分支 `research/climateos-physics-validation-001`，Draft PR堆叠在PR137分支。没有修改任何旧分支、历史no-run合同或法律公式。

`docs/research/carbonos/INDEX.md` 与 `NEXT_SESSION.md`仅存在于独立的PR132分支，不在当前依赖链。为避免引入PR132大量未合并材料或覆盖其DATA_NOT_READY状态，本轮不复制/改写canonical文件，改在已有动态量化索引和NEXT_SESSION链接本任务并记录此冲突。PR132的D1/D2、D3、INDEX/NEXT_SESSION已通过固定SHA只读核对。

请ChatGPT科学评审本受限计算包，再由Founder决定是否扩展。软件/报告PASS与科学准入PENDING并列，不升级真实设施结论。

包检查首轮因Windows默认cp1252读取含中文的QA JSON失败，已改为显式UTF-8后复查。该故障是报告检查器的编码问题，没有改动数值结果。

传统IPCC FOD本身已经是动态库存模型，2006 Table3.3还区分气候条件；本轮没有采用那些默认表值。P4只是同一库存结构上的受限假设扩展，不主张首创或优于既有方法。
