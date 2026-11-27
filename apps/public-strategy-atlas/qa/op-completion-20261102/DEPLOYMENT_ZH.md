# Council 原私人试用站 v6 — 发布与线上验收完成

[打开现有 Council 私人网站](https://council-strategy-intelligence.minshu.chatgpt.site/#/research)。请使用拥有者账号登录，从“来源梳理与交付”进入 OP。可以逐页读行动、触发条件、预算口径、角色与原件位置；展开条目查看详情，按页查询并导出来源矩阵/快照。原 PHE 阅读卡、审读任务、年度日历和本机保存流程保留。研究修改仍需按对应入口明确保存/导出；没有自动云同步或后台任务执行器。

本批研究与应用交付已完成；整体系统仍为 PARTIAL。80项是工程任务，目前51 VERIFIED、26 PARTIAL、3 BLOCKED，不是80个Council项目。143新增研究记录/911阅读单元也不代表已完成同等数量的实际工作。

## 精确版本

- canonical应用提交：`cf0936474e00cad07acf6782100fc7e35db431ee`，原Draft PR130/原分支，未合并。
- Sites源码提交：`ad876b976278d437878822c7eb6e24e7d3e64598`；artifact从这一已推送状态生成，51个文件逐字匹配Git（hosting+49runtime+manifest），无QA/原PDF/私有资料。
- Site：`appgprj_6ae5b063565c8191802c9d7f7eb3214b`；版本6。
- 版本ID：`appgprj_6ae5b063565c8191802c9d7f7eb3214b~appgver_800266427f648191a9edcd40c1b79c59`。
- 部署ID：`appgdep_6ae81182c56c81918558879a487b447f`，平台状态succeeded。
- 后续证据/说明提交不会改变上述已部署应用；当前README/NEXT_SESSION以本回执为准。

## 实际验收

49个不同native测试文件经过完整批次与受影响复测通过；全新登记与启动缓存等同性通过。主要7个本地浏览器套件、软件闭合5个套件/补充检查、容量实测与最后OP折叠显示检查分别有回执；不把汇总重跑称为每项只运行一次。

线上50个文件（含deployment-assets.json）与发布清单逐一匹配。通过支持的Sites服务鉴权，在真实Chromium运行4套检查：OP142页/911条逐项阅读及负例、PHE审读/日历流、已有路线/本机保存/多标签冲突、OP折叠阅读。桌面和390px手机尺寸实际操作、导出离线重验、来源撤回、旧版导入、条件丢失和超限输入均有证据。全从头登记在本地完整E0/native中验证；线上工作区测试明确是复用交互断言的有限检查，不冒充又跑了完整E0重建。

匿名首页、atlas.js和启动快照脚本均被拒绝。管理侧custom policy revision1，仅1个owner账户，无编辑者、群组或外部访客。服务鉴权检查不是代Owner登录：真实Owner交互登录仍NOT_TESTED。

v5是中间发布；截图发现OP技术冲突重复展开后，仅修复一个显示条件，保留全部数据/折叠入口。尝试中止v5检查未能确认所有子进程均已退出，迟到的v5回执写入复用的中间目录，已标注并排除：live-v6-initial-failed/live-validation.json实际属于v5，不能作为v6初次检查证据。v6首次检查在进入站点根路径时出现Page.goto错误，随后清理出现TargetClosedError和驱动管道关闭；完整首个异常未保留，不能判定唯一根因。最终只采用04:32:10UTC独立启动的完整v6运行，4套检查、50个文件、源码cf09364均已核实，结束后无验证器残留进程。复测代码、超时和支持鉴权方式均未改变；未证实应用回归，因此未回滚，也无需Founder处理。详见live-run-provenance-correction.json。后续验证器已改为每次独立输出目录与临时工作区，防止复用目录造成串写；这项验收后QA修正仅检查语法/路径隔离，不冒称又跑了一次线上浏览器。

## 容量和可用性限制

当前快照22,743,874字节。本轮确实将导入上限从10MiB提高到32MiB，并保留解析前拒绝。不是仅做compact而保持原上限。

最终v6服务鉴权实测如下；网络经验证工具转交真实线上响应，不是Owner普通浏览器网络基准。JS堆取148个样本/视口，未覆盖原生/GPU内存或保证捕捉完整峰值。

| 视口 | 应用就绪 | 修改条件快照导入 | 最高采样JS堆 |
|---|---:|---:|---:|
| 1440×900 | 16.036秒 | 5.487秒 | 382.0MiB |
| 390×844 | 16.766秒 | 3.946秒 | 396.0MiB |

云Linux的390px触摸模拟不能替代实体低内存手机实测。COI076的基本读屏实际听读也仍待可用辅助工具或人工验收；不新增专业认证或购买硬件门槛。

## 保护、回退与下一步

ClimateOS水文站保持v2、源码9f3a201d40c4b70d72f0b69c319805258769c242、部署appgdep_6adf008a3d1c81918a673531038410d1、原URL和owner-only policy revision1；只做读取比较。Council原已验收v4保留为回退版本，源码c488e14fcdde671698e826179cf2e3ccd57491e2；按需要可部署该已保存版本，不需重建。未合并PR、导入私人WCOS或扩展分享权限。

下一可直接继续的公开批次是既有登记DP原件的版本/页覆盖和CSP→DP→OP明确关系；资源/年度报告及当前规则证据仍有逐项缺口。私人002/031/040延后。动态架构地图仅交付实施计划，尚未编码；真实可运行原型及新主界面发布需要Founder审阅与独立批准。当前研究交付没有等待新增授权。

证据：deployment.json、packaging-receipt.json、deployment-assets.json、live/live-validation.json、acceptance.json、final-actual-readback-samples.json。GitHub工具未返回commit statuses或首屏PR触发workflow runs，未宣称CI通过。

本批交付说明已完成。
