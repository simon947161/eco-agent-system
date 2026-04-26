import json

def run_demo():
    print("=== Eco Agent System Demo ===\n")

    try:
        with open("example_output.json", "r") as f:
            data = json.load(f)

        print("Scenario:", data["scenario"])
        print("\n--- Summary ---")
        for k, v in data["summary"].items():
            print(f"{k}: {v}")

        print("\n--- Planning ---")
        print(data["planning"]["focus"])

        print("\n--- Delivery ---")
        print(data["delivery"]["focus"])

        print("\n--- Operations ---")
        print(data["operations"]["focus"])

        print("\n=== End of Demo ===")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    run_demo()