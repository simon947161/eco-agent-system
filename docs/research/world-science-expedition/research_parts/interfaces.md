# 接口站深读：从“名字一样”到“语义相容”

阅读范围：ESMF/NUOPC、ESMF Regridding 与 CSDMS BMI 官方资料；只读比较本仓库 PR155 修复基线 `a2863dbf3543f7e74f6b6a6a4725cb99f6fefe30` 的公开源码。
不是 ESMF 安装报告，不是完整 BMI 符合性认证，不含新的自然预测结论。科学准入 PENDING。

## ESMF / NUOPC：把耦合责任拆开

**官方事实**：NUOPC 为 ESMF 耦合应用规定通用组件及约定。Driver 管初始化和时间循环；Model 表达过程；Mediator 容纳通量等定制耦合；Connector 连接状态并承担重网格等转换。初始化先发布字段需求，再分配字段存储、准备转换、核相容性与时间戳。RunSequence 可嵌套并使用多时钟；能并行的计算资源不代表科学依赖允许并行。[ES01，Features](https://earthsystemmodeling.org/nuopc/)

```text
声明输入 / 输出 → 协商字段 → 分配存储 → 准备转换 → 校验 / 时间戳
                                  ↓
Driver 的时钟与运行序列 → Model ⇄ Connector ⇄ Mediator / Model
```

**AI INTERPRETATION**：PR155 的依赖图、`CoupledPorts` 和原 `advance` 分别承担了一部分调度、提案与提交职责；这只是责任划分可对照，不能据此宣称实现了 NUOPC。尤其不能把“同一个节点名称”当成双方变量的科学相容证据。

**官方事实**：ESMF 重网格先生成权重，再应用权重。保守方法保存相应面积定义下的场积分；它与双线性、最近邻等方法有区别，掩膜、未覆盖点和面积选择也是显式选项。[ES02，Overview / Regridding methods / masking](https://earthsystemmodeling.org/regrid/)

**本地源码观察**：PR152 `state.py` 的 `conservative_weights` 只接受明确的矩形面积重叠、同坐标系、完整覆盖；不是全球球面重网格。保守重网格也不会证明降雨源准确、变量定义正确，或两个过程的能水账闭合。

**反证设计**：若数据成功传输但把瞬时温度当月均温度，连接测试仍可能通过。下一阶段应先提交“应拒绝的单位/支撑/时间组合”，再决定是否需要安装 ESMF。当前建议 **LEARN**，不为学习站安装大型运行时。

## CSDMS BMI：可查询接口不等于可替代模型

**官方事实**：BMI 2.0 是统一查询和控制函数的接口规范，服务于模型组合；它不是一组环境方程。[BM01，Version 2.0](https://csdms.colorado.edu/wiki/BMI) 官方 Table 3 将状态更新、变量、时间及网格查询分开；`update` 推进状态，`get_value` 取副本，`get_value_ptr` 取引用。[BM07，Table 3](https://bmi.csdms.io/en/stable/bmi.spec.html)

Python 规范进一步说明：`initialize` 接收配置文件；`get_value(name,dest)` 将当前值复制到调用方缓冲并返回同一缓冲；变量需用 CSDMS Standard Names，时间单位遵循 UDUNITS。[BM06，Bmi 方法条款](https://github.com/csdms/bmi-python/blob/master/src/bmipy/bmi.py) 此处读取的是可变 master，未取得提交 SHA；不能声称永久固定了完整规范版本。

**本地源码观察**：`ModelPort.initialize(state, config)` 接受共享 State；本地空气/地表 `step(dt)` 要求已提供 exchange、匹配时步及同域字段，返回 `committed=False` 的提案。端口时钟已经推进，但共享物理库存尚未提交。只有 `CoupledPorts.step()` 调用原 `advance` 的迭代、收敛与守恒门后，才形成完整提交。把 `step` 简单改名为 `update` 会掩盖这个差异。

```text
教学外壳的更新请求
  → 完整 CoupledPorts 事务
  → 同一旧库存上的空气 / 地表提案
  → 收敛与守恒检查
  → 提交库存 / 时钟，或整体回滚
  → 读取已提交输出
```

**推荐给本轮实验的边界**：只包装公开的整个耦合事务；保持父物理代码不变；查询返回副本；写入仅限显式准许的合成 forcing，并校验单位、网格、时步、缺失与来源。拒绝任意时步、零拷贝指针和未知网格，不用“自动适配”隐藏缺口。精确 BMI 函数语义须有独立源条款，未覆盖函数继续标 UNSUPPORTED。测试相同输入的原路径/外壳路径是否相同，以及错误输入能否在修改库存前被拒绝。

**AI INTERPRETATION**：这条试验的科学价值在于揭露接口不相容，不在于证明 ClimateOS 胜过 CSDMS。即使所有对照通过，也只证明一个有界合成接口适配；不证明现实预测、CSDMS 生态集成或正式标准认证。

|对照点|本地 ModelPort 实际行为|本轮教学外壳建议与边界|
|---|---|---|
|初始化|共享 State 与 dict config|若继续用 dict，明确不同于官方文件配置签名|
|状态更新|局地 step 产出未提交提案|包装整个 CoupledPorts；禁止把单端口时钟等同提交|
|读写|通过 State / Field|复制到目标缓冲，限合成 forcing 写入；不提供裸指针|
|时钟|固定局地 dt，与慢域不同|仅准整步目标；非整数步拒绝，不宣称通用 update_until|
|语义与空间|本地短变量名、Grid对象|保留本地别名声明；未做完整 Standard Names/网格API映射|
|生命周期|无 finalize 规范方法|外壳显式关停，关停后操作拒绝；不修改父源码|

## 阅读与权利边界

实际调查9个不同官方页面：8个正文可读、1个工具不可访问（不将它伪记成HTTP403）。原旧 `https://bmi.readthedocs.io/en/stable/` 记录 BLOCKED，不反复尝试；从 CSDMS wiki 官方链接取得重定向后的 `bmi.csdms.io` 入口。BMI 与 bmi-python 官方仓库首页标示 MIT；未复制源码、安装软件或声称已经逐条核整套许可。ESMF 页面版权说明不等于可复制其图，本文流程图与中文解释为原创。[BMI 官方仓库](https://github.com/csdms/bmi) · [Python 规范仓库](https://github.com/csdms/bmi-python)

Founder 声音只引用既有完整导言；本页所有建议均为 AI 推论、待 Founder 确认。下一问：如果两个模型共享了相同的函数名，但一个返回提案、一个提交状态，哪条最小反例最早暴露错误？
