# Atlas — 唯一续接状态
日期：2026-10-29 Australia/Sydney
状态：M0_BROWSER_SMOKE_PASS / M1_SKELETON_IMPLEMENTED / M1_SOURCE_ADMISSION_PENDING / NOT_DEPLOYED
仓库：simon947161/eco-agent-system
唯一工程分支：feature/public-strategy-atlas-web-mvp-20261029
评审入口：Draft PR #130；不得合并。

## HEAD 与同步
启动远程基线：baaedfaf315e6554a84b26e01743e3952302fc1f。
M0阶段5ef063a002f5a27554da3bd6da4040b5846a0551及M1阶段e4cf9f24c74797f1e45b13ba61ed1ad9f4476127已实际push成功。当前文件所在提交包含M1数据骨架及检查结果；最新HEAD须读取GitHub分支，不将文件内自写哈希当当前HEAD。最终远端readback在本轮交付消息，下一设备必须再次核对。没有自动后台续跑。

## 已完成
- 保留原站点；修复键盘重绘焦点、抽屉残留、搜索与邻接筛选冲突、上溯/下游方向、移动搜索与可读SVG、关闭/Escape。
- 真实Edge桌面和390px iframe响应式检查；实际截图在qa/，不是模拟DOM测试。物理手机、跨浏览器及全WCAG未验。
- atlas-data.js / atlas-model.js拆分：来源、版本、节点、断言、内容块、事件和暗线反证；SHA-256、确定性序列化、不可原位追加API、篡改检测、有限多路径搜索。
- 网页显示关系状态和多路径，官方条款/实际KPI仍UNKNOWN。
- Node反例检查实际PASS，详见DATA_CONTRACT.md、qa/M0_RESULTS.md、qa/M1_RESULTS.md。

## 运行
python -m http.server 8877 --bind 127.0.0.1 （在本目录）
打开http://127.0.0.1:8877/；本轮实际测试端口8878。
node apps/public-strategy-atlas/model.test.cjs （仓库根目录）

## 唯一下一步
先读README、本文件和V1.3，核GitHub最新HEAD；继续M1的严格字段/引用校验及少量合法官方来源准入。逐一核版本、原文锚点、日期和地域；拿不到就UNKNOWN。补真实移动设备/窄屏抽屉导航验收，再考虑M2密度与增量展开。当前相邻导航不是动态展开算法。

## 边界与未完成
M1只是骨架，不是已完成可信知识系统。事件API无持久化、无独立见证；没有官方签名/Merkle证明/SCITT；原始R0-K5279eed仍LOCAL_UNAVAILABLE，不假称恢复。两V1.2历史保留，V1.3为当前开发授权。
只用公开/合成资料。每个可验证阶段检查、安全审查、commit+push，再读远端SHA；失败写SYNC_BLOCKED。禁止Council非公开资料、付费服务、部署Sites、修改PR129/main/业务系统。结束后停，下一设备显式续接。

跨设备修复：.gitattributes禁止原始合成字节文件换行转换；最终提交为该修复与续接更新，读取远端HEAD确定完整SHA。
