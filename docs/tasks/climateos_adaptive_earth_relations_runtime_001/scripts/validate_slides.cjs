const fs=require('fs'), path=require('path'), {pathToFileURL}=require('url');
const {chromium}=require(process.argv[2]||'playwright');
(async()=>{
 const root=path.resolve(__dirname,'..'),out=path.join(root,'evidence','ui');fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
 const report={viewports:[],networkRequests:[],consoleErrors:[],screenshots:[],status:'PENDING'};
 for(const [label,width,height]of [['desktop',1440,1000],['mobile',390,844]]){
  const page=await browser.newPage({viewport:{width,height}});page.on('pageerror',e=>report.consoleErrors.push(String(e)));
  page.on('request',r=>{if(/^https?:/.test(r.url()))report.networkRequests.push(r.url())});
  await page.goto(pathToFileURL(path.join(root,'slides.html')).href);
  let checks=[];
  for(let n=1;n<=10;n++){
   await page.evaluate(n=>show(n),n);
   const v=await page.evaluate(()=>({active:document.querySelectorAll('.slide.active').length,overflow:document.documentElement.scrollWidth>innerWidth+1,text:document.querySelector('.slide.active').innerText.length}));
   if(v.active!==1||v.overflow||v.text<50)throw Error(label+' page '+n+' layout '+JSON.stringify(v));
   const filename=`${label}-${n}.png`;await page.screenshot({path:path.join(out,filename),fullPage:true});report.screenshots.push(filename);checks.push({page:n,...v});
  }
  await page.evaluate(()=>show(1));const before=await page.locator('#airT').innerText();
  await page.selectOption('#scenario','HEAT_DRY_WIND');const after=await page.locator('#airT').innerText();if(before===after)throw Error('scenario did not update');
  await page.locator('#step').fill('0');await page.locator('#step').dispatchEvent('input');if(!((await page.locator('#clock').innerText()).includes('0.25')))throw Error('time replay failed');
  await page.locator('h1').click();await page.keyboard.press('ArrowRight');if(await page.locator('#pageLabel').innerText()!=='2 / 10')throw Error('keyboard failed');
  await page.locator('#next').click();if(await page.locator('#pageLabel').innerText()!=='3 / 10')throw Error('next failed');
  await page.evaluate(()=>show(10));await page.locator('.slide.active summary').click();
  report.viewports.push({label,width,height,checks,scenarioChanged:true,slider:true,keyboard:true,nextButton:true,sourceDisclosure:true});await page.close();
 }
 if(report.consoleErrors.length||report.networkRequests.length)throw Error(JSON.stringify(report));
 for(const label of ['desktop','mobile']){
  const html='<html><body style="margin:0;background:#ddd;display:grid;grid-template-columns:repeat(5,1fr);gap:8px;font-family:sans-serif">'+Array.from({length:10},(_,i)=>'<div><strong>'+label+' '+(i+1)+'</strong><img style="width:100%;height:'+(label==='desktop'?200:450)+'px;object-fit:contain;object-position:top" src="'+label+'-'+(i+1)+'.png"></div>').join('')+'</body></html>';
  const file=path.join(out,'contact-'+label+'.html');fs.writeFileSync(file,html);
  const p=await browser.newPage({viewport:{width:1400,height:1000}});await p.goto(pathToFileURL(file).href);await p.screenshot({path:path.join(out,'contact-'+label+'.png'),fullPage:true});await p.close();
 }
 report.slides_sha256=require('crypto').createHash('sha256').update(fs.readFileSync(path.join(root,'slides.html'))).digest('hex');
 report.initial_harness_failure='unscoped summary selector matched hidden pages; fixed to active page; not application failure';
 report.status='PASS';fs.writeFileSync(path.join(out,'qa.json'),JSON.stringify(report,null,2));await browser.close();console.log(JSON.stringify({status:'PASS',viewports:2,pages:20,offline:true}));
})().catch(e=>{console.error(e);process.exit(1)});
