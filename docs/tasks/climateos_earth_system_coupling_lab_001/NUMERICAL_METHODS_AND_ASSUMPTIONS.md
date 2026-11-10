# 方程、边界与假设

所有局地参数为ASSUMED_NOT_VALIDATED；非真实地区预报。T用K，水库存W与空气柱质量M用kg/m²，q用kg/kg，P/E/R用kg/m²/s，Rn/H用W/m²，Cs/Ca用J/m²/K。土壤水分是桶库存，不是现场体积含水率。合成时间从2000-01-01 UTC开始，仅是计算坐标。

FAO56 ch3 eq11给出`es=610.8 exp[17.27(T−273.15)/(T−35.85)] Pa`；本轮`qs=.622 es/(p−.378 es)`。限定水面近似243.15–333.15K、70–110kPa；低温冰相、凝结、云微物理未建模。湿度只受声明范围约束，未证明所有强迫均避免过饱和，不能将此柱用于云/降水预测。

```text
rho = p / (Rd Ta), U = sqrt(u²+v²), fW = clamp(W/Wmax,0,1)
H = rho cp Ce U (Ts−Ta)
E = min[rho Ce U max(qs(Ts,p)−qa,0) fW, W_old/dt + P]
W_new = W_old + (P−E−R) dt
R = max[0, W_old+(P−E)dt−Wmax]/dt
Cs (Ts_new−Ts_old)/dt = Rn−H−Lv E+Cs kappa Laplacian(Ts_old)
M = p_initial h/(Rd Ta_initial), Ca=M cp   (constant column approximation)
Ca dTa/dt = H + B,   B=−Ca(Ta−Ta_boundary)/tau
M dqa/dt = E − V,    V=M(qa−qa_boundary)/tau
```

Rd=287.05J/kg/K，cp=1004J/kg/K，Lv=2.45e6J/kg。Ce、Cs、h、tau、kappa为合成参数；Ce与U乘积不可独立辨识（已给反例）。Rn为外部规定净辐射，不包含全球CH4 ERF。风与气压为规定场，没有Navier–Stokes动量求解；不存在凭分数构造压力梯度力。

双向总水账：`Delta(W+M q) = (P−R)dt − integral(Vdt)`。
双向总焓账：`Delta(Cs Ts + Ca Ta + Lv M q) = (Rn+Cs kappa Laplacian Ts)dt + integral(Bdt) − Lv integral(Vdt)`。
这里雨/径流显热未显式计算，液体采用固定参考焓的简化账；不是完整多相热力学。热扩散零侧边界，面积积分为零。单向/独立只核地表开放账，H/LvE明确为边界输出。

大气每慢步两个显式子步；交换H/E在子步内固定。地表扩散显式有限体积，Neumann零通量。双向Picard松弛0.5，旧库存固定，最多60（硬上限80）迭代；误差按温度1K、水100kg/m²、q0.01kg/kg归一，阈值1e−8。达到迭代上限拒绝，不截断伪装收敛。显式扩散`kappa dt/dx² ≤ 0.5`，大气松弛`dt/(2 tau) ≤ 1`；这是本离散格式条件，不是全球气候稳定条件。

守恒门：每格水残差<1e−8kg/m²、能量<1e−5J/m²；侧边热量积分<1e−6W。误差小证明数值账闭合，不证明闭合项足够描述真实设施/生态系统。解析余弦扩散`cos(pi x/L) exp(−kappa(pi/L)²t)`提供空间二阶检验；时间误差对精确半离散特征模态比较，避免空间误差假装时间收敛。

差分：场差相同单位；梯度K/m（内部中心二阶，端点单边一阶）；时间率K/s；面通量散度W/m²。单参数中心差分、联合交互`Y11−Y10−Y01+Y00`是模型灵敏度。Jacobian无穷范数是局部收缩的充分界，≥1不能证明发散。lag=1/4只是离散延迟试验，非观测推断时滞。

“热且干”：Ta>303.15K且W/Wmax<0.25，解除Ta<301.15K或W/Wmax>0.30。该滞回是显式决策记忆，不是物理分岔、多稳态或现实警报标准。相关抽样rho=−0.6与独立rho=0提供输入误差结构敏感性，均非真实概率分布；未做参数拟合、多重比较发现宣称或事后阈值优化。
