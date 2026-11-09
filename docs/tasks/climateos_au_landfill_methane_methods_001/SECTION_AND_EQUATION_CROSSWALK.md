# 官方条款—变量—公式—实现对照

阅读级别为针对性章节精读，不宣称所有整份文件全文精读。精确来源与版本见[SOURCE_REGISTER](SOURCE_REGISTER.md)；变量保留来源命名，代码另用显式kg CH4接口。印刷页与PDF页不同，ACCU印刷p33=PDF39。

|ID/定位|原文数学关系或要求（自有转录/释义）|变量、单位及限制|执行状态|
|---|---|---|---|
|G01 IPCC2006 Eq3.2 p3.9|DDOCm=W×DOC×DOCf×MCF|W Gg湿废物；DOC碳/废物；DOCf可分解比例；MCF管理修正；DDOCm GgC，不是全碳|只读，未跑废物模型|
|G02 Eq3.4–3.5 pp3.9–3.10|A_T=D_T+A_(T−1)e^(−k)；Ddec=A_(T−1)(1−e^(−k))|年步长；k yr⁻¹；当年沉积在此简化索引下于下一年起衰减；不等同逐小时机理|PR143 E06审计，未改权限|
|G03 Eq3.6 p3.10|CH4generated_T=DDOCmdecomp_T×F×16/12|GgCH4/年；F甲烷体积分数/分配约定；碳换算16/12，不是NGER的1.336|作者合成单位例1|
|G04 Eq3.1 p3.8|`CH4 emissions=[Σ_x CH4generated_x,T−R_T]×(1−OX_T)`|GgCH4/年；R回收，OX只作用未回收部分；不单独证明设备滑漏为0|只读，物理扩展另列|
|B01 NGER s5.4D|CH4gen=(ΔC_ost+ΔC_at)×F×1.336×GWPmethane；ΔC_ost=Σ_i C_osit(1−e^(−ki))；ΔC_at=Σ_i C_ait[1−e^(−ki(13−M)/12)]|tCO2-e；C tC；M为产气前月数加7；C_ait=Q_it DOC_i DOC_fi MCF；本国系数/当年降解与G02不可随意混用|无NGER计算器|
|B02 s5.15(1)(b)，2026item55|`E_jz=[CH4genz−Qlostz−γ(Qcapz+Qflaredz+Qtrz)](1−OF)+Qlostz`；E_j=Σ_z E_jz|CH4genz、Qlostz和E为tCO2-e；三个Q为m³CH4标准状态；γ=6.784×10⁻⁴×GWPmethane；OF=.1。capture用途要分互斥去向；该条排除燃烧/火炬自身排放|只读。不能将kg漏排直接代入Qlostz|
|B03 s5.17H(2)|Qflux_i=V(dc/dt)/A|Qflux mgCH4 m⁻² s⁻¹，V m³，dc/dt mg m⁻³ s⁻¹，A m²；封闭箱斜率、代表性和专家认证另需证据|作者合成单位例2|
|B04 s5.17J(2)|HRF=2 RF/MRD|RF平均月降雨mm，MRD平均雨日；定义采样避雨窗口，不是产气气候乘数|只读；MRD未知/0不得硬算|
|B05 s5.17L(1–7)|Qtot_i,z=Qelevated_i,z+Qlow_i,z+Qwell_i,z；Qav_z=Σ_i Qtot_i,z/4；Qgen_avz=Qav_z/(1−OF)|地表/well分类汇总gCH4/h；地上基础设施Qlost另以kgCH4/h汇总；必须分清井基部与地上漏点，不重复。年度转tCO2-e遵(7)|只读；“至少4次”与分母4的扩展解释留待专家核查，不擅改n|
|B06 s5.17M steps1–5|Qz=collected+generated_not_collected；kiadj=kidef(1+incr%)；调至CH4gen距Qz±.001|按条款tCO2-e、各废物类型、步长≤1%；代表区小于分区时按ASFZ/ARZ外推；不是独立验证、不是无约束回归|未执行校准|
|B07 s2.32(7)/1.21(1)|dry standard:101.325kPa、15°C；法规体积到质量见1.21|不能把Nm³默认为0°C；法规gamma与P1理想气体摩尔质量约定分开|P1仅物理换算测试|
|C01 ACCU s6/s7|装置与完整燃烧定义涉及至少98%破坏及按厂家要求监控；s7列监控系统|资格定义不等于现场实测DRE，不能当全场回收率|释义|
|C02 s42 Eq9–11，pp31–33|MCom=Σ_h MCom,h；Eq10 MCom,h=MSent,h(1−PLh)(1−TLh)DECom；Eq11 MCom,h=DECom Σ_a(Oh,a MSent,h,a)|m³CH4；Eq10适用升级系统/锅炉/有监控火炬/内燃机；Eq11其他装置。DE内燃机1，其他.98；PL/TL有类型条件|Eq11原页视觉核对；仅运行状态契约，未算信用|
|C03 s43 Eq12–14，pp34–35|Eq12 MSent,h=QLFG,h WLFG,CH4,h；Eq13能量路线；Eq14发电/效率路线|QLFG m³LFG，W体积分数；后两路线变量表见原文，未实现。闭场仅火炬可选择W=.30的特定条件不能推广|不默填.5或.3|
|C04 s44 Eq15，p36|MCom,Ox=MCom,NCT×OF×(1−WB)|两个M均为tCO2-e，OF引用NGER5.4(1)，WB是无项目时本会燃烧的比例（Eq18/19）；扣除本会近表面氧化的部分，不是把已燃烧气体再物理氧化|原页视觉核对，信用边界只读|
|C05 s78 table2/3/7，pp62–65|Oh,a逐分钟判厂家条件；整小时合规为1，否则0；气体量与组成同时间/状态配对|Eq11小时窗口≤1h；QLFG连续测；W另有开/闭场仅火炬和其他项目条件，见测量报告|作者合成覆盖例3|
|C06 s79，pp66–67|缺测按参数/情形有专门替代规则；仍可能受监管执法|W表item1有3个月等特定条件、其他量要求保守估计；不是缺测一律填0或可无限补值|本代码更窄：缺测即拒绝，不宣称实现s79|
|C07 s48 Eq17 p39；s49 Eq18 p40|AB=MCom,NCT×WB；新项目WB=max(WB,Reg,WB,Def)|AB和M为tCO2-e，WB无量纲；Reg按Schedule1许可/监管要求；Def按项目类型和年份，不能选较小值扩大信用；其他项目另见s50/51 Eq19/20|原页视觉核对，只读、不算信用|
|D01 NSW2016 s5.2 p33|25m扫描格、5cm高度；500ppmv表面水平触发调查/纠正；月度，EPA可变更|覆盖类型/天气/校准条件；ppmv不是kg/h；具体许可证可能不同|方法比较；无排放转换|
|E01 NSW2024 P4523 pp1–3 Fig2|96%为食物废物运输/处理情景的净GHG比较|不同收运距离和高/平均回收填埋基线；非通用DRE/捕集率/测量结果|禁止用作本账参数|
|H01 IPCC2019 pp3.11–3.20|Table3.0 DOCf、3.1 MCF、3.5不确定性更新；未更新章节仍回2006|参数按废物/管理类型，默认不确定性不是场址置信区间|无2019参数混用|

本表没有复制长段原文。完整原文按收据到官方页面核对；数学转录和中文释义须接受独立审查。特别待审：NGER s5.17M Step2对s5.17D的交叉引用、s5.17L额外测量事件平均解释及井漏分类；本轮保持原条款，不自行“修正法规”。

原文短定位：NGER s2.32(7) “as measured on a dry gas basis”；s5.17K “at least four times”。ACCU s78 item2 “Otherwise, Oh, a = 0.”。更长上下文需读原件而不是从短引文单独推适用。

NGER s5.3(4)注释对设施全年scope1超过100,000tCO2-e时legacy/non-legacy分别报告指向Schedule4 Part6；这不是通用NGER企业注册门槛。s5.3(1)列填埋甲烷方法1/2/3并按1.18受限，本轮未作具体企业适用判定。s5.4方法1的collection efficiency limit仍存在；不要把方法2删除5.15A–C误写成全法删除。ACCU s6的collection efficiency特指生成气中被收集且燃烧的比例；本物理账C/G是单独捕集比例，两者须注明不同定义。

## 三个完整 worked example

均为 **AUTHOR_DERIVED_SYNTHETIC_EXAMPLE**，不是监管出版物原有数值案例。

1. G03：给定12kg已经分解的碳，F=.5，CH4=12×.5×16/12=8kg；甲烷中碳为6kg，其余6kg碳的分配须另列，不能把12kg全变甲烷。本例输入不是12kg垃圾，也未运行FOD时间演化。反例F缺失则拒绝。
2. B03：V=.1m³，A=.2m²，dc/dt=2mg/m³/s，则通量1mg/m²/s=3.6g/m²/h。只代表该合成箱/该窗口；没有面积或斜率时，ppm读数无法代入。A=0必须拒绝。
3. C05：相同小时的60条一分钟厂家合规布尔记录全True，Oh,a=1；一条False则0；少一条或UNKNOWN则本研究程序拒绝。这里0是信用运算的运行判别，不表示该小时物理甲烷消失。没有计算MCom或ACCU信用数量。

第四个P1辅助例在[evidence/worked-examples.json](evidence/worked-examples.json)：100m³已知湿气体，干基CH4=.5，101325Pa、293.15K、水汽2000Pa；显式转为15°C干参考体积并核对同一气体质量。不是从场外浓度推源强。
