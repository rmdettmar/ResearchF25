import json


def stimulus_gen():
    scenarios = []

    # Helper function to create binary input combinations
    def create_input_pair(a_val, b_val):
        return {"a": "1" if a_val else "0", "b": "1" if b_val else "0"}

    # Scenario 1: All Input Combinations
    all_combinations = {
        "scenario": "All Input Combinations",
        "input variable": [
            create_input_pair(0, 0),
            create_input_pair(0, 1),
            create_input_pair(1, 0),
            create_input_pair(1, 1),
        ],
    }
    scenarios.append(all_combinations)

    # Scenario 2: Input Transitions
    transitions = {
        "scenario": "Input Transitions",
        "input variable": [
            create_input_pair(0, 0),
            create_input_pair(0, 1),
            create_input_pair(1, 1),
            create_input_pair(1, 0),
            create_input_pair(0, 0),
        ],
    }
    scenarios.append(transitions)

    # Scenario 3: Setup and Hold Times
    setup_hold = {
        "scenario": "Setup and Hold Times",
        "input variable": [
            create_input_pair(0, 0),
            create_input_pair(1, 1),
            create_input_pair(0, 1),
            create_input_pair(1, 0),
        ],
    }
    scenarios.append(setup_hold)

    # Scenario 4: Output Verification AND Gate
    and_gate = {
        "scenario": "Output Verification AND Gate",
        "input variable": [
            create_input_pair(1, 1),
            create_input_pair(1, 0),
            create_input_pair(0, 1),
            create_input_pair(0, 0),
        ],
    }
    scenarios.append(and_gate)

    # Scenario 5: Output Verification OR Gate
    or_gate = {
        "scenario": "Output Verification OR Gate",
        "input variable": [
            create_input_pair(0, 0),
            create_input_pair(0, 1),
            create_input_pair(1, 0),
            create_input_pair(1, 1),
        ],
    }
    scenarios.append(or_gate)

    # Scenario 6: Output Verification XOR Gate
    xor_gate = {
        "scenario": "Output Verification XOR Gate",
        "input variable": [
            create_input_pair(0, 0),
            create_input_pair(0, 1),
            create_input_pair(1, 0),
            create_input_pair(1, 1),
        ],
    }
    scenarios.append(xor_gate)

    # Scenario 7: Output Verification NAND Gate
    nand_gate = {
        "scenario": "Output Verification NAND Gate",
        "input variable": [
            create_input_pair(1, 1),
            create_input_pair(1, 0),
            create_input_pair(0, 1),
            create_input_pair(0, 0),
        ],
    }
    scenarios.append(nand_gate)

    # Scenario 8: Output Verification NOR Gate
    nor_gate = {
        "scenario": "Output Verification NOR Gate",
        "input variable": [
            create_input_pair(0, 0),
            create_input_pair(0, 1),
            create_input_pair(1, 0),
            create_input_pair(1, 1),
        ],
    }
    scenarios.append(nor_gate)

    # Scenario 9: Output Verification XNOR Gate
    xnor_gate = {
        "scenario": "Output Verification XNOR Gate",
        "input variable": [
            create_input_pair(0, 0),
            create_input_pair(0, 1),
            create_input_pair(1, 0),
            create_input_pair(1, 1),
        ],
    }
    scenarios.append(xnor_gate)

    # Scenario 10: Output Verification ANOTB Gate
    anotb_gate = {
        "scenario": "Output Verification ANOTB Gate",
        "input variable": [
            create_input_pair(1, 0),
            create_input_pair(1, 1),
            create_input_pair(0, 0),
            create_input_pair(0, 1),
        ],
    }
    scenarios.append(anotb_gate)

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
