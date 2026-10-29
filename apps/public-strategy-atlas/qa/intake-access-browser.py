"""Actual localhost UI regression. Imported evidence is labelled QA ONLY.
No network source intake, deployment, source admission or production writes.
"""
from pathlib import Path
import datetime, hashlib, json, subprocess, tempfile
from playwright.sync_api import sync_playwright, expect

APP = Path(__file__).resolve().parents[1]
OUT = APP / 'qa/system/intake-access-20261030'
OUT.mkdir(parents=True, exist_ok=True)
results = []

def tool(page, control):
    page.keyboard.press('Escape')
    if not page.locator('#toolsMenu').evaluate('(e) => e.open'):
        page.locator('#toolsMenu>summary').click()
    page.locator(control).click()

with tempfile.TemporaryDirectory(prefix='atlas-access-qa-') as tmp:
    subprocess.run(['node', str(APP/'qa/intake-access-fixture.cjs'), tmp], check=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        for width, height in [(1440, 900), (390, 844)]:
            context = browser.new_context(viewport={'width': width, 'height': height}, accept_downloads=True, reduced_motion='reduce')
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto('http://127.0.0.1:8877/')
            expect(page.locator('#contentCount')).to_have_text('127')
            for case, access, owner in [
                ('retrieved', 'AVAILABLE', 'SOURCE_RESEARCHER_AND_AUTHORISED_REVIEWER'),
                ('verified', 'AVAILABLE', 'SOURCE_RIGHTS_REVIEWER'),
                ('withdrawn', 'NOT_CHECKED', 'SOURCE_RESEARCHER_AND_AUTHORISED_REVIEWER'),
            ]:
                tool(page, '#importSnapshotBtn')
                page.locator('#snapshotFile').set_input_files(str(Path(tmp)/(case+'.json')))
                expect(page.locator('#applySnapshot')).to_be_enabled()
                page.locator('#applySnapshot').click()
                expect(page.locator('#snapshotMessage')).to_contain_text('explicitly loaded in memory')
                tool(page, '#coverageBtn')
                entry = page.locator('[data-source-record="qa-retrieval-only"]')
                card = entry.locator('..')
                expect(card).to_contain_text(access+' · '+owner)
                expect(card).not_to_contain_text('ENVIRONMENT_ADMIN')
                entry.click()
                details = page.locator('#details')
                expect(details).to_contain_text('QA ONLY: simulated retrieval')
                expect(details).to_contain_text('Access from retained evidence: '+access)
                expect(details).to_contain_text('No extracted source content registered')
                expect(details).not_to_contain_text('No source content retrieved')
                expect(details).to_contain_text('rights UNKNOWN')
                details.get_by_text('Historical access at registration', exact=True).click()
                expect(details).to_contain_text('BLOCKED_BY_PERMISSION')
                if case == 'verified':
                    expect(details).to_contain_text('Confirm permitted reuse before extracting')
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                assert page.locator('#inspector').evaluate('(e) => e.scrollWidth <= e.clientWidth')
                page.screenshot(path=str(OUT/f'{case}-{width}.png'))
                if case == 'verified':
                    (OUT/f'accessible-source-{width}.txt').write_text(details.aria_snapshot())
                results.append({'viewport': [width, height], 'case': case, 'status': 'PASS_TESTED_HERE', 'evidenceClass': 'QA_ONLY_SIMULATED_NO_OFFICIAL_RETRIEVAL'})
            # Export/import verification must retain correction history and base.
            page.keyboard.press('Escape')
            if not page.locator('#toolsMenu').evaluate('(e) => e.open'):
                page.locator('#toolsMenu>summary').click()
            with page.expect_download() as download:
                page.locator('#exportBtn').click()
            export = Path(tmp)/f'export-{width}.json'
            download.value.save_as(str(export))
            subprocess.run(['node', str(APP/'verify-snapshot.cjs'), str(export)], check=True)
            assert not errors, errors
            print(f'PASS: {width}x{height} replayed access, historical labels, rights ownership, withdrawn evidence and independent snapshot verification', flush=True)
            context.close()
        browser.close()

(OUT/'browser-results.json').write_text(json.dumps({'generatedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'results': results, 'testedFiles': {name: 'sha256:'+hashlib.sha256((APP/name).read_bytes()).hexdigest() for name in ['atlas-intake.js', 'atlas.js', 'qa/intake-access-fixture.cjs', 'qa/intake-access-browser.py']}, 'officialSourceCoverageAdded': 0, 'limits': 'Chromium viewport emulation; no physical device or professional screen-reader certification.'}, indent=2)+'\n')
