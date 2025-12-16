import json


def stimulus_gen():
    scenarios = []

    # Helper function to create a binary sequence for counter operation
    def create_count_sequence(cycles, reset_pattern):
        sequence = []
        for i in range(cycles):
            sequence.append(
                {
                    "clk": "1",
                    "reset": reset_pattern[i] if i < len(reset_pattern) else "0",
                }
            )
        return sequence

    # Scenario 1: Basic Counter Operation
    basic_op = {
        "scenario": "Basic Counter Operation",
        "input variable": create_count_sequence(20, ["0"] * 20),
    }
    scenarios.append(basic_op)

    # Scenario 2: Reset During Counting
    reset_during_count = {
        "scenario": "Reset During Counting",
        "input variable": create_count_sequence(
            20, ["0"] * 5 + ["1"] + ["0"] * 5 + ["1"] + ["0"] * 8
        ),
    }
    scenarios.append(reset_during_count)

    # Scenario 3: Counter Rollover
    rollover = {
        "scenario": "Counter Rollover",
        "input variable": create_count_sequence(20, ["0"] * 20),
    }
    scenarios.append(rollover)

    # Scenario 4: Power-on State
    power_on = {
        "scenario": "Power-on State",
        "input variable": create_count_sequence(5, ["1"] + ["0"] * 4),
    }
    scenarios.append(power_on)

    # Scenario 5: Multiple Reset Pulses
    multiple_resets = {
        "scenario": "Multiple Reset Pulses",
        "input variable": create_count_sequence(
            10, ["1", "1", "1", "1", "1"] + ["0"] * 5
        ),
    }
    scenarios.append(multiple_resets)

    # Scenario 6: Reset Release Timing
    reset_timing = {
        "scenario": "Reset Release Timing",
        "input variable": create_count_sequence(
            15, ["1", "1", "0", "0", "1", "1", "0"] + ["0"] * 8
        ),
    }
    scenarios.append(reset_timing)

    # Scenario 7: Long-term Operation
    long_term = {
        "scenario": "Long-term Operation",
        "input variable": create_count_sequence(50, ["0"] * 50),
    }
    scenarios.append(long_term)

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
