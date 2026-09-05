import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = ROOT / "GEGG_BUSINESS_OPERATING_MODEL_FIXTURE_v0.1.json"

def validate(model):
    checks = []
    def check(name, condition):
        checks.append({"check": name, "result": "PASS" if condition else "FAIL"})

    check("four_domains_present", {d["id"] for d in model["domains"]} == {"GOVERNANCE","FINANCE","MARKET","OPERATIONS"})
    check("business_loop_complete", model["north_stars"]["business_loop"] == ["DEMAND","OFFER","DELIVERY","ACCEPTANCE","INVOICE","CASH","LEARNING"])
    check("no_customer_claim", model["market"]["validated_customers"] == 0 and not model["controls"]["customer_selected"])
    check("no_wtp_claim", model["market"]["validated_willingness_to_pay"] == 0)
    check("financial_unknowns_preserved", all(v == "UNKNOWN" for v in model["finance"].values()))
    check("shadow_controls", not any(model["controls"][k] for k in ["external_contact","quote","contract","application","capital_commitment"] ))
    check("selection_controls", not any(model["controls"][k] for k in ["customer_selected","supplier_selected","technology_selected"] ))
    check("climateos_boundary", model["controls"]["climateos_mainline_write"] is False)
    check("personal_asset_boundary", model["controls"]["private_personal_assets_included"] is False)
    check("stage_hold", model["stage_state"] == {"sg_01":"NOT_ENTERED","sg_02":"HOLD_UNCHANGED"})
    check("next_stage_bounded", model["next_stage"] == "COMMERCIAL_READINESS_LAYER_DESIGN_ONLY")
    return checks

if __name__ == "__main__":
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    checks = validate(model)
    result = {"model": model["model_version"], "checks": checks, "passed": sum(c["result"] == "PASS" for c in checks), "total": len(checks)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] == result["total"] else 1)
