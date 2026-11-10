# 验证与复现证据

当前结论LOCAL_VERIFIED / SYNTHETIC_TESTED，正式科学准入PENDING。远程CI必须看最终HEAD回执，不能从本地结果推定。

- 全仓739项测试：738通过、1项因Windows symlink权限跳过；包括65项新增耦合测试。evidence/full-tests.txt。首次沙箱回环套接字WinError10013导致8个旧HTTP用例错误；允许本机回环后整套重跑通过。初始失败保留sandbox-tests-initial.txt，没有删去负例或改旧测试。
- PR149既有validate.py真实执行：55新+152继承=207项，PR149/148/147结果hash仍分别为87f2708d3982dc62be76aeb405d73334153c80c6e32a2c0c1e88e68a5f8e3cf2、3ff13534e28825ae932694589ccb61ad180d176c5dfff4afc63040737355edfd、279d823da5ee835a9b3e889a0e4777ff0ee0be9be813c8a992ef62aedcada28a；新任务归档继承验证回执。旧测试自动生成的四份报告已恢复，未纳入变更。
- 主批10008记录、3336成对配置、3策略、12族；5145完成，4863拒绝。五个无故意契约破坏的正常/极端族4170条全完成。最终同seed完整重放hash一致；新seed另300条；120次相关性诊断、数值小例不拼入主计数。
- 主批65.93秒，最终整批含重放137.67秒；连初次冒烟和接口完善前完整批次累计277.44秒。该计数覆盖归档批次执行进程，不是整个人工研究会话墙钟，单元测试/文档构建耗时另记。总工件字节及hash见evidence/validation.json（低于200MB）。无常驻研究进程或付费服务。
- 独立实现scripts/independent_audit.py不导入物理运行器，从保存轨迹重建全域库存差及边界账：水最大残差7.474e−15kg/m²，能量1.116e−7J/m²。它核实所有运行条数、各族六种网格/时间组合、策略配对及联合阈值；不同聚合浮点次序使残差与单格略有差异，均低于声明门限。
- 七CLI都有真正输出与子进程测试。统一ModelPort的四类实际调用见component-interface.json；时间/支撑拒绝、协方差PSD、观测不可覆盖、可逆差异、稳定性、不收敛回滚、Ce×U不可辨识和解析收敛均测试。
- 12页离线Slides在1440×1000与390×844检查24视图、前后/键盘Home/箭头/末页、来源展开、横向无溢出、无外部网络请求。24张截图与contact sheet已目视复核。页面只读取本地生成结果，无发布或部署。
- 2026-11-10实时复核PR143–149仍open/draft/unmerged、HEAD未变，回执protected-pr-heads.json；冻结旧文件blob和LF hash见reuse-blobs.json。本PR只增加新命名空间/任务/测试并加根索引。

## 离线复核

```text
python docs/tasks/climateos_earth_system_coupling_lab_001/scripts/validate.py
python -m unittest tests.test_earth_system_coupling
python docs/tasks/climateos_earth_system_coupling_lab_001/scripts/independent_audit.py
```

validate.py仅核清单/数据/独立账，不运行万次实验。JSONL及PNG使用原字节hash，文本使用LF归一；.gitattributes固定原字节策略。跨平台浮点库可能有末位差异，科学误差门仍按单位阈值；本机双次JSONL字节一致是实际证据，不冒称所有平台都逐字相同。

主batch源码hash固定在EXPERIMENT_RESULTS.json；PRE_RUN_PROTOCOL原字节hash也固定。manifest不自哈希，不包含自身、生成validation.json及两份D交接元数据，以免自引用。研究R由提交冻结；D只填两份交接文件；最终D、D独立CI及R..D范围由PR交接评论固定。
