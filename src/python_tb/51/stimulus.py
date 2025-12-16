import json

from cocotb.binary import BinaryValue


def create_binary_input(value, width=3):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Mapping Verification
    scenario1 = {
        "scenario": "Basic Mapping Verification",
        "input variable": [{"a": create_binary_input(i)} for i in range(8)],
    }
    scenarios.append(scenario1)

    # Scenario 2: Random Access Pattern
    scenario2 = {
        "scenario": "Random Access Pattern",
        "input variable": [
            {"a": create_binary_input(4)},
            {"a": create_binary_input(1)},
            {"a": create_binary_input(1)},
            {"a": create_binary_input(3)},
            {"a": create_binary_input(5)},
        ],
    }
    scenarios.append(scenario2)

    # Scenario 3: Rapid Input Changes
    scenario3 = {
        "scenario": "Rapid Input Changes",
        "input variable": [
            {"a": create_binary_input(i)} for i in [0, 7, 1, 6, 2, 5, 3, 4]
        ],
    }
    scenarios.append(scenario3)

    # Scenario 4: Input Stability
    scenario4 = {
        "scenario": "Input Stability",
        "input variable": [{"a": create_binary_input(2)} for _ in range(10)],
    }
    scenarios.append(scenario4)

    # Scenario 5: X-Value Handling
    # Note: Since we can't use 'X', we'll transition from valid values
    scenario5 = {
        "scenario": "X-Value Handling",
        "input variable": [
            {"a": create_binary_input(0)},
            {"a": create_binary_input(3)},
            {"a": create_binary_input(7)},
        ],
    }
    scenarios.append(scenario5)

    # Scenario 6: Multiple Transitions
    scenario6 = {
        "scenario": "Multiple Transitions",
        "input variable": [{"a": create_binary_input(1)} for _ in range(5)],
    }
    scenarios.append(scenario6)

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
