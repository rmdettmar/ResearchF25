import json

from cocotb.binary import BinaryValue


def bin_str(value, width=4):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Specified Zero Outputs
    zero_outputs = {
        "scenario": "Specified Zero Outputs",
        "input variable": [
            {"x": bin_str(0b0001)},
            {"x": bin_str(0b0110)},
            {"x": bin_str(0b0100)},
        ],
    }
    scenarios.append(zero_outputs)

    # Scenario 2: Specified One Outputs
    one_outputs = {
        "scenario": "Specified One Outputs",
        "input variable": [
            {"x": bin_str(0b1000)},
            {"x": bin_str(0b1001)},
            {"x": bin_str(0b1100)},
            {"x": bin_str(0b1101)},
        ],
    }
    scenarios.append(one_outputs)

    # Scenario 3: Don't Care Conditions
    dont_care = {
        "scenario": "Don't Care Conditions",
        "input variable": [
            {"x": bin_str(0b0000)},
            {"x": bin_str(0b0010)},
            {"x": bin_str(0b0011)},
            {"x": bin_str(0b0111)},
            {"x": bin_str(0b1010)},
            {"x": bin_str(0b1011)},
        ],
    }
    scenarios.append(dont_care)

    # Scenario 4: Adjacent Cell Transitions
    transitions = {
        "scenario": "Adjacent Cell Transitions",
        "input variable": [
            {"x": bin_str(0b0100)},
            {"x": bin_str(0b0101)},
            {"x": bin_str(0b0110)},
        ],
    }
    scenarios.append(transitions)

    # Scenario 5: Boundary Value Analysis
    boundary = {
        "scenario": "Boundary Value Analysis",
        "input variable": [{"x": bin_str(0b0000)}, {"x": bin_str(0b1111)}],
    }
    scenarios.append(boundary)

    # Scenario 6: Single Bit Changes
    single_bit = {
        "scenario": "Single Bit Changes",
        "input variable": [
            {"x": bin_str(0b0000)},
            {"x": bin_str(0b0001)},
            {"x": bin_str(0b0010)},
            {"x": bin_str(0b0100)},
            {"x": bin_str(0b1000)},
        ],
    }
    scenarios.append(single_bit)

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
