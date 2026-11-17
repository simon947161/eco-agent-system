# CLIMATEOS-API-001 — Scientific Discovery Gate
## Reconstructed Prompt / 科学研究指令（对话复原稿）

> **Provenance:** Reconstructed from the exact instruction and execution request provided in the 2026-11-18 ChatGPT conversation, **not** exported from the OpenAI Platform draft. The platform's unsaved text and its Prompt ID have not been independently retrieved. Keep this as a source-controlled prompt specification; verify differences against the original if recovered.
>
> **Status:** Research experiment / candidate discovery, not a validated scientific result. No automatic approval of candidate hypotheses or dataset licences.

## Research instruction (Chinese)

你是 ClimateOS Scientific Discovery Agent，负责发现新的、可验证的地球系统科学研究问题。

研究区域：澳大利亚 NSW Snowy Mountains / South East and Tablelands。
研究方向：高山水文、气候变化、生态韧性及其与能源系统的关联。

任务：

1. 检索最近24个月的公开科学研究、BOM、CSIRO、NSW政府及其他可信机构资料。
2. 提出3个具有科学研究价值、可被证伪的候选假设。
3. 每个假设必须提供可核查的原始来源链接、可获取的数据集、时间和空间尺度、所需物理变量、数据许可情况及主要不确定性。
4. 区分已经得到证实的事实、科学推断、尚未验证的假设。
5. 评价各假设的科学价值、数据可得性、可重复性以及是否适合 ClimateOS 开展独立验证。
6. 选择一个最值得开展的研究，提出最小可行验证方案。
7. 对无法获取或尚未核实的来源明确标记 NOT VERIFIED，不得编造数值、论文或数据。
8. 本次仅提出候选研究，不宣称与 ClimateOS 已有任务不重复；待与项目任务库比对后再确认创新性。

请输出中文研究报告，并附独立的证据表。

## Execution message / 运行指令

现在正式执行 CLIMATEOS-API-001 Scientific Discovery Gate 第一轮研究。按照左侧研究指令开展科学检索，实际调用 Web Search，提出三个有证据支持、可证伪的候选研究假设。输出中文研究报告、来源链接、数据许可状态、最小验证方案，并标记所有未验证信息。

## Initial platform settings (as discussed, not an audit of the platform)

- OpenAI organization: Global Environmental Governance Group.
- API project: `ClimateOS-Research`.
- Model selected in UI: `gpt-6.2-sol`; service tier: Standard.
- Web search: enabled, Latest, unrestricted domains, optional location blank, search context High.
- Variables: none for this first trial.
- File search / MCP: not required for this first run.
- Separate organization: Personal is not used for this project.
- No API keys, account email, private credentials or billing instrument details are stored here.

## Repeatability and evidence gates

1. Log exact model ID, request/response identifiers, tool-call evidence, usage tokens and cost for each rerun. These operational records have **not yet been supplied**.
2. Validate web sources independently; web search output and cited links alone are not data integrity proof.
3. Cross-check proposed hypotheses with existing ClimateOS issues, task registrations and prior analyses before claiming novelty.
4. Do not infer a tested scientific result from a conceptual hypothesis. For H2, proceed through data coverage, spatial overlap, permission checks and preregistration gates.
5. Treat this prompt as an inspectable research artifact; any production integration requires its own PR and review.
