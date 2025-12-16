import json


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Input Combinations
    input_combinations = [
        {"in1": "0", "in2": "0"},
        {"in1": "0", "in2": "1"},
        {"in1": "1", "in2": "0"},
        {"in1": "1", "in2": "1"},
    ]
    scenarios.append(
        {"scenario": "All Input Combinations", "input variable": input_combinations}
    )

    # Scenario 2: Input Transitions
    transition_sequence = [
        {"in1": "0", "in2": "0"},
        {"in1": "0", "in2": "1"},
        {"in1": "1", "in2": "1"},
        {"in1": "1", "in2": "0"},
        {"in1": "0", "in2": "0"},
    ]
    scenarios.append(
        {"scenario": "Input Transitions", "input variable": transition_sequence}
    )

    # Scenario 3: Simultaneous Input Changes
    simultaneous_changes = [
        {"in1": "0", "in2": "0"},
        {"in1": "1", "in2": "1"},
        {"in1": "0", "in2": "0"},
        {"in1": "1", "in2": "1"},
    ]
    scenarios.append(
        {
            "scenario": "Simultaneous Input Changes",
            "input variable": simultaneous_changes,
        }
    )

    # Scenario 4: Propagation Delay
    delay_sequence = [
        {"in1": "0", "in2": "0"},
        {"in1": "1", "in2": "0"},
        {"in1": "1", "in2": "1"},
        {"in1": "0", "in2": "1"},
        {"in1": "0", "in2": "0"},
    ]
    scenarios.append(
        {"scenario": "Propagation Delay", "input variable": delay_sequence}
    )

    # Scenario 5: Input Signal Stability
    stability_sequence = [
        {"in1": "0", "in2": "0"},
        {"in1": "0", "in2": "0"},
        {"in1": "1", "in2": "1"},
        {"in1": "1", "in2": "1"},
        {"in1": "1", "in2": "1"},
    ]
    scenarios.append(
        {"scenario": "Input Signal Stability", "input variable": stability_sequence}
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
