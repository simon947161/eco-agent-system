import json
from pathlib import Path
from orchestrator.orchestrator import run_system
from utils.loader import load_json
from utils.eco_dna_adapter import normalize_eco_dna

def main() -> None:
    base_dir = Path(__file__).resolve().parent
    project_root = base_dir.parent
    real_eco_dna_path = project_root / "eco_dna_B_hot_dry_windy_hyper_evap.json"
    sample_eco_dna_path = base_dir / "data" / "sample_eco_dna.json"
    if real_eco_dna_path.exists():
        source_path = real_eco_dna_path
        source_type = "real_eco_dna"
    else:
        source_path = sample_eco_dna_path
        source_type = "sample_eco_dna"
    raw_data = load_json(str(source_path))
    eco_data = normalize_eco_dna(raw_data)
    result = run_system(eco_data)
    final_report = {
        "ok": True,
        "source_type": source_type,
        "source_path": str(source_path),
        "normalized_eco_data": eco_data,
        "agent_report": result,
    }
    output_path = base_dir / "professional_agent_report.json"
    output_path.write_text(json.dumps(final_report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n================ PROFESSIONAL AGENT SYSTEM RESULT ================")
    print(json.dumps(final_report, indent=2, ensure_ascii=False))
    print("==================================================================")
    print(f"\nSaved to: {output_path}")

if __name__ == "__main__":
    main()
