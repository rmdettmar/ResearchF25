import json

from cocotb.binary import BinaryValue


def int_to_bin_str(value, width=8):
    binary_val = BinaryValue(value=value, n_bits=width)
    return binary_val.binstr


def stimulus_gen():
    scenarios = []

    # Scenario 1: All Different Values
    scenario1 = {
        "scenario": "All Different Values",
        "input variable": [
            {
                "a": int_to_bin_str(100),
                "b": int_to_bin_str(150),
                "c": int_to_bin_str(50),
                "d": int_to_bin_str(200),
            }
        ],
    }
    scenarios.append(scenario1)

    # Scenario 2: Equal Values
    scenario2 = {
        "scenario": "Equal Values",
        "input variable": [
            {
                "a": int_to_bin_str(128),
                "b": int_to_bin_str(128),
                "c": int_to_bin_str(128),
                "d": int_to_bin_str(128),
            }
        ],
    }
    scenarios.append(scenario2)

    # Scenario 3: Boundary Values
    scenario3 = {
        "scenario": "Boundary Values",
        "input variable": [
            {
                "a": int_to_bin_str(255),
                "b": int_to_bin_str(0),
                "c": int_to_bin_str(255),
                "d": int_to_bin_str(255),
            }
        ],
    }
    scenarios.append(scenario3)

    # Scenario 4: Consecutive Values
    scenario4 = {
        "scenario": "Consecutive Values",
        "input variable": [
            {
                "a": int_to_bin_str(100),
                "b": int_to_bin_str(101),
                "c": int_to_bin_str(102),
                "d": int_to_bin_str(103),
            }
        ],
    }
    scenarios.append(scenario4)

    # Scenario 5: Partial Equal Values
    scenario5 = {
        "scenario": "Partial Equal Values",
        "input variable": [
            {
                "a": int_to_bin_str(50),
                "b": int_to_bin_str(50),
                "c": int_to_bin_str(100),
                "d": int_to_bin_str(100),
            }
        ],
    }
    scenarios.append(scenario5)

    # Scenario 6: Single Minimum
    scenario6 = {
        "scenario": "Single Minimum",
        "input variable": [
            {
                "a": int_to_bin_str(200),
                "b": int_to_bin_str(25),
                "c": int_to_bin_str(200),
                "d": int_to_bin_str(200),
            }
        ],
    }
    scenarios.append(scenario6)

    # Scenario 7: Random Values
    import random

    scenario7 = {
        "scenario": "Random Values",
        "input variable": [
            {
                "a": int_to_bin_str(random.randint(0, 255)),
                "b": int_to_bin_str(random.randint(0, 255)),
                "c": int_to_bin_str(random.randint(0, 255)),
                "d": int_to_bin_str(random.randint(0, 255)),
            }
        ],
    }
    scenarios.append(scenario7)

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
