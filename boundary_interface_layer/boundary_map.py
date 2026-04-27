import json
from pathlib import Path

try:
    import folium
except ImportError:
    folium = None

INPUT_FILE = Path("boundary_output.json")
OUTPUT_FILE = Path("boundary_map.html")

COLOR_BY_CLASS = {
    "wet": "green",
    "boundary": "yellow",
    "semi_arid": "orange",
    "arid": "red",
}


def main() -> None:
    if folium is None:
        print("folium is not installed. Install folium to generate boundary_map.html")
        return

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        points = json.load(f)

    avg_lat = sum(p["latitude"] for p in points) / len(points)
    avg_lon = sum(p["longitude"] for p in points) / len(points)

    boundary_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=6)

    for point in points:
        popup_text = (
            f"<b>{point['name']}</b><br>"
            f"Precipitation: {point['precipitation']}<br>"
            f"Evapotranspiration: {point['evapotranspiration']}<br>"
            f"Boundary Value: {point['boundary_value']}<br>"
            f"Boundary Class: {point['boundary_class']}"
        )

        folium.CircleMarker(
            location=[point["latitude"], point["longitude"]],
            radius=7,
            color=COLOR_BY_CLASS.get(point["boundary_class"], "blue"),
            fill=True,
            fill_color=COLOR_BY_CLASS.get(point["boundary_class"], "blue"),
            fill_opacity=0.8,
            popup=folium.Popup(popup_text, max_width=300),
        ).add_to(boundary_map)

    boundary_map.save(OUTPUT_FILE)
    print(f"Saved map to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
