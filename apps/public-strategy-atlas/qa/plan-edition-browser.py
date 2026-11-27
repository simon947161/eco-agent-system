"""Real route-first acceptance of the November plan editions and portable export."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from pathlib import Path
import os
import subprocess
import tempfile
from playwright.sync_api import sync_playwright, expect

app=Path(__file__).resolve().parents[1]
out=Path(os.environ.get('ATLAS_QA_OUT','/tmp/atlas-plan-browser'))
out.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):
        pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(app)))
Thread(target=server.serve_forever,daemon=True).start()
try:
    with sync_playwright() as pw, tempfile.TemporaryDirectory() as tmp:
        browser=pw.chromium.launch(executable_path=os.getenv('ATLAS_CHROMIUM','/usr/bin/chromium'))
        for width,height,family,pdf in [(1440,900,'dp',61),(390,844,'op',68)]:
            page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
            errors=[]
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto('http://127.0.0.1:'+str(server.server_port))
            expect(page.locator('#startupNotice')).to_be_hidden(timeout=30000)
            page.locator('[data-node-id="'+family+'"]').focus()
            page.keyboard.press('Enter')
            page.get_by_role('button',name='Compare published water plans',exact=True).click()
            result=page.locator('#planComparison')
            expect(result).to_contain_text('SUPPORTED_RESEARCH_CANDIDATE')
            expect(result).to_contain_text('ANNUAL_PLAN')
            expect(result).to_contain_text('MULTIYEAR_PROGRAM')
            expect(result).to_contain_text('UNKNOWN')
            page.screenshot(path=str(out / f'comparison-{width}.png'))
            with page.expect_download() as comparison_download:
                result.get_by_role('button',name='Export comparison receipt').click()
            proof=Path(tmp)/f'comparison-{width}.json'
            comparison_download.value.save_as(str(proof))
            page.locator('#projectLocality').fill('Cooma')
            page.get_by_role('button',name='Check project evidence').click()
            expect(result).to_contain_text('REJECTED_CANDIDATE')
            page.get_by_role('button',name='Back to station',exact=True).click()
            page.get_by_role('button',name='Knowledge & work dossier',exact=True).click()
            page.locator('#stationRecordQuery').fill('november:nimmitabel-water:budget')
            page.locator('#stationRecords button').click()
            expect(page.locator('#details')).to_contain_text('150000')
            expect(page.locator('#details')).to_contain_text('PDF '+str(pdf))
            expect(page.locator('#details')).to_contain_text('NO_ADDITION_ACROSS_PLAN_LEVELS')
            page.get_by_role('button',name='Evidence inputs and citing records',exact=True).click()
            page.locator('#inputQuery').fill('SOURCE_EDITION')
            page.locator('#inputResults button').click()
            expect(page.locator('#details')).to_contain_text('RAW_BYTES_VERIFIED')
            page.get_by_role('button',name='Earlier edition',exact=False).click()
            expect(page.locator('#details')).to_contain_text('Later recorded edition')
            page.screenshot(path=str(out / f'editions-{width}.png'))
            if width==1440:
                page.keyboard.press('Escape')
                page.locator('#toolsMenu > summary').click()
                with page.expect_download() as download:
                    page.locator('#exportBtn').click()
                target=Path(tmp)/'snapshot.json'
                download.value.save_as(str(target))
                checkpoint='sha256:303ed78563c2139756c367b87c457dd198baebc1274a95aa6a64dca4f260d634'
                subprocess.run(['node',str(app/'verify-snapshot.cjs'),str(target),checkpoint],check=True)
                subprocess.run(['node',str(app/'verify-plan-comparison.cjs'),str(target),str(proof),checkpoint],check=True)
            assert not errors,errors
            page.close()
        browser.close()
    print('PASS desktop DP and mobile OP, published fiscal bases, old edition traversal and independent browser snapshot verification')
finally:
    server.shutdown()
    server.server_close()
