import json


def stimulus_gen():
    scenarios = []

    # Helper function to create binary strings
    def bin_str(val):
        return "1" if val else "0"

    # Scenario 1: All Input Combinations
    input_combinations = [
        {"a": bin_str(0), "b": bin_str(0)},
        {"a": bin_str(0), "b": bin_str(1)},
        {"a": bin_str(1), "b": bin_str(0)},
        {"a": bin_str(1), "b": bin_str(1)},
    ]
    scenarios.append(
        {"scenario": "All Input Combinations", "input variable": input_combinations}
    )

    # Scenario 2: Input Transitions
    transition_sequence = [
        {"a": bin_str(0), "b": bin_str(0)},
        {"a": bin_str(0), "b": bin_str(1)},
        {"a": bin_str(1), "b": bin_str(1)},
        {"a": bin_str(1), "b": bin_str(0)},
    ]
    scenarios.append(
        {"scenario": "Input Transitions", "input variable": transition_sequence}
    )

    # Scenario 3: Glitch Detection
    glitch_sequence = [
        {"a": bin_str(0), "b": bin_str(0)},
        {"a": bin_str(1), "b": bin_str(0)},
        {"a": bin_str(1), "b": bin_str(1)},
        {"a": bin_str(0), "b": bin_str(1)},
        {"a": bin_str(0), "b": bin_str(0)},
    ]
    scenarios.append(
        {"scenario": "Glitch Detection", "input variable": glitch_sequence}
    )

    # Scenario 4: Signal Stability
    stability_sequence = [
        {"a": bin_str(1), "b": bin_str(1)},
        {"a": bin_str(1), "b": bin_str(1)},
        {"a": bin_str(1), "b": bin_str(1)},
        {"a": bin_str(0), "b": bin_str(0)},
        {"a": bin_str(0), "b": bin_str(0)},
        {"a": bin_str(0), "b": bin_str(0)},
    ]
    scenarios.append(
        {"scenario": "Signal Stability", "input variable": stability_sequence}
    )

    # Scenario 5: Timing Verification
    timing_sequence = [
        {"a": bin_str(0), "b": bin_str(0)},
        {"a": bin_str(1), "b": bin_str(0)},
        {"a": bin_str(1), "b": bin_str(1)},
        {"a": bin_str(0), "b": bin_str(1)},
        {"a": bin_str(0), "b": bin_str(0)},
        {"a": bin_str(1), "b": bin_str(1)},
    ]
    scenarios.append(
        {"scenario": "Timing Verification", "input variable": timing_sequence}
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
