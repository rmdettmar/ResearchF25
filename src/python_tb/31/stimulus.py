import json

from cocotb.binary import BinaryValue


def create_binary_str(value, width=1):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Load Operation
    load_op = {
        "scenario": "Load Operation",
        "input variable": [
            {"clk": "0", "L": "1", "q_in": "0", "r_in": "0"},
            {"clk": "1", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "0", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "1", "L": "1", "q_in": "0", "r_in": "0"},
        ],
    }
    scenarios.append(load_op)

    # Scenario 2: Feedback Path
    feedback = {
        "scenario": "Feedback Path",
        "input variable": [
            {"clk": "0", "L": "0", "q_in": "0", "r_in": "0"},
            {"clk": "1", "L": "0", "q_in": "1", "r_in": "0"},
            {"clk": "0", "L": "0", "q_in": "1", "r_in": "0"},
            {"clk": "1", "L": "0", "q_in": "0", "r_in": "0"},
        ],
    }
    scenarios.append(feedback)

    # Scenario 3: Load-to-Feedback Transition
    transition = {
        "scenario": "Load-to-Feedback Transition",
        "input variable": [
            {"clk": "0", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "1", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "0", "L": "0", "q_in": "1", "r_in": "0"},
            {"clk": "1", "L": "0", "q_in": "1", "r_in": "0"},
        ],
    }
    scenarios.append(transition)

    # Scenario 4: Clock Edge Sensitivity
    clock_edge = {
        "scenario": "Clock Edge Sensitivity",
        "input variable": [
            {"clk": "0", "L": "1", "q_in": "0", "r_in": "0"},
            {"clk": "0", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "1", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "1", "L": "1", "q_in": "1", "r_in": "0"},
        ],
    }
    scenarios.append(clock_edge)

    # Scenario 5: Setup/Hold Time
    setup_hold = {
        "scenario": "Setup/Hold Time",
        "input variable": [
            {"clk": "0", "L": "1", "q_in": "0", "r_in": "0"},
            {"clk": "0", "L": "1", "q_in": "1", "r_in": "1"},
            {"clk": "1", "L": "1", "q_in": "1", "r_in": "1"},
            {"clk": "1", "L": "0", "q_in": "0", "r_in": "0"},
        ],
    }
    scenarios.append(setup_hold)

    # Scenario 6: Rapid Toggle
    rapid_toggle = {
        "scenario": "Rapid Toggle",
        "input variable": [
            {"clk": "0", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "1", "L": "0", "q_in": "1", "r_in": "0"},
            {"clk": "0", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "1", "L": "0", "q_in": "1", "r_in": "0"},
        ],
    }
    scenarios.append(rapid_toggle)

    # Scenario 7: Initial Power-up
    power_up = {
        "scenario": "Initial Power-up",
        "input variable": [
            {"clk": "0", "L": "0", "q_in": "0", "r_in": "0"},
            {"clk": "1", "L": "0", "q_in": "0", "r_in": "0"},
            {"clk": "0", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "1", "L": "1", "q_in": "0", "r_in": "1"},
        ],
    }
    scenarios.append(power_up)

    # Scenario 8: Long-term Stability
    stability = {
        "scenario": "Long-term Stability",
        "input variable": [
            {"clk": "0", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "1", "L": "1", "q_in": "0", "r_in": "1"},
            {"clk": "0", "L": "0", "q_in": "1", "r_in": "0"},
            {"clk": "1", "L": "0", "q_in": "1", "r_in": "0"},
            {"clk": "0", "L": "0", "q_in": "0", "r_in": "0"},
            {"clk": "1", "L": "0", "q_in": "0", "r_in": "0"},
        ],
    }
    scenarios.append(stability)

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
