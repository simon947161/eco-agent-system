import json

def simple_logic(location, project):
    # 简单规则（以后可以接你真正系统）
    
    location = location.lower()
    project = project.lower()

    if "egypt" in location or "desert" in location:
        risk = "High evaporation risk"
        suggestion = "Focus on water retention and shading"
    else:
        risk = "Moderate risk"
        suggestion = "Standard environmental controls"

    return {
        "location": location,
        "project": project,
        "risk": risk,
        "suggestion": suggestion
    }

def run_cli():
    print("=== Eco Agent Simple CLI ===\n")

    location = input("Enter location: ")
    project = input("Enter project type: ")

    result = simple_logic(location, project)

    print("\n--- Result ---")
    print(f"Location: {result['location']}")
    print(f"Project: {result['project']}")
    print(f"Risk: {result['risk']}")
    print(f"Suggestion: {result['suggestion']}")

    print("\n=== End ===")

if __name__ == "__main__":
    run_cli()