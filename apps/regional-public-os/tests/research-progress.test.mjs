import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createWorker} from '../worker/handler.mjs';
import {evaluateProgress, evidenceCommit, evidenceFiles, taskDirectory} from '../worker/research-progress.mjs';
import {generateProgress, verifyProgressBytes, sha256} from '../scripts/generate-research-progress.mjs';

const text = await readFile(new URL('../data/research-progress.json', import.meta.url), 'utf8');
const manifest = JSON.parse(text);
const now = Date.parse('2026-11-01T12:00:00Z');
const bundle = {researchManifest: text, researchManifestSha256: sha256(text), researchHtml: '<h1>research</h1>', researchJavascript: 'void 0;'};
const workerFor = (value = bundle, clock = now) => createWorker(value, {now: () => clock});
const get = (worker, route = '/api/research-progress') => worker.fetch(new Request('https://owner.example' + route));
const rehash = value => {const body = JSON.stringify(value); return {...bundle, researchManifest:body, researchManifestSha256:sha256(body)};};

test('committed manifest replays from exact Git blobs; each link resolves to the hashed path', () => {
  assert.equal(generateProgress(), text);
  assert.equal(verifyProgressBytes(text), text);
  for (const [id, [file, date]] of Object.entries(evidenceFiles)) {
    const ref = manifest.evidence[id];
    assert.equal(ref.path, taskDirectory + file);
    assert.equal(ref.commit, evidenceCommit);
    assert.equal(ref.recorded_on, date);
    assert.ok(ref.url.endsWith('/blob/' + evidenceCommit + '/' + taskDirectory + file));
  }
});

test('build rejects invented claims and hash receipts even when JSON is well formed', () => {
  for (const change of [m => m.cards[1].summary = 'Already deployed', m => m.evidence.p03.sha256 = 'a'.repeat(64)]) {
    const changed = structuredClone(manifest); change(changed);
    assert.throws(() => verifyProgressBytes(JSON.stringify(changed, null, 2) + '\n'), /Evidence review required/);
  }
});

test('three stages preserve publication, retrospective and scientific boundaries', async () => {
  const result = await get(workerFor()); assert.equal(result.status, 200);
  const data = await result.json();
  assert.equal(data.deployment_status, 'NOT_DEPLOYED');
  assert.equal(data.automation_status, 'NOT_ESTABLISHED');
  assert.equal(data.scientific_admission, false);
  assert.equal(data.live_status_verified, false);
  assert.deepEqual(data.cards.map(c => c.publication_status), ['PUBLISHED_PRIVATE_V2','NOT_ON_SITES','NOT_ON_SITES']);
  assert.match(data.cards[1].limits.join(), /不属于原始月度审阅证据/);
  assert.match(data.cards[2].scope, /2000 年 7 月.*单个网格/);
  assert.match(data.cards[2].limits.join(), /不能推广/);
});

test('expired snapshot keeps last-known evidence but downgrades EVERY card and never implies live verification', () => {
  const boundary = evaluateProgress(manifest, Date.parse('2026-11-07T23:59:59Z'));
  assert.equal(boundary.snapshot_status, 'RECORDED_SNAPSHOT');
  const stale = evaluateProgress(manifest, Date.parse('2026-11-08T00:00:00Z'));
  assert.equal(stale.snapshot_status, 'STALE_SNAPSHOT');
  assert.ok(stale.cards.every(c => c.display_status === 'STALE_SNAPSHOT'));
  assert.equal(stale.cards[0].recorded_status, 'VERIFIED_HISTORICAL_RECORD');
  assert.equal(stale.live_status_verified, false);
});

test('future, invalid and unknown clocks fail closed', async () => {
  for (const clock of [Date.parse('2026-10-31T23:59:59Z'), NaN, Infinity]) {
    const result = await get(workerFor(bundle, clock));
    assert.equal(result.status, 503); assert.deepEqual((await result.json()).cards, []);
  }
});

test('missing or corrupt manifest cannot expose progress cards', async () => {
  for (const value of [{...bundle,researchManifest:undefined}, {...bundle,researchManifest:text+' '}, {...bundle,researchManifestSha256:'a'.repeat(64)}]) {
    const result = await get(workerFor(value));
    assert.equal(result.status, 503); assert.deepEqual((await result.json()).cards, []);
  }
});

test('unknown schema, states, release, automation and scientific admission fail closed', async () => {
  for (const change of [
    m => m.schema = 'future.v2', m => m.cards[1].recorded_status = 'COMPLETE',
    m => m.cards[1].publication_status = 'PUBLISHED_PRIVATE_V2', m => m.deployment_status = 'DEPLOYED',
    m => m.automation_status = 'RUNNING', m => m.scientific_admission = true,
    m => m.cards.pop(), m => m.cards.push({...m.cards[0],id:'P99'}), m => m.generated_on = '2026-11-30',
  ]) {
    const value = structuredClone(manifest); change(value);
    const result = await get(workerFor(rehash(value)));
    assert.equal(result.status, 503); assert.deepEqual((await result.json()).cards, []);
  }
});

test('wrong paths, card associations, evidence dates, commits and unpinned URLs fail closed even with a matching payload hash', async () => {
  for (const change of [
    m => m.evidence.p03.path = m.evidence.p02.path,
    m => m.cards[1].evidence_ids = m.cards[0].evidence_ids,
    m => m.cards[1].evidence_date = '2026-11-01',
    m => m.evidence.p03.commit = 'a'.repeat(40),
    m => m.evidence.p03.recorded_on = '2026-11-01',
    m => m.evidence.p03.url = m.evidence.p03.url.replace(evidenceCommit, 'main'),
    m => m.evidence.p03.url = 'javascript:alert(1)',
    m => delete m.evidence.p03,
  ]) {
    const value = structuredClone(manifest); change(value);
    const result = await get(workerFor(rehash(value)));
    assert.equal(result.status, 503); assert.deepEqual((await result.json()).cards, []);
  }
});

test('research routes are read-only and private; query strings cannot select files or refresh data', async () => {
  for (const route of ['/research','/research.html','/research.js','/api/research-progress']) {
    const result = await get(workerFor(),route);
    assert.equal(result.status,200); assert.equal(result.headers.get('Cache-Control'),'private, no-store');
    assert.equal(result.headers.get('Access-Control-Allow-Origin'),null);
    assert.match(result.headers.get('Content-Security-Policy'), /connect-src 'self'/);
    const write = await workerFor().fetch(new Request('https://owner.example'+route,{method:'POST'}));
    assert.equal(write.status,405);
  }
  assert.equal((await get(workerFor(),'/api/research-progress?refresh=1')).status,400);
  assert.equal((await get(workerFor(),'/data/research-progress.json')).status,404);
});
