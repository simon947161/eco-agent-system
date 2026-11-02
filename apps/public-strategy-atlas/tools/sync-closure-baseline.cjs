/* Attach the frozen original-scope assessment to the existing 80 tasks. */
const fs=require('node:fs'),path=require('node:path');
const app=path.resolve(__dirname,'..'),file=path.join(app,'COI_TASK_REGISTRY_V1_7.json'),registry=JSON.parse(fs.readFileSync(file)),baseline=require('../qa/audit-closure-20261102/author/closure-baseline.json');
if(registry.tasks.length!==80||baseline.tasks.length!==80)throw Error('ORIGINAL_80_TASKS_REQUIRED');
const fields=['actualBoundedImplementation','remainingGap','gapTypes','independentlyExecutableNextAction','completionCriterion','founderActionNeededNow','eventualDependency','whatDoesNotRequireFounderAction','softwareCapabilityAssessment','publicEvidenceAssessment','humanAdmissionAssessment','subcriteria'];
for(const task of registry.tasks){const row=baseline.tasks.find(t=>t.id===task.id);if(!row||row.exactOriginalRequirement!==task.title_and_scope)throw Error('ORIGINAL_TASK_SCOPE_MISMATCH:'+task.id);task.closureBaseline={basis:'Frozen assessment of 1bd44ea96bf742e63072d866502479ca34d34061, before the full OP review; later changes are recorded separately.',evidence:'qa/audit-closure-20261102/author/closure-baseline.json',...Object.fromEntries(fields.map(k=>[k,row[k]]))};}
fs.writeFileSync(file,JSON.stringify(registry,null,2)+'\n');
console.log('PASS: all80 original task scopes retained; detailed closure baseline attached without changing statuses.');
