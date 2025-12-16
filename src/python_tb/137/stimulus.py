import json


def stimulus_gen():
    scenarios = []

    # Helper function to create input sequence
    def create_input_sequence(reset_val, in_val):
        return {"clk": "1", "reset": reset_val, "in": in_val}

    # Scenario 1: Reset Verification
    reset_verify = {
        "scenario": "Reset Verification",
        "input variable": [
            create_input_sequence("1", "0"),
            create_input_sequence("1", "1"),
            create_input_sequence("0", "0"),
        ],
    }
    scenarios.append(reset_verify)

    # Scenario 2: State B Transitions
    state_b_trans = {
        "scenario": "State B Transitions",
        "input variable": [
            create_input_sequence("1", "0"),  # Reset to B
            create_input_sequence("0", "0"),  # B->A
            create_input_sequence("0", "1"),  # Stay in A
            create_input_sequence("0", "1"),  # B->B
            create_input_sequence("0", "0"),  # B->A
        ],
    }
    scenarios.append(state_b_trans)

    # Scenario 3: State A Transitions
    state_a_trans = {
        "scenario": "State A Transitions",
        "input variable": [
            create_input_sequence("1", "0"),  # Reset to B
            create_input_sequence("0", "0"),  # B->A
            create_input_sequence("0", "1"),  # A->A
            create_input_sequence("0", "0"),  # A->B
            create_input_sequence("0", "1"),  # B->B
        ],
    }
    scenarios.append(state_a_trans)

    # Scenario 4: Input Toggle
    input_toggle = {
        "scenario": "Input Toggle",
        "input variable": [
            create_input_sequence("1", "0"),  # Reset to B
            create_input_sequence("0", "1"),  # Toggle
            create_input_sequence("0", "0"),  # Toggle
            create_input_sequence("0", "1"),  # Toggle
            create_input_sequence("0", "0"),  # Toggle
        ],
    }
    scenarios.append(input_toggle)

    # Scenario 5: Reset During Operation
    reset_during_op = {
        "scenario": "Reset During Operation",
        "input variable": [
            create_input_sequence("1", "0"),  # Initial reset
            create_input_sequence("0", "0"),  # Go to A
            create_input_sequence("1", "1"),  # Reset while in A
            create_input_sequence("0", "0"),  # Normal operation
            create_input_sequence("0", "1"),  # Continue operation
        ],
    }
    scenarios.append(reset_during_op)

    # Scenario 6: Output Stability
    output_stability = {
        "scenario": "Output Stability",
        "input variable": [
            create_input_sequence("1", "0"),  # Reset to B
            create_input_sequence("0", "0"),  # Stable in B
            create_input_sequence("0", "0"),  # B->A transition
            create_input_sequence("0", "0"),  # Stable in A
            create_input_sequence("0", "1"),  # A->A stable
        ],
    }
    scenarios.append(output_stability)

    # Scenario 7: Multiple State Sequences
    multiple_sequences = {
        "scenario": "Multiple State Sequences",
        "input variable": [
            create_input_sequence("1", "0"),  # Reset to B
            create_input_sequence("0", "0"),  # B->A
            create_input_sequence("0", "1"),  # A->A
            create_input_sequence("0", "0"),  # A->B
            create_input_sequence("0", "1"),  # B->B
            create_input_sequence("0", "0"),  # B->A
            create_input_sequence("0", "1"),  # A->A
        ],
    }
    scenarios.append(multiple_sequences)

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
