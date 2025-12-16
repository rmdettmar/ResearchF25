import json


def stimulus_gen():
    scenarios = []

    # Helper function to convert input values to binary strings
    def get_binary_str(val, width=1):
        return format(val, f"0{width}b")

    # Scenario 1: All Input Combinations
    input_combinations = []
    for i in range(16):
        input_combinations.append(
            {
                "a": get_binary_str((i >> 3) & 1),
                "b": get_binary_str((i >> 2) & 1),
                "c": get_binary_str((i >> 1) & 1),
                "d": get_binary_str(i & 1),
            }
        )
    scenarios.append(
        {"scenario": "All Input Combinations", "input variable": input_combinations}
    )

    # Scenario 2: Adjacent Cell Transitions
    adjacent_transitions = []
    transitions = [(0, 1), (1, 3), (3, 2), (2, 0)]  # Example transitions
    for t in transitions:
        adjacent_transitions.append(
            {
                "a": get_binary_str((t[0] >> 3) & 1),
                "b": get_binary_str((t[0] >> 2) & 1),
                "c": get_binary_str((t[0] >> 1) & 1),
                "d": get_binary_str(t[0] & 1),
            }
        )
    scenarios.append(
        {
            "scenario": "Adjacent Cell Transitions",
            "input variable": adjacent_transitions,
        }
    )

    # Scenario 3: Output 1 Verification
    output_1_cases = []
    # Cases where output should be 1
    cases_1 = [0b0000, 0b0001, 0b0100, 0b0101, 0b1011, 0b1111, 0b1110]
    for case in cases_1:
        output_1_cases.append(
            {
                "a": get_binary_str((case >> 3) & 1),
                "b": get_binary_str((case >> 2) & 1),
                "c": get_binary_str((case >> 1) & 1),
                "d": get_binary_str(case & 1),
            }
        )
    scenarios.append(
        {"scenario": "Output 1 Verification", "input variable": output_1_cases}
    )

    # Scenario 4: Output 0 Verification
    output_0_cases = []
    # Cases where output should be 0
    cases_0 = [0b1100, 0b0111, 0b0011, 0b1010]
    for case in cases_0:
        output_0_cases.append(
            {
                "a": get_binary_str((case >> 3) & 1),
                "b": get_binary_str((case >> 2) & 1),
                "c": get_binary_str((case >> 1) & 1),
                "d": get_binary_str(case & 1),
            }
        )
    scenarios.append(
        {"scenario": "Output 0 Verification", "input variable": output_0_cases}
    )

    # Scenario 5: Input Setup Time
    setup_time = []
    test_case = 0b0101  # Example case
    setup_time.append(
        {
            "a": get_binary_str((test_case >> 3) & 1),
            "b": get_binary_str((test_case >> 2) & 1),
            "c": get_binary_str((test_case >> 1) & 1),
            "d": get_binary_str(test_case & 1),
        }
    )
    scenarios.append({"scenario": "Input Setup Time", "input variable": setup_time})

    # Scenario 6: Input Hold Time
    hold_time = []
    test_case = 0b1010  # Example case
    hold_time.append(
        {
            "a": get_binary_str((test_case >> 3) & 1),
            "b": get_binary_str((test_case >> 2) & 1),
            "c": get_binary_str((test_case >> 1) & 1),
            "d": get_binary_str(test_case & 1),
        }
    )
    scenarios.append({"scenario": "Input Hold Time", "input variable": hold_time})

    # Scenario 7: Simultaneous Input Changes
    simultaneous = []
    changes = [(0b0000, 0b1111)]  # Example simultaneous changes
    for change in changes:
        simultaneous.append(
            {
                "a": get_binary_str((change[0] >> 3) & 1),
                "b": get_binary_str((change[0] >> 2) & 1),
                "c": get_binary_str((change[0] >> 1) & 1),
                "d": get_binary_str(change[0] & 1),
            }
        )
    scenarios.append(
        {"scenario": "Simultaneous Input Changes", "input variable": simultaneous}
    )

    # Scenario 8: Power-On State
    power_on = []
    initial_state = 0b0000
    power_on.append(
        {
            "a": get_binary_str((initial_state >> 3) & 1),
            "b": get_binary_str((initial_state >> 2) & 1),
            "c": get_binary_str((initial_state >> 1) & 1),
            "d": get_binary_str(initial_state & 1),
        }
    )
    scenarios.append({"scenario": "Power-On State", "input variable": power_on})

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
