import argparse
from pathlib import Path
from cczps_lite.site_reading.cooma import run

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Produce the bounded Cooma Site Reading v0.1")
    parser.add_argument("--output-root", type=Path, default=Path("cczps_lite/output/cooma_site_reading_v0_1"))
    args = parser.parse_args()
    for name, path in run(args.output_root).items():
        print(f"{name}: {path}")

