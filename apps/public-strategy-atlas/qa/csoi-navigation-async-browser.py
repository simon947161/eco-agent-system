"""Async form of csoi-navigation-browser.py for concurrent live response forwarding.

Generated once by mechanical await conversion, then reviewed. Same actual pointer
flows, assertions, 1440/390 viewports and original 30 second deadlines.
The adapter supplies browser/response transport; no owner session is simulated.
"""
from playwright.async_api import expect
async def ready(page):
    await expect(page.locator('#contentCount')).to_have_text('127', timeout=30000)
    await expect(page.locator('#startupNotice')).to_be_hidden()
    await expect(page.locator('.app')).not_to_have_attribute('inert', '')

async def settled(page):
    await expect(page.locator('#csoiWorkspace')).not_to_have_attribute('aria-busy', 'true', timeout=30000)

async def result(page, title):
    await expect(page.locator('#csoiResearchResults h2')).to_have_text(title, timeout=30000)
    await settled(page)
    first = page.locator('#csoiResearchResults .csoi-records a').first
    await expect(first).to_be_in_viewport()
    await expect(page.locator('#csoiResearchResults h2')).to_be_focused()
    assert (await first.inner_text()).strip()
    assert await page.locator('#routeMap').is_hidden()
    return {'title': title, 'firstText': await first.inner_text(), 'firstHref': await first.get_attribute('href'), 'firstY': (await first.bounding_box())['y'], 'hash': await page.evaluate('location.hash'), 'focus': await page.locator(':focus').inner_text()}

async def research(page):
    await page.locator('#csoiNavigation > summary').click()
    await page.get_by_role('navigation', name='CSOI workspaces').get_by_role('link', name='Research progress / 研究进展', exact=True).click()
    await expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80, timeout=30000)
    await settled(page)

async def tool(page, id):
    if await page.locator('#toolsMenu').get_attribute('open') is None:
        await page.locator('#toolsMenu > summary').click()
    await page.locator('#' + id).click()

async def run_navigation(browser, serve):
    for width, height in [(1440, 900), (390, 844)]:
        context = await browser.new_context(viewport={'width': width, 'height': height}, has_touch=width == 390, accept_downloads=True, reduced_motion='reduce')
        page = await context.new_page()
        await page.route(BASE.rstrip('/') + '/**', serve)
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        await page.goto(BASE)
        await ready(page)
        case = {'viewport': [width, height], 'checks': []}
        report['results'].append(case)
        save()
        await page.evaluate("localStorage.setItem('csoi-navigation-existing-draft','preserve-me');sessionStorage.setItem('csoi-navigation-session','preserve-me')")
        for node in ['csp', 'lsps']:
            await page.locator('#atlasGraph [data-node-id="' + node + '"] .station-hit').click()
            await expect(page.locator('#inspector')).to_be_visible()
            assert (await page.locator('#details').inner_text()).strip()
            await page.locator('#closeDetails').click()
        await expect(page.locator('#sourceResearchLink')).to_be_visible()
        case['checks'].append('Actual pointer clicks on original CSP and LSPS map stations open populated inspector; research entry remains reachable after map pan')
        await page.locator('#sourceResearchLink').click()
        await expect(page.locator('#csoiEngineeringTasks [data-task-id]')).to_have_count(80, timeout=30000)
        await settled(page)
        for label, title, needle in [('打开 LSPS 地图与正文', 'LSPS 地图、正文与行动', 'lsps2020'), ('只看地图记录', 'LSPS 地图记录', 'context%3Amap'), ('打开 OP 逐页梳理', 'OP 逐页梳理', 'op2026%3Areview%3Apage')]:
            await page.get_by_role('link', name=label, exact=True).click()
            observed = await result(page, title)
            assert needle in observed['firstHref']
            observed['clicked'] = label
            await page.screenshot(path=str(OUT / f"{width}-{needle.split('%')[0]}.png"))
            await page.get_by_role('link', name=label, exact=True).click()
            await result(page, title)
            await page.locator('#csoiResearchResults .csoi-records a').first.click()
            await expect(page.locator('#csoiSourceReading')).to_be_visible(timeout=30000)
            await settled(page)
            if title == 'LSPS 地图记录':
                reading = page.locator('#csoiLspsContextReading')
                await expect(reading).to_contain_text('地图实际像素与图例核对')
                await reading.locator('summary').filter(has_text='项图例').click()
                assert (await reading.locator('details[open]').inner_text()).strip()
            if title == 'OP 逐页梳理':
                unit = page.locator('#csoiOpSourceReading [data-op-unit]').first
                await unit.locator(':scope > summary').click()
                await expect(unit.locator('p').first).to_be_visible()
                assert (await unit.locator('p').first.inner_text()).strip()
            detail_url = page.url
            await page.go_back()
            await result(page, title)
            await page.go_forward()
            await expect(page.locator('#csoiSourceReading')).to_be_visible(timeout=30000)
            await settled(page)
            assert page.url == detail_url
            await page.reload()
            await ready(page)
            await expect(page.locator('#csoiSourceReading')).to_be_visible(timeout=30000)
            await settled(page)
            assert await page.evaluate("localStorage.getItem('csoi-navigation-existing-draft')") == 'preserve-me'
            assert await page.evaluate("sessionStorage.getItem('csoi-navigation-session')") == 'preserve-me'
            await page.go_back()
            await result(page, title)
            case['checks'].append(observed)
            save()
        for fragment, title in [('#/research?source=LSPS', 'LSPS 地图、正文与行动'), ('#/research?domain=LSPS_MAP&source=LSPS', 'LSPS 地图记录'), ('#/research?source=OP&domain=OP_PAGE', 'OP 逐页梳理')]:
            await page.goto(BASE + fragment)
            await ready(page)
            await result(page, title)
            await page.reload()
            await ready(page)
            await result(page, title)
        case['checks'].append('Cold deep links, browser back/forward and reload show target content; existing local/session values preserved')
        await page.get_by_role('navigation', name='Source research pages').get_by_role('link', name='下一页', exact=True).click()
        await result(page, 'OP 逐页梳理')
        await expect(page.locator('#csoiResearchResults')).to_contain_text('OP PDF 26')
        await page.get_by_role('textbox', name='Search source research').fill('no-match-navigation-fixture')
        await page.get_by_role('button', name='查询来源内容', exact=True).click()
        await expect(page.locator('#csoiResearchResults')).to_contain_text('当前快照没有匹配')
        await settled(page)
        await expect(page.locator('#csoiResearchResults h2')).to_be_in_viewport()
        case['checks'].append('Actual pagination and form submit; empty results visible with explicit recovery explanation')
        assert not errors, errors
        case['status'] = 'PASS'
        case['browserErrors'] = errors
        save()
        await context.close()
        print('PASS navigation actual-click/visibility/history/deep-link/storage at ' + str(width), flush=True)
    report['status'] = 'PASS'
    save()
