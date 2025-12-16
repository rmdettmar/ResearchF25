import json

from cocotb.binary import BinaryValue


def get_truth_table_sequence():
    inputs = []
    for i in range(8):
        binary = format(i, "03b")
        inputs.append({"x3": binary[0], "x2": binary[1], "x1": binary[2]})
    return inputs


def get_single_transitions():
    inputs = []
    base_patterns = ["000", "001", "010", "011", "100", "101", "110", "111"]
    for pattern in base_patterns:
        for bit in range(3):
            new_pattern = list(pattern)
            new_pattern[bit] = "1" if pattern[bit] == "0" else "0"
            inputs.append({"x3": pattern[0], "x2": pattern[1], "x1": pattern[2]})
            inputs.append(
                {"x3": new_pattern[0], "x2": new_pattern[1], "x1": new_pattern[2]}
            )
    return inputs


def get_gray_code_sequence():
    gray_code = ["000", "001", "011", "010", "110", "111", "101", "100"]
    return [{"x3": code[0], "x2": code[1], "x1": code[2]} for code in gray_code]


def stimulus_gen():
    scenarios = []

    # Scenario 1: Truth Table Verification
    scenarios.append(
        {
            "scenario": "Truth Table Verification",
            "input variable": get_truth_table_sequence(),
        }
    )

    # Scenario 2: Input Transitions
    scenarios.append(
        {"scenario": "Input Transitions", "input variable": get_single_transitions()}
    )

    # Scenario 3: Simultaneous Input Changes
    scenarios.append(
        {
            "scenario": "Simultaneous Input Changes",
            "input variable": [
                {"x3": "0", "x2": "0", "x1": "0"},
                {"x3": "1", "x2": "1", "x1": "1"},
                {"x3": "0", "x2": "1", "x1": "1"},
                {"x3": "1", "x2": "0", "x1": "0"},
            ],
        }
    )

    # Scenario 4: Static Input Stability
    scenarios.append(
        {
            "scenario": "Static Input Stability",
            "input variable": [{"x3": "1", "x2": "0", "x1": "1"}] * 10,
        }
    )

    # Scenario 5: Gray Code Sequence
    scenarios.append(
        {"scenario": "Gray Code Sequence", "input variable": get_gray_code_sequence()}
    )

    # Scenario 6: Random Input Patterns
    import random

    random_patterns = []
    for _ in range(10):
        val = random.randint(0, 7)
        binary = format(val, "03b")
        random_patterns.append({"x3": binary[0], "x2": binary[1], "x1": binary[2]})
    scenarios.append(
        {"scenario": "Random Input Patterns", "input variable": random_patterns}
    )

    # Scenario 7: Propagation Delay
    scenarios.append(
        {
            "scenario": "Propagation Delay",
            "input variable": [
                {"x3": "0", "x2": "0", "x1": "0"},
                {"x3": "0", "x2": "1", "x1": "0"},
                {"x3": "1", "x2": "0", "x1": "1"},
                {"x3": "1", "x2": "1", "x1": "1"},
            ],
        }
    )

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
