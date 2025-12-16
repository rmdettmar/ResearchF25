import json


def stimulus_gen():
    # List to store all test scenarios
    scenarios = []

    # Scenario 1: Basic Logic Verification
    basic_logic = {
        "scenario": "Basic Logic Verification",
        "input variable": [{"in": "0"}, {"in": "1"}],
    }
    scenarios.append(basic_logic)

    # Scenario 2: Signal Transition
    signal_transition = {
        "scenario": "Signal Transition",
        "input variable": [
            {"in": "0"},
            {"in": "1"},
            {"in": "0"},
            {"in": "1"},
            {"in": "0"},
        ],
    }
    scenarios.append(signal_transition)

    # Scenario 3: Glitch Detection
    glitch_detection = {
        "scenario": "Glitch Detection",
        "input variable": [
            {"in": "0"},
            {"in": "1"},
            {"in": "0"},
            {"in": "1"},
            {"in": "0"},
            {"in": "1"},
            {"in": "0"},
            {"in": "1"},
        ],
    }
    scenarios.append(glitch_detection)

    # Scenario 4: Power-on State
    power_on = {"scenario": "Power-on State", "input variable": [{"in": "0"}]}
    scenarios.append(power_on)

    # Scenario 5: Unknown Input
    unknown_input = {
        "scenario": "Unknown Input",
        "input variable": [{"in": "0"}, {"in": "1"}],
    }
    scenarios.append(unknown_input)

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
