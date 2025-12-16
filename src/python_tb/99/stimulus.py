import json

from cocotb.binary import BinaryValue


def get_binary_str(value, width=8):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Synchronous Reset Operation
    reset_seq = {
        "scenario": "Synchronous Reset Operation",
        "input variable": [
            {"clk": "0", "reset": "1", "d": get_binary_str(0xFF)},
            {"clk": "1", "reset": "1", "d": get_binary_str(0xFF)},
            {"clk": "0", "reset": "1", "d": get_binary_str(0xAA)},
            {"clk": "1", "reset": "1", "d": get_binary_str(0xAA)},
        ],
    }
    scenarios.append(reset_seq)

    # Scenario 2: Normal Data Capture
    data_capture = {
        "scenario": "Normal Data Capture",
        "input variable": [
            {"clk": "0", "reset": "0", "d": get_binary_str(0x00)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0x00)},
            {"clk": "0", "reset": "0", "d": get_binary_str(0xFF)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0xFF)},
            {"clk": "0", "reset": "0", "d": get_binary_str(0xAA)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0xAA)},
            {"clk": "0", "reset": "0", "d": get_binary_str(0x55)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0x55)},
        ],
    }
    scenarios.append(data_capture)

    # Scenario 3: Reset During Data Change
    reset_during_data = {
        "scenario": "Reset During Data Change",
        "input variable": [
            {"clk": "0", "reset": "1", "d": get_binary_str(0x12)},
            {"clk": "1", "reset": "1", "d": get_binary_str(0x34)},
            {"clk": "0", "reset": "1", "d": get_binary_str(0x56)},
            {"clk": "1", "reset": "1", "d": get_binary_str(0x78)},
        ],
    }
    scenarios.append(reset_during_data)

    # Scenario 4: Setup Time Verification
    setup_time = {
        "scenario": "Setup Time Verification",
        "input variable": [
            {"clk": "1", "reset": "0", "d": get_binary_str(0x00)},
            {"clk": "0", "reset": "0", "d": get_binary_str(0xFF)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0xFF)},
            {"clk": "0", "reset": "0", "d": get_binary_str(0xAA)},
        ],
    }
    scenarios.append(setup_time)

    # Scenario 5: Hold Time Verification
    hold_time = {
        "scenario": "Hold Time Verification",
        "input variable": [
            {"clk": "1", "reset": "0", "d": get_binary_str(0x55)},
            {"clk": "0", "reset": "0", "d": get_binary_str(0x55)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0xAA)},
            {"clk": "0", "reset": "0", "d": get_binary_str(0x55)},
        ],
    }
    scenarios.append(hold_time)

    # Scenario 6: Reset Deactivation
    reset_deactivation = {
        "scenario": "Reset Deactivation",
        "input variable": [
            {"clk": "0", "reset": "1", "d": get_binary_str(0xFF)},
            {"clk": "1", "reset": "1", "d": get_binary_str(0xFF)},
            {"clk": "0", "reset": "0", "d": get_binary_str(0x55)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0x55)},
        ],
    }
    scenarios.append(reset_deactivation)

    # Scenario 7: Glitch Immunity
    glitch_immunity = {
        "scenario": "Glitch Immunity",
        "input variable": [
            {"clk": "1", "reset": "0", "d": get_binary_str(0x00)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0xFF)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0x00)},
            {"clk": "0", "reset": "0", "d": get_binary_str(0xFF)},
        ],
    }
    scenarios.append(glitch_immunity)

    # Scenario 8: Power-On State
    power_on = {
        "scenario": "Power-On State",
        "input variable": [
            {"clk": "0", "reset": "0", "d": get_binary_str(0x00)},
            {"clk": "0", "reset": "0", "d": get_binary_str(0x00)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0x00)},
            {"clk": "1", "reset": "0", "d": get_binary_str(0x00)},
        ],
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
