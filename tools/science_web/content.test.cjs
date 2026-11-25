'use strict';
// Presentation/provenance tests only. No research modules are imported.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '../..');
const site = path.join(root,'cczps_lite/dashboard/science');
const box = {};
for (const file of ['content.js','sources.js']) vm.runInNewContext(fs.readFileSync(path.join(site,file),'utf8'), box);
const content = box.SCIENCE_CONTENT;
const sources = box.SCIENCE_SOURCES;
const audit = JSON.parse(fs.readFileSync(path.join(root,'docs/tasks/climateos_explainable_science_web_001/REMOTE_PR_SNAPSHOT.json'),'utf8'));
const ids = [125,127,129,130,132,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,152,153,155,157,161,163,165,168,169];

test('all 29 requested research changes have one complete explanatory record', () => {
  assert.deepEqual(Array.from(content.stories,s=>s.pr).sort((a,b)=>a-b),ids);
  for (const story of [...content.stories, ...content.experiments, content.energy]) {
    for (const field of ['title','question','why','dataType','method','result','notProven','status','rawStatus','gate']) assert.ok(story[field]?.length>5, `${story.pr||story.id}: ${field}`);
  }
});
test('each P1–P4 experiment has assumptions, equations, controls and a reproducibility pointer', () => {
  assert.deepEqual(Array.from(content.experiments,e=>e.id),['p1','p2','p3','p4']);
  for (const e of content.experiments) {
    assert.equal(e.pr,138); assert.ok(e.analogy && e.proves && e.numerical && e.reproduction);
    assert.ok(e.inputs.length>=5 && e.equations.length>=3 && e.values.length>=2);
    assert.equal(e.resultsFile,`${e.id}.json`);
  }
});
test('remote fixed SHA adapters match the live audit snapshot', () => {
  assert.equal(sources.main,audit.main_sha);
  for (const pr of audit.pull_requests) {
    const src = sources.prs[pr.number];
    assert.equal(src.sha,pr.head_sha); assert.match(src.sha,/^[a-f0-9]{40}$/);
    assert.equal(src.state,pr.state); assert.equal(src.draft,pr.draft); assert.equal(src.merged,pr.merged);
    assert.ok(src.links.length>0); assert.ok(src.links.every(l=>!l.path.includes('..')&&!l.path.startsWith('/')));
  }
});
test('six routes only reference existing stories and expose the local-only exception', () => {
  assert.equal(content.topics.length,6);
  for (const topic of content.topics) for (const pr of topic.prs) assert.ok(ids.includes(pr));
  assert.equal(content.topics.find(t=>t.id==='energy').local,'energy');
  assert.match(content.energy.rawStatus,/NOT_FOUND_REMOTE.*INCONCLUSIVE/);
  assert.equal(content.energy.pr,undefined);
});
test('scientific no-go states are preserved independently of UI acceptance', () => {
  const preserved = {132:['D3 DATA_NOT_READY','P1-A PENDING'],140:['NO_VALID_PAIR'],141:['NO_VALID_VERTICAL_PROFILE'],145:['OPEN_CASE_DATA_NOT_READY'],148:['DATA_NOT_READY'],149:['SCIENCE_PENDING'],155:['ENGINEERING_CLOSEOUT_ACCEPTED_WITH_SCIENCE_PENDING'],163:['SYNTHETIC','REAL_DATA_NOT_READY','CREDIT_NOT_DETERMINED'],165:['NO_SUITABLE_DATASET'],169:['TOPOLOGY_UNVERIFIED','SCIENCE=PENDING','ALL_CALCULATIONS_NO_GO']};
  for (const [pr,tags] of Object.entries(preserved)) for (const tag of tags) assert.ok(content.stories.find(s=>s.pr===Number(pr)).rawStatus.includes(tag),`${pr}: ${tag}`);
});
test('P2 and P4 retain the pure-gas surrogate and uncalibrated response boundary', () => {
  const p2=content.experiments[1],p4=content.experiments[3];
  assert.match(p2.dataType,/纯甲烷.*非填埋场/); assert.match(p2.notProven,/真实填埋场/);
  assert.match(p4.method,/两种响应没有相乘/); assert.match(p4.notProven,/最终总产气潜力/);
});
test('runtime contains no scientific solver, network client, remote import or persistent store', () => {
  const js=fs.readFileSync(path.join(site,'science.js'),'utf8');
  assert.doesNotMatch(js,/\b(fetch|XMLHttpRequest|WebSocket|EventSource|eval|Worker)\s*\(|\bimport\s*\(|navigator\.sendBeacon|localStorage|sessionStorage|Math\.(exp|log|pow)/);
  const html=fs.readFileSync(path.join(site,'index.html'),'utf8');
  assert.match(html,/connect-src 'none'/); assert.doesNotMatch(html,/<(?:script|link)[^>]+(?:src|href)="https?:/);
  assert.doesNotMatch(fs.readFileSync(path.join(site,'science.css'),'utf8'),/@import|https?:/);
});
test('Chinese document, CSP, local assets and accessible navigation are present', () => {
  const html=fs.readFileSync(path.join(site,'index.html'),'utf8');
  assert.match(html,/<html lang="zh-CN">/); assert.match(html,/name="viewport"/);
  for(const [,asset] of html.matchAll(/(?:src|href)="([^"#:]+\.(?:css|js))"/g)) assert.ok(fs.existsSync(path.resolve(site,asset)),asset);
  assert.match(html,/aria-label="主导航"/); assert.match(html,/class="skip-link"/);
});
test('AWT input links point to original fixtures, not derived passports', () => {
  for (const letter of ['A','B','C','D']) assert.ok(sources.prs[163].links.some(l=>l.path.endsWith(`/fixtures/${letter}.json`)));
  const js=fs.readFileSync(path.join(site,'science.js'),'utf8');
  assert.match(js,/边界外另记项 L/); assert.match(js,/未知部分不能按零排放处理/);
});
test('page content cannot expose private local locations or private deployment URLs', () => {
  for(const file of ['index.html','content.js','sources.js','science.js']) {
    const text=fs.readFileSync(path.join(site,file),'utf8');
    assert.doesNotMatch(text,/[A-Z]:[\\/]|file:\/\/|(?:api[_-]?key|access[_-]?token)\s*[:=]/);
  }
});
test('science-reading CI does not execute research or deployment and existing core checks retain core paths', () => {
  const workflow=fs.readFileSync(path.join(root,'.github/workflows/science-reading-checks.yml'),'utf8');
  assert.doesNotMatch(workflow,/run_physics|engine\.py|scenario_compare|workflow_dispatch|pages: write/);
  const old=fs.readFileSync(path.join(root,'.github/workflows/cczps-lite-tests.yml'),'utf8');
  assert.equal((old.match(/!cczps_lite\/dashboard\/science\/\*\*/g)||[]).length,2);
  assert.equal((old.match(/"cczps_lite\/\*\*"/g)||[]).length,2);
});
