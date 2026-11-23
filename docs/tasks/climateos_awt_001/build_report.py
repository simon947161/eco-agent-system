"""Chinese offline pages. Reuses PR138 navigation/CSS; diagrams are authored SVG."""
import html
import json
import re
from pathlib import Path
import engine as e

T=e.HERE
r=e.read('evidence/results.json'); sens=e.read('evidence/sensitivities.json')
tests=e.read('evidence/unit-tests.json')
net=r['B']['calculation']['estimated_net_abatement_t_CO2e'];low,high=sens['B']['bounds']
pages=[
('同样1000吨，不能换成同样的信用',
 'P0–P3合成验证已运行；真实减排证据仍不足。',
 [f'中心假设下，AD相对填埋的条件差额为 {net:.2f} t CO₂e。',
  f'设定范围内可变为 {low:.2f} 至 {high:.2f} t CO₂e，符号可以反转。',
  '这解释参数与边界怎样影响结果。没有取得现场减排观测，信用数量始终NOT_DETERMINED。'],
 ['COUNTERFACTUAL_CASE_1000T.md','evidence/results.json'],'cover'),
('先复用已有成果，再补这次缺口',
 '主线没有增加模型平台、数据库或新的AI服务。',
 ['固定PR145 ae1050a…作为独立stacked分支基线。PR144提供甲烷物料账，PR145提供哈希、schema类型检查与提交事件。',
  'CarbonOS PR132、中文报告PR137和D3结果只读引用。既有观测和合成模型并未合并到main。',
  'D3三个候选停止、原始配套气体/气象数据未准入。私人EcoEngine与Council数据未访问。'],
 ['EXISTING_ASSETS_AND_GAPS.md','evidence/github-intake.json'],'plain'),
('九类主张分别有自己的证据门',
 '测到浓度、估计排放、计算反事实和获得信用是不同问题。',
 ['观测要有仪器、时间、单位和QC。这里的观测字段为null，明确NO_OBSERVATION。',
  '物理账区分生成、捕集、氧化、销毁、逸散与库存；项目排放和边界外泄漏不重复扣减。',
  '净减排、法规资格、权利重合和独立审查分别输出状态。没有任何一条推论自动变成已签发信用。'],
 ['PASSPORT_INTEGRATION.md','CLAIM_PASSPORT_SCHEMA.json','examples/B.json'],'flow'),
('先把比较边界锁在同一批物料上',
 '1000吨湿废物，假设100年累计，所有设施参数均为SYNTHETIC。',
 ['DOC=0.15，甲烷碳份额F=0.5；期间分解比例由作者设定，没有运行FOD或气候响应模型。',
  'B/C中消化残渣进入独立填埋端点。AD和残渣碳分配不能超过输入有机碳。',
  '累计物料时间与GWP100评价期分开。本轮不模拟排放发生年份，也不声称完整LCA、年度申报或真实增温。'],
 ['fixtures/B.json','COUNTERFACTUAL_CASE_1000T.md'],'plain'),
('捕集不等于销毁，去向必须对账',
 '既有PR144核心已实际检查接口和CH₄／碳元素守恒。',
 ['中心填埋路径：生成50,000 kg CH₄，捕集18,500 kg，大气逸散28,901.3 kg。',
  '未捕集气体可在覆盖层氧化；已捕集气体仍可能在管线泄漏或燃烧装置滑漏。',
  '初末甲烷存量、横向转移显式假设为0。实际场址缺测时不能复制这些0。反应生成的生物源CO₂单列。'],
 ['engine.py','evidence/results.json'],'ledger'),
('四个情景呈现两种不同的变化',
 'B与C物理数字相同，法规和反事实可信度可以不同。',
 ['A继续同一填埋路径是恒等控制，净差额0。B包含AD、残渣、能源、运输和单独泄漏项。',
  'C在FOGO收集义务情境下，继续填埋是否仍是可信反事实未知。相同算术不能自动赋予额外性。',
  'D缺残渣排放，系统保留已算片段，拒绝完整净值。四例的独立保证状态均为证据不足。'],
 ['evidence/results.json','evidence/decision-cases.json'],'table'),
('最不利组合会推翻中心结果',
 '我们保留负值，并展示模型对输入假设的依赖。',
 ['A/B/C各128个角点，共384次合成敏感性复算；D因缺数据停止，0次。',
  '参数包含填埋捕集和分解、AD收集和管漏、残渣分解/N₂O及进口电力系数。',
  '范围未经现场校准，固定GWP和其余参数；这是情景包络，不是置信区间，也不是总不确定性。'],
 ['evidence/sensitivities.json','COUNTERFACTUAL_CASE_1000T.md'],'range'),
('FOGO分收义务不直接指定AD路径',
 '按日期、对象、豁免和证据层级保守筛查。',
 ['EPA说明家庭收集义务从2030-07-01起，商业分期另行判断。本轮只实现有Council红桶服务家庭的有限筛查。',
  '测试2030日期只是在2026可读资料下的条件演练；真实项目必须重新检查届时法律、豁免及许可。',
  'NSW现行法HTML403后停止。具体处理路线和额外性仍未知，没有把指导网页当作完整法律审核。'],
 ['LEGAL_METHOD_VERSION_REGISTER.md','sources.json'],'plain'),
('历史方法到期，咨询仍然是咨询',
 '法规版本和法定输入不能由物理模型代替。',
 ['AWT2015已于2025-03-31到期；本程序只对其到期后的新注册路径返回NOT_ELIGIBLE。既有项目不能被一并否定。',
  'ARRC2026提案及DCCEEW tracker显示新AWT仍在开发。残渣、捕集和Safeguard讨论不自动成为法律。',
  '37%/24%历史AWT参照及75%旧CER上限仅用于作者情景；不是实测效率或当前默认值。无正式咨询投稿。'],
 ['LEGAL_METHOD_VERSION_REGISTER.md','sources.json'],'plain'),
('缺项和疑似重合会阻止“通过”',
 '规则解释可复查，不依赖LLM自行给出认可。',
 ['8个记录案例覆盖物理不一致、来源篡改、缺基线、缺残渣、未知豁免、到期方法及候选权利重合。',
  'D中同批次、同区间、同量边界出现在AWT和Safeguard候选记录下，只触发核对风险。没有真实登记、发行或欺诈判断。',
  '版本修订返回新护照和前版hash；提交链没有独立真人签名，不能冒充正式鉴证。'],
 ['evidence/decision-cases.json','PASSPORT_INTEGRATION.md','ASSURANCE_DECISION_TESTS.md'],'plain'),
('测试证明实现边界，科学审查仍待完成',
 f'{tests["tests"]}项本任务测试通过，输入和输出可离线复算。',
 ['独立手算、共享参数恒等控制、守恒、空值、错误单位、篡改、边界超限和审查状态均有测试。',
  '本机全仓库570项测试完成，1项Windows符号链接权限跳过。远程CI以绑定最终HEAD的PR回执为准。',
  '来源网页没有冒充原始气体数据；作者fixture有精确字节SHA，旧来源hash明确标记继承，缺原件仍为空。'],
 ['evidence/unit-tests.json','evidence/replay.json','ASSURANCE_DECISION_TESTS.md','evidence/reuse-hashes.json'],'plain'),
('下一步先补一条可独立核查的证据链',
 '本轮可交审阅，不能交正式减排申报。',
 ['建议先确认一批有合法许可的物料：湿重、组成、反事实去向、同区间集气/泄漏/残渣/能耗和校准记录。',
  '请ChatGPT审查时间边界、基线可行性、残渣归属、范围选取、法规筛查及错误“通过”的风险。审查状态PENDING。',
  'Founder需另批真实数据扩展、真实科学/独立保证、合并、部署、官方提交或ACCU申请；本轮未执行。'],
 ['NEXT_SESSION.md','CRP_HANDOFF.md','REVIEW_REQUEST.md'],'plain')]

def table():
    rows=[]
    for s in 'ABCD':
        c=r[s]['calculation']
        vals=[c[k] for k in ['baseline_t_CO2e','project_t_CO2e','leakage_t_CO2e','estimated_net_abatement_t_CO2e']]
        rows.append('<tr><th>'+s+'</th>'+''.join('<td>'+('缺失' if v is None else f'{v:.2f}')+'</td>' for v in vals)+'</tr>')
    return '<div class="table-scroll"><table><caption>合成累计值 · t CO₂e / 1000吨湿废物</caption><thead><tr><th>情景</th><th>基线</th><th>项目</th><th>泄漏</th><th>净值</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'
def graphic(kind):
    if kind=='table':return table()
    if kind=='cover':return f'<div class="big">{net:.2f}<span>t CO₂e / 合成中心差额</span></div>'
    if kind=='range':
        def x(v):return 80+(v+600)/1600*740
        return f'<figure><svg viewBox="0 0 900 180" role="img" aria-label="B和C合成净值范围从负459.66到正951.83，中心469.35"><line x1="80" y1="90" x2="820" y2="90" stroke="#a5b6aa"/><line x1="{x(0)}" y1="35" x2="{x(0)}" y2="135" stroke="#243a30" stroke-dasharray="4 4"/><line x1="{x(low)}" y1="90" x2="{x(high)}" y2="90" stroke="#b27a39" stroke-width="16"/><circle cx="{x(net)}" cy="90" r="11" fill="#155741"/><g font-size="22" fill="#243a30"><text x="{x(low)}" y="150" text-anchor="middle">{low:.2f}</text><text x="{x(0)}" y="25" text-anchor="middle">0</text><text x="{x(net)}" y="55" text-anchor="middle">{net:.2f}</text><text x="{x(high)}" y="150" text-anchor="middle">{high:.2f}</text></g></svg><figcaption>作者设定角点包络，单位t CO₂e；不是置信区间。</figcaption></figure>'
    if kind in ['flow','ledger']:
        labels=['证据与假设','物理与反事实','法规与权利','独立审查'] if kind=='flow' else ['产生 50,000','捕集 18,500','氧化 3,150','大气 28,901.3']
        return '<div class="flow">'+''.join('<div>'+v+'</div>' for v in labels)+'</div>'
    return ''

old=(T.parent/'climateos_physics_validation_001/index.html').read_text(encoding='utf-8')
css=re.search(r'<style>(.*?)</style>',old,re.S).group(1)
nav=re.search(r'(<nav.*?</script>)',old,re.S).group(1)
# Reuse frozen navigation, improve focus handling for interactive details/buttons.
nav=nav.replace("['SELECT','INPUT','TEXTAREA']","['SELECT','INPUT','TEXTAREA','BUTTON','SUMMARY','A']")
extra='body{background:#e6eae5;color:#203c30}main{background:#fafbf7}nav{background:#203c30}.big{font-size:76px;line-height:1.15;color:#155741;margin:25px 0}.big span{display:block;font-size:19px}.flow{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:24px 0}.flow div{border-top:3px solid #3d8061;padding:14px 0}.notice{color:#755427}.page-label{color:#416950}.badge{font-size:13px;letter-spacing:.05em;color:#755427}svg{width:100%}caption{text-align:left;font-size:14px}li{margin:12px 0}h1{font-size:34px} @media(max-width:650px){.big{font-size:55px}.flow{grid-template-columns:repeat(2,1fr)}h1{font-size:26px}}'
sections=[];md=['# CLIMATEOS–AWT–001｜Founder验收报告','', '2026-11-23 · SYNTHETIC · SCIENCE PENDING · NOT DEPLOYED','']
for i,(title,lead,points,links,kind) in enumerate(pages,1):
    section=f'<section id="slide-{i}" aria-labelledby="title-{i}" hidden><div class="page-label">CLIMATEOS–AWT–001 · {i:02d} / 12</div><h1 id="title-{i}">{html.escape(title)}</h1><p class="lead">{html.escape(lead)}</p>'+graphic(kind)+'<ul>'+''.join('<li>'+html.escape(p)+'</li>' for p in points)+'</ul><p class="badge">SYNTHETIC · SCIENCE PENDING · CREDIT NOT_DETERMINED</p><details><summary>展开来源、公式与证据</summary><ul>'+''.join(f'<li><a href="{html.escape(link)}">{html.escape(link)}</a></li>' for link in links)+'</ul></details></section>'
    sections.append(section)
    md += [f'## {i:02d}｜{title}','',lead,'']+['- '+p for p in points]+['','证据：'+ ' · '.join(f'[{x}]({x})' for x in links),'']
doc='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\'; style-src \'unsafe-inline\'; img-src \'self\' data:; connect-src \'none\'"><title>ClimateOS AWT 验收</title><style>'+css+extra+'</style></head><body><main>'+''.join(sections)+'</main>'+nav+'</body></html>'
(T/'index.html').write_text(doc,encoding='utf-8',newline='\n')
(T/'FOUNDER_ACCEPTANCE_CN.md').write_text('\n'.join(md),encoding='utf-8',newline='\n')
print('12 Chinese slides and Markdown generated from actual outputs; PR138 CSS/navigation reused.')
