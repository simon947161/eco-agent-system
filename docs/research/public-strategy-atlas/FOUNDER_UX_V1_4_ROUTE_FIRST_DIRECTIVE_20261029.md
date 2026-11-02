# ClimateOS Public Strategy Atlas — Founder V1.4 Route-First UX Directive
**Date:** 2026-10-29 Australia/Sydney  
**Type:** Founder design correction + **implementation instruction**, not a research hold  
**Baseline verified when authored:** Draft PR #130, HEAD `a30755c09a03fa5b90deaab78873f3bd0d0e4dd1`; branch `feature/public-strategy-atlas-web-mvp-20261029`  
**Status:** IMPLEMENT ROUTE-FIRST EXPERIENCE / KEEP ALL EXISTING DATA, HASH, EDITING AND TESTS

## 1. Founder intent — correct the visual thesis

Founder rejects the current **traditional three-column administrative website** as the primary experience. The 2026-10-29 `qa/workspace-desktop.jpg` displays top-level controls, left menu, right editor, then a tiny chain of boxes in the central panel. Although the engine is advancing, the page does not clearly communicate how **ideas, modules, policies, decisions, actions and evidence connect as continuous routes**.

**The product is an interactive strategic ROUTE MAP, not a records dashboard.** The thing to understand at first sight is the **logic of the lines**: multiple origins, branching paths, convergences, diverging legal/regional applicability, time-dependent routes, and hidden candidate links that invite inspection. Every station can expand into an internal line network. Deep content is important but should not occupy the first visual plane.

This feedback supersedes V1.3's assumption that the existing topbar/sidebar/main/inspector is an acceptable long-term primary composition. **It does not supersede or undo any verified engineering work.**

## 2. New first-screen hierarchy

1. **PRIMARY (70–85% of available content viewport):** wide, immersive, full-bleed-ish `Route Map` canvas. Route lines dominate; stations are readable at normal zoom. Minimise permanent cards, tables and editors.
2. **SECONDARY (small persistent elements):** one compact floating header (Atlas / search / map modes), clear legend, evidence caution, zoom and focus/reset controls. No two rows of administrative buttons.
3. **CONTEXTUAL (only on selection):** a **slide-over / bottom sheet** for source, exact section, authority/revision/date/region, status, content tree, history, annotations, counterevidence. It overlays without shrinking the initial map to a thin middle column.
4. **UTILITY (explicit user action):** editing, workspace save/import/export, source admission, audit tooling and detailed table/list alternative remain available as discrete inspector modes. They must not be destroyed or displayed as the primary experience.
5. **Mobile:** naturally traversable horizontal/vertical route segments; pan/scroll, select a station, then a bottom sheet with full-size text. Never use 45% zoom to make all content illegible.

### Suggested schematic (semantic, not a claimed official route)
- **Strategic spine (teal):** CSP → Strategic objectives → DP → OP → Actions → KPI definitions → Evidence.
- **Planning spine (blue):** LSPS → Planning priorities → context-specific LEP/DCP/SEPP → geographic/effective scope.
- **Interchange nodes:** where evidence actually supports more than one typed relationship. A shared label is **not** an interchange proof.
- **Hidden candidate connections (amber dotted):** other-route hypotheses that must stay distinct from admitted or statutory links.
- **Local review/history (purple/grey annotation layer):** changes/version drift and contested records are overlays, not fictitious public authority.
- **Internal decomposition:** one station → sub-route → section → clause → action → indicator → evidence; return via breadcrumb/minimap, keep viewport and prior selection stable. This is an internal containment relationship, **not necessarily** the legal/planning chain.

## 3. Route geometry, meaning and visual language

- Routes are the **primary graphical entities**: readable continuous paths with smooth junctions and clear stops; curve length and spacing may vary organically. Station positioning for same dataset/layout settings must be stable and reproducible. No spontaneous jitter, no gratuitous physics animation.
- Type the edges (formal parent/implementation, jurisdictional applicability, content containment, research-inferred, hidden hypothesis, evidence support/counterevidence). Use line colors *for category*, dashes for uncertain/hypothetical and small markers for contested/retracted. No unsupported cross-path transitivity.
- **Growth** uses a separate semantic visual channel over a neutral route baseline: (a) scoped evidence review coverage, (b) elapsed period, or (c) actual KPI with comparable public result/target/units. These cannot be combined; no real KPI means UNKNOWN grey. Current fixture progress percentages must retain conspicuous SYNTHETIC DEMO labels.
- **Hash/receipt verification** belongs to the contextual audit layer and station detail, never represented as completed Council work. A local digest is not an external witness or official signature.
- Screen variants: 16:9 laptop, 21:9 ultrawide, 32:9 multi-view, ~390px phone. Dual-monitor sidecar is optional, **not** a prerequisite for first release.
- At >60/200 nodes use progressive disclosure/semantic zoom/route grouping, focus one corridor plus nearest connections, a minimap and bounded hidden candidates; no spaghetti graph.
- Natural navigation verbs: **Follow route**, **Explore branch**, **Compare paths**, **Find a crossing**, **Trace back to source**, **Show changes over time**, **Challenge this connection**. Put raw CRUD controls behind utility mode.
- Preserve accessible keyboard focus order, labels for routes and stations, reduced motion, high-contrast, non-colour-only legend, responsive scroll/pan. Map must have a usable linear/text alternative, not just an inaccessible SVG.
- Avoid resembling a fictional metro map that implies official endorsement: mark synthetic lines/stations clearly and distinguish external actual source observations.

## 4. Implement now — NO new study gate

**U1: deliver a working route-map slice to PR #130**
- Use the existing `AtlasData`, `AtlasModel`, source admission and `AtlasWorkspace` modules; no duplicate dataset, no fake official clauses.
- Make `Route Map` the default first view when Atlas loads. Existing `Relationships`/recursive `Inside content` and editing modes remain reachable.
- Compose at least **two spatially distinct continuous routes and one opt-in hypothesis/cross-line** on the existing 15-node synthetic fixture. Use SVG (or similarly accessible vector DOM) with deterministic station/edge mapping and actual graph edge IDs. Avoid purely decorative lines that are not backed by the model.
- Clicking a station must reveal a contextual overlay, with **Follow route** / **Explore inside** entry to the existing recursive content explorer. Support source inspector, hash receipt, local annotation, reverse trace. Keep original source status and pending-review gates unchanged.
- Clicking a connection must show its **typed assertion**, source/counterevidence and direct vs inferred/unknown status. Cross-line candidate selection remains `HYPOTHESIS_ONLY` and can be dismissed.
- Make the opening experience visually different from the previous dashboard: linework occupies most of the screen; a compact command bar, legend and optional inspector sheet. Restore state on closing the overlay.
- Introduce compact visual tutorial/onboarding no more than 2 steps; optional clear sample route; avoid covering the drawing with explanation paragraphs.
- Add a **route-first screenshot** at laptop 1440x900 and mobile 390px. Do actual Chrome click/keyboard checks for node/edge, focus, scroll, candidate and inspector.

**U2: evidence/history map overlays**
- Highlight source ancestry, revision-time deltas, conflicts and withdrawn links using existing verification records; if status is unknown, mark UNKNOWN not success. Parent/child content roots have child-linked hashes but are not external signatures.
- Show the CSP 6.1 observation/review gate as pending and clearly distinct from fictional strategic relationships.
- Preserve revision editing, compare, export/import, two-tab conflict tests and serverless local operation.

**U3: progressive route scalability**
- Test density 15/60/200 with legibility at normal zoom and focus+grouping, not just DOM count or single-digit model calculation.
- Keep geometry stability across expansion, pan/zoom and preview/update. Explicitly label aggregation, unverified paths, and offscreen continuation.

## 5. Evidence / acceptance matrix

**Requires actual implementation, not another concept PDF:**
- At 1440×900, primary opening viewport is route-dominant (target ≥70% map presentation area) and no full-height left/right administrative panels occupy the map by default.
- Two distinct traversable colour-coded lines, one explicit candidate connector; route/stop labels readable, no fake "official" line.
- At least 3 path demonstrations: CSP→DP→OP (synthetic), LSPS→LEP/DCP scope (synthetic), one rejected/unknown cross-route hypothesis; selection yields existing real underlying assertion IDs.
- Switch station → recursive six-level content and back without losing meaningful map context. Real CSP 6.1 public observation may be opened but cannot be promoted to legal mapping.
- Annotations/revision diff/audit/export/import remain operational; include regression tests for each, not just screenshots.
- A text/list route description exists for keyboard/screen readers. 390px interaction has no broken overlays or inescapable focus.
- Synthetic review percentage and elapsed time visibly distinct; actual KPI continues UNKNOWN. No unsupported signatures or Council approvals.
- No external dependencies, new procurement, Council nonpublic content, site deployment, or merge. Run existing tests then capture screenshots in actual browser; state exactly which were executed.

## 6. Continuity contract

- Start from latest remote PR #130 HEAD, **not hardcoded a30755c if advanced**.
- This document is the Founder-approved UI direction for next implementation. Do not reopen O1/O2 option debate and do not rewrite V1.2/V1.3 research.
- Update `apps/public-strategy-atlas/NEXT_SESSION.md` **after route-first implementation** to record U1/U2/U3 actual PASS/PARTIAL and remaining limits.
- Commit+push in small verified stages, re-read remote HEAD; one writer at a time, avoid collision with other Work/Codex sessions.
- Keep PR #130 OPEN/DRAFT; do not modify main, PR #129, Council systems, earlier private Sites, or create a second standalone official graph.
- If the source admission still lacks reuse/legal scope/reviewer, keep PENDING; route redesign should **not** be blocked by that separate validation gap.

## 7. Exact Codex / Work execution order

> Continue Atlas PR #130 from latest HEAD; read `NEXT_SESSION.md` and this V1.4 route-first directive. Founder now requires a **visually route-dominant website**, not a three-column dashboard. **Implement U1 in actual source code** using existing nodes/assertions, with full map viewport, integrated stations, typed crossing/candidate lines, drilldown into the existing 127 items, unobtrusive contextual evidence/history/editing panel, and human-readable keyboard route alternative. Preserve CSP 6.1 pending admission, local immutable workspace, import/export, snapshot verification, previous tests and privacy gates. Then continue U2/U3 as possible. Browser-test screenshots, run Node regression, commit/push PR #130 and update NEXT_SESSION. Do not stop after a design document; do not deploy or merge.
