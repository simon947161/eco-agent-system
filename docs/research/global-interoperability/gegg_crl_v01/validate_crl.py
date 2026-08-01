import json
from pathlib import Path

ROOT = Path(__file__).parent
checks = []
def check(name, ok):
    checks.append({"check": name, "status": "PASS" if ok else "FAIL"})

runtime = json.loads((ROOT / "GEGG_CRL_RUNTIME_FIXTURE_v0.1.json").read_text())
adapter = json.loads((ROOT / "AUTO_COMPANY_SYNTHETIC_SHADOW_ADAPTER_DESIGN_v0.1.json").read_text())
kpi = json.loads((ROOT / "CRL_005_COMMERCIAL_KPI_SCORECARD_FIXTURE_v0.1.json").read_text())
cost = json.loads((ROOT / "CRL_002_ACTIVITY_COST_MODEL_FIXTURE_v0.1.json").read_text())

check("all_crl_tasks_complete", all(runtime["tasks"][f"CRL-00{i}"] == "COMPLETE" for i in range(1,7)))
check("all_data_synthetic", runtime["controls"]["real_data"] is False and cost["evidence_state"] == "SYNTHETIC")
check("no_external_commercial_action", not any(runtime["controls"][k] for k in ["external_contact","quote","contract","price_release"]))
check("no_daemon", runtime["controls"]["daemon_install"] is False and adapter["daemon_installed"] is False)
check("no_unattended_execution", runtime["controls"]["unattended_execution"] is False)
check("protected_actions_present", all(x in adapter["protected_actions"] for x in ["CONTACT","QUOTE","CONTRACT","DEPLOY","MAINLINE_WRITE"]))
check("founder_gate_preserved", adapter["translation"]["ceo_decision"] == "founder_gate_candidate")
check("no_fake_revenue", kpi["finance"]["revenue"] == 0 and kpi["finance"]["cash_collected"] == 0)
check("no_fake_market_evidence", kpi["market"]["validated_buyers"] == 0 and kpi["market"]["validated_wtp"] == 0)
check("fair_exit_controls", all(runtime["exit_design"].values()))
check("mainline_protected", runtime["controls"]["mainline_write"] is False)
check("next_gate_founder_review", runtime["next_gate"] == "FOUNDER_REVIEW_CRL_V0_1")

report = {"version":"crl-validation.v0.1","summary":{"pass":sum(c["status"]=="PASS" for c in checks),"total":len(checks)},"checks":checks}
(ROOT / "VALIDATION_REPORT_v0.1.json").write_text(json.dumps(report, indent=2) + "\n")
raise SystemExit(0 if report["summary"]["pass"] == report["summary"]["total"] else 1)

