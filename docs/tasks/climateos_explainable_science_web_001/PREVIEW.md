# 在本机阅读 ClimateOS 中文科学解释站

这是已有 `cczps_lite/dashboard/` 网站的增量入口，无需登录、数据库或构建。**未正式部署**；GitHub 的源码页不是在线运行的网站。

## 最短预览步骤

在包含本 Draft PR 的仓库目录打开终端，运行：

```powershell
python -m http.server 8766 --bind 127.0.0.1 --directory cczps_lite/dashboard
```

保持此终端运行，在浏览器打开：

**[中文科学阅读首页](http://127.0.0.1:8766/science/)**

读完在终端按 `Ctrl+C` 关闭。只监听本机，不开放公网，不部署到任何网站。若端口已被占用，可同时把命令和浏览器地址中的 `8766` 改为其他空闲端口。

已有本机工作副本的用户可在 `D:\Codex\ClimateOS\explainable-science-web-001` 运行；其他人从本 Draft PR 分支取得代码后，在自己的仓库根目录运行同一命令。若需对照旧网站，主 dashboard 导航已增加“中文科学阅读”入口；本次未变更旧页面的科学功能。

## 三分钟阅读路线

1. 首页 → 实验一：分清比例、每立方米浓度与每小时排放。
2. “四个实验”：了解换算、容器释放、逐年库存、假设响应各为什么做。
3. “证据与边界”：搜索研究号或问题，展开固定 SHA 的原文件；再从研究地图进入其他分支。

交互包括研究路线切换、30秒摘要、原公式与证据展开、来源搜索与筛选、AWT 四情景归档切换。它们只读取随网页打包的文字和结果，不向外请求数据、不运行模型。外部 GitHub 链接由读者点击后才打开。

## 浏览器验收如何复现

使用已安装的 Node.js、Playwright 和 Chrome。无需安装新的科学依赖。给 `PLAYWRIGHT_MODULE` 指定本机已有 Playwright 模块路径（或让 Node 正常解析 `playwright`），给 `BROWSER_EXECUTABLE` 指定 Chrome 可执行文件，然后在仓库根目录运行：

```powershell
node tools/science_web/browser_qa.cjs
```

脚本自建仅允许六个静态资产的回环服务，测试后自动关闭浏览器与服务。输出写入本任务 `evidence/`；**不要在没有必要时重复覆盖已提交的验收证据**。若环境的网络沙箱阻止本机浏览器连接，需允许该进程访问回环服务；不需要开放外部网站。

展示与来源检查（不运行研究代码）：

```powershell
node --test tools/science_web/content.test.cjs
python tools/science_web/build_sources.py --check
node tools/science_web/source_map.cjs --check
```

`--verify-git` 和 `audit_archived_values.py` 额外要求本机已有对应固定研究 Git 对象；只读取原归档，不自动拉取或重算。

手机验收采用真实 Chrome 的390px触控模拟和320px窄屏，不声称已在实体手机或 Safari 上测试。截图与详细范围见 [中文验收报告](FOUNDER_ACCEPTANCE_CN.md)。
