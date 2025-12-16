import json


def stimulus_gen():
    scenarios = []

    # Helper function to create binary string for single bit
    def bin_str(val):
        return "1" if val else "0"

    # Scenario 1: Basic Signal Routing
    basic_routing = {
        "scenario": "Basic Signal Routing",
        "input variable": [
            {"a": "0", "b": "0", "c": "0"},
            {"a": "1", "b": "0", "c": "0"},
            {"a": "0", "b": "1", "c": "0"},
            {"a": "0", "b": "0", "c": "1"},
        ],
    }
    scenarios.append(basic_routing)

    # Scenario 2: All Zeros
    all_zeros = {
        "scenario": "All Zeros",
        "input variable": [{"a": "0", "b": "0", "c": "0"}],
    }
    scenarios.append(all_zeros)

    # Scenario 3: All Ones
    all_ones = {
        "scenario": "All Ones",
        "input variable": [{"a": "1", "b": "1", "c": "1"}],
    }
    scenarios.append(all_ones)

    # Scenario 4: Individual Signal Toggle
    toggle_signals = {
        "scenario": "Individual Signal Toggle",
        "input variable": [
            {"a": "0", "b": "0", "c": "0"},
            {"a": "1", "b": "0", "c": "0"},
            {"a": "0", "b": "0", "c": "0"},
            {"a": "0", "b": "1", "c": "0"},
            {"a": "0", "b": "0", "c": "0"},
            {"a": "0", "b": "0", "c": "1"},
            {"a": "0", "b": "0", "c": "0"},
        ],
    }
    scenarios.append(toggle_signals)

    # Scenario 5: Rapid Input Changes
    rapid_changes = {
        "scenario": "Rapid Input Changes",
        "input variable": [
            {"a": "0", "b": "0", "c": "0"},
            {"a": "1", "b": "1", "c": "1"},
            {"a": "0", "b": "0", "c": "0"},
            {"a": "1", "b": "1", "c": "1"},
        ],
    }
    scenarios.append(rapid_changes)

    # Scenario 6: Signal Propagation Delay
    prop_delay = {
        "scenario": "Signal Propagation Delay",
        "input variable": [
            {"a": "0", "b": "0", "c": "0"},
            {"a": "1", "b": "1", "c": "1"},
            {"a": "0", "b": "1", "c": "0"},
            {"a": "1", "b": "0", "c": "1"},
        ],
    }
    scenarios.append(prop_delay)

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
