import json

from cocotb.binary import BinaryValue


def get_binary_str(value, width=8):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Data Capture
    basic_data = {
        "scenario": "Basic Data Capture",
        "input variable": [
            {"d": get_binary_str(0x00)},  # All zeros
            {"d": get_binary_str(0xFF)},  # All ones
            {"d": get_binary_str(0x55)},  # Alternating 0,1
            {"d": get_binary_str(0xAA)},  # Alternating 1,0
        ],
    }
    scenarios.append(basic_data)

    # Scenario 2: Setup Time Verification
    setup_time = {
        "scenario": "Setup Time Verification",
        "input variable": [
            {"d": get_binary_str(0x55)},
            {"d": get_binary_str(0xAA)},
            {"d": get_binary_str(0x33)},
            {"d": get_binary_str(0xCC)},
        ],
    }
    scenarios.append(setup_time)

    # Scenario 3: Hold Time Verification
    hold_time = {
        "scenario": "Hold Time Verification",
        "input variable": [
            {"d": get_binary_str(0x0F)},
            {"d": get_binary_str(0xF0)},
            {"d": get_binary_str(0x3C)},
            {"d": get_binary_str(0xC3)},
        ],
    }
    scenarios.append(hold_time)

    # Scenario 4: Alternating Bits Pattern
    alternating = {
        "scenario": "Alternating Bits Pattern",
        "input variable": [
            {"d": get_binary_str(0x01)},
            {"d": get_binary_str(0x02)},
            {"d": get_binary_str(0x04)},
            {"d": get_binary_str(0x08)},
            {"d": get_binary_str(0x10)},
            {"d": get_binary_str(0x20)},
            {"d": get_binary_str(0x40)},
            {"d": get_binary_str(0x80)},
        ],
    }
    scenarios.append(alternating)

    # Scenario 5: Rapid Data Changes
    rapid_changes = {
        "scenario": "Rapid Data Changes",
        "input variable": [
            {"d": get_binary_str(0x55)},
            {"d": get_binary_str(0xAA)},
            {"d": get_binary_str(0x33)},
            {"d": get_binary_str(0xCC)},
            {"d": get_binary_str(0x0F)},
        ],
    }
    scenarios.append(rapid_changes)

    # Scenario 6: Power-on State
    power_on = {
        "scenario": "Power-on State",
        "input variable": [{"d": get_binary_str(0x00)}],
    }
    scenarios.append(power_on)

    # Scenario 7: Clock Glitch Immunity
    clock_glitch = {
        "scenario": "Clock Glitch Immunity",
        "input variable": [
            {"d": get_binary_str(0x55)},
            {"d": get_binary_str(0xAA)},
            {"d": get_binary_str(0x33)},
        ],
    }
    scenarios.append(clock_glitch)

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
