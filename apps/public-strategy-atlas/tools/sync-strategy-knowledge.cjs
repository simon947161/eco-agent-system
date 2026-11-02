/* Validate source-primary bundles before emitting exact classic-script mirrors. */
const fs=require('node:fs'),path=require('node:path'),K=require('../csoi-knowledge.js');
const app=path.resolve(__dirname,'..'),assets=[['csp-public-knowledge','CsoiCspKnowledge'],['lsps-public-knowledge','CsoiLspsKnowledge'],['op-water-public-knowledge','CsoiOpWaterKnowledge']];
const outputs=assets.map(([name,global])=>{const bundle=JSON.parse(fs.readFileSync(path.join(app,'sources',name+'.json'),'utf8'));K.validateBundle(bundle);return [path.join(app,'sources',name+'.js'),`(function(root){const value=${JSON.stringify(bundle)};root.${global}=value;if(typeof module!=='undefined')module.exports=value;})(typeof window!=='undefined'?window:globalThis);\n`];});
for(const [file,body]of outputs){if(process.argv.includes('--check')){if(fs.readFileSync(file,'utf8')!==body)throw Error('STRATEGY_MIRROR_STALE:'+path.basename(file));}else fs.writeFileSync(file,body);}
console.log('PASS: three source-primary knowledge bundles validate and browser mirrors match exact JSON.');
