# QGIS Cooma 10-minute Restart Guide

For QGIS Desktop 3.44.11 and a returning GIS user. The project contains a
synthetic navigation point and rectangle, not real spatial evidence.

## Minute 0–1 — Open the project

Double-click `Cooma Spatial Foundation v0.1` under Recent Projects, or run:

```powershell
.\run_qgis_local_spatial_foundation.ps1 -Action Open
```

If QGIS asks whether to save the current Untitled Project:

- choose **Don't Save** if the current project is empty;
- do not choose **Cancel**, because Cancel stops the Cooma project from opening;
- choose **Save** only if you intentionally created work that must be preserved.

Three-step check:

1. Double-click `Cooma Spatial Foundation v0.1`.
2. Choose **Don't Save** for the empty Untitled Project.
3. Wait until the title bar shows `Cooma Spatial Foundation v0.1 — QGIS`.

## Minute 1–2 — Confirm the visible anchor

The canvas should show a green provisional rectangle and labelled centre point.
They are local learning aids. They are not a catchment, Council boundary,
scientific study boundary or evidence of Cooma conditions.

## Minute 2–4 — Expand groups and read INFO layers

Expand groups using the arrow. Double-clicking a layer group does not open data.

- `02_TERRAIN` contains `INFO — Terrain data not yet retrieved`; later it may
  contain an approved DEM, hillshade, slope and contours.
- `03_WATER` contains `INFO — Hydrology data not yet retrieved`; later it may
  contain approved rivers, streams, waterbodies and catchment boundaries.

No real terrain or hydrology data exists yet by design.

## Minute 4–6 — Activate two bookmarks

Open existing bookmarks through **View → Panels → Spatial Bookmarks**, or expand
**Browser → Spatial Bookmarks**. Then:

1. Find `Cooma Town`, `Wider Cooma Context`, `Terrain Overview`,
   `Main Waterways`, and `Catchment Context`.
2. Double-click one bookmark.
3. Confirm the canvas extent changes.
4. Repeat with a second bookmark and confirm a visibly different extent.

**View → New Spatial Bookmark** creates a new bookmark. It does not open the
existing bookmark list. All five entries are provisional navigation bookmarks;
`Main Waterways` does not mean waterways are currently displayed.

## Minute 6–8 — Pan, zoom, scale and coordinates

Use the hand tool to pan and the mouse wheel or Zoom tools to change scale. The
status bar shows scale and cursor coordinates. Return with `Cooma Town`.

## Minute 8–10 — Identify `NOT_EVIDENCE`

Select **Identify Features**, then click `Cooma Provisional Centre` or the
provisional rectangle. Read:

- `scientific_status: NOT_EVIDENCE`
- `scope_status: PROVISIONAL`
- `purpose: LEARNING_AND_NAVIGATION_ONLY`

Use layer **Properties → Information/Source** to confirm the source stays in the
controlled local `runtime_data/qgis/cooma_spatial_foundation/local_anchor/`
directory. Save new work under a new versioned filename; do not overwrite the
template.

## Interpretation boundary

What you may say:

> “The project shows a provisional learning location and navigation extent.”

What you may not say:

> “The project proves Cooma terrain, hydrology, climate risk or infrastructure conditions.”
