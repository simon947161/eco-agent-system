import json
from pathlib import Path

INPUT_FILE = Path("sample_boundary_points.json")
OUTPUT_FILE = Path("boundary_output.json")


def classify_boundary(boundary_value: float) -> str:
    if boundary_value > 20:
        return "wet"
    if -20 <= boundary_value <= 20:
        return "boundary"
    if -80 <= boundary_value < -20:
        return "semi_arid"
    return "arid"


def main() -> None:
    with INPUT_FILE.open("r", encoding="utf-8") as f:
        points = json.load(f)

    output = []
    for point in points:
        boundary_value = point["precipitation"] - point["evapotranspiration"]
        point_result = {
            **point,
            "boundary_value": boundary_value,
            "boundary_class": classify_boundary(boundary_value),
        }
        output.append(point_result)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Saved {len(output)} points to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
