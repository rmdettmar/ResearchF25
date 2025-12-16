import json

from cocotb.binary import BinaryValue


def decimal_to_binary_dict(decimal_num):
    binary = BinaryValue(value=decimal_num, n_bits=4, bigEndian=False)
    bin_str = binary.binstr
    return {"a": bin_str[3], "b": bin_str[2], "c": bin_str[1], "d": bin_str[0]}


def stimulus_gen():
    scenarios = []

    # Scenario 1: Logic-1 Output Patterns
    logic1_inputs = [2, 7, 15]
    scenario1 = {
        "scenario": "Logic-1 Output Patterns",
        "input variable": [decimal_to_binary_dict(num) for num in logic1_inputs],
    }
    scenarios.append(scenario1)

    # Scenario 2: Logic-0 Output Patterns
    logic0_inputs = [0, 1, 4, 5, 6, 9, 10, 13, 14]
    scenario2 = {
        "scenario": "Logic-0 Output Patterns",
        "input variable": [decimal_to_binary_dict(num) for num in logic0_inputs],
    }
    scenarios.append(scenario2)

    # Scenario 3: Invalid Input Combinations
    invalid_inputs = [3, 8, 11, 12]
    scenario3 = {
        "scenario": "Invalid Input Combinations",
        "input variable": [decimal_to_binary_dict(num) for num in invalid_inputs],
    }
    scenarios.append(scenario3)

    # Scenario 4: Rapid Input Transitions
    transition_sequence = [2, 7, 15, 0, 1, 4]  # Mix of 1s and 0s outputs
    scenario4 = {
        "scenario": "Rapid Input Transitions",
        "input variable": [decimal_to_binary_dict(num) for num in transition_sequence],
    }
    scenarios.append(scenario4)

    # Scenario 5: Output Consistency
    consistency_inputs = [2, 7, 15, 0, 1, 4, 5, 6, 9, 10, 13, 14]
    scenario5 = {
        "scenario": "Output Consistency",
        "input variable": [decimal_to_binary_dict(num) for num in consistency_inputs],
    }
    scenarios.append(scenario5)

    # Scenario 6: All Possible Combinations
    all_combinations = list(range(16))
    scenario6 = {
        "scenario": "All Possible Combinations",
        "input variable": [decimal_to_binary_dict(num) for num in all_combinations],
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
