// Local adapter QA only. This loopback preview is NOT hosted private access.
import http from 'node:http';
import {readFile} from 'node:fs/promises';
const source=await readFile(new URL('../dist/server/index.js',import.meta.url),'utf8');
const {default:worker}=await import('data:text/javascript;base64,'+Buffer.from(source).toString('base64'));
http.createServer(async(req,res)=>{
 try {const result=await worker.fetch(new Request('http://127.0.0.1:8788'+req.url,{method:req.method}));
 res.writeHead(result.status,Object.fromEntries(result.headers));res.end(Buffer.from(await result.arrayBuffer()));}
 catch{res.writeHead(500);res.end('Unavailable');}
}).listen(8788,'127.0.0.1',()=>console.log('Local QA: http://127.0.0.1:8788'));
