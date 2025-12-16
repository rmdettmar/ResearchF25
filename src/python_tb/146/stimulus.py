import json

from cocotb.binary import BinaryValue


def create_sensor_pattern(s3, s2, s1):
    return f"{s3}{s2}{s1}"


def stimulus_gen():
    scenarios = []

    # Scenario 1: Basic Water Level Above s[3]
    scenario1 = {
        "scenario": "Basic Water Level Above s[3]",
        "input variable": [{"reset": "0", "s": "111"}, {"reset": "0", "s": "111"}],
    }
    scenarios.append(scenario1)

    # Scenario 2: Water Level Between s[3] and s[2]
    scenario2 = {
        "scenario": "Water Level Between s[3] and s[2]",
        "input variable": [{"reset": "0", "s": "011"}, {"reset": "0", "s": "011"}],
    }
    scenarios.append(scenario2)

    # Scenario 3: Water Level Between s[2] and s[1]
    scenario3 = {
        "scenario": "Water Level Between s[2] and s[1]",
        "input variable": [{"reset": "0", "s": "001"}, {"reset": "0", "s": "001"}],
    }
    scenarios.append(scenario3)

    # Scenario 4: Water Level Below s[1]
    scenario4 = {
        "scenario": "Water Level Below s[1]",
        "input variable": [{"reset": "0", "s": "000"}, {"reset": "0", "s": "000"}],
    }
    scenarios.append(scenario4)

    # Scenario 5: Rising Water Level Transition
    scenario5 = {
        "scenario": "Rising Water Level Transition",
        "input variable": [
            {"reset": "0", "s": "001"},
            {"reset": "0", "s": "011"},
            {"reset": "0", "s": "011"},
        ],
    }
    scenarios.append(scenario5)

    # Scenario 6: Falling Water Level Transition
    scenario6 = {
        "scenario": "Falling Water Level Transition",
        "input variable": [
            {"reset": "0", "s": "011"},
            {"reset": "0", "s": "001"},
            {"reset": "0", "s": "001"},
        ],
    }
    scenarios.append(scenario6)

    # Scenario 7: Synchronous Reset
    scenario7 = {
        "scenario": "Synchronous Reset",
        "input variable": [
            {"reset": "0", "s": "111"},
            {"reset": "1", "s": "111"},
            {"reset": "0", "s": "111"},
        ],
    }
    scenarios.append(scenario7)

    # Scenario 8: Multiple Level Changes
    scenario8 = {
        "scenario": "Multiple Level Changes",
        "input variable": [
            {"reset": "0", "s": "000"},
            {"reset": "0", "s": "001"},
            {"reset": "0", "s": "011"},
            {"reset": "0", "s": "111"},
            {"reset": "0", "s": "011"},
            {"reset": "0", "s": "001"},
            {"reset": "0", "s": "000"},
        ],
    }
    scenarios.append(scenario8)

    # Scenario 9: Invalid Sensor Patterns
    scenario9 = {
        "scenario": "Invalid Sensor Patterns",
        "input variable": [
            {"reset": "0", "s": "101"},
            {"reset": "0", "s": "110"},
            {"reset": "0", "s": "100"},
        ],
    }
    scenarios.append(scenario9)

    # Scenario 10: Rapid Level Changes
    scenario10 = {
        "scenario": "Rapid Level Changes",
        "input variable": [
            {"reset": "0", "s": "000"},
            {"reset": "0", "s": "111"},
            {"reset": "0", "s": "001"},
            {"reset": "0", "s": "011"},
            {"reset": "0", "s": "000"},
        ],
    }
    scenarios.append(scenario10)

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
