import json

from cocotb.binary import BinaryValue


def decimal_to_bcd_str(decimal_num):
    bcd = ""
    for digit in f"{decimal_num:04d}":
        bcd = f"{int(digit):04b}" + bcd
    return bcd


def stimulus_gen():
    scenarios = []

    # Scenario 1: Reset Verification
    reset_scenario = {
        "scenario": "Reset Verification",
        "input variable": [{"reset": "1"}, {"reset": "0"}],
    }
    scenarios.append(reset_scenario)

    # Scenario 2: Single Digit Counting
    single_digit = {
        "scenario": "Single Digit Counting",
        "input variable": [{"reset": "0"} for _ in range(10)],
    }
    scenarios.append(single_digit)

    # Scenario 3: Tens Digit Transition
    tens_transition = {
        "scenario": "Tens Digit Transition",
        "input variable": [{"reset": "1"}, {"reset": "0"}]
        + [{"reset": "0"} for _ in range(10)],
    }
    scenarios.append(tens_transition)

    # Scenario 4: Hundreds Digit Transition
    hundreds_transition = {
        "scenario": "Hundreds Digit Transition",
        "input variable": [{"reset": "1"}, {"reset": "0"}]
        + [{"reset": "0"} for _ in range(100)],
    }
    scenarios.append(hundreds_transition)

    # Scenario 5: Thousands Digit Transition
    thousands_transition = {
        "scenario": "Thousands Digit Transition",
        "input variable": [{"reset": "1"}, {"reset": "0"}]
        + [{"reset": "0"} for _ in range(1000)],
    }
    scenarios.append(thousands_transition)

    # Scenario 6: Maximum Value Rollover
    max_rollover = {
        "scenario": "Maximum Value Rollover",
        "input variable": [{"reset": "1"}, {"reset": "0"}]
        + [{"reset": "0"} for _ in range(10000)],
    }
    scenarios.append(max_rollover)

    # Scenario 7: BCD Range Verification
    bcd_range = {
        "scenario": "BCD Range Verification",
        "input variable": [{"reset": "1"}, {"reset": "0"}]
        + [{"reset": "0"} for _ in range(100)],
    }
    scenarios.append(bcd_range)

    # Scenario 8: Enable Signal Timing
    enable_timing = {
        "scenario": "Enable Signal Timing",
        "input variable": [{"reset": "1"}, {"reset": "0"}]
        + [{"reset": "0"} for _ in range(20)],
    }
    scenarios.append(enable_timing)

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
