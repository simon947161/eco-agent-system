# Council 私人试用版 v4：LSPS 原文、地图和行动条件

本次研究批次已发布并完成线上验证；整个 Council Intelligence 仍为 PARTIAL。

打开 https://council-strategy-intelligence.minshu.chatgpt.site/#/research?source=LSPS ，使用持有该站的 ChatGPT 账户。选择“只看地图记录”或“只看逐段阅读”，打开记录后展开图例、条件和原页证据。正文说明、研究范围与剩余缺口可直接在原站查看。

## 已验证的发布身份

- 同一个 Council Site：`appgprj_6ae5b063565c8191802c9d7f7eb3214b`，版本 **4**，active。
- canonical 已验收应用：`4abe263be3d383ecf3ac1367ffb462d8fe683035`，原 Draft PR130，未合并。
- Sites 精确推送来源：`c488e14fcdde671698e826179cf2e3ccd57491e2`；镜像只用于同一应用的发布，不是第二套实现。
- 部署：`appgdep_6ae7f3f4ec5c81918e0b10ae3d4c962c`，succeeded。版本 ID 与完整回执见 [deployment.json](deployment.json)。
- 47 个运行文件加部署清单，共 **48 个线上文件**逐字节匹配。49 文件的包另含 hosting 清单；平台归档哈希与本地 tar 分别记录，不将二者误称同一字节流。

## 实际检查与限制

45 个原生测试文件通过（完整运行加失败项修复复测），6 组本地 Chromium 回归通过。发布后5组实际线上 Chromium 验证通过：LSPS103详情/512阅读单元/27地图图例、CSP63指标、来源列表/冲突/引用、PHE工作卡与日历、路线地图/导出/显式本地保存/双窗口冲突。桌面1440与手机390均验收；原路线检查另含2560。线上请求没有写入服务或访问其他域。

访问策略仍是 custom revision1：1名owner，0其他用户/编辑者/组/外部访客。匿名首页与2个脚本均返回403。浏览器验收使用平台支持的该站服务认证；**没有本人交互登录会话，不能宣称本人登录测试通过**。未伪造用户身份或改分享权限。

原 ClimateOS 水文站仍为版本2，源码 `9f3a201d40c4b70d72f0b69c319805258769c242`，部署 `appgdep_6adf008a3d1c81918a673531038410d1`，网址及访问权限均未改变。证据见 [access-comparison.json](access-comparison.json)。

## 可回退与未完成内容

保留 Council v3，版本 ID `appgprj_6ae5b063565c8191802c9d7f7eb3214b~appgver_aac9007af8ec8191abe0a2e08ee7cf3f`，Sites 来源 `a1330593c3ee3654e51487e0b4d1c50b636055d5`。若需要回退，应使用该已保存版本的私人部署操作，保持原 Site 与 owner-only 访问，不新建网站。本次没有执行回退。

本批是2020LSPS历史原件有界复核；不是现行法、地块适用、正式准入、实际执行或全部Council研究完成。完整OP及DP/资源/预算/年度报告关系仍待继续；80工程任务保持49VERIFIED/28PARTIAL/3BLOCKED。原未提交Phase2原存储仍不可访问，本次是官方原件补做。三个私有WCOS项继续暂缓。

新动态架构地图任务仅归档，未开始改造。须先审计和提交计划，Founder看实际效果后明确批准，才能发布该新主界面；不能沿用本次研究内容发布授权。

## 证据入口

[中文研究报告](REPORT_ZH.md) · [Excel覆盖矩阵](LSPS原文地图覆盖矩阵.xlsx) · [完整验收回执](acceptance.json) · [线上逐项结果](live/live-validation.json) · [手机入口截图](live/lsps/lsps-progress-390.png) · [桌面图例截图](live/lsps/MAP-114-1440.png)。

GitHub代码提交未返回commit status或第一页PR触发的workflow记录，未声称独立CI通过。后续文档提交只补录发布证据；生产运行文件仍精确对应上述canonical应用提交。
