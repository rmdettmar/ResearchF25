import json


def stimulus_gen():
    scenarios = []

    # Helper function to generate binary strings
    def bin_str(value, width=1):
        return format(value, f"0{width}b")

    # Scenario 1: Basic Counting Sequence
    basic_count = {
        "scenario": "Basic Counting Sequence",
        "input variable": [{"clk": "0", "reset": "0"} for _ in range(20)],
    }
    scenarios.append(basic_count)

    # Scenario 2: Counter Rollover
    rollover = {
        "scenario": "Counter Rollover",
        "input variable": [{"clk": "0", "reset": "0"} for _ in range(15)],
    }
    scenarios.append(rollover)

    # Scenario 3: Synchronous Reset Operation
    sync_reset = {
        "scenario": "Synchronous Reset Operation",
        "input variable": [
            {"clk": "0", "reset": "0"},
            {"clk": "0", "reset": "1"},
            {"clk": "0", "reset": "1"},
            {"clk": "0", "reset": "0"},
            {"clk": "0", "reset": "0"},
        ],
    }
    scenarios.append(sync_reset)

    # Scenario 4: Reset During Count
    reset_during_count = {
        "scenario": "Reset During Count",
        "input variable": [
            *[{"clk": "0", "reset": "0"} for _ in range(5)],
            {"clk": "0", "reset": "1"},
            {"clk": "0", "reset": "1"},
            *[{"clk": "0", "reset": "0"} for _ in range(5)],
        ],
    }
    scenarios.append(reset_during_count)

    # Scenario 5: Multiple Rollover Cycles
    multiple_rollover = {
        "scenario": "Multiple Rollover Cycles",
        "input variable": [{"clk": "0", "reset": "0"} for _ in range(30)],
    }
    scenarios.append(multiple_rollover)

    # Scenario 6: Reset Release Behavior
    reset_release = {
        "scenario": "Reset Release Behavior",
        "input variable": [
            {"clk": "0", "reset": "1"},
            {"clk": "0", "reset": "1"},
            {"clk": "0", "reset": "0"},
            *[{"clk": "0", "reset": "0"} for _ in range(10)],
        ],
    }
    scenarios.append(reset_release)

    # Scenario 7: Reset Pulse Width
    reset_pulse = {
        "scenario": "Reset Pulse Width",
        "input variable": [
            {"clk": "0", "reset": "0"},
            {"clk": "0", "reset": "1"},
            {"clk": "0", "reset": "0"},
            {"clk": "0", "reset": "1"},
            {"clk": "0", "reset": "1"},
            {"clk": "0", "reset": "1"},
            {"clk": "0", "reset": "0"},
        ],
    }
    scenarios.append(reset_pulse)

    # Scenario 8: Initial Power-up State
    power_up = {
        "scenario": "Initial Power-up State",
        "input variable": [
            {"clk": "0", "reset": "0"},
            *[{"clk": "0", "reset": "0"} for _ in range(10)],
        ],
    }
    scenarios.append(power_up)

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
