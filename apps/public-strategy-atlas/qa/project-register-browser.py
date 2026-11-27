"""Navigate two published environmental project rows and their exact CSP reference at both acceptance viewports."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import os
from threading import Thread
from playwright.sync_api import sync_playwright,expect

app=Path(__file__).resolve().parents[1]
out=Path(os.getenv('ATLAS_QA_OUT','/tmp/atlas-project-browser'));out.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):
        pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(app)))
Thread(target=server.serve_forever,daemon=True).start()
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=os.getenv('ATLAS_CHROMIUM','/usr/bin/chromium'))
        for width,height in [(390,844),(1440,900)]:
            page=browser.new_page(viewport={'width':width,'height':height},reduced_motion='reduce')
            errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto('http://127.0.0.1:'+str(server.server_port))
            expect(page.locator('#startupNotice')).to_be_hidden(timeout=30000)
            page.locator('[data-node-id="op"]').focus();page.keyboard.press('Enter')
            page.get_by_role('button',name='Browse OP project rows',exact=True).click()
            expect(page.locator('#registerStatus')).to_contain_text('117 named rows')
            page.locator('#tableSearch').fill('Murrumbidgee')
            page.locator('#registerRows button').filter(has_text='Aquatic weed control').click()
            expect(page.locator('#details')).to_contain_text('$20,000')
            expect(page.locator('#details')).to_contain_text('ANNUAL_PLAN')
            page.get_by_role('button',name='CSP 6.2',exact=True).click()
            page.get_by_role('button',name='Browse DP project rows',exact=True).click()
            expect(page.locator('#registerStatus')).to_contain_text('Printed CSP reference 6.2')
            page.locator('#registerRows button').filter(has_text='Aquatic weed control').click()
            expect(page.locator('#details')).to_contain_text('$60,000')
            expect(page.locator('#details')).to_contain_text('MULTIYEAR_PROGRAM')
            page.screenshot(path=str(out/f'register-{width}.png'))
            page.get_by_role('button',name='Open registered project').click()
            expect(page.locator('#details')).to_contain_text('PLAN_TABLE_ROW')
            page.get_by_role('button',name='Explore source content').click()
            page.get_by_role('button',name='Inspect original PDF pages').click()
            expect(page.locator('#pdfReading')).to_contain_text('PDF page 65 of 100',timeout=15000)
            page.get_by_role('button',name='Read project rows on this page').click()
            expect(page.locator('#registerRows')).to_contain_text('2 matching project rows')
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert not errors,errors
            page.close()
        browser.close()
    print('PASS actual OP project, printed CSP 6.2, DP project and independently scoped budgets, existing domain history, exact original page and bounded row list on 390/1440 Chromium')
finally:
    server.shutdown()
    server.server_close()
