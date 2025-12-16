import json

from cocotb.binary import BinaryValue


def generate_truth_table_combinations(num_bits):
    combinations = []
    for i in range(2**num_bits):
        binary = BinaryValue(value=i, n_bits=num_bits, bigEndian=True)
        combinations.append(binary.binstr)
    return combinations


def create_input_dict(p1a, p1b, p1c, p1d, p1e, p1f, p2a, p2b, p2c, p2d):
    return {
        "p1a": p1a,
        "p1b": p1b,
        "p1c": p1c,
        "p1d": p1d,
        "p1e": p1e,
        "p1f": p1f,
        "p2a": p2a,
        "p2b": p2b,
        "p2c": p2c,
        "p2d": p2d,
    }


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic P1Y Functionality
    scenario1 = {
        "scenario": "Basic P1Y Functionality",
        "input variable": [
            create_input_dict("1", "1", "1", "0", "0", "0", "0", "0", "0", "0"),
            create_input_dict("0", "0", "0", "1", "1", "1", "0", "0", "0", "0"),
        ],
    }
    scenarios.append(scenario1)

    # Scenario 2: Basic P2Y Functionality
    scenario2 = {
        "scenario": "Basic P2Y Functionality",
        "input variable": [
            create_input_dict("0", "0", "0", "0", "0", "0", "1", "1", "0", "0"),
            create_input_dict("0", "0", "0", "0", "0", "0", "0", "0", "1", "1"),
        ],
    }
    scenarios.append(scenario2)

    # Scenario 3: P1Y Complete Truth Table
    p1_combinations = generate_truth_table_combinations(6)
    scenario3 = {"scenario": "P1Y Complete Truth Table", "input variable": []}
    for combo in p1_combinations:
        scenario3["input variable"].append(
            create_input_dict(
                combo[0],
                combo[1],
                combo[2],
                combo[3],
                combo[4],
                combo[5],
                "0",
                "0",
                "0",
                "0",
            )
        )
    scenarios.append(scenario3)

    # Scenario 4: P2Y Complete Truth Table
    p2_combinations = generate_truth_table_combinations(4)
    scenario4 = {"scenario": "P2Y Complete Truth Table", "input variable": []}
    for combo in p2_combinations:
        scenario4["input variable"].append(
            create_input_dict(
                "0", "0", "0", "0", "0", "0", combo[0], combo[1], combo[2], combo[3]
            )
        )
    scenarios.append(scenario4)

    # Scenario 5: Simultaneous Output Changes
    scenario5 = {
        "scenario": "Simultaneous Output Changes",
        "input variable": [
            create_input_dict("1", "1", "1", "0", "0", "0", "1", "1", "0", "0"),
            create_input_dict("0", "0", "0", "1", "1", "1", "0", "0", "1", "1"),
            create_input_dict("1", "1", "1", "1", "1", "1", "1", "1", "1", "1"),
            create_input_dict("0", "0", "0", "0", "0", "0", "0", "0", "0", "0"),
        ],
    }
    scenarios.append(scenario5)

    # Scenario 6: Input Transition Times
    scenario6 = {
        "scenario": "Input Transition Times",
        "input variable": [
            create_input_dict("0", "0", "0", "0", "0", "0", "0", "0", "0", "0"),
            create_input_dict("1", "0", "0", "0", "0", "0", "1", "0", "0", "0"),
            create_input_dict("1", "1", "0", "0", "0", "0", "1", "1", "0", "0"),
            create_input_dict("1", "1", "1", "0", "0", "0", "1", "1", "1", "0"),
            create_input_dict("1", "1", "1", "1", "0", "0", "1", "1", "1", "1"),
        ],
    }
    scenarios.append(scenario6)

    # Scenario 7: Glitch Detection
    scenario7 = {
        "scenario": "Glitch Detection",
        "input variable": [
            create_input_dict("1", "1", "1", "0", "0", "0", "1", "1", "0", "0"),
            create_input_dict("0", "1", "1", "1", "0", "0", "0", "1", "1", "0"),
            create_input_dict("0", "0", "1", "1", "1", "0", "0", "0", "1", "1"),
            create_input_dict("0", "0", "0", "1", "1", "1", "0", "0", "0", "1"),
        ],
    }
    scenarios.append(scenario7)

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
