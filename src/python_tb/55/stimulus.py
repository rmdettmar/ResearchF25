import json


def gen_reset_sequence():
    # Generate sequence for reset verification
    seq = []
    # Reset high, other inputs varying
    seq.append({"clk": "0", "in": "0", "areset": "1"})
    seq.append({"clk": "1", "in": "1", "areset": "1"})
    seq.append({"clk": "0", "in": "0", "areset": "1"})
    return seq


def gen_state_sequence(start_state, input_val, cycles):
    # Generate sequence for state verification
    seq = []
    for i in range(cycles):
        seq.append({"clk": "0", "in": input_val, "areset": "0"})
        seq.append({"clk": "1", "in": input_val, "areset": "0"})
    return seq


def stimulus_gen():
    scenarios = []

    # Scenario 1: Asynchronous Reset Verification
    reset_scenario = {
        "scenario": "Asynchronous Reset Verification",
        "input variable": gen_reset_sequence(),
    }
    scenarios.append(reset_scenario)

    # Scenario 2: State B Self-Loop
    state_b_loop = {
        "scenario": "State B Self-Loop",
        "input variable": gen_state_sequence("B", "1", 4),
    }
    scenarios.append(state_b_loop)

    # Scenario 3: State B to A Transition
    b_to_a = {
        "scenario": "State B to A Transition",
        "input variable": gen_state_sequence("B", "0", 2),
    }
    scenarios.append(b_to_a)

    # Scenario 4: State A Self-Loop
    state_a_loop = {
        "scenario": "State A Self-Loop",
        "input variable": gen_state_sequence("A", "1", 4),
    }
    scenarios.append(state_a_loop)

    # Scenario 5: State A to B Transition
    a_to_b = {
        "scenario": "State A to B Transition",
        "input variable": gen_state_sequence("A", "0", 2),
    }
    scenarios.append(a_to_b)

    # Scenario 6: Input Toggle Test
    toggle_seq = []
    for i in range(4):
        toggle_seq.append({"clk": "0", "in": str(i % 2), "areset": "0"})
        toggle_seq.append({"clk": "1", "in": str(i % 2), "areset": "0"})
    toggle_test = {"scenario": "Input Toggle Test", "input variable": toggle_seq}
    scenarios.append(toggle_test)

    # Scenario 7: Reset During Transition
    reset_trans_seq = []
    reset_trans_seq.extend(gen_state_sequence("B", "0", 1))
    reset_trans_seq.append({"clk": "0", "in": "0", "areset": "1"})
    reset_during_trans = {
        "scenario": "Reset During Transition",
        "input variable": reset_trans_seq,
    }
    scenarios.append(reset_during_trans)

    # Scenario 8: Power-On State
    power_on_seq = []
    power_on_seq.append({"clk": "0", "in": "0", "areset": "0"})
    power_on_seq.append({"clk": "1", "in": "0", "areset": "0"})
    power_on = {"scenario": "Power-On State", "input variable": power_on_seq}
    scenarios.append(power_on)

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
