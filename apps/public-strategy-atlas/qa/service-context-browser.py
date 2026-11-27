"""Navigate actual service evidence and a nested source branch at both acceptance viewports."""
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import os
from threading import Thread
from playwright.sync_api import sync_playwright,expect

app=Path(__file__).resolve().parents[1]
out=Path(os.getenv('ATLAS_QA_OUT','/tmp/atlas-service-browser'));out.mkdir(parents=True,exist_ok=True)
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
            page.locator('[data-node-id="water"]').focus();page.keyboard.press('Enter')
            page.get_by_role('button',name='Compare published water plans').click()
            host=page.locator('#planComparison')
            expect(host).to_contain_text('536 samples')
            expect(host).to_contain_text('FY2024-25')
            expect(host).to_contain_text('Water-service revenue boundary')
            host.get_by_role('button',name='Reservoir inventory · 25 reservoirs').click()
            expect(page.locator('#sourcePinState')).to_contain_text('SOURCE_PINNED_RESEARCH_PENDING_REVIEW')
            page.locator('#sourceTrail').get_by_role('button',name='Water Asset Management Plan 2025–2035').click()
            page.locator('#sourceSubtreeQuery').fill('average')
            page.locator('#sourceChildren').get_by_role('button',name='Average network water supply').click()
            expect(page.locator('#sourceChildren')).to_contain_text('No further recorded children')
            page.get_by_role('button',name='Inspect original PDF pages').click()
            expect(page.locator('#pdfCheck')).to_contain_text('Page index verified')
            expect(page.locator('#pdfReading')).to_contain_text('PDF page 8 of 56')
            expect(page.locator('#pdfReading')).to_contain_text('HAS_PINNED_RECORDS')
            page.locator('#pdfReading details summary').click()
            expect(page.locator('#pdfReading details')).to_contain_text('Grayscale rendering')
            page.screenshot(path=str(out/f'pages-{width}.png'))
            page.get_by_role('button',name='Next PDF page').click()
            expect(page.locator('#pdfReading')).to_contain_text('PAGE_INTERPRETATION_PENDING')
            page.locator('#pdfPage').fill('56');page.get_by_role('button',name='Go to page').click()
            assert not page.get_by_role('button',name='Next PDF page').count()
            assert page.get_by_role('link',name='Open publisher PDF at page 56').get_attribute('href').endswith('#page=56')
            page.locator('#pdfPage').fill('8');page.get_by_role('button',name='Go to page').click()
            page.locator('#pdfReading').get_by_role('button',name='Average network water supply').click()
            page.get_by_role('button',name='Open evidence and history').click()
            expect(page.locator('#details')).to_contain_text('AVERAGE_FLOW_RATE')
            page.screenshot(path=str(out/f'flow-{width}.png'))
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            page.goto('http://127.0.0.1:'+str(server.server_port)+'/#/research?source=ANNUAL_REPORT')
            expect(page.locator('#csoiResearchResults')).to_contain_text('Water samples reported',timeout=30000)
            assert not errors,errors
            page.close()
        browser.close()
    print('PASS 390/1440 service evidence, historical sample and finance scope, source ancestors, subtree query, leaf, quantity history and annual-report filter; verified original page index, last page, empty interpretation and return to exact evidence')
finally:
    server.shutdown()
    server.server_close()
