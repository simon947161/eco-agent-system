"""Render existing frozen experiment results, no numerical experiments."""
from pathlib import Path
import hashlib,html,json,statistics,subprocess,sys
TASK=Path(__file__).resolve().parents[1];ROOT=TASK.parents[2];sys.path.insert(0,str(ROOT))
from cczps_lite.integration.earth_system_coupling.state import CATALOG
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(name,text):(TASK/name).write_text(text.rstrip()+'\n',encoding='utf-8',newline='\n')
def dump(name,value):write(name,json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2))
def make():
    r=read(TASK/'EXPERIMENT_RESULTS.json');d=read(TASK/'evidence/diagnostics.json');receipt=read(TASK/'evidence/batch-receipt.json')
    initial=read(TASK/'evidence/smoke_initial_receipt.json');pre=read(TASK/'evidence/pre_interface_batch_receipt.json')
    aggregate=receipt['total_script_wall_seconds']+pre['total_script_wall_seconds']+initial['elapsed_seconds']
    assert aggregate<1200 and pre['replay_sha256']==r['runs_sha256']
    rows=[json.loads(x) for x in (TASK/'evidence/main/runs.jsonl').read_text(encoding='utf-8').splitlines()]
    fail=r['failure_distribution'];normal={'nominal','heat_dry','rain_pulse','zero_wind','lagged'}
    clean=[x for x in rows if x['family'] in normal];assert all(x['status']=='COMPLETED' for x in clean)
    def avg(strategy,key):return statistics.mean(d['runs'][strategy]['final_values'][key])
    table='|策略|终态地表K|空气K|水kg/m²|累计蒸发kg/m²|\n|---|---:|---:|---:|---:|\n'
    for s in ('independent','one_way','two_way'):table+=f"|{s}|{avg(s,'ts'):.6f}|{avg(s,'ta'):.6f}|{avg(s,'water'):.6f}|{d['runs'][s]['evaporation_kg_m2']:.6f}|\n"
    report=f'''# Founder报告：共享状态与水热反馈已运行，现实预测仍待验证

Issue #150本轮交付一套可运行的共享时空状态、四类模型组件、三种耦合对照及有界实验器。以PR149 D ea6fd79b41138cbcb16f9bd1aadd68f6a4b771df为固定父，旧PR143–149未改。本轮没有读取或上传私人EcoEngine v200。

## 我们实际找到了什么

可复用机制是“状态有单位和时空支撑、组件只提出变化、同一通量两侧对账、失败回到原状态、最后再比较情景”。气温、气压、风、湿度、降雨、净辐射、水库存、蒸发和径流在同一局地状态中参与计算。空气与地表双向影响；ENSO统计与全球甲烷ERF在同一证据接口中独立存在，不伪造局地因果连接。

在固定6小时合成例子中，双向交换使空气增湿，蒸发驱动力减小。结果如下（不是Wagga天气预报）：

{table}

预先设定的热旱反例：基准、只升温、只减水均未触发；同时升温和减水触发。阈值是研究假设，未获得真实预警有效性。交换系数减半、风速加倍后轨迹完全相同，说明观测曲线吻合仍不足以识别参数。

## 万次运行究竟意味着什么

主批实际完成记录{r['completed_runs']}条，为3336个配置各运行3策略，12族每族834条；不是一万次独立现场实验。{fail['COMPLETED']}条完成数值推进（{100*fail['COMPLETED']/r['completed_runs']:.2f}%），{r['completed_runs']-fail['COMPLETED']}条被显式拒绝。五个正常/极端但未故意破坏契约的族共{len(clean)}条全部完成。其余包括故意错单位/时间/空间、缺值、稳定性与迭代上限负例，不能把总通过率解释成预测准确率。

失败分布：{json.dumps({k:v for k,v in fail.items() if k!='COMPLETED'},ensure_ascii=False)}。主批同seed重放10008条，原始JSONL字节SHA-256一致：`{r['runs_sha256']}`。新seed另300条；120次相关性诊断及解析/扰动小例单列，未凑数。正式主批{r['elapsed_seconds']:.2f}秒；含最终重放/诊断{receipt['total_script_wall_seconds']:.2f}秒。初版冒烟、接口完善前整批、冻结后整批累计{aggregate:.2f}秒，小于1200秒护栏。最终归档总字节见QA清单，低于200MB。

最大单格质量残差{r['max_water_residual_kg_m2']:.3e}kg/m²，能量残差{r['max_energy_residual_j_m2']:.3e}J/m²。解析扩散空间误差约按4倍下降、时间约按2倍下降；耦合dt减半结果趋近。这证明声明的离散账和算子可复算，不证明现实模型完整。

## 什么仍然不知道

没有与此多变量过程同支撑的独立现场通量/库存序列，参数尚未校准；没有真实区域预测技能。凝结、云、液体显热、植被与复杂土壤阻力未完整建模；局地网格是合成矩形。单向空气是规定边界储库，双向空气可改变，因此两者不同不自动等于精度改进。已有Wagga历史统计保持46个保留SON、缺测与混杂限制；全球CH4 ERF仍只在原全球年域有效。

状态：LOCAL_VERIFIED；合成机制SYNTHETIC_TESTED；READY_FOR_SCIENTIFIC_REVIEW；SCIENCE=PENDING；DEPLOYED=false。ECOChain权威目录仍NOT_FOUND，Enotebook仍PENDING。代码通过不能替代独立科学评审。

## Founder需要的最少决策

先把最终D/R和本包交ChatGPT独立复核。评审后决定下一受限批次优先增加哪一种独立观测和替代模型，而非直接放大到十万次。十万次建议分预注册参数域、独立种子、模型对照及留出验证四组，每批定成本/停止条件；本轮没有启动该下一阶段。

主线GitHub交付完成后，旧系统独特方法与新机制关系另作独立研究。本次未进入私人EcoEngine v200，未合并、未部署、未扩大科学准入或真实排放实验授权。评审入口见CRP_HANDOFF.md、REVIEW_REQUEST.json和NEXT_SESSION.md。
'''
    write('FOUNDER_REPORT_ZH.md',report)
    write('COUNTEREVIDENCE_AND_FAILURES.md',f'''# 失败、反证及不能据此宣称的结论

主批实际分布：

|状态|条数|含义|
|---|---:|---|
'''+''.join(f'|{k}|{v}|'+('完成声明模型推进' if k=='COMPLETED' else '按门限拒绝，详见原run_id/config/failure')+'|\n' for k,v in fail.items())+'''
missing_q族中独立地表可完成，两交换策略阻塞；iteration_limit族的单/独立可完成、双向拒绝；stiff族由CFL而非名称决定拒绝。正常五族415? 不应猜数，准确值见FOUNDER报告和原始矩阵。失败初始化与失败步回滚分别记录stage，未初始化时不谎称发生过步回滚。

反证1：零风条件使三策略相同，反驳“耦合必然带来差异”。反证2：Ce×U不可辨识，反驳“同一输出唯一确定机制”。反证3：联合热旱与单独扰动结论不同，反驳单变量排序可解释所有阈值。反证4：双向需要额外迭代与观测变量，迭代耗尽或缺湿度时比独立模型更脆弱。反证5：Guillod2015显示土壤水分—降雨的时空关联符号可不同，不能把本模型内反馈方向普遍化。

当前局部Jacobian范数与松弛界见diagnostics.json；只是局部充分界。决策记忆不证明物理滞回。rho变化导致输出散布变化，但不是现实置信区间。所有负例保留，不调参掩盖。缺乏观测误差对照，不能排名真实准确率。

发布前仍需科学评审：理想气柱、无凝结、固定参考液体焓、空间代表性、未知参数、现有观测权利与缺测。当前软件验收不关闭这些门。
'''.replace('正常五族415? 不应猜数，准确值见FOUNDER报告和原始矩阵。',f'正常五族共{len(clean)}条，准确范围见原始矩阵。'))
    write('README.md','''# Earth System Coupling Lab — Issue #150

从[中文Founder报告](FOUNDER_REPORT_ZH.md)和[12页离线展示](slides.html)开始。所有局地计算为声明合成模型；正式科学准入PENDING。

|研究索引|内容|
|---|---|
|[唯一任务书](TASKBOOK_ZH.md)、[复用审计](REUSE_AUDIT.md)|父PR149、旧架构与真实能力|
|[方法研究](MECHANISM_RESEARCH.md)、[来源登记](SOURCE_REGISTER.json)|官方方法、版权与反证|
|[状态模式](SHARED_STATE_SCHEMA.json)、[接口](MODEL_INTERFACE.md)、[耦合设计](COUPLER_DESIGN.md)|真实源码入口与限制|
|[公式和假设](NUMERICAL_METHODS_AND_ASSUMPTIONS.md)、[实验矩阵](EXPERIMENT_MATRIX.md)|物理量、设计、参数与预注册|
|[主批结果](EXPERIMENT_RESULTS.json)、[分类表](summary.csv)、[诊断](evidence/diagnostics.json)|10008实际记录、完整轨迹与联合反例|
|[失败](COUNTEREVIDENCE_AND_FAILURES.md)、[权利](DATA_AND_MODEL_RIGHTS.md)、[科学门](PHYSICAL_AND_STATISTICAL_GATES.md)|拒绝、许可与UNKNOWN|
|[QA](QA_AND_VALIDATION.md)、[治理交接](CCZPS_ECOCHAIN_HANDOFF.md)|测试、hash、决策边界|
|[交接协议](CRP_HANDOFF.md)、[下次入口](NEXT_SESSION.md)|精确R/D见HANDOFF_STATUS.json|

源码：仓库cczps_lite/integration/earth_system_coupling；测试：tests/test_earth_system_coupling.py。无需安装依赖。运行入口见MODEL_INTERFACE.md。仅独立Draft PR，未合并/部署，未触碰私人EcoEngine v200。
''')
    sources=[('CF1.12','https://cfconventions.org/Data/cf-conventions/cf-conventions-1.12/cf-conventions.html','1.12 / 2024-12-04','CC0 document','units, calendar, bounds, cell methods','ADOPT'),
      ('BMI','https://github.com/csdms/bmi','2.0 README on 2026-11-10','MIT declared by repository','variable/grid/clock/update contract','ADOPT_CONCEPT'),
      ('NUOPC','https://earthsystemmodeling.org/nuopc/','web documentation 2026-11-10','code-release licence not admitted','run sequence, field dictionary, clocks','DEFER_LIBRARY'),
      ('ESMF','https://earthsystemmodeling.org/regrid/','official regridding page 2026-11-10','release-specific licence PENDING; no code imported','area overlap conservative regridding','ADOPT_CONCEPT'),
      ('FAO56_ES','https://www.fao.org/4/x0490e/x0490e07.htm','FAO56 1998 ch3 eq11','linked/paraphrased only','saturation vapour pressure','WRAP_FORMULA'),
      ('FAO56_ET','https://www.fao.org/4/x0490e/x0490e06.htm','FAO56 1998 ch2','linked/paraphrased only','Penman-Monteith resistance countermodel','DEFER_IMPLEMENTATION'),
      ('GUILLOD','https://www.nature.com/articles/ncomms7443','2015 / DOI 10.1038/ncomms7443','CC-BY-4.0 article; no figures copied','spatial/temporal sign and confounding counterevidence','ADOPT_COUNTEREVIDENCE'),
      ('ERA5','https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels','product page 2026-11-10','dataset terms not used; no download','assimilation combines model and observations','DEFER_DATA'),
      ('SCIPY','https://docs.scipy.org/doc/scipy-1.14.1/reference/generated/scipy.integrate.solve_ivp.html','1.14.1 fixed documentation','no code imported; release licence check before adoption','RK45/Radau/BDF alternate solver','DEFER_LIBRARY')]
    dump('SOURCE_REGISTER.json',[dict(source_id=i,url=u,version=v,rights=l,scope=b,decision=a,access='OFFICIAL_PAGE_READ',page_byte_sha256=None,access_date='2026-11-10') for i,u,v,l,b,a in sources])
    paths=['docs/00_MASTER_ARCHITECTURE/SYSTEM_RELATIONSHIP_MAP.md','docs/00_MASTER_ARCHITECTURE/ECOENGINE_V2_SYSTEM_DEFINITION.md','docs/00_MASTER_ARCHITECTURE/CCZPS_LITE_V0_4_REVIEW.md','docs/03_RUNTIME_LAYER/DIFFERENTIAL_FIELD_INFERENCE.md','docs/03_RUNTIME_LAYER/FORCING_LAYER.md','docs/02_GOVERNANCE_LAYER/POSSIBILITY_COMPUTING_FRAMEWORK.md','docs/02_GOVERNANCE_LAYER/CLIMATE_ZONAL_RESPONSIBILITY_METHOD.md','docs/architecture/climateos_v2_review/02_V1_CAPABILITY_AND_DEBT_MAP.md','cczps_lite/engine/differential_field.py','cczps_lite/engine/forcing_layer.py','cczps_lite/integration/environmental_coupling.py','cczps_lite/integration/ecoengine_v192b_adapter.py','cczps_lite/integration/physical_process_trajectory.py','cczps_lite/integration/multisource_data_admission.py','cczps_lite/integration/physics_validation.py','cczps_lite/integration/global_natural_systems_atlas.py','cczps_lite/integration/dynamic_quantification.py']
    for pattern in ('task2021_2030*','task2031_2040*'):
        for folder in (ROOT/'docs/tasks').glob(pattern):paths.extend(p.relative_to(ROOT).as_posix() for p in folder.glob('*.md'))
    parent='ea6fd79b41138cbcb16f9bd1aadd68f6a4b771df';blobs=[]
    for path in paths:
        p=ROOT/path
        if not p.exists():raise RuntimeError('REUSE_PATH_NOT_FOUND '+path)
        blob=subprocess.check_output(['git','rev-parse',parent+':'+path],cwd=ROOT,text=True).strip()
        blobs.append({'path':path,'parent_commit':parent,'git_blob':blob,'lf_sha256':hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()})
    dump('evidence/reuse-blobs.json',blobs)
    fixture=read(TASK/'evidence/fixture-state.json');sample=fixture['fields']['ta'];properties={}
    for key,value in sample.items():
        properties[key]={'type':'null'} if value is None else {'type':'boolean' if isinstance(value,bool) else 'string' if isinstance(value,str) else 'array' if isinstance(value,list) else 'object' if isinstance(value,dict) else 'number'}
    properties['covariance']={'type':['null','array']};properties['standard_name']={'type':['null','string']}
    properties['kind']={'enum':['OBSERVED_STATE','CONSTRAINED_ESTIMATE','SIMULATED_STATE','HYPOTHESIS_SCENARIO']};properties['input_sha256']={'type':'string','pattern':'^[0-9a-f]{64}$'}
    dump('SHARED_STATE_SCHEMA.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'ClimateOS state metadata structural subset; scientific gates are Python validators','type':'object','required':['revision','fields'],'properties':{'revision':{'type':'integer','minimum':0},'fields':{'type':'object','propertyNames':{'enum':list(CATALOG)},'additionalProperties':{'type':'object','required':list(sample),'properties':properties,'additionalProperties':False}}},'additionalProperties':False,'$comment':'Python enforces units/shape/PSD/support/hash format. Neither this schema nor source prefixes authenticate scientific evidence.'})
    dump('evidence/field-catalog.json',{k:dict(unit=v[0],dimensions_M_L_T_Theta=v[1],standard_name=v[2],medium=v[3],temporal_kind=v[4]) for k,v in CATALOG.items()})
    slides(d,r,receipt,aggregate,table)

def chart(d,key,label):
    colors=['#d48c46','#38a6c7','#92c98f'];series=[(s,[statistics.mean(p['values'][key]) for p in r['trace']]) for s,r in d['runs'].items()]
    vals=[v for _,vs in series for v in vs];lo=min(vals);hi=max(vals);span=max(hi-lo,1e-5);parts=[]
    for color,(s,vs) in zip(colors,series):
        points=' '.join(f'{65+i*700/(len(vs)-1):.1f},{235-(v-lo)/span*180:.1f}' for i,v in enumerate(vs));parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{points}"/><text x="{65+230*len(parts)}" y="288" fill="{color}">{s}</text>')
    return f'<svg viewBox="0 0 820 310" role="img" aria-label="{label}，合成三策略6小时曲线"><text x="20" y="24">{label} · 合成6小时</text><text x="8" y="57">{hi:.3f}</text><text x="8" y="239">{lo:.3f}</text><path d="M65 40 V245 H765" fill="none" stroke="#8299a7"/><text x="65" y="266">0 h</text><text x="730" y="266">6 h</text>'+''.join(parts)+'</svg>'
def slides(d,r,receipt,aggregate,table):
    f=r['failure_distribution'];er=r['max_energy_residual_j_m2'];wr=r['max_water_residual_kg_m2']
    heat='<table><tr><th>ΔT (K)</th><th>Δ风 (m/s)</th><th>终态Ts (K)</th></tr>'+''.join(f"<tr><td>{x['delta_temperature_K']:+g}</td><td>{x['delta_wind_m_s']:+g}</td><td>{x['final_ts_K']:.3f}</td></tr>" for x in d['heatmap'])+'</table>'
    pages=[
    ('共享状态与反馈机制已经跑通','<p class="lead">四类组件、三种策略、10,008条真实运行记录。</p><p>共享单位与时空支撑，同一通量两侧记账，失败回滚后再比较情景。</p><p class="badge">LOCAL_VERIFIED · SYNTHETIC_TESTED · SCIENCE PENDING</p><p>缺少独立现场验证，尚不能预测真实区域风险。</p>','FOUNDER_REPORT_ZH.md'),
    ('复用原架构，补上可执行协调','<p>观察与来源 → 共享环境状态 → 物理运行 → CCZPS多未来 → ECOChain候选记录 → 人类决策。</p><p>保留PR143–149的甲烷、Atlas、RONI与Wagga历史成果。旧差异场分数没有被改称物理梯度。</p><p>私人EcoEngine v200未读取、未上传。旧方法关系研究另列后续任务。</p>','REUSE_AUDIT.md'),
    ('17种字段定义保留证据边界','<p>气温、地表温度、气压、风、湿度、降雨、水库存、辐射、蒸发和径流。</p><p>每个字段保留单位、介质、网格、时间、来源hash、质量与不确定性。缺湿度只阻断依赖它的交换。</p><p>面积重映射守恒，错误点面映射或月到小时转换会被拒绝。</p>','COUPLER_DESIGN.md'),
    ('水与热用同一笔交换量对账','<p class="formula">W′ = W + (P − E − R) Δt</p><p class="formula">Cₛ ΔTₛ = (Rn − H − LᵥE + 扩散) Δt</p><p>蒸发带走地表能量与水，同时进入空气水汽库存。外边界通风和显热明确列账。</p><p>凝结、云与液体显热等过程仍有简化，守恒成立不证明物理过程完整。</p>','NUMERICAL_METHODS_AND_ASSUMPTIONS.md'),
    ('空气反馈改变地表温度轨迹',chart(d,'ts','地表温度 / K')+'<p>单向空气保持规定边界；双向空气可变。曲线差异是边界与机制的结果，尚无观测准确率比较。</p>','evidence/diagnostics.json'),
    ('增湿抑制后续蒸发',chart(d,'q','空气比湿 / kg kg⁻¹')+f"<p>固定合成例：单向累计蒸发{d['runs']['one_way']['evaporation_kg_m2']:.3f} kg/m²，双向{d['runs']['two_way']['evaporation_kg_m2']:.3f} kg/m²。这个方向不能普遍化为真实增雨规律。</p>",'evidence/diagnostics.json'),
    ('联合变化才能看见这个阈值','<table><tr><th>合成情景</th><th>热且干</th></tr><tr><td>基准</td><td>未触发</td></tr><tr><td>只升温</td><td>未触发</td></tr><tr><td>只减水</td><td>未触发</td></tr><tr><td>联合升温减水</td><td>触发</td></tr></table><p>预设Ta &gt; 303.15K且W/Wmax &lt; 0.25。阈值未经真实风险验证，退出记忆不证明物理多稳态。</p>','evidence/diagnostics.json'),
    ('温度与风的灵敏度是条件性的',heat+'<p>表为预定3×3扰动。Ce减半且风加倍产生相同轨迹，参数不能仅凭输出独立识别。相关误差也会改变输出散布。</p>','NUMERICAL_METHODS_AND_ASSUMPTIONS.md'),
    ('万次包含成功与明确拒绝',f'<p class="lead">{f["COMPLETED"]:,}条完成推进，{10008-f["COMPLETED"]:,}条拒绝。</p><p>3336个配置，每个三策略对照。12族包括正常、热旱、强雨、零风、缺测及故意错配。</p><p>278条双向迭代上限负例被保留。总通过率不是预测准确率。</p><p>固定seed完整重放字节一致；新seed另300条。</p>','EXPERIMENT_RESULTS.json'),
    ('数值证据支持声明的简化账',f'<p>最大水残差 {wr:.2e} kg/m²<br>最大能量残差 {er:.2e} J/m²</p><p>解析扩散：空间误差约4倍下降，时间约2倍下降。实际dt减半、2/4/8格、时滞与协方差均有结果。</p><p>正式主批{r["elapsed_seconds"]:.1f}秒；含初版与最终重放的累计批次{aggregate:.1f}秒，低于20分钟上限。</p>','QA_AND_VALIDATION.md'),
    ('全球与季节证据保持原尺度','<p>全球CH₄年ERF = 0.569344413968403 W/m²。</p><p>Wagga旧统计13/17只是46个保留春季内的条件频率，缺测、IOD/SAM混杂与不确定性未消失。</p><p>这两类证据可被查询和审阅，不进入局地降雨、净辐射或次日温度方程。</p>','CCZPS_ECOCHAIN_HANDOFF.md'),
    ('先独立评审，再决定下一批','<p>ChatGPT核公式、代码、账、失败和证据边界，Founder决定下一受限实验。</p><p>未来十万次应增加替代模型、独立观测与留出验证，每批固定参数域、种子和预算。仅扩大样本不会解决模型结构误差。</p><p class="badge">未合并 · 未部署 · 科学准入 PENDING</p><p>主线交付后单独研究旧方法，本轮不自动启动下一长期任务。</p>','NEXT_SESSION.md')]
    body=''.join(f'<section id="page-{i}"'+(' hidden' if i>1 else '')+f'><h1>{title}</h1>{content}<details><summary>查看来源与证据状态</summary><p>合成机制研究／正式科学准入 PENDING。<a href="{source}">本页依据</a> · <a href="SOURCE_REGISTER.json">官方来源目录</a></p></details></section>' for i,(title,content,source) in enumerate(pages,1))
    css='''*{box-sizing:border-box}body{margin:0;background:#111f2b;color:#edf3f5;font:25px/1.55 "Segoe UI","Microsoft YaHei",sans-serif}main{max-width:1100px;margin:auto;padding:48px 40px 110px}h1{font-size:clamp(30px,4vw,46px);line-height:1.23;color:#92c98f;margin:0 0 32px}p{margin:22px 0}.lead{font-size:1.35em;font-weight:600}.badge{color:#92c98f;border-top:1px solid #536777;padding-top:20px}a{color:#83d3ee;overflow-wrap:anywhere}details{font-size:17px;margin-top:35px}summary{cursor:pointer}table{border-collapse:collapse;width:100%;font-size:21px}td,th{text-align:left;padding:8px 12px;border-bottom:1px solid #536777}svg{width:100%;display:block;background:#152936;border-radius:8px}svg text{font:18px sans-serif;fill:#edf3f5}.formula{font-size:1.15em;color:#f3c28f}nav{position:fixed;bottom:0;left:0;right:0;background:#111f2bf5;border-top:1px solid #536777;display:flex;justify-content:center;align-items:center;gap:20px;padding:12px;font-size:17px}button{font:inherit;padding:8px 20px;background:#204557;color:white;border:1px solid #83d3ee;border-radius:4px;cursor:pointer}button:disabled{opacity:.35}section[hidden]{display:none}@media(max-width:600px){body{font-size:21px}main{padding:30px 20px 110px}h1{margin-bottom:26px}table{font-size:16px}td,th{padding:7px 5px}details{font-size:16px}.lead{font-size:1.2em}nav{gap:10px}}'''
    js='''const slides=[...document.querySelectorAll('section')];let n=0;function show(i){n=Math.max(0,Math.min(slides.length-1,i));slides.forEach((s,j)=>s.hidden=j!==n);document.querySelector('#count').textContent=`${n+1} / ${slides.length}`;document.querySelector('#prev').disabled=n===0;document.querySelector('#next').disabled=n===slides.length-1;history.replaceState(null,'',`#page-${n+1}`);scrollTo(0,0)}document.querySelector('#prev').onclick=()=>show(n-1);document.querySelector('#next').onclick=()=>show(n+1);document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown','ArrowLeft','PageUp','Home','End'].includes(e.key)){e.preventDefault();show(e.key==='Home'?0:e.key==='End'?slides.length-1:n+(['ArrowRight','PageDown'].includes(e.key)?1:-1))}});show((Number(location.hash.replace('#page-',''))||1)-1);'''
    write('slides.html','<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ClimateOS 共享状态与物理反馈研究</title><style>'+css+'</style><main>'+body+'</main><nav aria-label="翻页"><button id="prev">上一页</button><span id="count" aria-live="polite"></span><button id="next">下一页</button></nav><script>'+js+'</script></html>')
if __name__=='__main__':make()
