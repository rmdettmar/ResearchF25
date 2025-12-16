import json


def stimulus_gen():
    scenarios = []

    # Helper function to create binary strings
    def bin_str(val):
        return "1" if val else "0"

    # Scenario 1: Basic Selection Control
    basic_sel = {
        "scenario": "Basic Selection Control",
        "input variable": [
            {"a": "1", "b": "0", "sel": "0"},  # Should select a=1
            {"a": "1", "b": "0", "sel": "1"},  # Should select b=0
            {"a": "0", "b": "1", "sel": "0"},  # Should select a=0
            {"a": "0", "b": "1", "sel": "1"},  # Should select b=1
        ],
    }
    scenarios.append(basic_sel)

    # Scenario 2: All Input Combinations
    all_combinations = {
        "scenario": "All Input Combinations",
        "input variable": [
            {"a": "0", "b": "0", "sel": "0"},
            {"a": "0", "b": "0", "sel": "1"},
            {"a": "0", "b": "1", "sel": "0"},
            {"a": "0", "b": "1", "sel": "1"},
            {"a": "1", "b": "0", "sel": "0"},
            {"a": "1", "b": "0", "sel": "1"},
            {"a": "1", "b": "1", "sel": "0"},
            {"a": "1", "b": "1", "sel": "1"},
        ],
    }
    scenarios.append(all_combinations)

    # Scenario 3: Input Transitions
    input_transitions = {
        "scenario": "Input Transitions",
        "input variable": [
            {"a": "0", "b": "0", "sel": "0"},
            {"a": "1", "b": "0", "sel": "0"},
            {"a": "0", "b": "0", "sel": "1"},
            {"a": "0", "b": "1", "sel": "1"},
        ],
    }
    scenarios.append(input_transitions)

    # Scenario 4: Selection Transitions
    sel_transitions = {
        "scenario": "Selection Transitions",
        "input variable": [
            {"a": "1", "b": "0", "sel": "0"},
            {"a": "1", "b": "0", "sel": "1"},
            {"a": "1", "b": "0", "sel": "0"},
            {"a": "1", "b": "0", "sel": "1"},
        ],
    }
    scenarios.append(sel_transitions)

    # Scenario 5: Simultaneous Transitions
    simultaneous = {
        "scenario": "Simultaneous Transitions",
        "input variable": [
            {"a": "0", "b": "0", "sel": "0"},
            {"a": "1", "b": "1", "sel": "1"},
            {"a": "0", "b": "0", "sel": "0"},
            {"a": "1", "b": "1", "sel": "1"},
        ],
    }
    scenarios.append(simultaneous)

    # Scenario 6: Glitch Detection
    glitch_detection = {
        "scenario": "Glitch Detection",
        "input variable": [
            {"a": "0", "b": "1", "sel": "0"},
            {"a": "1", "b": "1", "sel": "0"},
            {"a": "1", "b": "0", "sel": "1"},
            {"a": "1", "b": "1", "sel": "1"},
        ],
    }
    scenarios.append(glitch_detection)

    # Scenario 7: Setup and Hold Times
    setup_hold = {
        "scenario": "Setup and Hold Times",
        "input variable": [
            {"a": "0", "b": "1", "sel": "0"},
            {"a": "0", "b": "1", "sel": "1"},
            {"a": "1", "b": "0", "sel": "0"},
            {"a": "1", "b": "0", "sel": "1"},
        ],
    }
    scenarios.append(setup_hold)

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
