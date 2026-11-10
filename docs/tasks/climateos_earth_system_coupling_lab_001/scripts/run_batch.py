"""Explicit opt-in bounded local batch. Never launched on import or CI."""
from pathlib import Path
import argparse,json,sys,time,hashlib,platform
TASK=Path(__file__).resolve().parents[1];ROOT=TASK.parents[2];sys.path.insert(0,str(ROOT))
from cczps_lite.integration.earth_system_coupling import experiments as e,diagnostics as d,models as m
from cczps_lite.integration.earth_system_coupling.ports import demonstrate

def save(path,value):path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');a=p.parse_args()
    if not a.execute:raise SystemExit('Requires explicit --execute; no implicit experiments.')
    started=time.monotonic();out=TASK/'evidence';out.mkdir(exist_ok=True)
    def remaining():
        seconds=1200-(time.monotonic()-started)
        if seconds<=0:raise RuntimeError('TOTAL_WALL_TIME_BUDGET')
        return seconds
    smoke=e.sweep(300,20261110,out/'smoke',remaining())
    if smoke['completed_runs']!=300:raise RuntimeError('SMOKE_INCOMPLETE')
    mainrun=e.sweep(10008,20261110,out/'main',remaining())
    replay=e.sweep(10008,20261110,ROOT/'runtime_data/earth_coupling/main-replay',remaining())
    fresh=e.sweep(300,20261111,out/'new_seed',remaining())
    diag=d.compare();save(out/'diagnostics.json',diag);save(out/'baseline.json',m.context_snapshot())
    save(out/'component-interface.json',demonstrate())
    save(out/'fixture-state.json',m.initial_state(m.default_config()).inspect())
    receipt={'python':sys.version,'platform':platform.platform(),'main_runs':mainrun['completed_runs'],'smoke_runs':300,'new_seed_runs':fresh['completed_runs'],
        'replay_runs':replay['completed_runs'],'replay_same_sha256':replay['runs_sha256']==mainrun['runs_sha256'],
        'replay_sha256':replay['runs_sha256'],'replay_elapsed_seconds':replay['elapsed_seconds'],
        'diagnostic_ensemble_runs':120,'other_diagnostics':'paired baselines, perturbations, grid/time refinement, lag, analytical diffusion; not added to main count',
        'total_script_wall_seconds':time.monotonic()-started,'source_hashes':e.code_hashes(),'scientific_admission':'PENDING',
        'declared_guardrails':{'seconds':1200,'bytes':200000000},'count_interpretation':'10008 paired strategy executions, including explicit rejection cases; not independent field experiments'}
    receipt['current_evidence_bytes']=sum(p.stat().st_size for p in out.rglob('*') if p.is_file())
    if not receipt['replay_same_sha256']:raise RuntimeError('NONDETERMINISTIC_REPLAY')
    if receipt['current_evidence_bytes']>200000000 or receipt['total_script_wall_seconds']>1200:raise RuntimeError('TOTAL_BUDGET')
    save(out/'batch-receipt.json',receipt)
    save(TASK/'EXPERIMENT_RESULTS.json',dict({k:v for k,v in mainrun.items() if k!='pairs'},paired_records_path='evidence/main/summary.json#/pairs'))
    (TASK/'summary.csv').write_bytes((out/'main/summary.csv').read_bytes())
    print(json.dumps(receipt,ensure_ascii=False))
if __name__=='__main__':main()
