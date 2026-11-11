# 世界地球科学探索站 · Issue156

独立、离线优先的中文个人学习原型。6站、5条路线、23个官方来源目标（含5项访问缺口），
11页完整思想导言、逐站5章节、3组实际接口实验回放、笔记/书签/进度与导入导出。
科学准入PENDING；无机构合作声明。没有云账户、后台上传、生产部署或私人数据。

## 打开

直接用Chrome/Edge打开本目录 `index.html`，无需安装、服务器或网络即可学习、检索及回放。
外部原始来源链接由用户点击后访问。浏览器file存储行为不同；笔记请导出备份。

或在仓库根运行：
```sh
python apps/earth-science-expedition/serve.py
```
打开 `http://127.0.0.1:8896/apps/earth-science-expedition/index.html#/home`。
仅运行它的这台电脑可访问；该地址不是公开网站。预览只允许站点与本研究档案两条路径。
退出终端即可停止。file和HTTP是不同存储来源，笔记用导出/导入迁移。

## 复现与验收

```sh
python apps/earth-science-expedition/research/interface_experiment.py
python apps/earth-science-expedition/build_data.py
python -m unittest tests.test_science_expedition
node --test apps/earth-science-expedition/notebook.test.cjs
node --check apps/earth-science-expedition/app.js
```

浏览器开发验收需要Playwright与Chrome，不是网站运行依赖：
`node apps/earth-science-expedition/qa/browser.cjs PATH_TO_PLAYWRIGHT`。
Windows可用环境变量 `BROWSER_EXECUTABLE` 指向已安装的Chrome；无需下载运行时。

公开来源的研究编辑入口在 `docs/research/world-science-expedition/research_parts/`。
运行build_data生成SOURCE_REGISTER/CLAIM_LEDGER/STATION_REGISTER与data.js；不手工编辑生成副本。
schema.json定义来源字段；构建与测试验证引用、数量、状态、URL和档案一致性。
追加理解版本与反证，不能静默覆盖旧主张。初始科学状态不能被本机“已读”按钮提升。

完整BMI规范、ESMF运行时、WIS2现场网络与ERA5下载均未集成；接口实验只包装已有公开合成耦合器。
原模型与现有个人/Council站点不改。下一步需看研究目录中的CRP_HANDOFF与NEXT_SESSION。
