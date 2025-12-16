import json

from cocotb.binary import BinaryValue


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Input Combinations
    input_combinations = {"scenario": "All Input Combinations", "input variable": []}
    for i in range(8):
        binary = format(i, "03b")
        input_combinations["input variable"].append(
            {"in1": binary[0], "in2": binary[1], "in3": binary[2]}
        )
    scenarios.append(input_combinations)

    # Scenario 2: XNOR Gate Verification
    xnor_verify = {
        "scenario": "XNOR Gate Verification",
        "input variable": [
            {"in1": "0", "in2": "0", "in3": "0"},
            {"in1": "0", "in2": "1", "in3": "0"},
            {"in1": "1", "in2": "0", "in3": "0"},
            {"in1": "1", "in2": "1", "in3": "0"},
        ],
    }
    scenarios.append(xnor_verify)

    # Scenario 3: XOR Gate Verification
    xor_verify = {
        "scenario": "XOR Gate Verification",
        "input variable": [
            {"in1": "1", "in2": "1", "in3": "0"},
            {"in1": "1", "in2": "1", "in3": "1"},
            {"in1": "0", "in2": "0", "in3": "0"},
            {"in1": "0", "in2": "0", "in3": "1"},
        ],
    }
    scenarios.append(xor_verify)

    # Scenario 4: Input Transitions
    transitions = {
        "scenario": "Input Transitions",
        "input variable": [
            {"in1": "0", "in2": "0", "in3": "0"},
            {"in1": "1", "in2": "0", "in3": "0"},
            {"in1": "1", "in2": "1", "in3": "0"},
            {"in1": "1", "in2": "1", "in3": "1"},
        ],
    }
    scenarios.append(transitions)

    # Scenario 5: Simultaneous Input Changes
    simultaneous = {
        "scenario": "Simultaneous Input Changes",
        "input variable": [
            {"in1": "0", "in2": "0", "in3": "0"},
            {"in1": "1", "in2": "1", "in3": "1"},
            {"in1": "0", "in2": "0", "in3": "0"},
            {"in1": "1", "in2": "1", "in3": "1"},
        ],
    }
    scenarios.append(simultaneous)

    # Scenario 6: Static Input Values
    static_values = {
        "scenario": "Static Input Values",
        "input variable": [
            {"in1": "1", "in2": "1", "in3": "1"},
            {"in1": "1", "in2": "1", "in3": "1"},
            {"in1": "1", "in2": "1", "in3": "1"},
            {"in1": "1", "in2": "1", "in3": "1"},
        ],
    }
    scenarios.append(static_values)

    # Scenario 7: Glitch Detection
    glitch_detection = {
        "scenario": "Glitch Detection",
        "input variable": [
            {"in1": "0", "in2": "0", "in3": "0"},
            {"in1": "1", "in2": "1", "in3": "0"},
            {"in1": "1", "in2": "0", "in3": "1"},
            {"in1": "0", "in2": "1", "in3": "1"},
        ],
    }
    scenarios.append(glitch_detection)

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
