// Optional UI check with an already installed Playwright. No dependency install.
// node check_slides.cjs ABSOLUTE_PLAYWRIGHT_MODULE [browser-channel]
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require(process.argv[2]||'playwright');
const task=path.resolve(__dirname,'..');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.argv[3]?{channel:process.argv[3]}:{})});
 const report={type:'LOCAL_HTML_ONLY',network_requests:[],views:[],screenshots:[],errors:[],deployed:false};
 for(const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]]){
  const page=await browser.newPage({viewport:{width,height}});
  page.on('pageerror',e=>report.errors.push(String(e)));
  page.on('request',r=>{if(/^https?:/.test(r.url()))report.network_requests.push(r.url())});
  await page.goto(pathToFileURL(path.join(task,'slides.html')).href);
  if(await page.locator('section').count()!==12)throw Error('PAGE_COUNT');
  for(let i=1;i<=12;i++){
   const section=page.locator(`#page-${i}`);if(!await section.isVisible())throw Error('WRONG_PAGE');
   const dims=await page.evaluate(()=>({page:document.documentElement.scrollWidth,view:innerWidth,visible:document.querySelectorAll('section:not([hidden])').length}));
   if(dims.page>dims.view||dims.visible!==1)throw Error('OVERFLOW_OR_HIDDEN');
   await section.locator('summary').click();if(!await section.locator('details').getAttribute('open')&&await section.locator('details').getAttribute('open')!=="")throw Error('SOURCE_EXPAND');
   await section.locator('summary').click();
   // Capture every page for visual review, then return to header before moving.
   await page.evaluate(()=>scrollTo(0,0));
   const file=`slides-${name}-${String(i).padStart(2,'0')}.png`;
   await page.screenshot({path:path.join(task,'evidence',file),fullPage:true});report.screenshots.push(file);
   report.views.push({viewport:name,page:i,horizontal_overflow:false,source_expand:true});
   if(i<12)await page.locator('#next').click();
  }
  if(!await page.locator('#next').isDisabled())throw Error('END_BOUNDARY');
  await page.locator('h1:visible').click();await page.keyboard.press('Home');if(!await page.locator('#prev').isDisabled())throw Error('HOME_KEY');
  await page.keyboard.press('ArrowRight');if(!await page.locator('#page-2').isVisible())throw Error('ARROW_KEY');
  await page.keyboard.press('ArrowLeft');if(!await page.locator('#page-1').isVisible())throw Error('ARROW_BACK');
  await page.close();
 }
 await browser.close();if(report.errors.length||report.network_requests.length)throw Error(JSON.stringify(report));
 report.completed_utc=new Date().toISOString();report.status='PASS_24_PAGE_VIEWPORT_CHECKS';
 fs.writeFileSync(path.join(task,'evidence/slides-validation.json'),JSON.stringify(report,null,2)+'\n');console.log(report.status);
})().catch(e=>{console.error(e);process.exit(1)});
