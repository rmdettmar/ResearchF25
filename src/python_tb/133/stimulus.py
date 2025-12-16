import json


def generate_clock_cycle(num_cycles):
    sequence = []
    for _ in range(num_cycles):
        sequence.append({"clk": "0", "j": "0", "k": "0", "reset": "0"})
        sequence.append({"clk": "1", "j": "0", "k": "0", "reset": "0"})
    return sequence


def stimulus_gen():
    scenarios = []

    # Reset Verification
    reset_seq = generate_clock_cycle(2)
    reset_seq[1]["reset"] = "1"  # Assert reset on rising edge
    reset_seq[3]["reset"] = "1"  # Keep reset asserted
    scenarios.append({"scenario": "Reset Verification", "input variable": reset_seq})

    # OFF to ON Transition
    off_to_on = generate_clock_cycle(2)
    off_to_on[1]["j"] = "1"  # Assert j on rising edge
    scenarios.append({"scenario": "OFF to ON Transition", "input variable": off_to_on})

    # ON to OFF Transition
    on_to_off = generate_clock_cycle(2)
    on_to_off[1]["k"] = "1"  # Assert k on rising edge
    scenarios.append({"scenario": "ON to OFF Transition", "input variable": on_to_off})

    # State Persistence OFF
    persist_off = generate_clock_cycle(4)
    for i in range(len(persist_off)):
        persist_off[i]["j"] = "0"
    scenarios.append(
        {"scenario": "State Persistence OFF", "input variable": persist_off}
    )

    # State Persistence ON
    persist_on = generate_clock_cycle(4)
    persist_on[1]["j"] = "1"  # First transition to ON
    for i in range(3, len(persist_on)):
        persist_on[i]["k"] = "0"  # Keep k=0 to stay in ON
    scenarios.append({"scenario": "State Persistence ON", "input variable": persist_on})

    # Input Toggle
    toggle_seq = generate_clock_cycle(4)
    toggle_seq[1]["j"] = "1"
    toggle_seq[3]["k"] = "1"
    toggle_seq[5]["j"] = "1"
    toggle_seq[7]["k"] = "1"
    scenarios.append({"scenario": "Input Toggle", "input variable": toggle_seq})

    # Setup Time Verification
    setup_seq = generate_clock_cycle(2)
    setup_seq[0]["j"] = "1"  # Change input just before clock edge
    scenarios.append(
        {"scenario": "Setup Time Verification", "input variable": setup_seq}
    )

    # Reset During Transition
    reset_trans = generate_clock_cycle(2)
    reset_trans[1]["j"] = "1"
    reset_trans[1]["reset"] = "1"  # Assert reset during transition
    scenarios.append(
        {"scenario": "Reset During Transition", "input variable": reset_trans}
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
