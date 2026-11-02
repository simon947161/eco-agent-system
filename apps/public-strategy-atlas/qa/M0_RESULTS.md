# M0 real-browser QA — 2026-10-29
Baseline: baaedfaf315e6554a84b26e01743e3952302fc1f. Edge via browser connector, localhost:8878, desktop viewport 1069px; 390px responsive iframe (real rendering, not a physical phone).

PASS: actual HTML/CSS/JS loaded; node click opens SYNTHETIC drawer; water → upstream OP; OP drawer exposes downstream water/KPI; Enter activates CSP and retains data-node-id=csp focus after redraw; candidate toggle shows HYPOTHESIS and missing official source, hiding clears selected candidate drawer; KPI mode has zero colour paths and explicit UNKNOWN; time mode states not completion; coverage states demonstration only; 14 visible nodes without candidate. Captured console warnings/errors: []. Unequal Bézier spans inspected from rendered DOM. Desktop document overflow=false. Responsive search visible and water selection/drawer confirmed through browser accessibility tree.

Fixed: stale candidate/root drawer; keyboard focus loss during redraw; ambiguous upstream/downstream buttons; mobile search hidden; tiny scaled SVG text (fixed readable canvas with horizontal scroll); close/Escape control and touch target sizing.

Screenshots: m0-desktop.png and m0-mobile-390.png are actual browser viewport captures, not mocks. Full-page capture timed out; viewport capture succeeded. Mobile evidence is a 390px iframe, not touch-device certification. Browser translation extension overlays visible in screenshots are not application UI.

NOT_TESTED: physical mobile/touch, Safari/Firefox, screen reader, 60/200 nodes, dual-screen, full WCAG, remote official page availability. Official links are directory references, never admitted clause evidence. Branch expansion currently means adjacent navigation/highlight, not dynamic node generation. M0 bounded smoke passes; these limits remain for M2.
