# OP selected-source reconstruction — 1 November 2026

本次从 Council 官方公开网址重新取得 OP 原件，与登记的37,500,187字节、SHA-256完全匹配。这是**新的公开来源补做**，不是找回原任务未提交的第二阶段文件。原审计已归档的材料保留不动。

这批完成 PDF／印刷第73–74页的八个水务活动，另有一个部门计划、一个52.5FTE资源观察及文档版本记录，共11项结构化研究记录。逐项带原件版本、页码、坐标、页面hash及七栏独立校验。八个活动是两个指定页面的完整动作行清点，**不是整份OP、全部水务工作或80项Council项目**。

实际清点得到10次印刷CSP标签，但只有9个独立“活动→策略”引用：水务事件活动的两个KPI子行重复印刷8.2；服务请求活动同时引用8.2和12.2。代码保留原始10次出现、只生成9个不同引用。引用不是已执行的政策关系、法定义务或减排因果链。

数字边界：52.5FTE为部门公开计划资源，不能换成实际工时、实际支出或单项活动人数。<15/100km/year和<47pa、<20/1000connections/year和<175pa分别来自KPI与目标栏，不自动互推。Monthly是报告周期，不能替代每日检测周期。源表的“-”和“- -”均明确保留为缺失，不能当零或合格。80%及100%没有印刷比较符号，保留数值并把比较关系标UNKNOWN；不补成等于或至少。所有实际产出、执行、支出和环境结果仍UNKNOWN。

**版本冲突仍存在：**网址文件名为v3.1，PDF第3页最后填入的版本为1.3，日期30/06/2026、决议225/26；同页仍有working-draft和intranet-controlled-copy文字。因此本批未授予currentVersion或官方准入。

独立来源核验通过：11项、8活动、56个原始表格单元、9独立引用／10出现；12类损坏／缺失／伪造负例均拒绝。`source-verification.json`、`negative-results.json`、`coverage-matrix.csv/json`可检查实际结果。实现状态先标`PENDING_PARENT_INTEGRATION`，由主任务在真实集成与浏览器验证后更新其总矩阵，来源核验本身不冒充网站验收。

PDF27食品首个体量行、PDF30LTW投诉行也重新按原列检查。它们对应3个独立CSP文本引用，当前模型以4条CSP候选和4条同表字段归属表达，共8条候选，不能说成8个独立官方关系。旧csp6/csp8终点仍是研究站点；本核验没有擅自更改它们。详见`existing-op-relationships.json`。

`document-coverage.json`逐页列出142页的实际检查范围，并从第4–5页读取47个目录条目。第75–78页还有其他污水运营、基建／资本项目和期限行动；第79页无可提取文字，其图像未单独解释。完整OP原子项和引用总数**尚未清点，分母UNKNOWN**。资本开支清单从107页、服务预算112页、预算总表118页、收入政策124页起，也没有因本批来源核验而自动成为实际财政数据。

复现（在app目录）：

```sh
python3 tools/build-op-water-knowledge.py /tmp/csoi-strategy-completion-20261101/op.pdf
python3 tools/verify-op-water-knowledge.py /tmp/csoi-strategy-completion-20261101/op.pdf --negative
node -e "console.log(require('./csoi-knowledge.js').validateBundle(require('./sources/op-water-public-knowledge.json')))"
```

原PDF只在临时目录，未提交；没有原文长段、页面图像、客户／员工资料或凭据。核验是可复现的来源定位、数值／列约束和AI辅助有界语义检查，不是正式法律审查或全部文档理解证明。
