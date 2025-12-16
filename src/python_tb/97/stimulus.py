import json


def generate_reset_sequence(cycles):
    return [{"clk": "1", "reset": "1", "x": "0"} for _ in range(cycles)]


def generate_state_transition_sequence(x_val, cycles):
    return [{"clk": "1", "reset": "0", "x": x_val} for _ in range(cycles)]


def stimulus_gen():
    scenarios = []

    # Scenario 1: Reset Verification
    reset_scenario = {
        "scenario": "Reset Verification",
        "input variable": generate_reset_sequence(5)
        + generate_state_transition_sequence("0", 2),
    }
    scenarios.append(reset_scenario)

    # Scenario 2: Basic State Transitions x=0
    x0_transitions = {
        "scenario": "Basic State Transitions x=0",
        "input variable": generate_reset_sequence(1)
        + generate_state_transition_sequence("0", 10),
    }
    scenarios.append(x0_transitions)

    # Scenario 3: Basic State Transitions x=1
    x1_transitions = {
        "scenario": "Basic State Transitions x=1",
        "input variable": generate_reset_sequence(1)
        + generate_state_transition_sequence("1", 10),
    }
    scenarios.append(x1_transitions)

    # Scenario 4: Output Generation
    output_verify = {
        "scenario": "Output Generation",
        "input variable": generate_reset_sequence(1)
        + [{"clk": "1", "reset": "0", "x": "1"} for _ in range(3)]
        + [{"clk": "1", "reset": "0", "x": "0"} for _ in range(2)],
    }
    scenarios.append(output_verify)

    # Scenario 5: Reset During Operation
    reset_during_op = {
        "scenario": "Reset During Operation",
        "input variable": generate_state_transition_sequence("1", 3)
        + generate_reset_sequence(2)
        + generate_state_transition_sequence("0", 2),
    }
    scenarios.append(reset_during_op)

    # Scenario 6: Extended State Sequence
    extended_seq = {
        "scenario": "Extended State Sequence",
        "input variable": generate_reset_sequence(1)
        + [{"clk": "1", "reset": "0", "x": str(i % 2)} for i in range(20)],
    }
    scenarios.append(extended_seq)

    # Scenario 7: Invalid State Recovery
    invalid_recovery = {
        "scenario": "Invalid State Recovery",
        "input variable": generate_reset_sequence(1)
        + generate_state_transition_sequence("1", 5)
        + generate_reset_sequence(2)
        + generate_state_transition_sequence("0", 5),
    }
    scenarios.append(invalid_recovery)

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
