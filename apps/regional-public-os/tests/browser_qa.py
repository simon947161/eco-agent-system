"""Optional loopback-only browser QA; requires existing Playwright + Chromium.

Build and run scripts/preview.mjs first. No Sites authentication/deployment check.
Outputs go to the chosen ignored/local directory; no source or database retrieval.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, expect


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'scope': 'LOCAL_LOOPBACK_NOT_DEPLOYED', 'checks': [], 'screenshots': {}}
    errors, external = [], []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, locale='zh-CN')
        def local_only(route):
            if urlparse(route.request.url).hostname == '127.0.0.1':
                route.continue_()
            else:
                external.append(route.request.url)
                route.abort()
        context.route('**/*', local_only)
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        def loaded():
            page.goto('http://127.0.0.1:8788/research')
            page.locator('#researchCards').wait_for(state='visible')
            assert page.locator('.card').count() == 3
            assert 'NOT_DEPLOYED' in page.locator('.notice').inner_text()
            assert '未建立' in page.locator('main > .meta').first.inner_text()
        def no_overflow():
            assert page.evaluate('() => document.documentElement.scrollWidth <= window.innerWidth')
        def screenshot(name):
            path = output / (name + '.png')
            page.screenshot(path=str(path), full_page=True)
            result['screenshots'][name] = {'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        loaded()
        response = page.request.get('http://127.0.0.1:8788/api/research-progress')
        original = response.json()
        result['manifest_sha256'] = original['manifest_sha256']
        result['evidence_commit'] = original['source_commit']
        result['local_release'] = page.request.get('http://127.0.0.1:8788/api/release').json()
        no_overflow(); screenshot('desktop')
        page.locator('details summary').first.focus()
        page.keyboard.press('Enter')
        assert page.locator('details').first.get_attribute('open') is not None
        for link in page.locator('.evidence a').all():
            href = link.get_attribute('href')
            assert '/blob/' + original['source_commit'] + '/' in href
            assert link.get_attribute('rel') == 'noopener noreferrer'
        no_overflow()
        result['checks'].append('desktop 1440px: 3 cards, publication boundaries, pinned links and keyboard evidence disclosure')
        page.set_viewport_size({'width':390,'height':844})
        loaded(); no_overflow(); screenshot('mobile')
        for summary in page.locator('details summary').all():
            summary.click()
        no_overflow()
        assert original['evidence']['p03']['sha256'] in page.locator('body').inner_text()
        result['checks'].append('mobile 390px: no overflow with every SHA/path expanded')
        # UI fixtures are explicitly simulated; worker clock/integrity behavior has separate unit tests.
        stale = json.loads(json.dumps(original))
        stale['snapshot_status'] = 'STALE_SNAPSHOT'
        for card in stale['cards']:
            card['display_status'] = 'STALE_SNAPSHOT'
        page.route('**/api/research-progress', lambda route: route.fulfill(json=stale))
        page.reload(); expect(page.locator('#researchStatus')).to_have_attribute('data-state', 'STALE_SNAPSHOT')
        assert page.locator('.card[data-state="STALE_SNAPSHOT"]').count() == 3
        assert page.get_by_text('上次发布记录：已发布 · 私有 Sites v2', exact=True).count() == 1
        no_overflow(); screenshot('stale-mobile')
        page.unroute('**/api/research-progress')
        page.route('**/api/research-progress', lambda route: route.fulfill(status=503, json={'error':'RESEARCH_EVIDENCE_UNVERIFIED','cards':[]}))
        page.reload(); expect(page.locator('#researchStatus')).to_have_attribute('data-state', 'UNKNOWN')
        assert page.locator('#researchCards').is_hidden()
        assert page.locator('.card').count() == 0
        no_overflow(); screenshot('unavailable-mobile')
        page.unroute('**/api/research-progress')
        unknown = json.loads(json.dumps(original))
        unknown['cards'][1]['display_status'] = 'UNKNOWN_FUTURE_STATE'
        page.route('**/api/research-progress', lambda route: route.fulfill(json=unknown))
        page.reload(); expect(page.locator('#researchStatus')).to_have_attribute('data-state', 'UNKNOWN')
        assert page.locator('.card').count() == 0
        page.unroute('**/api/research-progress')
        result['checks'].append('simulated stale, unavailable and unknown-state UI: last-known warning or all cards hidden')
        # Existing HRS flow still works after navigating through the new view.
        page.get_by_role('link', name='历史流量', exact=True).click()
        page.locator('#flowStart').fill('2026-02-01')
        page.locator('#flowEnd').fill('2026-02-28')
        page.locator('#flowLoad').click()
        expect(page.locator('#flowRows tr')).to_have_count(28)
        no_overflow()
        assert 'HISTORICAL_STALE_FOR_CURRENT_USE' in page.locator('#flowStatus').inner_text()
        page.locator('#flowStart').fill('2026-03-01')
        page.locator('#flowEnd').fill('2026-03-28')
        page.locator('#flowLoad').click()
        expect(page.locator('#flowRows tr')).to_have_count(0)
        assert 'NO_DATA_IN_SELECTED_INTERVAL' in page.locator('#flowStatus').inner_text()
        page.get_by_role('link', name='研究进度与证据 / Research progress').click()
        page.locator('#researchCards').wait_for(state='visible')
        result['checks'].append('mobile HRS navigation: February 28 rows, historical warning, empty March clears rows, return to progress')
        assert errors == [], errors
        assert external == [], external
        result.update({'page_errors':errors, 'external_requests':external, 'status':'PASS'})
        browser.close()
    (output/'browser-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
