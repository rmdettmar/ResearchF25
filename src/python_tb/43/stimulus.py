import json

from cocotb.binary import BinaryValue


def generate_binary_string(value, width):
    binary = BinaryValue(value=value, n_bits=width)
    return binary.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Shift Operation
    shift_scenario = {
        "scenario": "Basic Shift Operation",
        "input variable": [
            {"enable": "1", "S": "1", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "0", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "1", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "0", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "1", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "0", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "1", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "0", "A": "0", "B": "0", "C": "0"},
        ],
    }
    scenarios.append(shift_scenario)

    # Scenario 2: Disabled Shift Operation
    disabled_scenario = {
        "scenario": "Disabled Shift Operation",
        "input variable": [
            {"enable": "0", "S": "1", "A": "0", "B": "0", "C": "0"},
            {"enable": "0", "S": "0", "A": "0", "B": "0", "C": "0"},
            {"enable": "0", "S": "1", "A": "0", "B": "0", "C": "0"},
            {"enable": "0", "S": "0", "A": "0", "B": "0", "C": "0"},
        ],
    }
    scenarios.append(disabled_scenario)

    # Scenario 3: Random Access Read
    read_scenario = {
        "scenario": "Random Access Read",
        "input variable": [
            {"enable": "0", "S": "0", "A": "0", "B": "0", "C": "0"},
            {"enable": "0", "S": "0", "A": "0", "B": "0", "C": "1"},
            {"enable": "0", "S": "0", "A": "0", "B": "1", "C": "0"},
            {"enable": "0", "S": "0", "A": "0", "B": "1", "C": "1"},
            {"enable": "0", "S": "0", "A": "1", "B": "0", "C": "0"},
            {"enable": "0", "S": "0", "A": "1", "B": "0", "C": "1"},
            {"enable": "0", "S": "0", "A": "1", "B": "1", "C": "0"},
            {"enable": "0", "S": "0", "A": "1", "B": "1", "C": "1"},
        ],
    }
    scenarios.append(read_scenario)

    # Scenario 4: Address Transition
    addr_transition = {
        "scenario": "Address Transition",
        "input variable": [
            {"enable": "0", "S": "0", "A": "0", "B": "0", "C": "0"},
            {"enable": "0", "S": "0", "A": "1", "B": "1", "C": "1"},
            {"enable": "0", "S": "0", "A": "0", "B": "1", "C": "0"},
            {"enable": "0", "S": "0", "A": "1", "B": "0", "C": "1"},
        ],
    }
    scenarios.append(addr_transition)

    # Scenario 5: Simultaneous Shift and Read
    simul_scenario = {
        "scenario": "Simultaneous Shift and Read",
        "input variable": [
            {"enable": "1", "S": "1", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "0", "A": "0", "B": "0", "C": "1"},
            {"enable": "1", "S": "1", "A": "0", "B": "1", "C": "0"},
            {"enable": "1", "S": "0", "A": "0", "B": "1", "C": "1"},
        ],
    }
    scenarios.append(simul_scenario)

    # Scenario 6: Enable Toggle
    toggle_scenario = {
        "scenario": "Enable Toggle",
        "input variable": [
            {"enable": "1", "S": "1", "A": "0", "B": "0", "C": "0"},
            {"enable": "0", "S": "0", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "1", "A": "0", "B": "0", "C": "0"},
            {"enable": "0", "S": "0", "A": "0", "B": "0", "C": "0"},
        ],
    }
    scenarios.append(toggle_scenario)

    # Scenario 7: Setup and Hold Time
    timing_scenario = {
        "scenario": "Setup and Hold Time",
        "input variable": [
            {"enable": "1", "S": "1", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "0", "A": "0", "B": "0", "C": "0"},
            {"enable": "1", "S": "1", "A": "0", "B": "0", "C": "0"},
        ],
    }
    scenarios.append(timing_scenario)

    # Scenario 8: Power-on State
    poweron_scenario = {
        "scenario": "Power-on State",
        "input variable": [{"enable": "0", "S": "0", "A": "0", "B": "0", "C": "0"}],
    }
    scenarios.append(poweron_scenario)

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
