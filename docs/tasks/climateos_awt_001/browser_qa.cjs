// Offline page QA, reused browser runner only; no network services or deployment.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async()=>{
 const t=__dirname, out=path.join(t,'evidence','ui');fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({headless:true,executablePath:process.env.BROWSER_EXECUTABLE});
 const errors=[],network=[],checks=[];
 for(const [label,width,height] of [['desktop',1440,1000],['mobile',390,844]]){
  const page=await browser.newPage({viewport:{width,height}});
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url());});
  await page.goto(pathToFileURL(path.join(t,'index.html')).href);
  for(let i=1;i<=12;i++){
   await page.selectOption('select',String(i-1));
   await page.locator('#slide-'+i).waitFor({state:'visible'});
   const result=await page.evaluate(()=>({visible:[...document.querySelectorAll('section')].filter(s=>!s.hidden).length,
     overflow:document.documentElement.scrollWidth>innerWidth,
     pending:document.querySelector('section:not([hidden])').innerText.includes('PENDING'),
     title:document.querySelector('section:not([hidden]) h1').innerText}));
   if(result.visible!==1||result.overflow||!result.pending)throw Error('Layout '+label+' '+i+' '+JSON.stringify(result));
   await page.locator('#slide-'+i+' summary').click();
   if(!(await page.locator('#slide-'+i+' details').getAttribute('open')!==null))throw Error('Details');
   await page.locator('#slide-'+i+' summary').click();
   await page.evaluate(()=>window.scrollTo(0,0));
   await page.waitForFunction(()=>window.scrollY===0);
   if([1,6,7,12].includes(i))await page.screenshot({path:path.join(out,label+'-'+i+'.png'),fullPage:true});
   checks.push({viewport:label,page:i,...result,details:true});
  }
  await page.locator('body').click({position:{x:2,y:150}});
  await page.keyboard.press('Home');
  if(!(await page.locator('#slide-1').isVisible()))throw Error('Home');
  await page.keyboard.press('ArrowRight');
  if(!(await page.locator('#slide-2').isVisible()))throw Error('ArrowRight');
  await page.click('#next');await page.reload();
  if(!(await page.locator('#slide-3').isVisible()))throw Error('Hash reload');
  await page.click('#prev');
  if(!(await page.locator('#slide-2').isVisible()))throw Error('Previous');
  await page.locator('body').click({position:{x:2,y:150}});await page.keyboard.press('End');
  if(!(await page.locator('#slide-12').isVisible()))throw Error('End');
  await page.close();
 }
 const result={browser:await browser.version(),views:checks.length,checks,errors,automatic_network_requests:network,
   navigation:'Home/End/arrows/next/previous/hash-reload PASS',scope:'Chromium simulated viewports; not physical device or all browsers'};
 await browser.close();fs.writeFileSync(path.join(out,'qa.json'),JSON.stringify(result,null,2)+'\n');
 if(errors.length||network.length)throw Error('Errors or network requests');
 console.log(JSON.stringify({views:checks.length,errors:errors.length,network:network.length,browser:result.browser}));
})().catch(e=>{console.error(e);process.exitCode=1;});
