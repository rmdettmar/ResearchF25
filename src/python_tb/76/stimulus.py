import json

from cocotb.binary import BinaryValue


def binary_str(value, width=8):
    return BinaryValue(value=value, n_bits=width, bigEndian=True).binstr


def stimulus_gen():
    scenarios = []

    # Basic Data Loading
    basic_load = {
        "scenario": "Basic Data Loading",
        "input variable": [
            {"d": binary_str(0x55), "reset": "0", "clk": "0"},
            {"d": binary_str(0xAA), "reset": "0", "clk": "0"},
            {"d": binary_str(0xFF), "reset": "0", "clk": "0"},
            {"d": binary_str(0x00), "reset": "0", "clk": "0"},
        ],
    }
    scenarios.append(basic_load)

    # Synchronous Reset Operation
    sync_reset = {
        "scenario": "Synchronous Reset Operation",
        "input variable": [
            {"d": binary_str(0xFF), "reset": "0", "clk": "0"},
            {"d": binary_str(0xFF), "reset": "1", "clk": "0"},
            {"d": binary_str(0xFF), "reset": "1", "clk": "0"},
            {"d": binary_str(0xFF), "reset": "1", "clk": "0"},
        ],
    }
    scenarios.append(sync_reset)

    # Reset Deassert Recovery
    reset_recovery = {
        "scenario": "Reset Deassert Recovery",
        "input variable": [
            {"d": binary_str(0x00), "reset": "1", "clk": "0"},
            {"d": binary_str(0xFF), "reset": "0", "clk": "0"},
            {"d": binary_str(0xFF), "reset": "0", "clk": "0"},
            {"d": binary_str(0xFF), "reset": "0", "clk": "0"},
        ],
    }
    scenarios.append(reset_recovery)

    # Setup Time Verification
    setup_time = {
        "scenario": "Setup Time Verification",
        "input variable": [
            {"d": binary_str(0x55), "reset": "0", "clk": "0"},
            {"d": binary_str(0xAA), "reset": "0", "clk": "0"},
            {"d": binary_str(0xFF), "reset": "0", "clk": "0"},
        ],
    }
    scenarios.append(setup_time)

    # Hold Time Verification
    hold_time = {
        "scenario": "Hold Time Verification",
        "input variable": [
            {"d": binary_str(0x55), "reset": "0", "clk": "0"},
            {"d": binary_str(0x55), "reset": "0", "clk": "1"},
            {"d": binary_str(0xAA), "reset": "0", "clk": "1"},
        ],
    }
    scenarios.append(hold_time)

    # Alternating Bits Pattern
    alternating = {
        "scenario": "Alternating Bits Pattern",
        "input variable": [
            {"d": binary_str(0x55), "reset": "0", "clk": "0"},
            {"d": binary_str(0xAA), "reset": "0", "clk": "0"},
            {"d": binary_str(0x55), "reset": "0", "clk": "0"},
            {"d": binary_str(0xAA), "reset": "0", "clk": "0"},
        ],
    }
    scenarios.append(alternating)

    # Reset During Data Change
    reset_during_change = {
        "scenario": "Reset During Data Change",
        "input variable": [
            {"d": binary_str(0x55), "reset": "0", "clk": "0"},
            {"d": binary_str(0xAA), "reset": "1", "clk": "0"},
            {"d": binary_str(0xFF), "reset": "1", "clk": "0"},
            {"d": binary_str(0x00), "reset": "1", "clk": "0"},
        ],
    }
    scenarios.append(reset_during_change)

    # Walking Ones Pattern
    walking_ones = {
        "scenario": "Walking Ones Pattern",
        "input variable": [
            {"d": binary_str(0x01), "reset": "0", "clk": "0"},
            {"d": binary_str(0x02), "reset": "0", "clk": "0"},
            {"d": binary_str(0x04), "reset": "0", "clk": "0"},
            {"d": binary_str(0x08), "reset": "0", "clk": "0"},
            {"d": binary_str(0x10), "reset": "0", "clk": "0"},
            {"d": binary_str(0x20), "reset": "0", "clk": "0"},
            {"d": binary_str(0x40), "reset": "0", "clk": "0"},
            {"d": binary_str(0x80), "reset": "0", "clk": "0"},
        ],
    }
    scenarios.append(walking_ones)

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
