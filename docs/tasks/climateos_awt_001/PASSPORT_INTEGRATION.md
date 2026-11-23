# 最小领域扩展，不建立新证据库

本目录 JSON 文件就是版本化工件；没有数据库、账户、网络代理或LLM执行依赖。复用PR145的canonical/digest、基本类型检查和事件链，调用PR144物料账。Bondo schema原样保留，本护照不是对其直接合格验证。

|既有语义|AWT扩展字段|边界|
|---|---|---|
|CLAIM / Bondo claims|claim_id、9种typed entities及depends_on|气体观测、物理估计、基线、项目、泄漏、净值、资格、权利、审查分离；图拒绝环及悬空引用|
|DATA / evidence|dataset、observation|本轮NO_OBSERVATION，仪器/位置/时间/不确定性均null；绝不生成假观测|
|SOURCE_LICENCE|dataset.source/licence/sha256，sources.json|fixture精确字节hash与外部来源网页状态分开；外部原件本轮SHA=null，不哈希URL冒充原件|
|METHOD / CALCULATION|formula、output_provenance、input_sha256|源版本、输入canonical hash、代码LF hash；field单位与文件时间支持强校验|
|version conflicts/gaps|legal、rights_links、assurance/reasons|具体旧方法路径NOT_ELIGIBLE与缺证据INSUFFICIENT_EVIDENCE区分|
|REVIEW / OUTCOME|review及提交事件|人工reviewer=null、PENDING，未伪造独立人审事件或发证|

版本为awt-claim-passport/1，schema采用JSON Schema2020-12兼容子集，runtime仅承诺本schema所用关键字。完整外部JSON Schema通用引擎没有实现。运行期语义检查比schema更严格：fixture/代码hash、单位、9类型覆盖、无环图、日期、授权质量与时间边界。schema中的可空测量字段为将来接口形状准备，本轮运行器明确拒绝非null测量。

每个修订含revision与previous_revision_sha256。`revision()`返回新对象，不改旧对象；`append_event/verify_events`复用PR145链。演示只有SUBMITTED，没有模拟真人批准。Git commit作为外部版本锚记录于PR评论；可写工作树和同树哈希并不构成防篡改存储、可信时间戳或数字签名。若未来多人申报，需正式角色任命、独立获取原件、真实权属登记及不可改写的外部审计锚，本轮不搭建这些基础设施。

结果JSON引用可追溯到实际fixture和源码。物理结果保留kgCH4、反应CO2和守恒残差；净值为tCO2e/合成cohort。`INTERNAL_FIXTURE_REPLAY_ONLY`明确表示只重放内部质量账，不把申报单位错误视为现场复算成立。
