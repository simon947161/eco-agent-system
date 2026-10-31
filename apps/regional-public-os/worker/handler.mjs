// Hosted access is enforced by Sites dispatch's owner-only policy for EVERY route.
// Never publish this module to a separate unauthenticated Worker origin.
const headers = {'Cache-Control':'private, no-store', 'X-Content-Type-Options':'nosniff',
  'X-Frame-Options':'DENY', 'Referrer-Policy':'no-referrer',
  'Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"};
const response = (value, status=200, type='application/json; charset=utf-8') => new Response(type.startsWith('application/json') ? JSON.stringify(value) : value, {status, headers:{...headers,'Content-Type':type}});
const digest = async text => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text)))).map(x=>x.toString(16).padStart(2,'0')).join('');
const day = value => {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error('Invalid date');
  const result = Date.parse(value+'T00:00:00Z');
  if (!Number.isFinite(result) || new Date(result).toISOString().slice(0,10)!==value) throw new Error('Invalid date');
  return result;
};

export function createWorker(bundle) {
  return {async fetch(request) {
    const url = new URL(request.url);
    if (!['GET','HEAD'].includes(request.method)) return response({error:'READ_ONLY'},405);
    if (url.pathname==='/signin-with-chatgpt' || url.pathname==='/callback') return response({error:'AUTH_OWNED_BY_SITES_DISPATCH'},404);
    if (url.pathname==='/' || url.pathname==='/program.html') return response(bundle.html,200,'text/html; charset=utf-8');
    if (url.pathname==='/streamflow.js') return response(bundle.javascript,200,'text/javascript; charset=utf-8');
    if (!['/api/streamflow','/api/release'].includes(url.pathname)) return response({error:'NOT_FOUND'},404);
    let index;
    try {
      if (await digest(bundle.index) !== bundle.indexSha256) throw new Error('Index integrity failure');
      index = JSON.parse(bundle.index);
      if (!index.shards.length) throw new Error('Snapshot missing');
      if (url.pathname==='/api/release') return response({...bundle.release,index_sha256:bundle.indexSha256,data_package_sha256:index.data_package_sha256,source_sha256:index.metadata.source_sha256,records:index.records});
    } catch { return response({error:'SNAPSHOT_INTEGRITY_FAILURE',rows:[]},503); }
    let start, end;
    try {
      if ([...url.searchParams.keys()].some(k=>!['start','end'].includes(k)) || [...new Set(url.searchParams.keys())].some(k=>url.searchParams.getAll(k).length!==1)) throw new Error('Only one start/end allowed');
      end=url.searchParams.get('end') || index.metadata.coverage_end;
      start=url.searchParams.get('start') || new Date(day(end)-27*86400000).toISOString().slice(0,10);
      if (day(start)>day(end) || (day(end)-day(start))/86400000>365) throw new Error('Select an ordered window of at most 366 days');
    } catch(error) { return response({error:error.message,rows:[]},400); }
    try {
      const rows=[], used=[];
      for (const shard of index.shards.filter(s=>s.start<=end && s.end>=start)) {
        const text=bundle.shards[shard.file];
        if (typeof text!=='string' || await digest(text)!==shard.sha256) throw new Error('Shard integrity failure');
        const parsed=JSON.parse(text);
        if (parsed.length!==shard.count) throw new Error('Shard count failure');
        rows.push(...parsed.filter(r=>r.date>=start && r.date<=end)); used.push(shard);
      }
      const age=Math.floor((Date.now()-day(index.metadata.coverage_end))/86400000);
      return response({...index.metadata, rows, selected_start:start, selected_end:end,
        selected_absent_dates:(day(end)-day(start))/86400000+1-rows.length,
        age_days:age, status:rows.length ? (age>90?'HISTORICAL_STALE_FOR_CURRENT_USE':'HISTORICAL_RECORDS') : 'NO_DATA_IN_SELECTED_INTERVAL',
        source_code_baseline:index.source_code_baseline, index_sha256:bundle.indexSha256,
        data_package_sha256:index.data_package_sha256, shards:used,
        python_refresh_status:index.python_refresh_status,automatic_updates:false,release:bundle.release});
    } catch { return response({error:'SNAPSHOT_INTEGRITY_FAILURE',rows:[]},503); }
  }};
}
