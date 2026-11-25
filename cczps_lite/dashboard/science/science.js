'use strict';
(() => {
  const content = globalThis.SCIENCE_CONTENT;
  const sources = globalThis.SCIENCE_SOURCES;
  const main = document.getElementById('reading');
  const repository = 'https://github.com/simon947161/eco-agent-system';
  const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const link = (href, label) => `<a href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a>`;
  const fileUrl = (pr, path) => `${repository}/blob/${sources.prs[pr].sha}/${path}`;
  const route = (href, label, cls='') => `<a class="${cls}" href="#/${href}">${esc(label)}</a>`;
  const byPR = number => content.stories.find(story => story.pr === number);
  const chips = story => `<div class="chips"><span class="chip">${esc(story.dataType)}</span><span class="chip caution">${esc(story.status)}</span></div>`;
  const section = (heading, body, cls='') => `<section class="${cls}"><h2>${esc(heading)}</h2>${body}</section>`;
  const para = text => `<p>${esc(text)}</p>`;
  const breadcrumbs = title => `<div class="breadcrumbs">${route('home','首页')}<span aria-hidden="true">/</span>${route('map','研究地图')}<span aria-hidden="true">/</span><span>${esc(title)}</span></div>`;

  function sourceBlock(pr, resultFile) {
    const source = sources.prs[pr];
    const links = source.links.map(item => `<li>${link(fileUrl(pr,item.path),item.label)}</li>`).join('');
    const result = resultFile ? `<p>${link(fileUrl(pr,`docs/tasks/climateos_physics_validation_001/${resultFile}`),'直接查看本实验归档结果')}</p>` : '';
    const discussions = source.discussions.length ? `<details><summary>原研究公开评审与交接记录（${source.discussions.length}项）</summary><div class="details-body"><p>这些记录有不同范围与时间；公开评审中的有条件接受不等于合并、科学准入或部署批准。</p><ul class="source-list">${source.discussions.map((item,index) => `<li>${link(item.url,`记录 ${index+1} · ${item.date.slice(0,10)}`)}</li>`).join('')}</ul></div></details>` : '<p class="technical-meta">读取时未发现公开讨论回执；不据此推定已通过独立评审。</p>';
    return `${result}<ul class="source-list">${links}<li>${link(source.url,`源草稿变更 #${pr} 的当前讨论`)}</li></ul><p class="technical-meta">固定提交标识（SHA）：<code>${esc(source.sha)}</code><br>源变更最近更新时间：${esc(source.updated)}<br>状态核验：2026年11月26日；开放、草稿、未合并。这里的文件链接固定版本，讨论页可能继续更新。</p>${discussions}`;
  }

  function topicCards() {
    return `<div class="topic-grid">${content.topics.map((topic,i) => `<a href="#/topic/${topic.id}" class="topic-card"><span class="topic-count">路线 ${String(i+1).padStart(2,'0')} · ${topic.local ? '本地研究，远程待登记' : `${topic.prs.length}项已有研究`}</span><h3>${esc(topic.title)}</h3><p>${esc(topic.subtitle)}</p><span class="read-more">沿着这条线读下去 →</span></a>`).join('')}</div>`;
  }

  function misconceptions() {
    return `<div class="faq">${content.misconceptions.map(([title,body]) => `<details><summary>${esc(title)}</summary><div class="details-body">${para(body)}</div></details>`).join('')}</div>`;
  }

  function home() {
    return `<section class="hero"><div class="wrap hero-grid"><div><span class="kicker">从一个容易误读的数字开始</span><h1>甲烷浓度变低，<br>就代表排得更少吗？</h1><p class="intro">同样的甲烷比例，气压低一些，一立方米空气里的甲烷就少一些。但这还不能告诉我们，一个场地每小时排出了多少。</p><div class="actions">${route('experiment/p1','从第一个实验开始 →','button light')}<a class="text-link" href="#/journey">三分钟阅读路线 ↓</a></div></div><div class="pressure-panel" aria-label="合成参考结果比较"><p class="panel-label">相同比例 2 ppm · 相同温度 20°C · 无水汽</p><h2>变的是每立方米的质量</h2><div class="pressure-row"><header><span>气压 101325 Pa</span><strong>1.333853 <small>mg/m³</small></strong></header><div class="pressure-track"><span class="pressure-fill"></span></div></div><div class="pressure-row"><header><span>气压 80000 Pa</span><strong>1.053129 <small>mg/m³</small></strong></header><div class="pressure-track"><span class="pressure-fill lower"></span></div></div><p class="panel-caption">归档换算结果的示意比较，非现场观测。两组甲烷比例相同，都没有提供每小时排放量。</p><p class="proof-line">${route('experiment/p1','查看输入、公式与固定版本证据 →')}</p></div></div></section>
      <section class="wrap section mission-grid"><div><span class="kicker">ClimateOS 为什么存在</span><h2>让环境判断，<br>有一条可以追问的证据链。</h2><p>从“一个数字是什么意思”走到“它能支持什么决定”，ClimateOS 把观测、假设、计算和人的审核接在一起。本页把已有研究讲清楚，让你能读懂，也能查证。</p></div><aside class="boundary"><h3>我们已经做了什么</h3><p>整理公开来源、检查数据资格、验证受限物理账本，并记录不能继续的原因。</p><h3>还有什么没有证明</h3><p>现场预测、实际减排、污染归因和停电保供效果，仍需各自的观测与独立验证。网站变得好读，不会改变这些科学状态。</p></aside></section>
      <section class="wrap section" id="journey"><div class="section-heading"><div><span class="kicker">只用三分钟</span><h2>先读懂，再往深处走</h2></div><p>先分清量，再看实验，最后确认哪些问题还不能下结论。</p></div><div class="journey"><a class="journey-card" href="#/experiment/p1"><span class="step">01</span><h3>第一分钟 · 分清三个量</h3><p>比例是占多少，浓度是有多密，排放是每单位时间出去多少。</p><span class="read-more">读实验一 →</span></a><a class="journey-card" href="#/experiments"><span class="step">02</span><h3>第二分钟 · 看四个为什么</h3><p>换算、释放、库存、响应。每个实验只解决一个受限问题。</p><span class="read-more">看四实验路线 →</span></a><a class="journey-card" href="#/sources"><span class="step">03</span><h3>第三分钟 · 找到证据边界</h3><p>什么是合成结果，什么是真实观测，下一步还缺哪道验证门。</p><span class="read-more">查看来源与闸门 →</span></a></div></section>
      <section class="wrap section"><div class="section-heading"><div><span class="kicker">同一条证据链，不同研究尺度</span><h2>从分子，到天气，再到社区</h2></div><p>这些分支共享核查方法，尚未组成一个已验证的统一预测系统。</p></div>${topicCards()}<p class="connection">物理量与质量守恒 → 气象、水文与空间边界 → 碳核算和地方问题 → 建筑服务与社区韧性。<br>共同底座：来源、单位、时间、使用权与人的审核。</p></section>
      <section class="wrap section"><span class="kicker">先避开四个常见误解</span><h2>一个好解释，也要说清楚不能推出什么</h2>${misconceptions()}</section>`;
  }

  function experiments() {
    return `<header class="wrap page-head">${breadcrumbs('四个实验')}<span class="kicker">甲烷物理 · 原研究 #138</span><h1>四个实验，四种不同的问题</h1><p class="lede">从单位换算到动态释放，再到逐年库存和假设响应。所有结果均来自已有归档；这里没有新的科学计算。</p>${chips(byPR(138))}</header><div class="wrap story-list">${content.experiments.map((exp,i) => `<article class="story-row"><div class="pr-no">0${i+1} / 04</div><div><h2>${esc(exp.title)}</h2><p><strong>为什么做：</strong>${esc(exp.why)}</p><p><strong>目前能说：</strong>${esc(exp.proves)}</p><div class="actions">${route(`experiment/${exp.id}`,'30秒读懂 →','button outline')}</div></div></article>`).join('')}</div>`;
  }

  function experimentNav(active) {
    return `<nav class="wrap experiment-nav" aria-label="四个实验顺序">${content.experiments.map((exp,i) => `<a href="#/experiment/${exp.id}" ${exp.id===active?'aria-current="step"':''}><span>0${i+1} / 04</span>${esc(exp.label.split(' · ')[1])}</a>`).join('')}</nav>`;
  }

  function scientificDetails(story, isExperiment=false) {
    let detail;
    if (isExperiment) {
      detail = `<h3>假设、参数与单位</h3><table class="data-table"><caption>原实验固定输入；不是在线计算器</caption><tbody>${story.inputs.map(([key,value]) => `<tr><th scope="row">${esc(key)}</th><td>${esc(value)}</td></tr>`).join('')}</tbody></table><h3>原方程怎么写</h3>${story.equations.map(eq=>`<div class="formula">${esc(eq)}</div>`).join('')}<h3>数值方法与对照</h3>${para(story.numerical)}<h3>怎样沿原研究复核</h3>${para(story.reproduction)}<p class="archive-note">原研究测试回执属于历史验证，不是本次网站测试。若要重新计算，需回到原分支的准入和授权流程。</p>`;
    } else {
      const extras = {
        137:'换算关系：c = x干(P−e)M/(RT)。c 是实际体积质量浓度，x 是摩尔比例；排放通量还需边界和时间。海拔是压力的相关条件，海岸距离不是可直接代入的排放因子。',
        143:'链A沿用 c = x干(P−e)M/(RT)。固定干基2 ppm、80000 Pa、293.15 K、水汽1000 Pa，得到归档1.039964673 mg/m³；不是因子拟合。链B仍因组成和时间尺度不一致而停止。',
        144:'分账结构：期初库存 + 输入 − 输出 = 期末库存；甲烷被燃烧或氧化后不能在碳账里消失。甲烷物种、总碳与设备边界分别核对。原方程和合成账本见下方物理账文件。',
        147:'三个独立尺度：全球有效辐射强迫（W/m²）、1961–2020季节状态转移的样本比例、合成节点水量变化。水网络用 ΔS = 输入 − 输出；同一内部通量在两个节点一正一负。完整辐射方程、变量与控制条件沿原说明查阅，未转成局地温度。',
        149:'条件频率 = 某季节类别中少雨的合格年份数 / 该类别的全部合格年份数。少雨阈值、站点组合和季节预注册定义以原文件为准；不能把13/17当因果效应。块状区间、缺测排除及其他季节不足在原报告分别登记。',
        152:'用共享水/热通量更新两端状态，质量与能量守恒各有单位与容差；独立、单向和双向策略使用同一边界契约。迭代、步长、拒绝与回滚规则见原数值方法和失败记录。配置拒绝次数不是准确率。',
        155:'这里比较的是图执行与回滚，不提出新的物理方程。降雨施加前保存检查点，失败恢复到相同状态；不同策略沿用相同物理调用。工程耗时与科学误差分别评审。',
        163:'物理净差 N = 基线累计排放 E_B − 项目累计排放 E_P − 边界外另记项 L。B/C 的 L 是5吨残渣运输化石二氧化碳，与项目内10吨进料运输不重叠；气体泄漏已在项目账内，不能重复扣减。固定1000吨湿有机物、100年累计窗口，气体使用既定换算口径；法律资格与信用状态另记。B/C的人为参数范围约 −459.664160 到 951.829072 吨二氧化碳当量，不是置信区间。四个原始输入、原实现与结果见下方；未知残渣不可填0。'
      };
      detail = `<h3>方法、尺度与复核入口</h3>${para(extras[story.pr] || '本卡解释原研究的目录、方法或准入结论，不提出额外方程。请沿下方固定版本的研究说明查找原参数、字段、输入、测试及局限；目录或任务书本身不构成数值实验。')}<p class="archive-note">本次仅核查已有归档与公开回执，没有获取新原始数据或重跑科学模型。原研究的计算方法与测试结果不等于本网站的本地界面测试。</p>`;
    }
    return `<details class="scientific-details"><summary>展开科学细节 · 方程、输入与 GitHub 证据</summary><div class="details-body">${detail}<h3>状态与固定版本</h3><p class="technical-meta">索引标签（保留源停止条件，补充阅读分类）：<code>${esc(story.rawStatus)}</code><br>解释整理日期：${content.date}。分类不是新增审批。</p>${sourceBlock(story.pr,story.resultsFile)}</div></details>`;
  }

  const awtScenarios = {
    a:{title:'A · 同一路径作为对照', value:'净差 0 吨二氧化碳当量', text:'基线与项目路径相同，物理账应退回零差值。它检验核算逻辑，不代表一个真实项目已达到净零。'},
    b:{title:'B · 厌氧消化及残渣填埋', value:'469.353312 吨二氧化碳当量', text:'整批进入厌氧消化（AD），残渣另入合成填埋路径。归档法律核查指出：到期2015方法的新注册路径不合格；实际基线和项目也没有实证。这个历史研究记录不能替代现行法规核查。'},
    c:{title:'C · 相同物理账，不同法律基线', value:'469.353312 吨二氧化碳当量', text:'复用B的物理输入，只改变厨余与园林有机废物分收（FOGO）的日期和义务背景。强制分收下继续填埋是否合理仍未知，不能认定额外性或信用。'},
    d:{title:'D · 残渣去向未知', value:'无法确定 · 保留空值', text:'未知部分不能按零排放处理。完整净差留空，等待残渣路径与相应证据。四个情景的信用资格都未确定。'}
  };

  function scenarioBody(id) {
    const scenario = awtScenarios[id];
    return `<h3>${esc(scenario.title)}</h3><strong>${esc(scenario.value)}</strong>${para(scenario.text)}<p class="archive-note">合成情景 · 非实测 · 不是年度减排 · 信用资格未确定</p>`;
  }

  function storyPage(story,isExperiment=false) {
    const label = isExperiment ? story.label : `研究 #${story.pr}`;
    const quick = `<aside id="quick-read" class="quick-read" hidden><h2>30秒读懂</h2>${para(story.question)}${para(story.result)}${para(`先别下这个结论：${story.notProven}`)}</aside>`;
    const analogy = isExperiment ? `<aside class="analogy"><span class="kicker">换个生活中的说法</span>${para(story.analogy)}</aside>` : '';
    const readings = isExperiment ? `<div class="result-grid">${story.values.map(([key,value,unit])=>`<div class="result-tile"><span>${esc(key)}</span><strong>${esc(value)}</strong><small>${esc(unit)}</small></div>`).join('')}</div><p class="archive-note">来自原实验固定归档，展示值可能四舍五入；未在浏览器重新计算。</p>` : '';
    const concepts = isExperiment && story.id==='p1' ? section('先分清这三个量', '<table class="data-table"><tbody><tr><th scope="row">比例 · 占多少</th><td>2 ppm：每百万个干空气分子中约有2个甲烷分子。</td></tr><tr><th scope="row">浓度 · 有多密</th><td>mg/m³：每立方米实际空气里有多少毫克甲烷，会随压力、温度与干湿口径变化。</td></tr><tr><th scope="row">排放 · 出去多少</th><td>kg/h：每小时跨过指定边界的甲烷质量。还需要流量、边界与时间等信息。</td></tr></tbody></table>') : '';
    const awt = story.pr===163 ? section('切换四个已有情景', `<p>切换仅显示归档解释，不运行计算。</p><div class="switches" role="group" aria-label="四个合成情景">${Object.keys(awtScenarios).map(id=>`<button type="button" data-scenario="${id}" aria-pressed="${id==='a'}">情景 ${id.toUpperCase()}</button>`).join('')}</div><div id="scenario-result" class="scenario-result" aria-live="polite">${scenarioBody('a')}</div>`) : story.pr===138 && !isExperiment ? section('逐个进入四个实验',`<p>每个实验都有生活类比、参数、归档数字、原公式及对照。</p><div class="actions">${route('experiments','开始四实验阅读路线 →','button')}</div>`) : '';
    const next = isExperiment ? content.experiments[content.experiments.indexOf(story)+1] : null;
    return `<header class="wrap page-head">${breadcrumbs(label)}<span class="kicker">${esc(label)}</span><h1>${esc(story.title)}</h1>${chips(story)}<div class="actions"><button type="button" class="button outline" data-action="summary" aria-controls="quick-read" aria-expanded="false">30秒读懂</button>${isExperiment?'':route('sources','查看来源索引','text-link')}</div></header>${isExperiment?experimentNav(story.id):''}<article class="wrap article">${quick}${section('我们在问什么',`<p class="question">${esc(story.question)}</p>`)}${section('为什么要研究',para(story.why))}${analogy}${concepts}${section('实际做了什么',para(story.method))}${section('发现了什么',para(story.result)+readings)}${awt}${story.proves?section('在假设范围内，证明了什么',para(story.proves)):''}${section('尚未证明什么',para(story.notProven),'not-proven')}${section('下一道验证门',para(story.gate))}${scientificDetails(story,isExperiment)}<nav class="next-story" aria-label="继续阅读">${route(isExperiment?'experiments':'map',isExperiment?'← 回到四个实验':'← 回到研究地图')}${next?route(`experiment/${next.id}`,`下一步：${next.label.split(' · ')[1]} →`):route('sources','查看证据与边界 →')}</nav></article>`;
  }

  function energyPage() {
    const story = content.energy;
    return `<header class="wrap page-head">${breadcrumbs('建筑与社区能源韧性')}<span class="kicker">建筑研究（BuildingOS）× 能源（Energy）× 韧性（Resilience）</span><h1>${esc(story.title)}</h1>${chips(story)}</header><article class="wrap article">${section('我们在问什么',para(story.question))}${section('为什么要研究',para(story.why))}${section('实际做了什么',para(story.method))}${section('目前发现',para(story.result))}${section('尚未证明什么',para(story.notProven),'not-proven')}${section('下一道验证门',para(story.gate))}<details><summary>展开科学细节 · 候选问题与来源缺口</summary><div class="details-body"><h3>待检验的问题</h3>${para(story.hypotheses)}<h3>来源与使用边界</h3>${para(story.provenance)}<p class="technical-meta">状态：<code>${esc(story.rawStatus)}</code><br>核查日期：2026-11-26。远程研究文件 / 固定 SHA：缺失，不伪造链接。</p><p>${link(`${repository}/issues/170`,'任务书规定的本地材料标记边界')}</p><p>对外联系、获取原始数据、模型计算与现场试点仍需另行授权。后续交流资料进入原唯一研究索引，本网站只维护经过授权的解释摘要。</p></div></details>${route('map','← 回到研究地图','button outline')}</article>`;
  }

  function topicPage(id) {
    const topic = content.topics.find(item=>item.id===id);
    if (!topic) return notFound();
    if (topic.local) return energyPage();
    return `<header class="wrap page-head">${breadcrumbs(topic.title)}<span class="kicker">${esc(topic.subtitle)}</span><h1>${esc(topic.title)}</h1><p class="lede">${esc(topic.note)}</p>${id==='methane'?`<div class="actions">${route('experiments','先读懂四个甲烷实验 →','button')}</div>`:''}</header><div class="wrap story-list">${topic.prs.map(number => { const story=byPR(number); return `<article class="story-row"><div class="pr-no">研究 #${number}</div><div><h2>${route(`story/${number}`,story.title)}</h2><p>${esc(story.question)}</p>${chips(story)}<p>${esc(story.result)}</p><div class="actions">${route(`story/${number}`,'30秒读懂与科学细节 →','button outline')}</div></div></article>`; }).join('')}</div>`;
  }

  function mapPage() {
    return `<header class="wrap page-head">${breadcrumbs('研究地图')}<span class="kicker">同一份研究地图</span><h1>沿着问题走，不必先懂缩写</h1><p class="lede">每条路线从“为什么研究”开始，最后回到来源与下一道验证门。跨分支的连接是问题关系，不是已经验证的因果模型。</p></header><section class="wrap section">${topicCards()}<p class="connection">比例与质量守恒连接甲烷和碳核算；气象与水文连接过程和场地；地方环境与建筑能源把“模型能算什么”接到“社区需要什么”。所有分支都要先经过证据与使用权核查。</p></section>`;
  }

  function sourceCard(story) {
    return `<details data-source-pr="${story.pr}"><summary><span>#${story.pr} · ${esc(story.title)}</span><small>草稿 · 未合并</small></summary><div class="details-body">${chips(story)}<p>${route(`story/${story.pr}`,'进入中文解释 →')}</p><h3>这份材料能支持什么</h3>${para(story.result)}<h3>仍不能支持什么</h3>${para(story.notProven)}<h3>下一道验证门</h3>${para(story.gate)}<p class="technical-meta">保留原状态：<code>${esc(story.rawStatus)}</code></p>${sourceBlock(story.pr)}</div></details>`;
  }

  function sourcesPage() {
    return `<header class="wrap page-head">${breadcrumbs('证据与边界')}<span class="kicker">29个远程草稿变更 + 1条本地研究线</span><h1>每项解释，都留一条回去的路</h1><p class="lede">先看资料类型，再看方法与限制。以下状态核查于2026年11月26日；全部源变更为开放草稿、未合并。文件固定到核查时的提交版本，页面不会自动取新数据。</p><div class="chips"><span class="chip">合成数据：人为设定输入</span><span class="chip">公开观测：保留质量与配对限制</span><span class="chip">目录资料：不等于数据已准入</span></div></header><section class="wrap section"><h2>下一阶段，先过科学闸门</h2><p class="lede">先独立评审和梳理分支，再定向补数据权利、时空配对、拓扑与现场边界。真实计算、外部联系、试点、合并和部署都不在本次授权内。</p>${misconceptions()}</section><section class="wrap source-register"><h2>查找研究与固定版本证据</h2><div class="source-filter"><label>按研究问题或编号搜索<input id="source-query" type="search" placeholder="例如：气压、AWT、140" autocomplete="off"></label><label>选择研究路线<select id="source-topic"><option value="all">所有远程研究</option>${content.topics.filter(topic=>!topic.local).map(topic=>`<option value="${topic.id}">${esc(topic.title)}</option>`).join('')}</select></label></div><p id="source-count" class="technical-meta" role="status">共29项远程研究</p><div id="source-results">${content.stories.slice().sort((a,b)=>a.pr-b.pr).map(sourceCard).join('')}</div><aside class="boundary section"><h3>建筑能源研究：远程版本未找到</h3><p>本地存在唯一研究索引；在已查的主线和29个研究分支内未找到对应版本。保留“证据不足，无法判定”，不编造远程文件或提交标识。</p>${route('topic/energy','查看已有线索与待确认事项 →')}</aside><p class="technical-meta">主线基准：<code class="sha">${esc(sources.main)}</code><br>核查时刻（协调世界时）：${esc(sources.checkedAt)}<br>说明：网页代码验收、原研究工程检查、独立科学评审、合并部署是不同决定。</p></section>`;
  }

  function notFound() {
    return `<section class="wrap section"><h1>这条阅读路线还不存在</h1><p class="lede">请从研究地图选择已有内容。未知地址不会发起请求或执行计算。</p><div class="actions">${route('map','回到研究地图','button')}</div></section>`;
  }

  function filterSources() {
    const query = document.getElementById('source-query').value.trim().toLowerCase();
    const topic = content.topics.find(item=>item.id===document.getElementById('source-topic').value);
    const list = content.stories.filter(story=>(!topic || topic.prs.includes(story.pr)) && `${story.pr} ${story.title} ${story.question} ${story.dataType} ${story.rawStatus} ${story.result}`.toLowerCase().includes(query));
    document.getElementById('source-results').innerHTML = list.sort((a,b)=>a.pr-b.pr).map(sourceCard).join('') || '<p class="empty-state">没有匹配的研究。试试更短的词，或选择所有远程研究。</p>';
    document.getElementById('source-count').textContent = `找到${list.length}项远程研究`;
  }

  function render() {
    if (location.hash === '#reading') { main.focus(); return; }
    const [kind='home',id=''] = (location.hash.replace(/^#\/?/,'') || 'home').split('/');
    let markup;
    let title='把科学讲明白';
    if (kind==='home' || kind==='journey') markup=home();
    else if (kind==='experiments') { markup=experiments(); title='四个甲烷实验'; }
    else if (kind==='experiment') { const exp=content.experiments.find(item=>item.id===id); markup=exp?storyPage(exp,true):notFound(); title=exp?.title || '路线未找到'; }
    else if (kind==='story') { const story=byPR(Number(id)); markup=story?storyPage(story):notFound(); title=story?.title || '路线未找到'; }
    else if (kind==='topic') { markup=topicPage(id); title=content.topics.find(item=>item.id===id)?.title || '路线未找到'; }
    else if (kind==='map') { markup=mapPage(); title='研究地图'; }
    else if (kind==='sources') { markup=sourcesPage(); title='证据与边界'; }
    else { markup=notFound(); title='路线未找到'; }
    main.innerHTML=markup;
    main.dataset.route = id ? `${kind}/${id}` : kind;
    document.title=`${title} · ClimateOS 科学阅读`;
    document.querySelectorAll('[data-nav]').forEach(item=>{ const active = item.dataset.nav === (kind==='experiment'?'experiments':kind==='topic'||kind==='story'?'map':kind==='journey'?'home':kind); if(active) item.setAttribute('aria-current','page'); else item.removeAttribute('aria-current'); });
    main.focus({preventScroll:true});
    if (kind==='journey') document.getElementById('journey').scrollIntoView();
    else window.scrollTo({top:0,behavior:'instant'});
  }

  main.addEventListener('click',event=>{
    const button=event.target.closest('button');
    if(!button) return;
    if(button.dataset.action==='summary') { const summary=document.getElementById('quick-read'); summary.hidden=!summary.hidden; button.setAttribute('aria-expanded',String(!summary.hidden)); if(!summary.hidden) summary.scrollIntoView({block:'nearest'}); }
    if(button.dataset.scenario && awtScenarios[button.dataset.scenario]) { main.querySelectorAll('[data-scenario]').forEach(item=>item.setAttribute('aria-pressed',String(item===button))); document.getElementById('scenario-result').innerHTML=scenarioBody(button.dataset.scenario); }
  });
  main.addEventListener('input',event=>{if(event.target.id==='source-query') filterSources();});
  main.addEventListener('change',event=>{if(event.target.id==='source-topic') filterSources();});
  window.addEventListener('hashchange',render);
  render();
})();
