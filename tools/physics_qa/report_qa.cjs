// Real headless Chromium rendering, keyboard and mobile checks; no network.
const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
(async()=>{
 const root=path.resolve(__dirname,'../..');
 const task=path.join(root,'docs/tasks/climateos_physics_validation_001');
 const shots=path.join(task,'qa/screenshots');fs.mkdirSync(shots,{recursive:true});
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const results=[],errors=[],network=[];
 try{
  for(const [name,width,height,mobile] of [['desktop',1440,1000,false],['mobile',390,844,true]]){
   const context=await browser.newContext({viewport:{width,height},isMobile:mobile,hasTouch:mobile});
   const page=await context.newPage();page.on('pageerror',e=>errors.push(String(e)));
   page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url())});
   await page.goto(pathToFileURL(path.join(task,'index.html')).href);
   for(let n=1;n<=12;n++){
    await page.selectOption('select',String(n-1));
    await page.locator(`#slide-${n}`).waitFor({state:'visible'});
    await page.locator('select').blur();
    const data=await page.evaluate(n=>{
     const section=document.querySelector(`#slide-${n}`);
     return {visible:!section.hidden,oneVisible:[...document.querySelectorAll('section')].filter(x=>!x.hidden).length===1,
       horizontalOverflow:document.documentElement.scrollWidth>innerWidth+1,
       imagesReady:[...section.querySelectorAll('img')].every(x=>x.complete&&x.naturalWidth>0),
       title:section.querySelector('h1').textContent,
       counter:document.querySelector('#counter').textContent};
    },n);
    if(!data.visible||!data.oneVisible||data.horizontalOverflow||!data.imagesReady||data.counter!==`${n} / 12`)throw Error(JSON.stringify(data));
    await page.screenshot({path:path.join(shots,`${name}-${String(n).padStart(2,'0')}.png`),fullPage:true});
    results.push({device:name,page:n,status:'PASS',...data});
   }
   await page.keyboard.press('Home');if(!await page.locator('#slide-1').isVisible())throw Error('Home failed');
   await page.keyboard.press('ArrowRight');if(!await page.locator('#slide-2').isVisible())throw Error('Right failed');
   await page.keyboard.press('ArrowLeft');if(!await page.locator('#slide-1').isVisible())throw Error('Left failed');
   await page.keyboard.press('End');if(!await page.locator('#slide-12').isVisible())throw Error('End failed');
   await page.goto(pathToFileURL(path.join(task,'index.html')).href+'#slide-7');
   if(!await page.locator('#slide-7').isVisible())throw Error('Hash failed');
   await page.reload();if(!await page.locator('#slide-7').isVisible())throw Error('Hash reload failed');
   await page.locator('#slide-7 summary').click();if(!await page.locator('#slide-7 details').evaluate(x=>x.open))throw Error('Sources failed');
   await page.locator('#next').click();if(!await page.locator('#slide-8').isVisible())throw Error('Next failed');
   await page.locator('#prev').click();if(!await page.locator('#slide-7').isVisible())throw Error('Prev failed');
   await context.close();
  }
  if(errors.length||network.length)throw Error(JSON.stringify({errors,network}));
  const result={status:'PASS',render_combinations:results.length,browser_version:browser.version(),playwright_version:require('playwright/package.json').version,
   keyboard:'Home End ArrowLeft ArrowRight PASS on both viewports',navigation:'select buttons hash reload details PASS',
   console_errors:errors,automatic_network_requests:network,results,scope:'UI/render QA only; no observational scientific admission'};
  fs.writeFileSync(path.join(task,'browser_qa.json'),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({...result,results:'24 detailed records in browser_qa.json'}));
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
