import json

from cocotb.binary import BinaryValue


def get_binary_str(value, width=8):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Single Bit Transition
    single_bit = {
        "scenario": "Single Bit Transition",
        "input variable": [
            {"in": "00000000"},
            {"in": "00000001"},
            {"in": "00000000"},
            {"in": "00010000"},
            {"in": "00000000"},
        ],
    }
    scenarios.append(single_bit)

    # Scenario 2: Multiple Simultaneous Transitions
    multi_trans = {
        "scenario": "Multiple Simultaneous Transitions",
        "input variable": [
            {"in": "00000000"},
            {"in": "11111111"},
            {"in": "00000000"},
            {"in": "10101010"},
        ],
    }
    scenarios.append(multi_trans)

    # Scenario 3: Consecutive Transitions
    consec_trans = {
        "scenario": "Consecutive Transitions",
        "input variable": [
            {"in": "00000000"},
            {"in": "11111111"},
            {"in": "00000000"},
            {"in": "11111111"},
            {"in": "00000000"},
        ],
    }
    scenarios.append(consec_trans)

    # Scenario 4: No Change Detection
    no_change = {
        "scenario": "No Change Detection",
        "input variable": [
            {"in": "00000000"},
            {"in": "00000000"},
            {"in": "11111111"},
            {"in": "11111111"},
        ],
    }
    scenarios.append(no_change)

    # Scenario 5: Alternating Patterns
    alt_patterns = {
        "scenario": "Alternating Patterns",
        "input variable": [
            {"in": "10101010"},
            {"in": "01010101"},
            {"in": "10101010"},
            {"in": "01010101"},
        ],
    }
    scenarios.append(alt_patterns)

    # Scenario 6: Walking Ones/Zeros
    walking = {
        "scenario": "Walking Ones/Zeros",
        "input variable": [
            {"in": "00000001"},
            {"in": "00000010"},
            {"in": "00000100"},
            {"in": "00001000"},
            {"in": "00010000"},
            {"in": "00100000"},
            {"in": "01000000"},
            {"in": "10000000"},
        ],
    }
    scenarios.append(walking)

    # Scenario 7: Setup Time Verification
    setup_time = {
        "scenario": "Setup Time Verification",
        "input variable": [
            {"in": "00000000"},
            {"in": "11111111"},
            {"in": "00000000"},
            {"in": "11111111"},
        ],
    }
    scenarios.append(setup_time)

    # Scenario 8: Power-On State
    power_on = {
        "scenario": "Power-On State",
        "input variable": [{"in": "00000000"}, {"in": "00000000"}, {"in": "00000000"}],
    }
    scenarios.append(power_on)

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
