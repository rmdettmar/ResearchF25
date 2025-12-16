import json


def stimulus_gen():
    scenarios = []

    # Helper function to create binary strings
    def create_state(state_val):
        return format(state_val, "04b")

    # Scenario 1: Basic State Transitions with in=0
    scenario1 = {
        "scenario": "Basic State Transitions with in=0",
        "input variable": [
            {"in": "0", "state": "0001"},  # A→A
            {"in": "0", "state": "0010"},  # B→C
            {"in": "0", "state": "0100"},  # C→A
            {"in": "0", "state": "1000"},  # D→C
        ],
    }
    scenarios.append(scenario1)

    # Scenario 2: Basic State Transitions with in=1
    scenario2 = {
        "scenario": "Basic State Transitions with in=1",
        "input variable": [
            {"in": "1", "state": "0001"},  # A→B
            {"in": "1", "state": "0010"},  # B→B
            {"in": "1", "state": "0100"},  # C→D
            {"in": "1", "state": "1000"},  # D→B
        ],
    }
    scenarios.append(scenario2)

    # Scenario 3: Output Verification
    scenario3 = {
        "scenario": "Output Verification",
        "input variable": [
            {"in": "0", "state": "0001"},  # A, out=0
            {"in": "1", "state": "0010"},  # B, out=0
            {"in": "0", "state": "0100"},  # C, out=0
            {"in": "1", "state": "1000"},  # D, out=1
            {"in": "0", "state": "1000"},  # D, out=1
        ],
    }
    scenarios.append(scenario3)

    # Scenario 4: One-Hot Encoding Integrity
    scenario4 = {
        "scenario": "One-Hot Encoding Integrity",
        "input variable": [
            {"in": "0", "state": "0001"},  # Valid A
            {"in": "0", "state": "0010"},  # Valid B
            {"in": "0", "state": "0100"},  # Valid C
            {"in": "0", "state": "1000"},  # Valid D
        ],
    }
    scenarios.append(scenario4)

    # Scenario 5: Invalid State Handling
    scenario5 = {
        "scenario": "Invalid State Handling",
        "input variable": [
            {"in": "0", "state": "0000"},  # All zeros
            {"in": "1", "state": "1111"},  # All ones
            {"in": "0", "state": "1010"},  # Multiple bits set
            {"in": "1", "state": "0101"},  # Multiple bits set
        ],
    }
    scenarios.append(scenario5)

    # Scenario 6: Input Toggling
    scenario6 = {
        "scenario": "Input Toggling",
        "input variable": [
            {"in": "0", "state": "0001"},
            {"in": "1", "state": "0001"},
            {"in": "0", "state": "0010"},
            {"in": "1", "state": "0010"},
            {"in": "0", "state": "0100"},
            {"in": "1", "state": "0100"},
            {"in": "0", "state": "1000"},
            {"in": "1", "state": "1000"},
        ],
    }
    scenarios.append(scenario6)

    # Scenario 7: State D Transition Check
    scenario7 = {
        "scenario": "State D Transition Check",
        "input variable": [
            {"in": "0", "state": "1000"},  # D→C
            {"in": "1", "state": "1000"},  # D→B
            {"in": "0", "state": "1000"},  # D→C
            {"in": "1", "state": "1000"},  # D→B
        ],
    }
    scenarios.append(scenario7)

    return scenarios


if __name__ == "__main__":
    result = stimulus_gen()
    # 将结果转换为 JSON 字符串
    if isinstance(result, list):
        result = json.dumps(result, indent=4)
    elif not isinstance(result, str):
        result = json.dumps(result, indent=4)

    with open("stimulus.json", "w") as f:
        f.write(result)
