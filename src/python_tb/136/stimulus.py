import json


def stimulus_gen():
    scenarios = []

    # Helper function to convert to binary string
    def to_bin(val):
        return "1" if val else "0"

    # Scenario 1: Truth Table Verification
    truth_table = {
        "scenario": "Truth Table Verification",
        "input variable": [
            {"a": "0", "b": "0"},
            {"a": "0", "b": "1"},
            {"a": "1", "b": "0"},
            {"a": "1", "b": "1"},
        ],
    }
    scenarios.append(truth_table)

    # Scenario 2: Input Transitions
    transitions = {
        "scenario": "Input Transitions",
        "input variable": [
            {"a": "0", "b": "0"},
            {"a": "0", "b": "1"},
            {"a": "1", "b": "1"},
            {"a": "1", "b": "0"},
            {"a": "0", "b": "0"},
        ],
    }
    scenarios.append(transitions)

    # Scenario 3: Simultaneous Input Changes
    simultaneous = {
        "scenario": "Simultaneous Input Changes",
        "input variable": [
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
        ],
    }
    scenarios.append(simultaneous)

    # Scenario 4: Input Signal Stability
    stability = {
        "scenario": "Input Signal Stability",
        "input variable": [
            {"a": "1", "b": "1"},
            {"a": "1", "b": "1"},
            {"a": "1", "b": "1"},
            {"a": "0", "b": "0"},
            {"a": "0", "b": "0"},
            {"a": "0", "b": "0"},
        ],
    }
    scenarios.append(stability)

    # Scenario 5: Setup and Hold Time
    setup_hold = {
        "scenario": "Setup and Hold Time",
        "input variable": [
            {"a": "0", "b": "0"},
            {"a": "1", "b": "0"},
            {"a": "1", "b": "1"},
            {"a": "0", "b": "1"},
            {"a": "0", "b": "0"},
        ],
    }
    scenarios.append(setup_hold)

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
