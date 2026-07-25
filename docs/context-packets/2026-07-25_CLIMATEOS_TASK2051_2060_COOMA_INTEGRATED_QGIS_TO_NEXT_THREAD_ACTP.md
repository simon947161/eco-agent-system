# ClimateOS ACTP

## Task2051–2060 Cooma Integrated QGIS Experience → Next Thread

- Date: 2026-07-25
- Status: READY_FOR_NEXT_THREAD
- Repository: `simon947161/eco-agent-system`
- Authoritative base: `main@4ed5afc98d547acb1cddb688fdca53c9a5fc975e`
- Working branch: `agent/task2051-2060-qgis-cooma-integrated-experience`
- Draft PR: [#101](https://github.com/simon947161/eco-agent-system/pull/101)
- Pre-ACTP reviewed Head: `1ebfc7db6f43e8eb05157176022bf3fa4125e589`
- Founder review result: `FOUNDER_QGIS_INTEGRATED_EXPERIENCE_PASS`
- Merge authorization: NOT GRANTED
- Scientific or engineering conclusion: NOT CLAIMED

---

## 1. Purpose of this ACTP

This packet closes the 2026-07-25 working session after Founder completed the Windows QGIS visual review of the integrated Cooma spatial project.

The next thread must continue from PR #101 and must not fall back to the earlier Terrain-only or Hydrology-only gates.

The user explicitly ended today's work and requested an ACTP.

---

## 2. Authoritative completed foundation

Before Task2051–2060:

- PR #95, Cooma Terrain and Boundary Pack, was Founder-reviewed and merged.
- Terrain merge moved authoritative `main` to `fb69dfe5e77882faebe05766a6205183fe4e8bac`.
- PR #96, Cooma Hydrology Pack, was Founder-reviewed and merged.
- Hydrology merge moved authoritative `main` to `4ed5afc98d547acb1cddb688fdca53c9a5fc975e`.

Founder reviews already passed for:

- Terrain bookmarks;
- DEM Identify;
- slope Identify;
- DEM / hillshade / slope layer differentiation;
- major and secondary watercourse display;
- catchment and subcatchment display;
- three Hydrology bookmarks;
- watercourse and catchment Identify.

Those earlier packs are now authoritative inherited foundations, not open review gates.

---

## 3. Task2051–2060 product decision

Founder requested that previously separate spatial views be brought together into one QGIS project while preserving independent layer control.

The accepted product model is:

> One primary QGIS project, many independently switchable layers.

Primary generated project:

`runtime_data/qgis/cooma_spatial_foundation/project/Cooma_Spatial_Foundation_v0_4_integrated.qgz`

The integrated project contains, in one map project:

- official Cooma locality boundary;
- DEM;
- hillshade;
- slope degrees;
- major rivers and watercourses;
- secondary streams;
- catchment context;
- subcatchment context;
- named water features;
- bounded NSW official road vectors;
- NSW official online aerial / satellite-style imagery.

The layers remain separate and switchable. The design does not flatten all information into one physical data layer.

---

## 4. Data and runtime boundaries

### Local and offline-capable core

- accepted Terrain layers;
- accepted Hydrology layers;
- bounded NSW official RoadSegment vector data.

### Optional online layer

- NSW Spatial Services `NSWWebImagery`;
- viewport display only;
- no bulk imagery download;
- no imagery tiles committed to GitHub.

If the network is unavailable, the imagery layer may not display. Terrain, Hydrology, boundaries and locally retrieved roads remain available.

Runtime spatial data and generated QGIS project outputs remain governed by existing git-ignore and local-runtime policies.

---

## 5. Technical validation already recorded

PR #101 was created from exact accepted base:

`main@4ed5afc98d547acb1cddb688fdca53c9a5fc975e`

Before Founder review, recorded validation included:

- Python AST parsing: PASS;
- focused tests: PASS;
- GitHub Actions CCZPS-Lite: SUCCESS;
- branch comparison: ahead-only from the accepted base;
- official NSW source metadata checked;
- no automatic merge.

At ACTP preparation preflight:

- PR #101: `OPEN / DRAFT / MERGEABLE / NOT MERGED`;
- base: `main@4ed5afc98d547acb1cddb688fdca53c9a5fc975e`;
- reviewed branch Head before this ACTP commit: `1ebfc7db6f43e8eb05157176022bf3fa4125e589`;
- PR scope before this ACTP: 10 changed files, 1,245 additions, 0 deletions.

The next thread must re-fetch PR #101 and use the post-ACTP Head returned by GitHub. It must not assume the pre-ACTP Head remains current.

---

## 6. Founder Windows QGIS review result

Founder opened the integrated project on Windows QGIS and reported:

- the project opened successfully;
- all expected information was present in the same project;
- the integrated layer arrangement was visible and usable;
- the single-map experience was strongly preferred;
- Founder explicitly stated that the map was very good and should remain as it is for today.

Formal review result:

`FOUNDER_QGIS_INTEGRATED_EXPERIENCE_PASS`

This review closes the core user-experience requirement of Task2051–2060.

The product preference to preserve is:

> Cooma daily spatial work should use one integrated master project, with information controlled through separate layers, rather than requiring the Founder to move between several project files.

Older v0.2 Terrain and v0.3 Hydrology projects may remain for provenance and rollback, but v0.4 integrated is the intended daily entry point.

---

## 7. Explicit limits of the review

The Founder review does not establish:

- flood hazard or flood extent;
- water quality;
- drinking-water safety;
- wastewater capacity or performance;
- route safety;
- engineering suitability;
- planning approval;
- ecological condition;
- scientific performance;
- project risk conclusions.

The integrated project is a spatial evidence and exploration foundation only.

No new road, land-cover, vegetation, fire, wastewater or other spatial sprint is authorized by this ACTP.

---

## 8. Current Founder Gate

The following are now complete:

- Windows project generation and opening;
- integrated visual experience review;
- Founder acceptance of the one-project-many-layers experience.

The following is not yet authorized:

- merging PR #101.

Therefore the correct current gate is:

`FOUNDER_QGIS_INTEGRATED_EXPERIENCE_PASS / PR101_MERGE_AUTHORIZATION_REQUIRED / DO_NOT_AUTO_MERGE`

The next thread must not interpret this ACTP, the Founder review, or the end-of-day instruction as merge authorization.

---

## 9. Required next-thread preflight

The next thread should begin with read-only checks:

1. Fetch PR #101 and confirm it remains open and unmerged.
2. Confirm its base is still `main`.
3. Confirm authoritative `main` still inherits merge commit `4ed5afc98d547acb1cddb688fdca53c9a5fc975e`, unless a newer legitimate main commit is present.
4. Resolve and record the exact post-ACTP PR Head.
5. Confirm the PR includes this ACTP and no unexpected scope expansion.
6. Confirm the Founder review evidence is present.
7. Confirm current checks are successful or explain any new failure.
8. Do not merge until the Founder gives explicit PR #101 merge authorization.

Recommended next Founder decision phrase:

> 合并 PR #101

If authorized, perform a controlled merge with an expected-Head lock, then verify the new authoritative `main` Head.

After merge, define the next spatial sprint separately. Do not silently bundle it into the merge.

---

## 10. CRP Harvest Block

### 核心知识点

- QGIS 可以把 Terrain、Hydrology、Roads 与在线影像装入同一个主项目，同时保持图层独立。
- “所有信息在一张图上”是统一项目体验，不是把不同数据破坏性地合并成一个物理图层。
- 影像在线、核心分析图层本地化，是可用性、仓库体积与可追溯性之间的合适平衡。

### 想法点

- 将 v0.4 integrated 项目作为 Cooma 日常空间工作的主入口。
- 保留旧版本项目用于来源追溯和阶段回滚。
- 后续空间能力继续加入统一主项目，但必须保持分组、默认可读性与独立 Founder Gate。

### 愿望点

- Founder 希望打开一个项目就能看到全部已有空间信息。
- Founder 明确喜欢当前统一地图的整体体验，希望先保持现状。

### 推理点

- 多个独立项目增加切换成本并削弱跨层观察。
- 一个主项目加可切换图层，可同时满足综合观察和信息清晰度。
- 所有图层默认全开会造成视觉拥挤，因此“项目中存在”与“默认开启”应继续分开管理。

### 关键决策

- `FOUNDER_QGIS_INTEGRATED_EXPERIENCE_PASS`。
- 采用 `ONE_PROJECT_MANY_LAYERS` 作为 Cooma Spatial Foundation 的默认用户体验。
- 今日工作到此结束。
- PR #101 尚未获合并授权。

### 未解决问题

- PR #101 的受控合并决定。
- 合并后下一批空间任务的范围与优先级。
- 更高层环境结论仍需后续证据、方法和独立科学门控。

### 下一步行动

1. 下一线程只读 preflight PR #101。
2. 请求或接收 Founder 对 PR #101 的明确合并授权。
3. 若授权，受控合并并核验新 `main` Head。
4. 合并后再独立规划下一 Sprint。

### 项目关联关键词

`ClimateOS`, `QGIS`, `Cooma`, `Task2051-2060`, `PR101`, `Integrated Map`, `Terrain`, `Hydrology`, `RoadSegment`, `NSWWebImagery`, `Founder Gate`, `ACTP`
