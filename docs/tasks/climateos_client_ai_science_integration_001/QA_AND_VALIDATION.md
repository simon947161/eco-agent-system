# QA与可复核验证

证据：evidence/tests.txt，81 tests / OK；新原型11、既有气象5、P1数学8、Bondo8、水文契约29、空间基础20。没有重跑P2–P4科学模拟。具体子情形在tests/test_client_ai_evidence.py，测试方法数不是独立科学证据数量。

```powershell
python -m unittest tests.test_client_ai_evidence tests.test_dynamic_quantification tests.test_physics_validation.GasTests tests.test_bondo_passport_ledger tests.test_qgis_cooma_hydrology_pack tests.test_qgis_local_spatial_foundation -v
```

覆盖：真实三日结果与独立手算oracle；坐标顺序与边界框；重复执行相同对象；mg/L、ppm干湿、K等单位混淆；跨相态与basis；错误UTC/日期/CRS；逐字段缺失、未知字段和缺来源；缺许可；路径遍历、UNC、可执行名、NTFS流、链接目标模拟；原始文件和receipt篡改；未经批准模型；跨租户及匿名principal；排放/法律/信用幻觉及提示注入文本拒绝。失败无observation_result或spatial_result，不以默认0掩盖。

旧气象测试另外检查NaN/Inf、缺值、负风速、非空QFLAG、站点错误、重复/缺日及短窗口；这些是显式合成变异，不能当新增观测。missing-licence测试只隔离内部合同、mock了已检查读取；生产路径仍要求固定receipt hash。

安全范围：代码本地标准库、无新网络工具/安装/外发；没有认证渗透或真实多租户部署证明。输入信任根由仓库维护者固定，不能防恶意维护者修改代码与hash。路径读取存在本地并发攻击威胁边界，未声称对敌对共享文件系统安全。成功输出不是对网上最新数据的保证。

来源许可证公开页与Senversa五页已读取，未获取客户/私人材料。无UI修改，不需要浏览器测试，未生成虚假截图。远程CI见PR最终交接评论；不将历史CI或本地测试冒充本次CI。测试适配当前代码，小范围静态与回归检查足以支撑本轮窄改动；全仓库科学运行不在本轮执行范围。

跨平台核验发现 core.autocrlf=true 会改变仓库编写的receipt文本字节。已仅对receipt采用CRLF→LF规范化SHA并测试两种checkout；NOAA原始观测始终精确原字节哈希。manifest中仓库文本同样明确标repository_text_LF，外部原始数据标exact_raw_bytes。规范化不改变空格、字段或数值；篡改仍拒绝。
