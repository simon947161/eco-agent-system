"""Actual UI readback of linear navigation and limited accessibility semantics.
Not a screen-reader session; no synthetic audio or professional certification.
"""
import datetime,json,os,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
HERE=Path(__file__).resolve().parent
OUT=HERE/'browser'/'linear-accessibility'
OUT.mkdir(parents=True,exist_ok=True)
BASE=os.environ['CSOI_AUDIT_BASE_URL']
results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    for width,height in [(390,844),(1440,900),(1600,900),(2560,1080),(3840,1080)]:
        context=browser.new_context(viewport={'width':width,'height':height},has_touch=width==390,reduced_motion='reduce')
        page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(BASE);expect(page.locator('#contentCount')).to_have_text('127',timeout=30000)
        assert page.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches')
        expect(page.locator('#routeMap')).to_be_visible()
        menu=page.locator('#toolsMenu>summary')
        if width==390:menu.tap()
        else:menu.focus();page.keyboard.press('Enter')
        button=page.locator('#textRoutesBtn')
        if width==390:button.tap()
        else:button.focus();page.keyboard.press('Enter')
        expect(page.locator('#details')).to_contain_text('Text route guide')
        route_count=page.locator('.text-route').count();assert route_count>0
        names=page.locator('[data-linear-node]').evaluate_all('(es)=>es.map(e=>({name:e.textContent,id:e.dataset.linearNode,tag:e.tagName}))')
        assert all(x['tag']=='BUTTON' and x['name'].strip() and x['id'] for x in names)
        ax=page.context.new_cdp_session(page).send('Accessibility.getFullAXTree')
        ax_nodes=[{'role':n.get('role',{}).get('value'),'name':n.get('name',{}).get('value'),'ignored':n.get('ignored')} for n in ax['nodes']]
        assert any(n['role']=='button' and n['name']=='Inspect origin' and not n['ignored'] for n in ax_nodes)
        assert any(n['role']=='heading' and n['name']=='Text route guide' and not n['ignored'] for n in ax_nodes)
        (OUT/f'linear-ax-{width}.json').write_text(json.dumps(ax_nodes,ensure_ascii=False,indent=2)+'\n')
        page.screenshot(path=str(OUT/f'linear-{width}.png'))
        origin=page.locator('[data-linear-node]').first
        origin_id=origin.get_attribute('data-linear-node')
        if width==390:origin.tap()
        else:origin.focus();page.keyboard.press('Enter')
        expect(page.locator('#inspector')).to_be_visible()
        expect(page.locator('#details')).not_to_contain_text('Text route guide')
        page.goto(BASE+'#/sources');heading=page.locator('#csoiWorkspace h1')
        expect(heading).to_have_text('Source register',timeout=30000)
        expect(heading).to_be_focused()
        assert heading.evaluate('(e)=>{const r=e.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight}')
        for name in ['Search records','Region','Recorded period year','Source ID or URL','Recorded legal reference text','Work ID or type','Unit']:
            expect(page.get_by_label(name,exact=True)).to_be_visible()
        ax=page.context.new_cdp_session(page).send('Accessibility.getFullAXTree')
        nodes=[{'role':n.get('role',{}).get('value'),'name':n.get('name',{}).get('value'),'ignored':n.get('ignored')} for n in ax['nodes']]
        assert any(n['role']=='heading' and n['name']=='Source register' and not n['ignored'] for n in nodes)
        assert any(n['role']=='textbox' and n['name']=='Recorded legal reference text' and not n['ignored'] for n in nodes)
        (OUT/f'sources-ax-{width}.json').write_text(json.dumps(nodes,ensure_ascii=False,indent=2)+'\n')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert not errors,errors
        results.append({'viewport':[width,height],'status':'PASS_ACTUALLY_TESTED','linearRoutes':route_count,'linearOriginOpened':origin_id,'input':'EMULATED_TOUCH_TAP' if width==390 else 'KEYBOARD_ENTER','reducedMotion':True,'routeHeadingFocusedInViewport':True,'accessibleNamesAndRoles':'CHROMIUM_ACCESSIBILITY_TREE_CHECKED','actualScreenReader':'NOT_TESTED','scriptErrors':errors})
        context.close()
    browser.close()
receipt={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_BOUNDED_BROWSER_CHECKS','results':results,'screenReaderTools':{name:shutil.which(name) for name in ['orca','speech-dispatcher','espeak','espeak-ng']},'limits':'Chromium AX-tree and keyboard/touch emulation, not an actual screen-reader listening session; no professional accessibility certification or physical-hardware claim.'}
(OUT/'results.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print('PASS: five-viewports linear route buttons, keyboard/emulated touch, reduced motion, focused headings, source filter accessible names; actual screen-reader session NOT_TESTED')
