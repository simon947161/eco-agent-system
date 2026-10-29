"""E0 native Chromium regression. Run with the Atlas served at 127.0.0.1:8877.
Requires the existing engineering Playwright/Chromium runtime; no app dependency.
Downloads and source bytes are kept in /tmp, screenshots are public/synthetic only.
"""
from pathlib import Path
import json
import subprocess
from playwright.sync_api import sync_playwright, expect

APP = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / 'e0'
OUT.mkdir(exist_ok=True)
TEMP = Path('/tmp/atlas-e0')
TEMP.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:8877/'
results = []

def passed(name):
    results.append({'check': name, 'status': 'PASS_TESTED_HERE'})
    print('PASS:', name, flush=True)

def tool(page, ident):
    page.locator('#toolsMenu > summary').click()
    page.locator('#'+ident).click()

def station(page, ident):
    page.locator('#atlasGraph [data-node-id="'+ident+'"]').focus()
    page.keyboard.press('Enter')
    expect(page.locator('#inspector')).to_be_visible()

def check_no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    assert page.locator('#inspector').evaluate('(e)=>e.scrollWidth <= e.clientWidth')

def accounting_in_view(page):
    page.wait_for_function("""() => {
      const section=document.querySelector('#accountingFlow').getBoundingClientRect();
      const header=document.querySelector('.sheet-heading').getBoundingClientRect();
      return section.top >= header.bottom && section.top < innerHeight - 100;
    }""")

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    context = browser.new_context(viewport={'width':1440,'height':900}, reduced_motion='reduce', accept_downloads=True)
    page = context.new_page()
    errors=[]
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(BASE)
    expect(page.locator('#contentCount')).to_have_text('127')
    expect(page.locator('#inspector')).to_be_hidden()
    digest = page.evaluate('AtlasModel.objectDigest(AtlasData)')
    assert digest == 'sha256:13e765c81f1340918322b1e985da85f2362da3c72e1997804f952865edf365d2'
    passed('Original 127-item base digest preserved')
    page.screenshot(path=str(OUT/'desktop-map.png'))
    for ident, value in [('csp6','29.9 t_CO2e/person'),('water','2000 AUD/ML'),('area','50 ha')]:
        station(page, ident)
        page.get_by_role('button',name='Quantities & budget',exact=True).click()
        accounting_in_view(page)
        expect(page.locator('#accountingFlow')).to_contain_text(value)
        expect(page.locator('#accountingFlow')).to_contain_text('UNKNOWN')
        if ident == 'csp6': expect(page.locator('#accountingFlow')).to_contain_text('PUBLIC_TEXT_OBSERVED')
        else: expect(page.locator('#accountingFlow')).to_contain_text('SYNTHETIC')
        check_no_overflow(page)
        page.screenshot(path=str(OUT/('desktop-'+ident+'.png')))
        page.keyboard.press('Escape')
        expect(page.locator('#inspector')).to_be_hidden()
        assert page.locator('[data-node-id="'+ident+'"]').evaluate('(e)=>e===document.activeElement')
    passed('Desktop csp6/water/area accounting shortcuts, units, explicit unknowns, keyboard return, overflow')
    with page.expect_download() as download_info:
        tool(page,'exportBtn')
    snapshot = TEMP/'snapshot.json'
    download_info.value.save_as(str(snapshot))
    subprocess.run(['node',str(APP/'verify-snapshot.cjs'),str(snapshot),page.evaluate('AtlasModel.migrateDataset(AtlasData,AtlasAccounting.cases).then(d=>AtlasModel.objectDigest(d))')],check=True)
    passed('Browser-exported base snapshot independently verified against frozen checkpoint')
    page.locator('#toolsMenu > summary').click() if page.locator('#toolsMenu').get_attribute('open') is not None else None
    station(page,'csp6')
    page.get_by_role('button',name='Explore inside',exact=True).click()
    expect(page.locator('#editLocalContent')).to_be_visible()
    page.locator('#editLocalContent').click()
    page.locator('#editTitle').fill('E0 synthetic local review')
    page.locator('#editText').fill('Synthetic local annotation for E0 regression; no Council data.')
    page.locator('#editReason').fill('Verify prior immutable workspace compatibility')
    page.locator('#previewDiff').click()
    expect(page.locator('#revisionDiff')).to_contain_text('E0 synthetic local review')
    page.locator('#commitRevision').click()
    expect(page.locator('#workspaceMessage')).to_contain_text('Revision appended')
    tool(page,'workspaceBtn')
    page.locator('#saveWorkspace').click()
    expect(page.locator('#workspaceMessage')).to_contain_text('Saved locally')
    other=context.new_page()
    other.goto(BASE)
    tool(other,'workspaceBtn')
    other.locator('#loadWorkspace').click()
    expect(other.locator('#workspaceMessage')).to_contain_text('Loaded and verified 1')
    page.keyboard.press('Escape')
    tool(page,'textRoutesBtn')
    page.locator('[data-linear-node]').first.click()
    page.locator('#editLocalContent').click()
    page.locator('#editText').fill('Second synthetic annotation for stale-writer regression.')
    page.locator('#editReason').fill('Advance first tab')
    page.locator('#commitRevision').click()
    expect(page.locator('#workspaceMessage')).to_contain_text('Revision appended')
    tool(page,'workspaceBtn')
    page.locator('#saveWorkspace').click()
    expect(page.locator('#workspaceMessage')).to_contain_text('Saved locally')
    other.locator('#saveWorkspace').click()
    expect(other.locator('#workspaceMessage')).to_contain_text('CONFLICT')
    with page.expect_download() as download_info:
        page.locator('#exportWorkspace').click()
    workspace=TEMP/'workspace.json'
    download_info.value.save_as(str(workspace))
    subprocess.run(['node',str(APP/'verify-workspace.cjs'),str(workspace)],check=True)
    passed('Real local edit/diff/save/load, two-tab stale-save rejection and exported workspace verification')
    assert not errors, errors
    passed('Desktop browser no unhandled script errors')
    context.close()
    for width,height in [(390,844),(2560,1080)]:
        context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
        page=context.new_page()
        page.on('pageerror',lambda e: errors.append(str(e)))
        page.goto(BASE)
        page.screenshot(path=str(OUT/(str(width)+'-map.png')))
        for ident in ['csp6','water','area']:
            station(page,ident)
            page.get_by_role('button',name='Quantities & budget',exact=True).click()
            accounting_in_view(page)
            expect(page.locator('#accountingFlow')).to_be_visible()
            check_no_overflow(page)
            if width==390:
                assert page.locator('#inspector').get_attribute('aria-modal')=='true'
                page.locator('#closeDetails').focus()
                page.keyboard.press('Shift+Tab')
                assert page.locator('#inspector').evaluate('(e)=>e.contains(document.activeElement)')
                page.screenshot(path=str(OUT/('mobile-'+ident+'.png')))
            page.keyboard.press('Escape')
            expect(page.locator('#inspector')).to_be_hidden()
        passed(f'{width}x{height} actual Chromium accounting panels and no horizontal document/panel overflow')
        context.close()
    assert not errors,errors
    browser.close()
(OUT/'browser-results.json').write_text(json.dumps({'browser':'system Chromium via Python Playwright','results':results,'scriptErrors':errors},indent=2)+'\n')
