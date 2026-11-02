# Council 私人试用网站第2版：已发布并核验

入口：https://council-strategy-intelligence.minshu.chatgpt.site/#/research 。本批审计补做与原站更新已完成，整个CSOI仍为PARTIAL。

在原网站点击“来源梳理 · 查看完成与缺口”，即可查看CSP14目标／44策略／63指标，LSPS12优先事项／83实施表行动及18个不同原文冲突观察，选定OP8项水务活动和9个明确CSP引用；还能下载覆盖矩阵并查看全部80项工程任务。正式准入、现行适用性、真实工作与成效仍单独显示UNKNOWN／PENDING。

发布基于已完成43个原生测试文件和26个Chromium叶套件的同一应用。上线后43个运行文件及部署清单共44文件逐字节匹配；匿名首页、atlas.js与完整默认数据脚本均返回403。服务认证下的真实Chromium完成研究页、PHE复核／工作／日历和原地图／显式存储／导入导出／多标签冲突三组验收，包含桌面和390px手机。无浏览器测试远程写入或外部请求。

访问策略仍是custom、revision1：仅1名owner，无其他用户、编辑者、群组或外部访问者。请用创建该站的owner ChatGPT账号打开；没有本人浏览器会话，因此没有声称替Founder完成交互登录。以上浏览器通过受支持Sites服务认证读取真实线上响应，既不是访问策略元数据检查本身，也不是本人已登录检查。

原ClimateOS水文站的版本2、源码9f3a201d40c4b70d72f0b69c319805258769c242、部署、URL及完整选定访问配置均与发布前一致。没有合并PR、扩大分享、私有Council导入、购买或权限调整。原Council第1版仍保留可回退。

## 可检查交付

- [中文审计报告](REPORT_ZH.md)和[本轮Excel矩阵](本轮来源与工程审计矩阵.xlsx)
- [最终验收](acceptance.json)、[发布回执](deployment.json)、[线上文件／浏览器记录](live/live-validation.json)
- [桌面截图](live/strategy/research-progress-1440.png)、[手机截图](live/strategy/research-progress-390.png)
- [水文站发布前](water-site-before.json)／[发布后相同](water-site-after.json)

<details><summary>源码、版本与部署技术记录</summary>

Canonical应用代码：`c46aceb115c05860266bcd7c4746af3c3a8c9d20`，原Draft PR130，同一分支；Sites发布镜像源码：`74f240e27cbfbbec5dffe225259eee1d42e58798`，没有第二套应用实现。

版本：`appgprj_6ae5b063565c8191802c9d7f7eb3214b~appgver_cb01c72c5bf48191bc3fa90a8ee3183f`；部署：`appgdep_6ae7d38f16108191bffb543c69b2cd79`；发布时间：2026-11-02T00:04:39.753297+00:00；核验记录时间：2026-11-02T00:13:36.612942+00:00。

本地产物tar和服务返回archive容器散列不同，未声称二者容器字节一致；两份散列均记录在deployment.json。所有实际运行文件及部署清单的字节，已经独立与canonical打包文件、Sites所推源码核对一致。上传包仅45个文件，包含hosting配置与44个静态文件，不发布QA目录或原始PDF。

旧v1源码：`54fed0a1b624a13c8670dc8bf01854587a73bb9b`；回退版本ID见deployment.json。GitHub查询时未返回commit statuses或PR-triggered workflows，因此没有声称独立CI通过。

</details>

原任务未提交的Phase2文件仍因原环境离线、当前环境不可访问而未取得，不能说已丢失；已保留的原报告／Excel确实恢复。本轮新来源资料和工具已提交。完整OP、LSPS剩余地图／正文、DP／资源／年度报告、现行文书及授权审核、私人WCOS仍是明确后续范围；工程任务保持49VERIFIED／28PARTIAL／3BLOCKED。

下一批可直接开展CSP63指标第二轮独立语义审读，再按清单补LSPS地图／非编号叙述和完整OP、DP／资源／预算／年报关系。公开资料工作不需新增权限；COI011／012／015／016仍PARTIAL，私有002／031／040仍BLOCKED并暂缓。浏览器26为全跑与影响复测汇总；分页覆盖252条目不等于逐252详情语义审读。
