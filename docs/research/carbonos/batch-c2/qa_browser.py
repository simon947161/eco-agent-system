"""Offline Chromium interaction/layout checks; no remote requests allowed."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'evidence'; OUT.mkdir(exist_ok=True)
result={'mode':'file:// offline','viewports':[],'errors':[],'external_requests':[], 'scientific_validation':False}
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=r'C:\Users\doras\AppData\Local\ms-playwright\chromium-1223\chrome-win64\chrome.exe',headless=True)
    for name,w,h in [('desktop',1440,1000),('mobile',390,844)]:
        context=browser.new_context(viewport={'width':w,'height':h},is_mobile=name=='mobile',has_touch=name=='mobile',offline=True)
        page=context.new_page()
        page.on('pageerror',lambda e:result['errors'].append(str(e)))
        page.on('request',lambda r:result['external_requests'].append(r.url) if r.url.startswith(('http:','https:')) else None)
        page.goto((ROOT/'index.html').as_uri())
        assert page.locator('.page:visible').count()==1
        assert page.locator('#prev').is_disabled()
        checks=[]
        for i in range(10):
            page.locator(f'nav button[data-page="{i}"]').click()
            assert page.locator('#counter').inner_text()==f'{i+1:02} / 10'
            assert page.locator('.page:visible').get_attribute('id')==f'page-{i+1}'
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), f'{name} page{i+1} overflow'
            source=page.locator('.page:visible .sources')
            source.locator('summary').click()
            assert source.get_attribute('open') is not None
            assert source.locator('li').count()>0
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'), f'{name} expanded page{i+1} overflow'
            if i==8: page.screenshot(path=str(OUT/f'{name}-sources.png'),full_page=True)
            source.locator('summary').click()
            if i in [0,6,7,8]: page.screenshot(path=str(OUT/f'{name}-page-{i+1}.png'),full_page=True)
            checks.append({'page':i+1,'layout':'PASS','source_expansion':'PASS'})
        assert page.locator('#next').is_disabled()
        for key,expected in [('Home',1),('ArrowRight',2),('PageDown',3),('ArrowLeft',2),('PageUp',1),('End',10)]:
            page.keyboard.press(key)
            assert page.locator('#counter').inner_text()==f'{expected:02} / 10'
        page.locator('#prev').click(); assert page.locator('#counter').inner_text()=='09 / 10'
        page.locator('#next').click(); assert page.locator('#counter').inner_text()=='10 / 10'
        page.reload(); assert page.locator('#counter').inner_text()=='10 / 10'
        result['viewports'].append({'name':name,'width':w,'height':h,'pages':checks,'keyboard_buttons_hash_reload':'PASS'})
        context.close()
    browser.close()
assert not result['errors'],result['errors']
assert not result['external_requests'],result['external_requests']
result['status']='PASS'
(OUT/'browser_qa.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'viewports':len(result['viewports']),'pages_checked':20,'automatic_remote_requests':0}))
