import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a stimulus dictionary
    def create_stimulus(name, input_list):
        return {"scenario": name, "input variable": input_list}

    # Scenario 1: Basic Selection Test
    basic_test = []
    # a=0, b=1, test all sel combinations
    basic_test.extend(
        [
            {"a": "0", "b": "1", "sel_b1": "0", "sel_b2": "0"},
            {"a": "0", "b": "1", "sel_b1": "0", "sel_b2": "1"},
            {"a": "0", "b": "1", "sel_b1": "1", "sel_b2": "0"},
            {"a": "0", "b": "1", "sel_b1": "1", "sel_b2": "1"},
        ]
    )
    scenarios.append(create_stimulus("Basic Selection Test", basic_test))

    # Scenario 2: Input Transition Test
    input_test = []
    # Toggle a and b with fixed sel
    input_test.extend(
        [
            {"a": "0", "b": "0", "sel_b1": "1", "sel_b2": "1"},
            {"a": "0", "b": "1", "sel_b1": "1", "sel_b2": "1"},
            {"a": "1", "b": "0", "sel_b1": "1", "sel_b2": "1"},
            {"a": "1", "b": "1", "sel_b1": "1", "sel_b2": "1"},
        ]
    )
    scenarios.append(create_stimulus("Input Transition Test", input_test))

    # Scenario 3: Select Signal Transitions
    sel_test = []
    # Change sel signals with fixed inputs
    sel_test.extend(
        [
            {"a": "1", "b": "0", "sel_b1": "0", "sel_b2": "0"},
            {"a": "1", "b": "0", "sel_b1": "1", "sel_b2": "0"},
            {"a": "1", "b": "0", "sel_b1": "0", "sel_b2": "1"},
            {"a": "1", "b": "0", "sel_b1": "1", "sel_b2": "1"},
        ]
    )
    scenarios.append(create_stimulus("Select Signal Transitions", sel_test))

    # Scenario 4: Output Consistency Check
    consistency_test = []
    # All possible input combinations
    for a in ["0", "1"]:
        for b in ["0", "1"]:
            for sel1 in ["0", "1"]:
                for sel2 in ["0", "1"]:
                    consistency_test.append(
                        {"a": a, "b": b, "sel_b1": sel1, "sel_b2": sel2}
                    )
    scenarios.append(create_stimulus("Output Consistency Check", consistency_test))

    # Scenario 5: Timing Verification
    timing_test = []
    # Rapid transitions on critical paths
    timing_test.extend(
        [
            {"a": "0", "b": "1", "sel_b1": "0", "sel_b2": "0"},
            {"a": "1", "b": "0", "sel_b1": "1", "sel_b2": "1"},
            {"a": "0", "b": "1", "sel_b1": "1", "sel_b2": "1"},
            {"a": "1", "b": "0", "sel_b1": "0", "sel_b2": "0"},
        ]
    )
    scenarios.append(create_stimulus("Timing Verification", timing_test))

    # Scenario 6: Concurrent Changes
    concurrent_test = []
    # Change all inputs simultaneously
    concurrent_test.extend(
        [
            {"a": "0", "b": "0", "sel_b1": "0", "sel_b2": "0"},
            {"a": "1", "b": "1", "sel_b1": "1", "sel_b2": "1"},
            {"a": "0", "b": "1", "sel_b1": "0", "sel_b2": "1"},
            {"a": "1", "b": "0", "sel_b1": "1", "sel_b2": "0"},
        ]
    )
    scenarios.append(create_stimulus("Concurrent Changes", concurrent_test))

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
