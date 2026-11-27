const fs = require('node:fs');
const M = require('./atlas-model.js');
const plans = require('./atlas-plan-comparison.js');
function read(filename, limit) {
 if (!filename || fs.statSync(filename).size > limit) throw Error('INPUT_SIZE_OR_PATH');
 const bytes = fs.readFileSync(filename);
 if (bytes.length > limit) throw Error('INPUT_SIZE_OR_PATH');
 return JSON.parse(bytes);
}
async function main() {
 const snapshot = read(process.argv[2],M.SNAPSHOT_MAX_BYTES);
 const receipt = read(process.argv[3],128*1024);
 if (!await M.verifySnapshot(snapshot,process.argv[4])) throw Error('SNAPSHOT_INVALID');
 if (!await plans.verify(snapshot.dataset,receipt)) throw Error('COMPARISON_DIFFERS_FROM_REPLAY');
 console.log('PASS project comparison independently reproduced:',receipt.digest,receipt.status);
}
main().catch(error=>{console.error(error.message);process.exitCode=1;});
