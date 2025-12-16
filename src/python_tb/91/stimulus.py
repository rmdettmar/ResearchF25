import json


def stimulus_gen():
    stimulus_list = []

    # Helper function to create a binary string
    def bin_str(val, width=1):
        return format(val, f"0{width}b")

    # Scenario 1: All Input Combinations
    input_combinations = []
    for i in range(8):
        input_combinations.append(
            {
                "a": bin_str((i >> 2) & 1),
                "b": bin_str((i >> 1) & 1),
                "c": bin_str(i & 1),
            }
        )
    stimulus_list.append(
        {"scenario": "All Input Combinations", "input variable": input_combinations}
    )

    # Scenario 2: Single Input Transitions
    single_transitions = [
        {"a": "0", "b": "0", "c": "0"},
        {"a": "1", "b": "0", "c": "0"},
        {"a": "0", "b": "0", "c": "0"},
        {"a": "0", "b": "1", "c": "0"},
        {"a": "0", "b": "0", "c": "0"},
        {"a": "0", "b": "0", "c": "1"},
    ]
    stimulus_list.append(
        {"scenario": "Single Input Transitions", "input variable": single_transitions}
    )

    # Scenario 3: Critical Path Test
    critical_path = [
        {"a": "0", "b": "0", "c": "0"},
        {"a": "1", "b": "1", "c": "1"},
        {"a": "0", "b": "0", "c": "0"},
    ]
    stimulus_list.append(
        {"scenario": "Critical Path Test", "input variable": critical_path}
    )

    # Scenario 4: Output Zero Condition
    zero_condition = [
        {"a": "0", "b": "0", "c": "0"},
        {"a": "0", "b": "0", "c": "0"},
        {"a": "0", "b": "0", "c": "0"},
    ]
    stimulus_list.append(
        {"scenario": "Output Zero Condition", "input variable": zero_condition}
    )

    # Scenario 5: Multiple Input Transitions
    multiple_transitions = [
        {"a": "0", "b": "0", "c": "0"},
        {"a": "1", "b": "1", "c": "0"},
        {"a": "0", "b": "1", "c": "1"},
        {"a": "1", "b": "0", "c": "1"},
    ]
    stimulus_list.append(
        {
            "scenario": "Multiple Input Transitions",
            "input variable": multiple_transitions,
        }
    )

    # Scenario 6: Input Signal Stability
    stability_test = [
        {"a": "1", "b": "1", "c": "1"},
        {"a": "1", "b": "1", "c": "1"},
        {"a": "1", "b": "1", "c": "1"},
        {"a": "0", "b": "0", "c": "0"},
        {"a": "0", "b": "0", "c": "0"},
        {"a": "0", "b": "0", "c": "0"},
    ]
    stimulus_list.append(
        {"scenario": "Input Signal Stability", "input variable": stability_test}
    )

    return stimulus_list


if __name__ == "__main__":
    result = stimulus_gen()
    # 将结果转换为 JSON 字符串
    if isinstance(result, list):
        result = json.dumps(result, indent=4)
    elif not isinstance(result, str):
        result = json.dumps(result, indent=4)

    with open("stimulus.json", "w") as f:
        f.write(result)
