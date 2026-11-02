"""Bind manually assessed task evidence to an actual code commit; never infer acceptance."""
import datetime, json, pathlib, re, subprocess, sys
APP=pathlib.Path(__file__).resolve().parents[1]
ROOT=APP.parents[1]
assessment=json.loads(pathlib.Path(sys.argv[1]).read_text())
pack=assessment['pack']
if pack not in 'ABCDEFGH' or len(pack)!=1:raise SystemExit('PACK_REQUIRED')
registry_path=APP/'COI_TASK_REGISTRY_V1_7.json'
registry=json.loads(registry_path.read_text())
if len(registry['tasks'])!=80 or len({t['id'] for t in registry['tasks']})!=80:raise SystemExit('TASK_REGISTRY_IDENTITY')
code_sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
if not re.fullmatch('[a-f0-9]{40}',code_sha):raise SystemExit('CODE_COMMIT_REQUIRED')
rows={t['id']:t for t in assessment['tasks']}
expected={t['id'] for t in registry['tasks'] if t['pack']==pack}
if set(rows)!=expected:raise SystemExit('EXACT_PACK_ASSESSMENT_REQUIRED')
for task in registry['tasks']:
 if task['id'] not in rows:continue
 row=rows[task['id']]
 if row['status'] not in registry['states']:raise SystemExit('TASK_STATE')
 if row['status']=='VERIFIED' and not all(row.get(k) for k in ['actual_code_files','actual_test_commands','evidence_links']):raise SystemExit('VERIFIED_EVIDENCE_REQUIRED')
 for name in row.get('actual_code_files',[])+row.get('evidence_links',[]):
  file=(APP/name).resolve()
  if not file.is_relative_to(APP) or not file.is_file():raise SystemExit('EVIDENCE_FILE_REQUIRED:'+name)
  relative=str(file.relative_to(ROOT))
  if subprocess.run(['git','cat-file','-e',code_sha+':'+relative],cwd=ROOT,capture_output=True).returncode:raise SystemExit('EVIDENCE_NOT_IN_CODE_COMMIT:'+name)
 task.update(row)
 task['remote_sha']=code_sha
 task['source_admission_status']=row.get('source_admission_status','PENDING_NOT_GRANTED')
 task['privacy_boundary']='PUBLIC_OR_SYNTHETIC_ONLY'
registry['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
registry.setdefault('pack_assessments',{})[pack]={k:v for k,v in assessment.items() if k!='tasks'}|{'code_sha':code_sha}
registry_path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
next_file=APP/'NEXT_SESSION.md'
header=f"# V1.7 Pack {pack} checkpoint — {assessment['software_status']}\n\nCode/evidence commit: `{code_sha}`. This continuity/registry commit follows it; resolve current remote HEAD after push.\n\n{assessment['summary']}\n\nSOFTWARE_CAPABILITY {assessment['software_status']}; PUBLIC_CORPUS_COVERAGE {assessment['corpus_status']}; OFFICIAL_ADMISSION {assessment['admission_status']}. Task statuses are evidence-based and do not imply Council approval.\n\nNext executable task: **{assessment['next_executable']}**. Continue the recovered V1.7 registry using the same model. Retain Draft PR #130; no deployment, merge, main/PR129 changes, protected business data or production WCOS writes.\n\nAssessment: `qa/csoi/pack-{pack.lower()}-assessment.json`.\n\n--- Previous checkpoint ---\n\n"
next_file.write_text(header+next_file.read_text())
print(json.dumps({'pack':pack,'code_sha':code_sha,'states':{state:sum(t['status']==state for t in rows.values()) for state in registry['states']},'next':assessment['next_executable']}))
