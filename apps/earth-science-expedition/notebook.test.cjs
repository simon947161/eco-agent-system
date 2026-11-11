const test=require('node:test'),assert=require('node:assert/strict'),N=require('./notebook.js');
const event=(id='a',text='这是虚构测试笔记')=>({id,kind:'note',station:'general',text,at:'2026-11-11T00:00:00Z'});
test('append and duplicate import are idempotent',()=>{const a=N.merge(N.empty(),{format:'expedition-notebook/1',events:[event()]});assert.equal(N.merge(a,a).events.length,1);});
test('same ID conflict never overwrites',()=>{const a={format:'expedition-notebook/1',events:[event()]};assert.throws(()=>N.merge(a,{format:a.format,events:[event('a','不同内容')]}),/同ID/);assert.equal(a.events[0].text,'这是虚构测试笔记');});
test('invalid schema and duplicate IDs rejected',()=>{assert.throws(()=>N.validate({events:[]}));assert.throws(()=>N.validate({format:'expedition-notebook/1',events:[event(),event()]}));});
test('entry size and count are bounded',()=>{assert.throws(()=>N.validate({format:'expedition-notebook/1',events:[event('a','a'.repeat(5001))]}));assert.throws(()=>N.validate({format:'expedition-notebook/1',events:Array.from({length:1001},(_,i)=>event(String(i)))}));});
test('valid merge cannot produce an unimportable export',()=>{assert.throws(()=>N.validate({format:'expedition-notebook/1',events:Array.from({length:300},(_,i)=>event(String(i),'字'.repeat(2000)))}),/1MiB/);});
test('markup remains data',()=>{const x=event('a','<img src=x onerror=alert(1)>');assert.equal(N.validate({format:'expedition-notebook/1',events:[x]}).events[0].text,x.text);});
