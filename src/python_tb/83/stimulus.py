import json

from cocotb.binary import BinaryValue


def get_binary_str(value, width=8):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Valid Scancode Detection
    valid_codes = [0x45, 0x16, 0x1E, 0x26, 0x25, 0x2E, 0x36, 0x3D, 0x3E, 0x46]
    scenario1 = {
        "scenario": "Valid Scancode Detection",
        "input variable": [{"code": get_binary_str(code)} for code in valid_codes],
    }
    scenarios.append(scenario1)

    # Scenario 2: Invalid Scancode Handling
    invalid_codes = [0x00, 0xFF, 0x20, 0x30, 0x40]
    scenario2 = {
        "scenario": "Invalid Scancode Handling",
        "input variable": [{"code": get_binary_str(code)} for code in invalid_codes],
    }
    scenarios.append(scenario2)

    # Scenario 3: Boundary Value Testing
    boundary_codes = [0x44, 0x47, 0x15, 0x17, 0x1D, 0x1F]
    scenario3 = {
        "scenario": "Boundary Value Testing",
        "input variable": [{"code": get_binary_str(code)} for code in boundary_codes],
    }
    scenarios.append(scenario3)

    # Scenario 4: Sequential Pattern Testing
    seq_codes = [0x45, 0x00, 0x16, 0xFF, 0x1E, 0x20]
    scenario4 = {
        "scenario": "Sequential Pattern Testing",
        "input variable": [{"code": get_binary_str(code)} for code in seq_codes],
    }
    scenarios.append(scenario4)

    # Scenario 5: Glitch Detection
    glitch_codes = [0x45, 0x00, 0x45, 0x00, 0x45]
    scenario5 = {
        "scenario": "Glitch Detection",
        "input variable": [{"code": get_binary_str(code)} for code in glitch_codes],
    }
    scenarios.append(scenario5)

    # Scenario 6: Power-on State
    scenario6 = {
        "scenario": "Power-on State",
        "input variable": [{"code": get_binary_str(0x00)}],
    }
    scenarios.append(scenario6)

    # Scenario 7: All-bits Coverage
    walking_ones = [1 << i for i in range(8)]
    walking_zeros = [(0xFF ^ (1 << i)) for i in range(8)]
    scenario7 = {
        "scenario": "All-bits Coverage",
        "input variable": [
            {"code": get_binary_str(code)} for code in walking_ones + walking_zeros
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
