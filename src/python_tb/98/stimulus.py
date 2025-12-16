import json

from cocotb.binary import BinaryValue


def create_binary_sequence(value, n_bits=1):
    binary_val = BinaryValue(value=value, n_bits=n_bits)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Reset Functionality
    reset_test = {
        "scenario": "Reset Functionality",
        "input variable": [
            {"clk": "1", "resetn": "0", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "0", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
        ],
    }
    scenarios.append(reset_test)

    # Initial F Pulse
    f_pulse_test = {
        "scenario": "Initial F Pulse",
        "input variable": [
            {"clk": "1", "resetn": "0", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
        ],
    }
    scenarios.append(f_pulse_test)

    # X Sequence Detection
    x_seq_test = {
        "scenario": "X Sequence Detection",
        "input variable": [
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
        ],
    }
    scenarios.append(x_seq_test)

    # Y Input Window Success
    y_success_test = {
        "scenario": "Y Input Window Success",
        "input variable": [
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "1"},
        ],
    }
    scenarios.append(y_success_test)

    # Y Input Window Timeout
    y_timeout_test = {
        "scenario": "Y Input Window Timeout",
        "input variable": [
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
        ],
    }
    scenarios.append(y_timeout_test)

    # Partial X Sequence
    partial_x_test = {
        "scenario": "Partial X Sequence",
        "input variable": [
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
        ],
    }
    scenarios.append(partial_x_test)

    # Reset During Operation
    reset_during_op_test = {
        "scenario": "Reset During Operation",
        "input variable": [
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "0", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
        ],
    }
    scenarios.append(reset_during_op_test)

    # Multiple State Cycles
    multiple_cycles_test = {
        "scenario": "Multiple State Cycles",
        "input variable": [
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "1", "y": "1"},
            {"clk": "1", "resetn": "0", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
        ],
    }
    scenarios.append(multiple_cycles_test)

    # Invalid Y Timing
    invalid_y_test = {
        "scenario": "Invalid Y Timing",
        "input variable": [
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "1"},
        ],
    }
    scenarios.append(invalid_y_test)

    # Glitch Immunity
    glitch_test = {
        "scenario": "Glitch Immunity",
        "input variable": [
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
            {"clk": "1", "resetn": "1", "x": "0", "y": "1"},
            {"clk": "1", "resetn": "1", "x": "1", "y": "0"},
        ],
    }
    scenarios.append(glitch_test)

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
