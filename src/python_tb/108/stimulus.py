import json

from cocotb.binary import BinaryValue


def gen_binary_str(value, width=2):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Equal Values
    equal_values = {
        "scenario": "All Equal Values",
        "input variable": [
            {"A": gen_binary_str(0), "B": gen_binary_str(0)},
            {"A": gen_binary_str(1), "B": gen_binary_str(1)},
            {"A": gen_binary_str(2), "B": gen_binary_str(2)},
            {"A": gen_binary_str(3), "B": gen_binary_str(3)},
        ],
    }
    scenarios.append(equal_values)

    # Scenario 2: All Unequal Values
    unequal_values = {"scenario": "All Unequal Values", "input variable": []}
    for a in range(4):
        for b in range(4):
            if a != b:
                unequal_values["input variable"].append(
                    {"A": gen_binary_str(a), "B": gen_binary_str(b)}
                )
    scenarios.append(unequal_values)

    # Scenario 3: Boundary Transitions
    boundary_trans = {
        "scenario": "Boundary Transitions",
        "input variable": [
            {"A": gen_binary_str(0), "B": gen_binary_str(3)},
            {"A": gen_binary_str(3), "B": gen_binary_str(0)},
            {"A": gen_binary_str(3), "B": gen_binary_str(3)},
            {"A": gen_binary_str(0), "B": gen_binary_str(0)},
        ],
    }
    scenarios.append(boundary_trans)

    # Scenario 4: Adjacent Value Comparison
    adjacent_values = {
        "scenario": "Adjacent Value Comparison",
        "input variable": [
            {"A": gen_binary_str(0), "B": gen_binary_str(1)},
            {"A": gen_binary_str(1), "B": gen_binary_str(2)},
            {"A": gen_binary_str(2), "B": gen_binary_str(3)},
        ],
    }
    scenarios.append(adjacent_values)

    # Scenario 5: Rapid Input Changes
    rapid_changes = {
        "scenario": "Rapid Input Changes",
        "input variable": [
            {"A": gen_binary_str(0), "B": gen_binary_str(0)},
            {"A": gen_binary_str(1), "B": gen_binary_str(0)},
            {"A": gen_binary_str(2), "B": gen_binary_str(2)},
            {"A": gen_binary_str(3), "B": gen_binary_str(2)},
            {"A": gen_binary_str(3), "B": gen_binary_str(3)},
        ],
    }
    scenarios.append(rapid_changes)

    # Scenario 6: Simultaneous Input Changes
    simultaneous_changes = {
        "scenario": "Simultaneous Input Changes",
        "input variable": [
            {"A": gen_binary_str(0), "B": gen_binary_str(0)},
            {"A": gen_binary_str(1), "B": gen_binary_str(1)},
            {"A": gen_binary_str(2), "B": gen_binary_str(3)},
            {"A": gen_binary_str(3), "B": gen_binary_str(2)},
        ],
    }
    scenarios.append(simultaneous_changes)

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
