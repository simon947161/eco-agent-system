# ClimateOS ACTP

## Task2051–2060 Cooma Integrated QGIS Post-Merge → Task2061+ Decision Gate

- Date: 2026-07-26
- Status: READY_FOR_NEXT_THREAD
- Repository: `simon947161/eco-agent-system`
- Authoritative branch: `main`
- Authoritative main HEAD: `2c41a8a95deb166f64f18252c28185cd3624a28c`
- Closed PR: [#101](https://github.com/simon947161/eco-agent-system/pull/101)
- Accepted PR Head: `75f9e79e4c13d10944444e26250e88ad02371cf4`
- Founder gate: `FOUNDER_QGIS_INTEGRATED_EXPERIENCE_PASS`
- Windows gate: `WINDOWS_INTEGRATED_VERIFY_PASS`
- Product direction: `ONE_PROJECT_MANY_LAYERS`
- Task2061+ authorization: NOT GRANTED
- Scientific, engineering, ecological or planning conclusion: NOT CLAIMED

---

## 1. Purpose

This packet supersedes the pre-merge handoff for Task2051–2060.

It records the controlled merge of PR #101, establishes the new authoritative ClimateOS main baseline, preserves the verified Windows/QGIS evidence, and transfers the project to a separate Task2061+ decision gate.

The next thread must not reopen the already completed Terrain, Hydrology or integrated-project Founder reviews unless new contradictory evidence appears.

---

## 2. Authoritative merge chain

The accepted Cooma QGIS foundation was built through three controlled stages:

1. PR #95 — Task2031–2040 Cooma Terrain and Boundary Pack.
   - Founder reviewed.
   - Merged.
   - Resulting main: `fb69dfe5e77882faebe05766a6205183fe4e8bac`.

2. PR #96 — Task2041–2050 Cooma Hydrology Pack.
   - Founder reviewed.
   - Accepted Head: `bc66e7f0d52e7b63a7f40627eb899ad3df5df6f2`.
   - Merged.
   - Resulting main: `4ed5afc98d547acb1cddb688fdca53c9a5fc975e`.

3. PR #101 — Task2051–2060 Cooma Integrated QGIS Experience.
   - Base: accepted `main@4ed5afc98d547acb1cddb688fdca53c9a5fc975e`.
   - Accepted Head: `75f9e79e4c13d10944444e26250e88ad02371cf4`.
   - Founder explicitly authorized merge.
   - Controlled merge completed.
   - Merge commit and current authoritative main:
     `2c41a8a95deb166f64f18252c28185cd3624a28c`.

PR #101 is now `CLOSED / MERGED / NOT DRAFT`. It is no longer an open merge gate.

---

## 3. Completed product outcome

The daily Cooma spatial entry point is:

`runtime_data/qgis/cooma_spatial_foundation/project/Cooma_Spatial_Foundation_v0_4_integrated.qgz`

It brings the existing spatial information into one QGIS project while retaining independent layer control.

Included project content:

- official Cooma locality boundary;
- DEM;
- hillshade;
- slope degrees;
- major rivers and watercourses;
- secondary streams;
- catchment context;
- subcatchment context;
- named water features;
- bounded NSW official RoadSegment vectors;
- NSW official online aerial imagery.

The data was not flattened into one physical layer. The accepted mental model is:

> One project, many independently switchable layers.

Default display and project membership remain separate concepts. Not every analytical layer should be enabled at startup.

---

## 4. Data and runtime boundaries

### Offline-capable core

- Terrain;
- Hydrology;
- Cooma boundary;
- bounded official NSW RoadSegment vectors.

### Online optional layer

- NSW Spatial Services `NSWWebImagery`;
- exact allowlisted tile service;
- viewport use only;
- no bulk imagery download;
- no imagery tiles committed to GitHub.

If the network is unavailable, imagery may not display. The local core remains usable.

Generated QGZ files, downloaded data, derived spatial data and runtime manifests remain local runtime artifacts governed by repository ignore rules.

---

## 5. Founder review evidence

Founder opened the v0.4 project in Windows QGIS 3.44.11 and confirmed:

- the project opened normally;
- the expected information was available in the same project;
- the integrated layer arrangement was usable;
- roads and imagery worked with the inherited Terrain and Hydrology content;
- the unified map was strongly preferred;
- the current map experience was considered very good.

Formal result:

`FOUNDER_QGIS_INTEGRATED_EXPERIENCE_PASS`

Accepted product preference:

`ONE_PROJECT_MANY_LAYERS`

Future Cooma spatial work should extend this master-project model rather than forcing routine switching among separate Terrain, Hydrology, Roads and Imagery projects.

Older staged projects may remain for provenance and rollback.

---

## 6. Windows technical verification

The first Windows `-Action Verify` exposed an over-strict imagery validation rule.

### Narrow repair

The guard was changed from raw XML text counting to semantic datasource validation:

- parse QGS XML;
- inspect `<datasource>` elements;
- require exactly one imagery datasource;
- require `type=xyz`;
- require the exact allowlisted NSWWebImagery service;
- retain the QGIS API network-layer checks;
- add regression coverage.

### Checksum recovery

After the code repair, the existing local QGZ failed its checksum comparison because it had been opened or rewritten after the generation manifest was created.

The bounded recovery was:

1. close QGIS;
2. move the prior integrated QGZ and project manifest into a recoverable backup;
3. rebuild the project only;
4. run `Verify` before reopening QGIS;
5. reopen through the normal launcher.

### Final Windows evidence

Founder screenshots confirmed:

- `"status": "PASS"`;
- project checksum:
  `e142e83b32e1659f8f9d711372fbb2e9624e0eab7025a45dd2504843afd1fb41`;
- `broken_layer_count: 0`;
- `network_layer_count: 1`;
- offline core: Terrain, Hydrology and Roads;
- online optional: NSWWebImagery;
- scientific conclusion: `NONE`;
- subsequent `-Action Open` succeeded;
- the integrated map still displayed normally.

Formal result:

`WINDOWS_INTEGRATED_VERIFY_PASS`

Operational caution:

> A QGZ binary checksum is a build-artifact check. Opening and saving the project can rewrite the archive even if the visible map is unchanged. When a clean checksum gate is required, rebuild and run Verify before opening or saving the project.

---

## 7. Validation and merge closure

Before merge:

- focused automated tests passed;
- imagery-source regression coverage passed;
- final GitHub Actions run passed;
- Founder visual review passed;
- Windows integrated Verify passed;
- accepted branch was ahead-only from the authorized main base;
- explicit Founder merge authorization was received.

Because PR #101 was still Draft, the controlled merge sequence was:

1. recheck exact expected Head;
2. confirm evidence and checks;
3. convert Draft to Ready as the required mechanical state transition;
4. merge using the expected Head lock;
5. verify the resulting merge commit and main HEAD.

No content drift was observed.

Current gate:

`TASK2051_2060_CLOSED / PR101_MERGED / MAIN_2C41A8A9 / FOUNDER_QGIS_INTEGRATED_EXPERIENCE_PASS / WINDOWS_INTEGRATED_VERIFY_PASS / ONE_PROJECT_MANY_LAYERS`

---

## 8. Explicit non-claims

This completed spatial foundation does not establish:

- flood hazard or flood extent;
- flood probability;
- water quality;
- drinking-water safety;
- wastewater capacity or performance;
- road or evacuation safety;
- engineering suitability;
- planning approval or compliance;
- ecological condition;
- bushfire risk;
- climate attribution;
- current or future environmental conclusions.

The project is a spatial evidence, orientation and exploration foundation.

It is now better equipped to support later analysis, but the presence of layers does not itself answer the Founder’s broader question: “What is Cooma’s environmental conclusion?”

---

## 9. Task2061+ decision boundary

Task2061+ has not been authorized.

No new sprint may be inferred from:

- PR #101 being merged;
- Founder liking the integrated map;
- Windows verification passing;
- this ACTP;
- the presence of roads or imagery.

The next thread should first decide what outcome is needed next.

Recommended planning direction:

### Preferred next stage

Define a bounded Cooma Spatial Foundation phase-closure and evidence-gap brief before adding more layers.

The brief should:

1. inventory what the integrated project can currently show;
2. identify which environmental questions remain impossible to answer;
3. rank the minimum next evidence needed for:
   - snow and climate context;
   - bushfire context;
   - drinking-water context;
   - wastewater resilience context;
4. separate display layers from analytical evidence;
5. propose a small Task2061–2070 scope;
6. return a Founder authorization gate before implementation.

This is a planning recommendation, not authorization to execute Task2061–2070.

Avoid adding Land Cover, Vegetation, Fire, Wastewater, Cadastre or other layers simply because they are available. Every addition should answer a named decision or evidence gap and preserve the integrated-master-project experience.

---

## 10. Required next-thread preflight

The next thread must begin with read-only checks:

1. Fetch `main` and record its current exact HEAD.
2. Confirm `main` contains merge commit
   `2c41a8a95deb166f64f18252c28185cd3624a28c`.
3. Confirm PR #101 remains merged.
4. Confirm the accepted PR Head was
   `75f9e79e4c13d10944444e26250e88ad02371cf4`.
5. Confirm PR #95 and PR #96 remain merged foundations.
6. Read this post-merge ACTP and the Task2051–2060 task documents.
7. Do not return to PR #101 as an open gate.
8. Do not modify or merge unrelated PRs.
9. Do not start Task2061+ without a separately stated Founder authorization.
10. Present a bounded recommended next scope and explain how it moves toward usable Cooma environmental understanding.

If the authoritative main has legitimately advanced, record the new Head and prove that it inherits `2c41a8a95…`; do not force the repository back to the ACTP Head.

---

## 11. Paste-ready next-thread instruction

> 请读取 `docs/context-packets/2026-07-26_CLIMATEOS_TASK2051_2060_POST_MERGE_TO_TASK2061_DECISION_ACTP.md`。先做只读 preflight：核验 PR #101 已合并、受控 Head `75f9e79e…`、合并提交及权威 main `2c41a8a95…`，并确认 PR #95/#96 的 Terrain 与 Hydrology 基础仍被继承。不得把 PR #101 当成开放 Gate，不得自动启动 Task2061+。请先给出 Task2061–2070 的有限候选范围，重点说明下一步怎样从“综合地图”走向可审计的 Cooma 环境证据与结论，但不能提前声称洪水、水质、工程、生态或规划结论。

---

## 12. CRP Harvest Block

### 核心知识点

- Cooma Terrain、Hydrology、Roads 与在线影像已进入同一个权威 QGIS 主项目。
- v0.4 integrated 已通过 Founder 体验复核和 Windows 自动验证。
- 地图集成完成不等于环境分析完成。
- QGZ checksum 是生成物一致性门；打开并保存可能改变二进制归档。

### 想法点

- 把 v0.4 integrated 作为 Cooma 日常空间主入口。
- 后续能力继续进入同一主项目，但必须分组、独立开关和保持默认可读。
- 下一步先做证据缺口与问题—图层映射，再决定新增数据。

### 愿望点

- Founder 希望打开一个项目即可查看已有空间信息。
- Founder 希望最终通过 ClimateOS 获得可理解、可审计的 Cooma 环境认识与结论。
- 使用体验应继续减少文件切换和人工运维负担。

### 推理点

- 一个主项目能降低跨项目切换成本，并支持跨层观察。
- 图层越多不自动意味着证据越强；没有问题定义、来源合同和分析方法时，只会增加视觉噪声。
- 因此 Task2061+ 应从“需要回答什么”倒推“还缺什么”，而不是继续无边界堆图层。

### 关键决策

- `FOUNDER_QGIS_INTEGRATED_EXPERIENCE_PASS`。
- `WINDOWS_INTEGRATED_VERIFY_PASS`。
- PR #101 已受控合并。
- 权威 main 为 `2c41a8a95deb166f64f18252c28185cd3624a28c`。
- `ONE_PROJECT_MANY_LAYERS` 成为默认产品方向。
- Task2061+ 保持独立 Founder Gate。

### 未解决问题

- Task2061–2070 的具体目标和授权范围。
- 从空间展示走向环境证据链的最小下一步。
- Cooma 雪、火、饮用水和污水四个主题的优先级与最低证据要求。
- 哪些结论可以先做描述性基线，哪些必须等待模型、时间序列或官方审查。

### 下一步行动

1. 新线程执行 post-merge read-only preflight。
2. 编制 Task2061–2070 有限候选任务书。
3. 建立“环境问题—所需证据—现有能力—缺口—门控”的映射。
4. 向 Founder 返回独立授权请求。
5. 获授权前不新增数据、不建新 PR、不作环境结论。

### 项目关联关键词

`ClimateOS`, `Cooma`, `QGIS`, `Task2051-2060`, `Task2061+`, `PR101`, `Terrain`, `Hydrology`, `RoadSegment`, `NSWWebImagery`, `ONE_PROJECT_MANY_LAYERS`, `Evidence Gap`, `Founder Gate`, `ACTP`
