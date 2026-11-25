'use strict';
// Actual Chromium browser, desktop + touch/mobile emulation. Does not run models.
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname,'../..');
const site = path.join(root,'cczps_lite/dashboard');
const output = path.join(root,'docs/tasks/climateos_explainable_science_web_001/evidence');
fs.mkdirSync(output,{recursive:true});
const box={};
vm.runInNewContext(fs.readFileSync(path.join(site,'science/content.js'),'utf8'),box);
const content=box.SCIENCE_CONTENT;
const routes=['home','map','sources','experiments',...content.experiments.map(e=>`experiment/${e.id}`),...content.topics.map(t=>`topic/${t.id}`),...content.stories.map(s=>`story/${s.pr}`)];
const report={date:new Date().toISOString(),scope:'presentation only; no science execution',browser:null,devices:[],routes_per_device:routes.length,console_errors:[],page_errors:[],unexpected_requests:[],http_errors:[],reading_scenarios:[],checks:[],screenshots:[],source_link_click:null};
const mime={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8'};
// Serve only the six reviewed site assets, not the repository or research data.
const allowed=new Set(['/science/index.html','/science/content.js','/science/sources.js','/science/science.js','/science/science.css','/styles.css']);
const server=http.createServer((request,response)=>{
  let url=new URL(request.url,'http://127.0.0.1').pathname;
  if(url==='/science/'||url==='/science')url='/science/index.html';
  if(!allowed.has(url)){response.writeHead(404);response.end('Not found');return;}
  response.writeHead(200,{'Content-Type':mime[path.extname(url)],'Cache-Control':'no-store'});
  response.end(fs.readFileSync(path.join(site,url)));
});
const profiles=[{name:'desktop',viewport:{width:1440,height:900},isMobile:false,hasTouch:false},{name:'mobile',viewport:{width:390,height:844},isMobile:true,hasTouch:true,deviceScaleFactor:2},{name:'narrow',viewport:{width:320,height:740},isMobile:true,hasTouch:true,deviceScaleFactor:1}];
const contains=async(page,text)=>page.waitForFunction(value=>document.getElementById('reading').innerText.includes(value),text,{timeout:5000});
async function noOverflow(page,label){
  const dimensions=await page.evaluate(()=>({viewport:document.documentElement.clientWidth,width:document.documentElement.scrollWidth,body:document.body.scrollWidth}));
  assert.ok(dimensions.width<=dimensions.viewport+1 && dimensions.body<=dimensions.viewport+1,`${label}: overflow ${JSON.stringify(dimensions)}`);
}
async function screenshot(page,name,fullPage=false){await page.screenshot({path:path.join(output,name),fullPage});report.screenshots.push(name);}

(async()=>{
  let browser;
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const origin=`http://127.0.0.1:${server.address().port}`;
  try{
    const options={headless:true};
    if(process.env.BROWSER_EXECUTABLE)options.executablePath=process.env.BROWSER_EXECUTABLE;
    browser=await chromium.launch(options);
    report.browser=await browser.version();
    for(const profile of profiles){
      const context=await browser.newContext({...profile,reducedMotion:'reduce'});
      await context.route('**/*',route=>{
        const url=route.request().url();
        if(!url.startsWith(origin+'/')){report.unexpected_requests.push(url);return route.abort();}
        return route.continue();
      });
      const page=await context.newPage();
      page.on('console',message=>{if(message.type()==='error')report.console_errors.push({device:profile.name,message:message.text()});});
      page.on('pageerror',error=>report.page_errors.push({device:profile.name,message:error.message}));
      page.on('response',response=>{if(response.status()>=400)report.http_errors.push(response.url());});
      const device={name:profile.name,viewport:profile.viewport,mobile_emulation:profile.isMobile,physical_device:false,routes_checked:0,collapsed_and_expanded:true};
      for(const route of routes){
        await page.goto(`${origin}/science/#/${route}`);
        await page.waitForFunction(value=>document.getElementById('reading').dataset.route===value,route);
        await page.locator('main h1').waitFor();
        assert.equal(await page.locator('main h1').count(),1,`${route}: main heading`);
        await noOverflow(page,`${profile.name}/${route}/collapsed`);
        await page.locator('details').evaluateAll(nodes=>nodes.forEach(node=>{node.open=true;}));
        await noOverflow(page,`${profile.name}/${route}/expanded`);
        const localLinks=await page.locator('main a[href^="#/"]').evaluateAll(nodes=>nodes.map(node=>node.getAttribute('href').slice(2)));
        for(const target of localLinks)assert.ok(routes.includes(target)||target==='journey',`broken route ${target}`);
        const external=await page.locator('main a[target="_blank"]').evaluateAll(nodes=>nodes.map(node=>({href:node.href,rel:node.rel})));
        for(const target of external){assert.ok(target.href.startsWith('https://github.com/simon947161/eco-agent-system/'));assert.ok(target.rel.includes('noopener'));if(target.href.includes('/blob/'))assert.match(target.href,/\/blob\/[a-f0-9]{40}\//);}
        device.routes_checked++;
      }
      // Scenario 1: first-time reader follows the actual main CTA.
      await page.goto(`${origin}/science/#/home`);
      if(profile.name!=='narrow')await screenshot(page,`${profile.name}-home.png`,profile.name==='mobile');
      await page.getByRole('link',{name:'从第一个实验开始 →'}).click();
      await page.getByRole('button',{name:'30秒读懂',exact:true}).click();
      assert.equal(await page.locator('#quick-read').isVisible(),true);
      for(const phrase of ['比例 · 占多少','浓度 · 有多密','排放 · 出去多少','没有测量任何场地排放'])await contains(page,phrase);
      await page.getByRole('button',{name:'30秒读懂',exact:true}).click();
      assert.equal(await page.locator('#quick-read').isVisible(),false);
      report.reading_scenarios.push({device:profile.name,reader:'普通读者代理走查',result:'比例/浓度/排放区分及限制可找到；非真实用户理解度研究'});
      // Scenario 2: Founder can find each of the four motivations and assumptions.
      await page.getByRole('link',{name:'四个实验',exact:true}).click();
      for(const exp of content.experiments)await contains(page,exp.why);
      if(profile.name==='desktop')await screenshot(page,'desktop-four-experiments.png',true);
      report.reading_scenarios.push({device:profile.name,reader:'Founder 代理走查',result:'四个实验的研究动机和受限结论完整可见'});
      // Scenario 3: researcher reaches actual formulas, input, code and test pointers.
      await page.goto(`${origin}/science/#/experiment/p2`);
      const details=page.locator('.scientific-details');
      await details.locator('summary').first().focus();
      await page.keyboard.press('Enter');
      assert.equal(await details.getAttribute('open'),'');
      assert.equal(await page.locator('.data-table th').first().evaluate(node=>getComputedStyle(node).textTransform),'none','Physical variable case must be preserved');
      for(const phrase of ['假设、参数与单位','原方程怎么写','显式欧拉','C×a×Δt','怎样沿原研究复核'])await contains(page,phrase);
      assert.ok(await details.getByRole('link',{name:'原始假设输入 ↗',exact:true}).count());
      assert.ok(await details.getByRole('link',{name:'计算实现 ↗',exact:true}).count());
      assert.ok(await details.getByRole('link',{name:'原测试定义 ↗',exact:true}).count());
      await noOverflow(page,`${profile.name}/keyboard-details`);
      if(profile.name!=='narrow'){await details.scrollIntoViewIfNeeded();await screenshot(page,`${profile.name}-science-details.png`);}
      report.reading_scenarios.push({device:profile.name,reader:'科研读者代理走查',result:'键盘展开可找到方程、固定输入、数值方法、对照、复算说明与代码/测试'});
      // Compare A/B/C/D without changing any inputs or triggering computation.
      await page.goto(`${origin}/science/#/story/163`);
      for(const id of ['b','c','d','a']){await page.locator(`[data-scenario="${id}"]`).click();assert.equal(await page.locator(`[data-scenario="${id}"]`).getAttribute('aria-pressed'),'true');await noOverflow(page,`${profile.name}/awt-${id}`);}
      await page.locator('[data-scenario="d"]').click();
      assert.match(await page.locator('#scenario-result').innerText(),/保留空值/);
      if(profile.name==='mobile'){await page.locator('.switches').scrollIntoViewIfNeeded();await screenshot(page,'mobile-awt.png');}
      // Provenance search, route filtering, no-result case and reset.
      await page.goto(`${origin}/science/#/sources`);
      await page.getByLabel('按研究问题或编号搜索').fill('140');
      assert.equal(await page.locator('[data-source-pr]').count(),1);
      await page.locator('[data-source-pr="140"] > summary').click();
      await contains(page,'NO_VALID_PAIR');
      await page.getByLabel('按研究问题或编号搜索').fill('不存在的测试文本');
      await contains(page,'没有匹配的研究');
      await page.getByLabel('按研究问题或编号搜索').fill('');
      await page.getByLabel('选择研究路线').selectOption('carbon');
      assert.equal(await page.locator('[data-source-pr]').count(),4);
      await page.getByLabel('选择研究路线').selectOption('all');
      assert.equal(await page.locator('[data-source-pr]').count(),29);
      if(profile.name==='desktop')await screenshot(page,'desktop-evidence-index.png');
      await page.goto(`${origin}/science/#/topic/energy`); await contains(page,'尚无一类');
      await page.reload(); await contains(page,'节费与停电保供');
      await page.goto(`${origin}/science/#/bad-route`); await contains(page,'这条阅读路线还不存在');
      await page.getByRole('link',{name:'回到研究地图',exact:true}).click(); await contains(page,'沿着问题走');
      await page.goBack(); await contains(page,'这条阅读路线还不存在');
      // Skip link and focus transfer under keyboard-only navigation.
      await page.goto(`${origin}/science/#/home`);
      await page.locator('.skip-link').focus(); await page.keyboard.press('Enter');
      assert.equal(await page.evaluate(()=>document.activeElement.id),'reading');
      report.devices.push(device);
      report.checks.push(`${profile.name}: navigation, AWT switches, search/filter/empty/reset, hash reload/back, keyboard details/skip, all fixed-SHA source targets`);
      if(profile.name==='desktop'){
        await page.evaluate(()=>{document.documentElement.style.zoom='2';});
        await noOverflow(page,'desktop/200-percent-zoom');
        await screenshot(page,'desktop-200-percent-zoom.png');
        await page.evaluate(()=>{document.documentElement.style.zoom='';});
        // A real external-link click is intercepted locally to inspect its target.
        // No GitHub request is sent from the browser; fixed objects checked separately.
        await page.goto(`${origin}/science/#/experiment/p1`);
        await page.locator('.scientific-details > summary').click();
        const evidenceLink=page.getByRole('link',{name:'原始假设输入 ↗',exact:true});
        const expected=await evidenceLink.getAttribute('href');
        await context.unroute('**/*');
        await context.route('https://github.com/**',async route=>{report.source_link_click={requested:route.request().url(),sent_to_network:false,checked:'popup target matches frozen file'};await route.fulfill({status:200,contentType:'text/plain; charset=utf-8',body:'仅本地核查外链目标；没有访问远程服务。'});});
        const [popup]=await Promise.all([page.waitForEvent('popup'),evidenceLink.click()]);
        await popup.waitForLoadState();
        assert.equal(popup.url(),expected);assert.equal(report.source_link_click.requested,expected);await popup.close();
      }
      await context.close();
    }
    assert.equal(report.console_errors.length,0,JSON.stringify(report.console_errors));
    assert.equal(report.page_errors.length,0,JSON.stringify(report.page_errors));
    assert.equal(report.http_errors.length,0,JSON.stringify(report.http_errors));
    assert.equal(report.unexpected_requests.length,0,JSON.stringify(report.unexpected_requests));
    report.pass=true;
  }catch(error){report.pass=false;report.failure=error.stack;throw error;}
  finally{
    report.site_sha256={};
    report.hash_scope='UTF-8 text with CRLF normalized to LF; comparable to Git blobs across operating systems';
    for(const file of [...fs.readdirSync(path.join(site,'science')).filter(x=>/\.(html|css|js)$/.test(x)).map(x=>`science/${x}`),'styles.css']) report.site_sha256[file]=crypto.createHash('sha256').update(fs.readFileSync(path.join(site,file),'utf8').replace(/\r\n/g,'\n')).digest('hex');
    fs.writeFileSync(path.join(output,'browser-qa.json'),JSON.stringify(report,null,2)+'\n');
    if(browser)await browser.close();
    await new Promise(resolve=>server.close(resolve));
    console.log(JSON.stringify({pass:report.pass,browser:report.browser,devices:report.devices,routes:report.routes_per_device,screenshots:report.screenshots.length,error:report.failure||null}));
  }
})().catch(()=>{process.exitCode=1;});
