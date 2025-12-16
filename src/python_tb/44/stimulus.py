import json


def stimulus_gen():
    scenarios = []

    # Basic Heating Mode Operation
    heating_mode = {
        "scenario": "Basic Heating Mode Operation",
        "input variable": [
            {"mode": "1", "too_cold": "0", "too_hot": "0", "fan_on": "0"},
            {"mode": "1", "too_cold": "1", "too_hot": "0", "fan_on": "0"},
            {"mode": "1", "too_cold": "0", "too_hot": "0", "fan_on": "0"},
        ],
    }
    scenarios.append(heating_mode)

    # Basic Cooling Mode Operation
    cooling_mode = {
        "scenario": "Basic Cooling Mode Operation",
        "input variable": [
            {"mode": "0", "too_cold": "0", "too_hot": "0", "fan_on": "0"},
            {"mode": "0", "too_cold": "0", "too_hot": "1", "fan_on": "0"},
            {"mode": "0", "too_cold": "0", "too_hot": "0", "fan_on": "0"},
        ],
    }
    scenarios.append(cooling_mode)

    # Manual Fan Control
    manual_fan = {
        "scenario": "Manual Fan Control",
        "input variable": [
            {"mode": "1", "too_cold": "0", "too_hot": "0", "fan_on": "1"},
            {"mode": "0", "too_cold": "0", "too_hot": "0", "fan_on": "1"},
            {"mode": "1", "too_cold": "0", "too_hot": "0", "fan_on": "0"},
        ],
    }
    scenarios.append(manual_fan)

    # Mode Switching
    mode_switch = {
        "scenario": "Mode Switching",
        "input variable": [
            {"mode": "1", "too_cold": "1", "too_hot": "0", "fan_on": "0"},
            {"mode": "0", "too_cold": "0", "too_hot": "1", "fan_on": "0"},
            {"mode": "1", "too_cold": "1", "too_hot": "0", "fan_on": "0"},
        ],
    }
    scenarios.append(mode_switch)

    # Invalid Temperature Combinations
    invalid_temp = {
        "scenario": "Invalid Temperature Combinations",
        "input variable": [
            {"mode": "1", "too_cold": "1", "too_hot": "1", "fan_on": "0"},
            {"mode": "0", "too_cold": "1", "too_hot": "1", "fan_on": "0"},
        ],
    }
    scenarios.append(invalid_temp)

    # Fan Priority Check
    fan_priority = {
        "scenario": "Fan Priority Check",
        "input variable": [
            {"mode": "1", "too_cold": "1", "too_hot": "0", "fan_on": "0"},
            {"mode": "1", "too_cold": "1", "too_hot": "0", "fan_on": "1"},
            {"mode": "0", "too_cold": "0", "too_hot": "1", "fan_on": "1"},
        ],
    }
    scenarios.append(fan_priority)

    # Rapid Mode Switching
    rapid_mode = {
        "scenario": "Rapid Mode Switching",
        "input variable": [
            {"mode": "1", "too_cold": "1", "too_hot": "0", "fan_on": "0"},
            {"mode": "0", "too_cold": "0", "too_hot": "1", "fan_on": "0"},
            {"mode": "1", "too_cold": "1", "too_hot": "0", "fan_on": "0"},
            {"mode": "0", "too_cold": "0", "too_hot": "1", "fan_on": "0"},
        ],
    }
    scenarios.append(rapid_mode)

    # All Inputs Toggling
    all_toggle = {
        "scenario": "All Inputs Toggling",
        "input variable": [
            {"mode": "0", "too_cold": "0", "too_hot": "0", "fan_on": "0"},
            {"mode": "1", "too_cold": "1", "too_hot": "1", "fan_on": "1"},
            {"mode": "0", "too_cold": "1", "too_hot": "0", "fan_on": "1"},
            {"mode": "1", "too_cold": "0", "too_hot": "1", "fan_on": "0"},
        ],
    }
    scenarios.append(all_toggle)

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
