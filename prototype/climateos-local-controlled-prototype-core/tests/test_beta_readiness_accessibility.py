from pathlib import Path


STATIC_DIR = Path(__file__).parents[1] / "static"


def test_alpha_workbench_has_semantic_human_test_controls():
    page = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    assert 'aria-label="Prototype sections"' in page
    assert 'role="note"' in page
    assert 'id="alpha-create-result"' in page and 'aria-live="polite"' in page
    assert 'id="alpha-review-result"' in page
    assert 'aria-label="Alpha Runtime skeleton JSON"' in page
    assert "readonly" in page
    assert page.count("<label>") >= 10


def test_accessibility_and_authority_meaning_is_not_colour_only():
    page = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    styles = (STATIC_DIR / "styles.css").read_text(encoding="utf-8")
    assert "Reviewer labels are locally declared labels, not verified identities" in page
    assert "cannot prove scientific truth" in page
    assert "No-conclusion rule" in page
    assert ".trial-grid" in styles
    assert "grid-template-columns: 1fr" in styles


def test_limited_beta_onboarding_and_readable_presentation_are_present():
    page = (STATIC_DIR / "index.html").read_text(encoding="utf-8")
    script = (STATIC_DIR / "app.js").read_text(encoding="utf-8")
    assert "Limited local Beta preparation" in page
    assert 'id="start"' in page
    assert "You remain responsible" in page
    assert "Technical JSON" in page
    assert "toLocaleString" in script
    assert "Not provided" in script
    assert "Declared actor" in script


def test_keyboard_focus_and_zoom_reflow_protection_remain_explicit():
    styles = (STATIC_DIR / "styles.css").read_text(encoding="utf-8")
    assert "outline: 3px solid" in styles
    assert "outline-offset: 2px" in styles
    assert ".onboarding-grid { grid-template-columns: 1fr; }" in styles
    assert "min-height: 44px" in styles
