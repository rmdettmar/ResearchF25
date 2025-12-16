import json


def stimulus_gen():
    scenarios = []

    # Basic Latch Operation
    basic_op = {
        "scenario": "Basic Latch Operation",
        "input variable": [
            {"d": "0", "ena": "1"},
            {"d": "1", "ena": "1"},
            {"d": "0", "ena": "1"},
            {"d": "1", "ena": "1"},
        ],
    }
    scenarios.append(basic_op)

    # Data Hold Operation
    data_hold = {
        "scenario": "Data Hold Operation",
        "input variable": [
            {"d": "1", "ena": "1"},  # Set initial value
            {"d": "1", "ena": "0"},  # Disable latch
            {"d": "0", "ena": "0"},  # Change input
            {"d": "1", "ena": "0"},  # Change input again
            {"d": "0", "ena": "0"},  # Value should hold
        ],
    }
    scenarios.append(data_hold)

    # Enable Edge Transition
    edge_trans = {
        "scenario": "Enable Edge Transition",
        "input variable": [
            {"d": "1", "ena": "1"},  # Set initial value
            {"d": "1", "ena": "0"},  # Capture value
            {"d": "0", "ena": "0"},  # Change input
            {"d": "1", "ena": "1"},  # Re-enable
            {"d": "0", "ena": "0"},  # Capture new value
        ],
    }
    scenarios.append(edge_trans)

    # Glitch Immunity
    glitch = {
        "scenario": "Glitch Immunity",
        "input variable": [
            {"d": "1", "ena": "1"},  # Set initial value
            {"d": "1", "ena": "0"},  # Disable latch
            {"d": "0", "ena": "0"},  # Glitch
            {"d": "1", "ena": "0"},  # Glitch
            {"d": "0", "ena": "0"},  # Glitch
        ],
    }
    scenarios.append(glitch)

    # Enable Setup/Hold
    setup_hold = {
        "scenario": "Enable Setup/Hold",
        "input variable": [
            {"d": "0", "ena": "1"},
            {"d": "1", "ena": "1"},
            {"d": "1", "ena": "0"},
            {"d": "0", "ena": "1"},
            {"d": "1", "ena": "0"},
        ],
    }
    scenarios.append(setup_hold)

    # Power-On State
    power_on = {
        "scenario": "Power-On State",
        "input variable": [
            {"d": "0", "ena": "0"},  # Initial state
            {"d": "0", "ena": "0"},  # Keep disabled
            {"d": "1", "ena": "0"},  # Change input while disabled
            {"d": "0", "ena": "0"},  # Keep disabled
        ],
    }
    scenarios.append(power_on)

    # Rapid Enable Toggle
    rapid_toggle = {
        "scenario": "Rapid Enable Toggle",
        "input variable": [
            {"d": "1", "ena": "1"},  # Set initial value
            {"d": "1", "ena": "0"},  # Toggle enable
            {"d": "1", "ena": "1"},
            {"d": "1", "ena": "0"},
            {"d": "1", "ena": "1"},
        ],
    }
    scenarios.append(rapid_toggle)

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
