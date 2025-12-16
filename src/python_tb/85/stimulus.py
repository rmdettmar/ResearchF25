import json


def stimulus_gen():
    scenarios = []

    # Helper function to create input dictionary
    def create_input_dict(a_val, b_val, c_val, d_val):
        return {"a": f"{a_val}", "b": f"{b_val}", "c": f"{c_val}", "d": f"{d_val}"}

    # Scenario 1: Basic Truth Table Verification
    basic_truth = {
        "scenario": "Basic Truth Table Verification",
        "input variable": [
            create_input_dict("0", "0", "0", "0"),
            create_input_dict("1", "0", "0", "0"),
            create_input_dict("0", "1", "0", "1"),
            create_input_dict("1", "1", "1", "1"),
            create_input_dict("1", "0", "1", "1"),
        ],
    }
    scenarios.append(basic_truth)

    # Scenario 2: Don't Care Conditions
    dont_care = {
        "scenario": "Dont Care Conditions",
        "input variable": [
            create_input_dict("0", "1", "0", "0"),
            create_input_dict("1", "0", "0", "1"),
            create_input_dict("1", "1", "0", "1"),
        ],
    }
    scenarios.append(dont_care)

    # Scenario 3: Input Transitions
    transitions = {
        "scenario": "Input Transitions",
        "input variable": [
            create_input_dict("0", "0", "0", "0"),
            create_input_dict("0", "1", "0", "0"),
            create_input_dict("1", "0", "0", "0"),
            create_input_dict("1", "1", "0", "0"),
        ],
    }
    scenarios.append(transitions)

    # Scenario 4: All Zeros Input
    all_zeros = {
        "scenario": "All Zeros Input",
        "input variable": [create_input_dict("0", "0", "0", "0")],
    }
    scenarios.append(all_zeros)

    # Scenario 5: All Ones Input
    all_ones = {
        "scenario": "All Ones Input",
        "input variable": [create_input_dict("1", "1", "1", "1")],
    }
    scenarios.append(all_ones)

    # Scenario 6: Alternating Patterns
    alternating = {
        "scenario": "Alternating Patterns",
        "input variable": [
            create_input_dict("0", "1", "0", "1"),
            create_input_dict("1", "0", "1", "0"),
            create_input_dict("0", "1", "0", "1"),
            create_input_dict("1", "0", "1", "0"),
        ],
    }
    scenarios.append(alternating)

    # Scenario 7: Rapid Input Changes
    rapid_changes = {
        "scenario": "Rapid Input Changes",
        "input variable": [
            create_input_dict("0", "0", "0", "0"),
            create_input_dict("1", "1", "1", "1"),
            create_input_dict("0", "0", "0", "0"),
            create_input_dict("1", "1", "1", "1"),
        ],
    }
    scenarios.append(rapid_changes)

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
