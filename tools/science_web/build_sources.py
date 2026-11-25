"""Build a thin static metadata adapter; never import or execute research code.

The snapshot is the canonical remote audit. --verify-git checks pinned file
objects in already-fetched refs; it neither fetches nor reads private inputs.
"""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / 'docs/tasks/climateos_explainable_science_web_001'
DEST = ROOT / 'cczps_lite/dashboard/science/sources.js'

PATHS = {
    125: 'docs/tasks/climate_assistant_demo_v0_1/README.md',
    127: 'docs/council_bridge/README.md',
    129: 'docs/tasks/climateos_regional_public_os_001/THREAD_HANDOFF_20261101_OWNER_VIEW.md',
    130: 'apps/public-strategy-atlas/README.md',
    132: 'docs/research/carbonos/INDEX.md',
    135: 'docs/tasks/climateos_dynamic_quant_001/FOUNDER_DYNAMIC_QUANTIFICATION_ROADMAP_ZH.md',
    136: 'docs/tasks/climateos_dynamic_quant_001/FACILITY_SPATIAL_CONTINUATION_ZH.md',
    137: 'docs/tasks/climateos_dynamic_quant_001/METHANE_ALTITUDE_PRESSURE_ZH.md',
    138: 'docs/tasks/climateos_physics_validation_001/README.md',
    139: 'docs/tasks/climateos_local_case_method_intake_001/README.md',
    140: 'docs/tasks/climateos_methane_factor_order_001/README.md',
    141: 'docs/tasks/climateos_spatial_ghg_hypothesis_validation_001/README.md',
    142: 'docs/tasks/climateos_client_ai_science_integration_001/README.md',
    143: 'docs/tasks/climateos_methane_physics_knowledge_engine_001/README.md',
    144: 'docs/tasks/climateos_au_landfill_methane_methods_001/README.md',
    145: 'docs/tasks/climateos_global_method_evidence_ecochain_001/README.md',
    146: 'docs/tasks/global_natural_systems_evidence_atlas_001/README.md',
    147: 'docs/tasks/climateos_physical_process_trajectory_001/README.md',
    148: 'docs/tasks/climateos_enso_regional_weather_probability_001/README.md',
    149: 'docs/tasks/climateos_multisource_data_admission_001/README.md',
    152: 'docs/tasks/climateos_earth_system_coupling_lab_001/README.md',
    153: 'docs/tasks/ecoengine_v200_private_method_comparison_001/PAIRWISE_RESULT_PUBLIC_ZH.md',
    155: 'docs/tasks/climateos_adaptive_earth_relations_runtime_001/REVIEW_CLOSURE_ZH.md',
    157: 'docs/research/world-science-expedition/INDEX.md',
    161: 'research/api-experiments/CLIMATEOS-API-001/README.md',
    163: 'docs/tasks/climateos_awt_001/COUNTERFACTUAL_CASE_1000T.md',
    165: 'docs/tasks/climateos_awt_001/p4/README.md',
    168: 'docs/tasks/climateos_science_handoff_20261124_001/UNIFIED_CODEX_TASKBOOK.md',
    169: 'docs/tasks/climateos_science_handoff_20261124_001/UNIFIED_TASK_INDEX.md',
}
# Only source paths used by the UI; all of them are verified against frozen objects.
EXTRA = {
    132: [('分批状态与下一步', 'docs/research/carbonos/NEXT_SESSION.md')],
    138: [('原始假设输入', 'docs/tasks/climateos_physics_validation_001/inputs.json'), ('计算实现', 'cczps_lite/integration/physics_validation.py'), ('原测试定义', 'tests/test_physics_validation.py'), ('原测试回执（不是本次重跑）', 'docs/tasks/climateos_physics_validation_001/physics-tests.json'), ('质量守恒记录', 'docs/tasks/climateos_physics_validation_001/conservation.json'), ('复算方法与原运行命令', 'docs/tasks/climateos_physics_validation_001/README.md'), *[(f'实验{i}的归档结果', f'docs/tasks/climateos_physics_validation_001/p{i}.json') for i in range(1,5)]],
    137: [('沿海与内陆研究设计', 'docs/tasks/climateos_dynamic_quant_001/coastal_inland_study_design.json')],
    140: [('独立评审与回执边界', 'docs/tasks/climateos_methane_factor_order_001/SCIENTIFIC_REVIEW_RECEIPT.md')],
    144: [('物理方程与质量账', 'docs/tasks/climateos_au_landfill_methane_methods_001/LANDFILL_PHYSICS_AND_MASS_BALANCE.md')],
    147: [('方法、结果与边界', 'docs/tasks/climateos_physical_process_trajectory_001/FOUNDER_REPORT_ZH.md')],
    149: [('样本与不确定性', 'docs/tasks/climateos_multisource_data_admission_001/FOUNDER_REPORT_ZH.md')],
    152: [('数值方法与假设', 'docs/tasks/climateos_earth_system_coupling_lab_001/NUMERICAL_METHODS_AND_ASSUMPTIONS.md'), ('拒绝与失败记录', 'docs/tasks/climateos_earth_system_coupling_lab_001/COUNTEREVIDENCE_AND_FAILURES.md')],
    163: [('四情景归档结果', 'docs/tasks/climateos_awt_001/evidence/results.json'), ('情景输入 A', 'docs/tasks/climateos_awt_001/fixtures/A.json'), ('情景输入 B', 'docs/tasks/climateos_awt_001/fixtures/B.json'), ('情景输入 C', 'docs/tasks/climateos_awt_001/fixtures/C.json'), ('情景输入 D', 'docs/tasks/climateos_awt_001/fixtures/D.json'), ('原计算实现（不在本网站执行）', 'docs/tasks/climateos_awt_001/engine.py')],
    169: [('拓扑冲突记录', 'docs/tasks/climateos_science_handoff_20261124_001/WHH_P0_TOPOLOGY_CONFLICT.md')],
}

def build(verify=False):
    snapshot = json.loads((TASK / 'REMOTE_PR_SNAPSHOT.json').read_text(encoding='utf-8'))
    result = {'checkedAt': snapshot['checked_at_utc'], 'main': snapshot['main_sha'], 'prs': {}}
    checked = 0
    for pr in snapshot['pull_requests']:
        n = pr['number']
        links = [('原研究说明与来源目录', PATHS[n]), *EXTRA.get(n, [])]
        for label, path in links:
            if verify:
                subprocess.run(['git', 'cat-file', '-e', f"{pr['head_sha']}:{path}"], cwd=ROOT, check=True, capture_output=True)
            checked += 1
        result['prs'][str(n)] = {
            'sha': pr['head_sha'], 'url': pr['url'], 'updated': pr['updated_at'],
            'state': pr['state'], 'draft': pr['draft'], 'merged': pr['merged'],
            'links': [{'label': label, 'path': path} for label, path in links],
            'discussions': [{'url': c['url'], 'date': c['date']} for c in pr['discussion_entries']],
        }
    return '// Generated from the canonical audit by tools/science_web/build_sources.py.\n' + 'globalThis.SCIENCE_SOURCES = ' + json.dumps(result, ensure_ascii=False, indent=2) + ';\n', checked

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-git', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    text, count = build(args.verify_git)
    if args.check:
        assert DEST.read_text(encoding='utf-8') == text, 'Generated source adapter is stale'
    else:
        DEST.write_text(text, encoding='utf-8')
    print(json.dumps({'source_files': count, 'git_objects_verified': args.verify_git, 'adapter_matches': True}))
