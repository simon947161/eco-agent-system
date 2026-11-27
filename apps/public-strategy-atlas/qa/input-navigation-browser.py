"""Exercise the original route, nested content, governed inputs and reverse citations."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import os
from playwright.sync_api import expect, sync_playwright

app = Path(__file__).resolve().parents[1]
out = Path(os.environ.get('ATLAS_QA_OUT', '/tmp/atlas-input-navigation'))
out.mkdir(parents=True, exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(app)))
Thread(target=server.serve_forever, daemon=True).start()
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.getenv('ATLAS_CHROMIUM','/usr/bin/chromium'))
        for width, height in [(1440,900),(390,844)]:
            page = browser.new_page(viewport={'width': width, 'height': height}, reduced_motion='reduce')
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto('http://127.0.0.1:' + str(server.server_port))
            expect(page.locator('#startupNotice')).to_be_hidden(timeout=30000)
            page.locator('#atlasGraph [data-node-id="op"]').focus()
            page.keyboard.press('Enter')
            page.get_by_role('button', name='Explore inside', exact=True).click()
            page.get_by_role('button', name='Knowledge & work dossier', exact=True).click()
            page.get_by_label('Find a station record').fill('activity:service-requests')
            page.locator('#stationRecords button').click()
            page.get_by_role('button', name='Evidence inputs and citing records', exact=True).click()
            page.get_by_label('Filter by title, identity or link type').fill('EXPLICIT_DOCUMENT_REFERENCE')
            expect(page.locator('#inputResults button')).to_have_count(2)
            page.locator('#inputResults button').first.click()
            page.get_by_role('button', name='Evidence inputs and citing records', exact=True).click()
            page.locator('#inputQuery').fill('activity:service-requests')
            expect(page.locator('#inputResults button')).to_contain_text('USED_BY')
            page.screenshot(path=str(out / f'reverse-{width}.png'))
            page.locator('#inputResults button').click()
            expect(page.locator('#details')).to_contain_text('activity:service-requests')
            assert not errors, errors
            page.close()
        browser.close()
    print('PASS 1440x900 and 390x844 real keyboard station > nested content > dossier > two printed CSP references > reverse OP activity')
finally:
    server.shutdown()
    server.server_close()
