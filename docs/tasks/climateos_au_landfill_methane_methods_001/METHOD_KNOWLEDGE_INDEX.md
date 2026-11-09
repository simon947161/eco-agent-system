# ClimateOS / Enotebook 长期方法知识索引

状态 **STANDALONE_REVIEWABLE / PENDING_INTEGRATION**。这是本轮正式交付的知识包，不声称已进入尚未确认的Enotebook主库。

审计：按文件名搜索Enotebook、CSP、knowledge、distill及docs内容；发现既有PR143方程/因素/来源/证据结构、历史Evidence Passport任务材料，未找到具有明确owner与schema的Enotebook/CSP正式接纳目录。复用PR143的source_id、locator、status、version、provenance和R/D交接方式；不复制其运行引擎、不覆盖旧条目。个人学习记录未访问。

机器入口[knowledge/catalog.json](knowledge/catalog.json)，每包七层：SOURCE_MASTER、KNOWLEDGE_CORE、SKILL_PROCEDURE、CASE_EVIDENCE、CONNECTIONS、LEARNING_PATH_ZH、UPDATE_LEDGER。README额外显式标SECTION_MAP、EQUATION_EXTRACT与METHOD_LIMITATIONS。每源3个练习/答案，总24个；F即使受阻仍保留完整结构但内容诚实标UNKNOWN。

|包|学习主题|阅读/完整性|
|---|---|---|
|[A_CER](knowledge/A_CER/README.md)|CER Estimating emissions and energy from solid waste and landfill biogas management guideline|TARGETED_SECTIONS_WITH_LOCAL_BYTES|
|[B_NGER](knowledge/B_NGER/README.md)|National Greenhouse and Energy Reporting (Measurement) Determination 2008; 2026 amendment and explanatory statement|TARGETED_SECTIONS_WITH_LOCAL_BYTES|
|[C_ACCU](knowledge/C_ACCU/README.md)|Carbon Credits (Carbon Farming Initiative—Reducing Methane Emissions from Landfill Gas) Methodology Determination 2025|TARGETED_SECTIONS_WITH_LOCAL_BYTES_AND_VISUAL_EQUATIONS|
|[D_NSW](knowledge/D_NSW/README.md)|Environmental Guidelines: Solid Waste Landfills|TARGETED_WEB_TEXT_ONLY_RAW_DOWNLOAD_BLOCKED|
|[E_FOGO](knowledge/E_FOGO/README.md)|Emissions impacts of food waste recovery technologies: composting and landfill fact sheets|P4523_TARGETED_WEB_TEXT_P4522_LIMITED_RAW_BLOCKED|
|[F_ORGANICS](knowledge/F_ORGANICS/README.md)|Environmental Guidelines: Composting and Related Organics Processing Facilities; 2026 consultation status|METADATA_ONLY_BODY_BLOCKED|
|[G_IPCC2006](knowledge/G_IPCC2006/README.md)|2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume5 Chapter3 Solid Waste Disposal|TARGETED_SECTIONS_WITH_LOCAL_BYTES|
|[H_IPCC2019](knowledge/H_IPCC2019/README.md)|2019 Refinement to the 2006 IPCC Guidelines, Volume5 Chapter3 Solid Waste Disposal|TARGETED_SECTIONS_WITH_LOCAL_BYTES|

## 可实际使用的本地检索入口

```powershell
rg -n "Qlost|500|DECom|DOCf|UNKNOWN" docs/tasks/climateos_au_landfill_methane_methods_001/knowledge
python docs/tasks/climateos_au_landfill_methane_methods_001/verify_package.py
```

更新时新增收据ID/不可变版本，追加UPDATE_LEDGER；保留旧版本，显式列受影响公式与练习，交独立评审后才改变阅读/科学状态。不要把无原件内容覆盖成已核实。正式接入须先确认canonical目录/schema/owner，随后仅添加引用，不再建另一套存储。该动作尚未完成，不是当前已实现能力。

[项目任务入口](README.md) ↔ 本索引 ↔ 各源笔记，所有链接由包验证器检查。长期学习从[中文学习路径](LEARNING_PATH_ZH.md)开始。
