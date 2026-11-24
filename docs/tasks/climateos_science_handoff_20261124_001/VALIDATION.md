# 验证证据与限度

2026-11-24 · LOCAL_METADATA_QA；科学独立审查PENDING。

运行目录：`D:\Codex\ClimateOS\whh-001-p0-p1`。Windows Codex Desktop / PowerShell / Python3.14；Git为现有安装。测试源码和结果都在本目录，实际运行时间见 [validation_results.json](validation_results.json)。

```powershell
python docs/tasks/climateos_science_handoff_20261124_001/build_preview.py
python docs/tasks/climateos_science_handoff_20261124_001/validate_package.py
git diff --check
git diff --name-status 9eb7577e145e76161f9f1cd8509348b19c2904cc
```

验证内容：14出版物/9门户/5深入的预算和ID；原始hash/sample_count为null；独立科学/许可闸门；任务书精确字节SHA；12屏报告及本地HTML；JSON/Python结构；内部链接；16个已有Git文件hash；只改变当前隔离任务目录。manifest不包含自身和运行结果，避免自引用。

本目录.gitattributes保留精确文件字节，避免Windows行尾转换使归档hash漂移。固定任务书自身的Markdown行尾空格原样保留，只对该原件关闭whitespace告警；新编文档仍执行git diff --check。

暂存检查曾将新生成文件的CRLF识别为行尾空白；已将本轮自编文本统一为LF，并令生成器显式写LF后重新检查。原任务书固定字节未改。

两个必须的对抗场景均使用人工元数据：错误/冲突的COO300方向不得作为confirmed对照；NO3-与NO3-N即使单位同写mg/L也不得直接连接。另有未知坐标、mg/L对µg/L、未知basis拒绝，以及假设完全确认的元数据正控制。没有执行数值转换、流量/浓度计算、模拟或健康评价。

初次检查发现尚未创建的本VALIDATION链接导致失败；第二次发现检查器尚未生成的结果文件也被作为缺链接，已修复生成输出的启动顺序处理，再次执行通过21项。没有隐藏这些失败。机器结果中的PASS只指本包检查，不是独立主机重跑、不证明外站内容永不改变，也不是科学结论。

## 本地展示检查

使用现有bundled Playwright与Edge157.0.4341.46，`node docs/tasks/climateos_science_handoff_20261124_001/qa_preview.cjs`。以file://读取自建报告，HTTP/S请求全部拦截；不启动公开网站或服务。首次沙箱内Edge启动因Windows权限失败，随后经执行工具批准在独立无头浏览器运行成功，没有更改用户配置或网站权限。

[ui_validation.json](ui_validation.json)记录2026-11-24T07:37:43.524Z实测：1440×900桌面、390×844手机，各12屏，共24个屏/视口检查；无横向溢出，前后按钮、方向键/Home/End、来源展开均通过；无页面错误或尝试远端请求。已目视复核[桌面](preview-desktop.png)及[手机](preview-mobile.png)首屏，字体/换行/导航可读。这些截图是作者报告的显示证据，绝不是官方PDF地图已复核的证据。

远程CI：主分支现有CCZPS测试工作流仅响应`cczps_lite/**`、`tests/**`及其工作流文件；本包为docs目录，不擅改workflow或手动触发科学计算。最终按精确HEAD查询实际checks/runs，结果写Issue167 EXECUTION_RECEIPT；零run明确NOT_TRIGGERED，不写CI PASS。部署工作流只对main push或手动触发，本分支不触发，也没有执行手动部署。

未执行/未声明通过：真实观测QC、许可原件逐行验证、2022/23全文和地图、COO300方向、410081站史、真实模型、人体风险、外站所有链接可达性、旧AWT570项测试或384合成计算。
