"""Actual CSOI hash-route acceptance, standalone localhost only; no deployment."""
from pathlib import Path
import json, os
from playwright.sync_api import sync_playwright, expect

APP = Path(__file__).resolve().parents[1]
OUT = APP / 'qa' / 'csoi'
OUT.mkdir(exist_ok=True)
BASE = os.environ.get('ATLAS_URL', 'http://127.0.0.1:8877/').rstrip('/') + '/'
ROUTES = {
    '/strategy': 'Strategy and plans',
    '/knowledge/csp%3Acontent': 'Inside the knowledge',
    '/domains/wcos': 'WCOS — controlled interface',
    '/domains/wcos/ltw': 'WCOS professional knowledge',
    '/domains/wcos/backflow': 'WCOS professional knowledge',
    '/domains/phe': 'Public health and environment',
    '/domains/phe/food': 'Public professional knowledge',
    '/domains/phe/ossm': 'Public professional knowledge',
    '/domains/phe/pools': 'Public professional knowledge',
    '/domains/phe/cooling': 'Public professional knowledge',
    '/domains/phe/skin': 'Public professional knowledge',
    '/domains/phe/environment': 'Public professional knowledge',
    '/operations': 'Operations and work',
    '/calendar': 'Operational year',
    '/metrics': 'Metrics and evidence',
    '/resources': 'Resource requirements',
    '/sources': 'Source register',
    '/discovery': 'Discovery and challenge',
    '/audit': 'History and independent audit',
    '/coverage': 'Coverage and gaps',
    '/assistant': 'Michele — draft assistance',
}
results=[]
PACK=os.environ.get('CSOI_PACK','H')
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    for width,height in [(1440,900),(390,844),(1600,900),(2560,1080),(3840,1080)]:
        context=browser.new_context(viewport={'width':width,'height':height}, reduced_motion='reduce')
        page=context.new_page(); errors=[]
        page.on('pageerror',lambda error: errors.append(str(error)))
        page.goto(BASE)
        expect(page.locator('#contentCount')).to_have_text('127')
        expect(page.locator('#routeMap')).to_be_visible()
        expect(page.locator('#csoiWorkspace')).to_be_hidden()
        for path,title in ROUTES.items():
            page.evaluate('(path)=>location.hash="\u0023"+path',path)
            expect(page.locator('#csoiWorkspace h1')).to_have_text(title)
            expect(page.locator('#csoiWorkspace')).to_be_visible()
            expect(page.locator('#routeMap')).to_be_hidden()
            expect(page.locator('#csoiWorkspace')).not_to_contain_text('Workspace could not be verified:')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'), (width,path,'document overflow')
            assert page.locator('#csoiWorkspace').evaluate('(e)=>e.scrollWidth<=e.clientWidth'),(width,path,'workspace overflow')
        page.evaluate('location.hash="\u0023/strategy"')
        expect(page.locator('#csoiWorkspace h1')).to_have_text('Strategy and plans')
        page.locator('#csoiWorkspace a[href="\u0023/strategy/csp"]').click()
        expect(page.locator('#csoiWorkspace h1')).to_have_text('Strategy dossier')
        page.go_back();expect(page.locator('#csoiWorkspace h1')).to_have_text('Strategy and plans')
        page.go_forward();expect(page.locator('#csoiWorkspace h1')).to_have_text('Strategy dossier')
        page.reload();expect(page.locator('#csoiWorkspace h1')).to_have_text('Strategy dossier')
        page.evaluate('location.hash="\u0023/knowledge/csp%3Acontent"')
        expect(page.locator('#csoiWorkspace h1')).to_have_text('Inside the knowledge')
        expect(page.locator('#csoiWorkspace')).to_contain_text('Children and downstream content')
        with page.expect_popup() as popup:
            page.locator('[data-csoi-companion]').click()
        companion=popup.value;companion.wait_for_load_state()
        expect(companion.locator('#csoiWorkspace h1')).to_have_text('Inside the knowledge')
        assert 'companion=1' in companion.url
        assert companion.evaluate('window.opener===null')
        companion.close()
        page.evaluate('location.hash="\u0023/sources"')
        expect(page.locator('#csoiWorkspace h1')).to_have_text('Source register')
        page.locator('.csoi-filters input[name=q]').fill('<img src=x onerror="window.CSOI_INJECTED=1">')
        page.get_by_role('button',name='Apply filters',exact=True).click()
        expect(page.locator('#csoiWorkspace')).to_contain_text('No records are available')
        assert page.evaluate('window.CSOI_INJECTED===undefined')
        assert 'q=' in page.url
        page.evaluate('location.hash="\u0023/calendar"')
        expect(page.locator('#csoiWorkspace h1')).to_have_text('Operational year')
        if PACK!='A':
            expect(page.locator('#csoiWorkspace')).not_to_contain_text('Calendar engine is not loaded')
            first=page.locator('#csoiWorkspace .csoi-records a').first
            first.click()
            expect(page.locator('#csoiWorkspace h1')).to_have_text('Calendar work item')
        page.evaluate('location.hash="\u0023/assistant"')
        expect(page.locator('#csoiWorkspace h1')).to_have_text('Michele — draft assistance')
        if PACK!='A': expect(page.locator('#csoiAssistantDraft')).to_contain_text('DRAFT')
        page.screenshot(path=str(OUT/f'assistant-{width}.png'))
        page.evaluate('location.hash="\u0023/does-not-exist"')
        expect(page.locator('#csoiWorkspace h1')).to_have_text('Page not found')
        page.locator('#csoiWorkspace a[href="\u0023/atlas"]').click()
        expect(page.locator('#routeMap')).to_be_visible()
        expect(page.locator('#csoiWorkspace')).to_be_hidden()
        page.locator('#csoiNavigation>summary').focus();page.keyboard.press('Enter')
        expect(page.locator('#csoiNavigation')).to_have_attribute('open','')
        page.locator('#csoiNavigation a[href="\u0023/domains/phe"]').click()
        expect(page.locator('#csoiWorkspace h1')).to_have_text('Public health and environment')
        page.screenshot(path=str(OUT/f'phe-{width}.png'))
        assert not errors,errors
        results.append({'viewport':{'width':width,'height':height},'routes':len(ROUTES),'status':'PASS_TESTED_HERE','browserErrors':errors})
        scope='page shells (calendar/draft engines deferred)' if PACK=='A' else 'calendar and draft assistant'
        print(f'PASS: {width}×{height} {len(ROUTES)} routes, back/forward/reload, source filter/HTML rejection, independent companion, {scope}',flush=True)
        context.close()
    browser.close()
(OUT/('browser-'+PACK.lower()+'.json')).write_text(json.dumps({'runner':'csoi-browser-1','pack':PACK,'calendarAndAssistantChecks':'NOT_TESTED_PACK_A' if PACK=='A' else 'EXECUTED','results':results},indent=2)+'\n')
