import json

from cocotb.binary import BinaryValue


def create_binary_value(value, n_bits=1):
    binary_val = BinaryValue(value=value, n_bits=n_bits)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Initial Reset Behavior
    scenario1 = {
        "scenario": "Initial Reset Behavior",
        "input variable": [
            {"reset": "1", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
        ],
    }
    scenarios.append(scenario1)

    # Scenario 2: State A to B Transition
    scenario2 = {
        "scenario": "State A to B Transition",
        "input variable": [
            {"reset": "0", "s": "1", "w": "0"},
            {"reset": "0", "s": "1", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
        ],
    }
    scenarios.append(scenario2)

    # Scenario 3: Exactly Two w=1 Detection
    scenario3 = {
        "scenario": "Exactly Two w=1 Detection",
        "input variable": [
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
        ],
    }
    scenarios.append(scenario3)

    # Scenario 4: Less Than Two w=1 Detection
    scenario4 = {
        "scenario": "Less Than Two w=1 Detection",
        "input variable": [
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
        ],
    }
    scenarios.append(scenario4)

    # Scenario 5: More Than Two w=1 Detection
    scenario5 = {
        "scenario": "More Than Two w=1 Detection",
        "input variable": [
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "0"},
        ],
    }
    scenarios.append(scenario5)

    # Scenario 6: Continuous Operation
    scenario6 = {
        "scenario": "Continuous Operation",
        "input variable": [
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
        ],
    }
    scenarios.append(scenario6)

    # Scenario 7: Mid-sequence Reset
    scenario7 = {
        "scenario": "Mid-sequence Reset",
        "input variable": [
            {"reset": "0", "s": "0", "w": "1"},
            {"reset": "1", "s": "0", "w": "1"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
        ],
    }
    scenarios.append(scenario7)

    # Scenario 8: Rapid State Changes
    scenario8 = {
        "scenario": "Rapid State Changes",
        "input variable": [
            {"reset": "0", "s": "1", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
            {"reset": "0", "s": "1", "w": "0"},
            {"reset": "0", "s": "0", "w": "0"},
        ],
    }
    scenarios.append(scenario8)

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
