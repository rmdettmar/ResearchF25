import json

from cocotb.binary import BinaryValue


def get_binary_str(value, width):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic State Transitions x=0
    scenario1 = {
        "scenario": "Basic State Transitions x=0",
        "input variable": [
            {"x": "0", "y": "000"},
            {"x": "0", "y": "001"},
            {"x": "0", "y": "010"},
            {"x": "0", "y": "011"},
            {"x": "0", "y": "100"},
        ],
    }
    scenarios.append(scenario1)

    # Scenario 2: Basic State Transitions x=1
    scenario2 = {
        "scenario": "Basic State Transitions x=1",
        "input variable": [
            {"x": "1", "y": "000"},
            {"x": "1", "y": "001"},
            {"x": "1", "y": "010"},
            {"x": "1", "y": "011"},
            {"x": "1", "y": "100"},
        ],
    }
    scenarios.append(scenario2)

    # Scenario 3: Output Generation
    scenario3 = {
        "scenario": "Output Generation",
        "input variable": [
            {"x": "0", "y": "000"},
            {"x": "0", "y": "001"},
            {"x": "0", "y": "010"},
            {"x": "0", "y": "011"},
            {"x": "0", "y": "100"},
        ],
    }
    scenarios.append(scenario3)

    # Scenario 4: Invalid State Handling
    scenario4 = {
        "scenario": "Invalid State Handling",
        "input variable": [
            {"x": "0", "y": "101"},
            {"x": "0", "y": "110"},
            {"x": "0", "y": "111"},
            {"x": "1", "y": "101"},
            {"x": "1", "y": "110"},
            {"x": "1", "y": "111"},
        ],
    }
    scenarios.append(scenario4)

    # Scenario 5: Multiple Clock Cycles
    scenario5 = {
        "scenario": "Multiple Clock Cycles",
        "input variable": [
            {"x": "0", "y": "000"},
            {"x": "0", "y": "000"},
            {"x": "1", "y": "000"},
            {"x": "1", "y": "001"},
            {"x": "0", "y": "100"},
            {"x": "0", "y": "011"},
        ],
    }
    scenarios.append(scenario5)

    # Scenario 6: Rapid Input Changes
    scenario6 = {
        "scenario": "Rapid Input Changes",
        "input variable": [
            {"x": "0", "y": "000"},
            {"x": "1", "y": "000"},
            {"x": "0", "y": "000"},
            {"x": "1", "y": "000"},
            {"x": "0", "y": "001"},
            {"x": "1", "y": "001"},
        ],
    }
    scenarios.append(scenario6)

    # Scenario 7: State Loops
    scenario7 = {
        "scenario": "State Loops",
        "input variable": [
            {"x": "0", "y": "000"},
            {"x": "1", "y": "000"},
            {"x": "0", "y": "001"},
            {"x": "1", "y": "001"},
            {"x": "0", "y": "100"},
            {"x": "1", "y": "100"},
        ],
    }
    scenarios.append(scenario7)

    # Scenario 8: Clock Edge Sensitivity
    scenario8 = {
        "scenario": "Clock Edge Sensitivity",
        "input variable": [
            {"x": "0", "y": "000"},
            {"x": "0", "y": "000"},
            {"x": "1", "y": "000"},
            {"x": "1", "y": "000"},
            {"x": "0", "y": "001"},
            {"x": "0", "y": "001"},
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
