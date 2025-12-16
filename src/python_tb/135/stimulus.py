import json


def stimulus_gen():
    scenarios = []

    # Helper function to create binary string
    def bin_str(val):
        return format(val, "01b")

    # Scenario 1: All Zero Inputs
    scenarios.append(
        {
            "scenario": "All Zero Inputs",
            "input variable": [{"a": "0", "b": "0", "c": "0", "d": "0"}],
        }
    )

    # Scenario 2: Single Input Transitions
    single_transitions = []
    for i in range(4):
        inputs = {"a": "0", "b": "0", "c": "0", "d": "0"}
        if i == 0:
            inputs["a"] = "1"
        elif i == 1:
            inputs["b"] = "1"
        elif i == 2:
            inputs["c"] = "1"
        else:
            inputs["d"] = "1"
        single_transitions.append(inputs)

    scenarios.append(
        {"scenario": "Single Input Transitions", "input variable": single_transitions}
    )

    # Scenario 3: Two Input Combinations
    two_input_combinations = []
    for i in range(4):
        for j in range(i + 1, 4):
            inputs = {"a": "0", "b": "0", "c": "0", "d": "0"}
            if i == 0 or j == 0:
                inputs["a"] = "1"
            if i == 1 or j == 1:
                inputs["b"] = "1"
            if i == 2 or j == 2:
                inputs["c"] = "1"
            if i == 3 or j == 3:
                inputs["d"] = "1"
            two_input_combinations.append(inputs)

    scenarios.append(
        {"scenario": "Two Input Combinations", "input variable": two_input_combinations}
    )

    # Scenario 4: Three Input Combinations
    three_input_combinations = []
    for i in range(4):
        inputs = {"a": "1", "b": "1", "c": "1", "d": "1"}
        if i == 0:
            inputs["a"] = "0"
        elif i == 1:
            inputs["b"] = "0"
        elif i == 2:
            inputs["c"] = "0"
        else:
            inputs["d"] = "0"
        three_input_combinations.append(inputs)

    scenarios.append(
        {
            "scenario": "Three Input Combinations",
            "input variable": three_input_combinations,
        }
    )

    # Scenario 5: All Ones Input
    scenarios.append(
        {
            "scenario": "All Ones Input",
            "input variable": [{"a": "1", "b": "1", "c": "1", "d": "1"}],
        }
    )

    # Scenario 6: Sequential Transitions
    sequential = []
    waveform_sequence = [
        {"a": "0", "b": "0", "c": "0", "d": "0"},
        {"a": "0", "b": "0", "c": "0", "d": "1"},
        {"a": "0", "b": "0", "c": "1", "d": "0"},
        {"a": "0", "b": "0", "c": "1", "d": "1"},
        {"a": "0", "b": "1", "c": "0", "d": "0"},
        {"a": "0", "b": "1", "c": "0", "d": "1"},
        {"a": "0", "b": "1", "c": "1", "d": "0"},
        {"a": "0", "b": "1", "c": "1", "d": "1"},
        {"a": "1", "b": "0", "c": "0", "d": "0"},
        {"a": "1", "b": "0", "c": "0", "d": "1"},
        {"a": "1", "b": "0", "c": "1", "d": "0"},
        {"a": "1", "b": "0", "c": "1", "d": "1"},
        {"a": "1", "b": "1", "c": "0", "d": "0"},
        {"a": "1", "b": "1", "c": "0", "d": "1"},
        {"a": "1", "b": "1", "c": "1", "d": "0"},
        {"a": "1", "b": "1", "c": "1", "d": "1"},
    ]

    scenarios.append(
        {"scenario": "Sequential Transitions", "input variable": waveform_sequence}
    )

    # Scenario 7: Input Stability
    scenarios.append(
        {
            "scenario": "Input Stability",
            "input variable": [{"a": "0", "b": "0", "c": "0", "d": "0"}] * 5,
        }
    )

    # Scenario 8: Propagation Delay
    prop_delay_sequence = [
        {"a": "0", "b": "0", "c": "0", "d": "0"},
        {"a": "1", "b": "1", "c": "1", "d": "1"},
        {"a": "0", "b": "0", "c": "0", "d": "0"},
    ]

    scenarios.append(
        {"scenario": "Propagation Delay", "input variable": prop_delay_sequence}
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
