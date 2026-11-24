// Local-file browser QA. No remote network or scientific data/model access.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const assert = require('assert/strict');
(async () => {
  const browser = await chromium.launch({headless:true, channel:'msedge'});
  const results = [], blockedRequests = [], errors = [];
  try {
    for (const [name,width,height] of [['desktop',1440,900],['mobile',390,844]]) {
      const context = await browser.newContext({viewport:{width,height}});
      await context.route(/^https?:\/\//, route => {blockedRequests.push(route.request().url());return route.abort();});
      const page = await context.newPage();
      page.on('pageerror', e => errors.push(e.message));
      await page.goto(pathToFileURL(path.join(__dirname,'index.html')).href);
      for(let i=1;i<=12;i++) {
        assert.equal(await page.locator('.slide:not([hidden])').count(),1);
        assert.equal(await page.locator('#counter').innerText(),`${i} / 12`);
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
        const details = page.locator('.slide:not([hidden]) details');
        await details.locator('summary').click();
        assert.equal(await details.getAttribute('open'),'');
        assert.ok(await details.locator('a').count()>=1);
        await details.locator('summary').click();
        if(i===1) await page.screenshot({path:path.join(__dirname,`preview-${name}.png`),fullPage:true});
        if(i<12) await page.locator('#next').click();
      }
      assert.equal(await page.locator('#next').isDisabled(),true);
      await page.keyboard.press('ArrowLeft');
      assert.equal(await page.locator('#counter').innerText(),'11 / 12');
      await page.keyboard.press('Home');
      assert.equal(await page.locator('#prev').isDisabled(),true);
      await page.keyboard.press('End');
      assert.equal(await page.locator('#counter').innerText(),'12 / 12');
      results.push({viewport:name,width,height,screens_checked:12,horizontal_overflow:false,source_panels:'PASS',buttons_and_keyboard:'PASS'});
      await context.close();
    }
    assert.deepEqual(errors,[]);
    assert.deepEqual(blockedRequests,[]);
    const result={status:'LOCAL_PREVIEW_PASS',run_utc:new Date().toISOString(),browser:browser.version(),results,console_page_errors:errors,attempted_remote_requests:blockedRequests,science:'PENDING',note:'Author-generated local report screenshots; not source PDF/map evidence'};
    fs.writeFileSync(path.join(__dirname,'ui_validation.json'),JSON.stringify(result,null,2)+'\n');
    console.log(JSON.stringify(result));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
