import json


def stimulus_gen():
    scenarios = []

    # Helper function to create binary sequence dictionary
    def create_input_dict(x_val, y_val):
        return {"x": str(x_val), "y": str(y_val)}

    # Scenario 1: Static Input Verification
    static_inputs = {
        "scenario": "Static Input Verification",
        "input variable": [
            create_input_dict("0", "0"),
            create_input_dict("0", "1"),
            create_input_dict("1", "0"),
            create_input_dict("1", "1"),
        ],
    }
    scenarios.append(static_inputs)

    # Scenario 2: Module A Functionality
    module_a_test = {
        "scenario": "Module A Functionality",
        "input variable": [
            create_input_dict("0", "0"),
            create_input_dict("0", "1"),
            create_input_dict("1", "0"),
            create_input_dict("1", "1"),
        ],
    }
    scenarios.append(module_a_test)

    # Scenario 3: Module B Timing Pattern
    module_b_timing = {
        "scenario": "Module B Timing Pattern",
        "input variable": [
            create_input_dict("0", "0"),
            create_input_dict("1", "0"),
            create_input_dict("0", "1"),
            create_input_dict("1", "1"),
            create_input_dict("0", "0"),
            create_input_dict("0", "1"),
            create_input_dict("1", "1"),
            create_input_dict("0", "1"),
            create_input_dict("1", "0"),
        ],
    }
    scenarios.append(module_b_timing)

    # Scenario 4: OR Gate Operation
    or_gate_test = {
        "scenario": "OR Gate Operation",
        "input variable": [
            create_input_dict("0", "0"),
            create_input_dict("0", "1"),
            create_input_dict("1", "0"),
            create_input_dict("1", "1"),
        ],
    }
    scenarios.append(or_gate_test)

    # Scenario 5: AND Gate Operation
    and_gate_test = {
        "scenario": "AND Gate Operation",
        "input variable": [
            create_input_dict("0", "0"),
            create_input_dict("0", "1"),
            create_input_dict("1", "0"),
            create_input_dict("1", "1"),
        ],
    }
    scenarios.append(and_gate_test)

    # Scenario 6: Final XOR Operation
    xor_gate_test = {
        "scenario": "Final XOR Operation",
        "input variable": [
            create_input_dict("0", "0"),
            create_input_dict("0", "1"),
            create_input_dict("1", "0"),
            create_input_dict("1", "1"),
        ],
    }
    scenarios.append(xor_gate_test)

    # Scenario 7: Input Transition Timing
    transition_timing = {
        "scenario": "Input Transition Timing",
        "input variable": [
            create_input_dict("0", "0"),
            create_input_dict("0", "1"),
            create_input_dict("1", "1"),
            create_input_dict("1", "0"),
            create_input_dict("0", "0"),
        ],
    }
    scenarios.append(transition_timing)

    # Scenario 8: Glitch Detection
    glitch_detection = {
        "scenario": "Glitch Detection",
        "input variable": [
            create_input_dict("0", "0"),
            create_input_dict("1", "0"),
            create_input_dict("1", "1"),
            create_input_dict("0", "1"),
            create_input_dict("0", "0"),
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
