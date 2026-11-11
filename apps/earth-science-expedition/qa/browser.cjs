/* Real Chromium regression. Runtime test dependency only; app has no dependencies. */
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.argv[2]||'playwright');
const ROOT=path.resolve(__dirname,'../../..'),APP=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'docs/research/world-science-expedition/evidence/ui');
fs.mkdirSync(OUT,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
 const base=pathToFileURL(path.join(APP,'index.html')).href;
 const receipt={status:'PASS',engine:'actual Chromium via Playwright',external_requests:[],errors:[],views:[],checks:[],science:'PENDING'};
 try{
  for(const viewport of [{width:1440,height:900},{width:390,height:844}]){
   const name=viewport.width===1440?'desktop':'mobile';const context=await browser.newContext({viewport,reducedMotion:'reduce',acceptDownloads:true});const page=await context.newPage();
   page.on('pageerror',e=>receipt.errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))receipt.external_requests.push(r.url());});
   await page.goto(base+'#/home');await page.waitForSelector('.station-link');
   const data=await page.evaluate(()=>window.EXPEDITION_DATA);
   const settled=async()=>page.waitForFunction(()=>document.querySelector('main').dataset.route===location.hash);
   const go=async(url)=>{await page.goto(url);await settled();};
   const snap=async(label)=>{const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);assert.equal(overflow,false,`${name}/${label} horizontal overflow`);await page.screenshot({path:path.join(OUT,`${name}-${label}.png`),fullPage:true});receipt.views.push({viewport,route:await page.evaluate(()=>location.hash),label,overflow:false});};
   await snap('home');await page.locator('[data-filter="couple"]').click();assert.equal(await page.locator('.station-link:not(.dim)').count(),2);await page.locator('[data-filter="all"]').click();
   for(const station of data.stations){
    await page.locator(`.station-link[href="#/station/${station.id}/0"]`).click();await settled();assert.match(await page.locator('h1').innerText(),new RegExp(station.title.split('·')[0].trim()));
    await snap(station.id);
    await page.keyboard.press('ArrowRight');await page.waitForURL(/\/1$/);await settled();assert.equal(await page.locator('.flow div').count(),station.mechanism.length);
    if(['wis2','bmi','esmf'].includes(station.id))await snap(station.id+'-mechanism');
    for(let t=2;t<=4;t++){await page.locator(`.tabs a[href="#/station/${station.id}/${t}"]`).click();await settled();assert.equal(await page.locator('.tabs [aria-current="page"]').count(),1);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);}
    await page.locator('nav a[href="#/home"]').click();await settled();
   }
   for(const route of data.routes){for(let i=0;i<route.steps.length;i++){await go(base+`#/route/${route.id}/${i}`);assert.equal(await page.locator('.timeline .active').count(),1);assert.equal(await page.locator('.source-ref').count()>0,true);}}
   await go(base+'#/station/bmi/3');await page.reload();await settled();assert.equal(await page.locator('.tabs [aria-current]').innerText(),'04 比较与反例');
   await page.locator('.tabs a[href="#/station/bmi/4"]').click();await page.goBack();await settled();assert.match(await page.evaluate(()=>location.hash),/bmi\/3$/);
   await go(base+'#/vision/0');const chapters=data.documents['FOUNDER_VISION_AND_DIALOGUE_20261111_ZH.md'].split(/\n## /).length;
   for(let i=0;i<chapters;i++){await go(base+`#/vision/${i}`);assert.equal(await page.locator('article').count(),1);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);}
   await go(base+'#/vision/1');await snap('vision');
   await go(base+'#/sources');await page.locator('#source-state').selectOption('BLOCKED');assert.equal(await page.locator('.source-list article').count(),data.sources.filter(s=>s.evidence_status==='BLOCKED').length);await snap('source-gaps');
   await page.locator('#source-state').selectOption('all');await page.locator('#source-search').fill('EC03');assert.equal(await page.locator('.source-list article').count(),1);await page.locator('summary').click();assert.match(await page.locator('details').innerText(),/CC-BY/);
   for(const source of data.sources){await go(base+`#/source/${source.id}`);const a=page.locator('.source-list a[target="_blank"]');assert.equal(await a.getAttribute('href'),source.canonical_url);assert.match(await a.getAttribute('rel'),/noopener/);}
   await go(base+'#/lab/0');const old=await page.locator('[data-value="water"]').innerText();await page.locator('#case').selectOption('2');await page.waitForURL(/lab\/2$/);await settled();assert.notEqual(await page.locator('[data-value="water"]').innerText(),old);
   await page.locator('#step').fill('0');assert.equal(await page.locator('#time-label').innerText(),'900 s');await snap('lab');
   await go(base+'#/notebook');await page.locator('#note').fill('虚构验收笔记 <img src=x onerror=alert(1)>');await page.locator('[data-save]').click();assert.equal(await page.locator('#notebook-events img').count(),0);await page.reload();await settled();assert.match(await page.locator('#notebook-events').innerText(),/虚构验收笔记/);
   const downloadEvent=page.waitForEvent('download');await page.locator('#export-notes').click();const download=await downloadEvent;const payload=fs.readFileSync(await download.path());const backup=JSON.parse(payload);assert.equal(backup.events.length,1);
   await page.locator('#import-notes').setInputFiles({name:'test.json',mimeType:'application/json',buffer:payload});await page.waitForFunction(()=>document.querySelector('#notice').textContent.includes('已合并'));assert.equal(await page.locator('#notebook-events article').count(),1);
   backup.events[0].text='冲突';await page.locator('#import-notes').setInputFiles({name:'conflict.json',mimeType:'application/json',buffer:Buffer.from(JSON.stringify(backup))});await page.waitForFunction(()=>document.querySelector('#notice').textContent.includes('未导入'));assert.match(await page.locator('#notebook-events').innerText(),/虚构验收笔记/);await snap('notebook');
   await go(base+'#/review');await snap('review');for(const id of ['un','interfaces','notes','compare','questions','rights','review','next','recovery']){await go(base+`#/document/${id}`);assert.equal(await page.locator('article.reading').count(),1);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false,`document ${id}`);}
   await go(base+'#/unknown');assert.match(await page.locator('h1').innerText(),/尚无对应/);
   await go(base+'#/home');await page.keyboard.press('Tab');assert.notEqual(await page.evaluate(()=>document.activeElement.tagName),'BODY');
   receipt.checks.push({viewport,status:'PASS',station_sections:30,vision_chapters:chapters,route_steps:data.routes.reduce((n,r)=>n+r.steps.length,0),source_destinations:data.sources.length,deep_link_reload_history:true,notes_export_import_conflict_xss:true,archived_numeric_controls:true,keyboard:true});
   await context.close();
  }
  assert.deepEqual(receipt.errors,[]);assert.deepEqual(receipt.external_requests,[]);
 }catch(e){receipt.status='FAIL';receipt.failure=e.stack;throw e;}
 finally{fs.writeFileSync(path.join(OUT,'qa.json'),JSON.stringify(receipt,null,2)+'\n');await browser.close();}
 console.log(JSON.stringify({status:receipt.status,views:receipt.views.length,viewports:2,external_requests:receipt.external_requests.length}));
})().catch(e=>{console.error(e);process.exit(1)});
