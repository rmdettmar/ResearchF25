import json


def stimulus_gen():
    scenarios = []

    # Helper function to create binary string
    def bin_str(val, width=1):
        return format(val, f"0{width}b")

    # Scenario 1: Basic Input Combinations
    basic_combinations = {
        "scenario": "Basic Input Combinations",
        "input variable": [
            {"a": "0", "b": "0"},
            {"a": "0", "b": "1"},
            {"a": "1", "b": "0"},
            {"a": "1", "b": "1"},
        ],
    }
    scenarios.append(basic_combinations)

    # Scenario 2: Input Transitions
    transitions = {
        "scenario": "Input Transitions",
        "input variable": [
            {"a": "0", "b": "0"},
            {"a": "0", "b": "1"},
            {"a": "1", "b": "1"},
            {"a": "1", "b": "0"},
            {"a": "0", "b": "0"},
        ],
    }
    scenarios.append(transitions)

    # Scenario 3: Propagation Delay
    prop_delay = {
        "scenario": "Propagation Delay",
        "input variable": [
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
        ],
    }
    scenarios.append(prop_delay)

    # Scenario 4: Simultaneous Input Changes
    simultaneous = {
        "scenario": "Simultaneous Input Changes",
        "input variable": [
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
        ],
    }
    scenarios.append(simultaneous)

    # Scenario 5: Input Stability
    stability = {
        "scenario": "Input Stability",
        "input variable": [
            {"a": "0", "b": "0"},
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
            {"a": "1", "b": "1"},
            {"a": "1", "b": "1"},
        ],
    }
    scenarios.append(stability)

    # Scenario 6: High-frequency Transitions
    high_freq = {
        "scenario": "High-frequency Transitions",
        "input variable": [
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
            {"a": "0", "b": "0"},
            {"a": "1", "b": "1"},
        ],
    }
    scenarios.append(high_freq)

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
