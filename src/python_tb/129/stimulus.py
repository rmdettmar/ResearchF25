import json

from cocotb.binary import BinaryValue


def get_binary_string(value, width=8):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Data Capture
    basic_data = {
        "scenario": "Basic Data Capture",
        "input variable": [
            {"clk": "0", "d": get_binary_string(0x55), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0x55), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0xAA), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0xAA), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0xFF), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0xFF), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0x00), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0x00), "areset": "0"},
        ],
    }
    scenarios.append(basic_data)

    # Scenario 2: Asynchronous Reset Assertion
    async_reset = {
        "scenario": "Asynchronous Reset Assertion",
        "input variable": [
            {"clk": "0", "d": get_binary_string(0xFF), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0xFF), "areset": "1"},
            {"clk": "1", "d": get_binary_string(0xFF), "areset": "1"},
            {"clk": "0", "d": get_binary_string(0xFF), "areset": "1"},
        ],
    }
    scenarios.append(async_reset)

    # Scenario 3: Reset Recovery
    reset_recovery = {
        "scenario": "Reset Recovery",
        "input variable": [
            {"clk": "0", "d": get_binary_string(0xAA), "areset": "1"},
            {"clk": "0", "d": get_binary_string(0xAA), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0xAA), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0xAA), "areset": "0"},
        ],
    }
    scenarios.append(reset_recovery)

    # Scenario 4: Setup Time Verification
    setup_time = {
        "scenario": "Setup Time Verification",
        "input variable": [
            {"clk": "0", "d": get_binary_string(0x00), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0xFF), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0xFF), "areset": "0"},
        ],
    }
    scenarios.append(setup_time)

    # Scenario 5: Hold Time Verification
    hold_time = {
        "scenario": "Hold Time Verification",
        "input variable": [
            {"clk": "0", "d": get_binary_string(0x55), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0x55), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0xAA), "areset": "0"},
        ],
    }
    scenarios.append(hold_time)

    # Scenario 6: Reset During Data Change
    reset_during_change = {
        "scenario": "Reset During Data Change",
        "input variable": [
            {"clk": "0", "d": get_binary_string(0x55), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0xAA), "areset": "1"},
            {"clk": "1", "d": get_binary_string(0xFF), "areset": "1"},
        ],
    }
    scenarios.append(reset_during_change)

    # Scenario 7: Walking Ones Pattern
    walking_ones = {
        "scenario": "Walking Ones Pattern",
        "input variable": [
            {"clk": "0", "d": get_binary_string(0x01), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0x01), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0x02), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0x02), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0x04), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0x04), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0x08), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0x08), "areset": "0"},
        ],
    }
    scenarios.append(walking_ones)

    # Scenario 8: Rapid Toggle
    rapid_toggle = {
        "scenario": "Rapid Toggle",
        "input variable": [
            {"clk": "0", "d": get_binary_string(0x00), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0x00), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0xFF), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0xFF), "areset": "0"},
            {"clk": "0", "d": get_binary_string(0x00), "areset": "0"},
            {"clk": "1", "d": get_binary_string(0x00), "areset": "0"},
        ],
    }
    scenarios.append(rapid_toggle)

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
